from discord.ext import commands
from discord import Message, Embed, TextChannel, Forbidden
from thonk.twitter import Twitter
from peony.data_processing import PeonyResponse
from urllib.parse import urlparse

import re
import logging
import html
import json

log = logging.getLogger(__name__)

class ContentEmbed(Embed):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.message_content = None

class ContentOnly:
    def __init__(self, content):
        self.message_content = content

class Expander:
    def create_embed(self, message: Message):
        e = ContentEmbed()

        e.set_footer(text=f"Posted to Discord by {message.author.display_name}",
                     icon_url=message.author.avatar_url)

        return e

    def matches(self, hostname):
        return self.filter.search(hostname) is not None

    async def expand(self, message: Message, object_id):
        pass

class TwitterExpander(Expander):
    def __init__(self, twitter_client: Twitter):
        self.twitter = twitter_client

    def matches(self, hostname):
        return hostname == "twitter.com"

    def create_twitter_embed(self, message: Message, tweet: PeonyResponse):
        e = super().create_embed(message)
        e.colour = int(tweet.user.profile_link_color, 16)

        return e

    def format_tweet_text(self, tweet: PeonyResponse):
        full_text = tweet.text
        start, end = tweet.display_text_range
        full_text = full_text[start:end]

        for url_ent in tweet.entities.urls:
            us, ue = url_ent.indices
            full_text = full_text[:us] + f"[{url_ent.display_url}]({url_ent.expanded_url})" + full_text[ue:]

        return html.unescape(full_text)

    def format_normal_tweet(self, message: Message, tweet: PeonyResponse, *, with_text: bool=False):
        embeds = []

        if 'extended_entities' in tweet:
            for ent in tweet.extended_entities.media:
                e = self.create_twitter_embed(message, tweet)

                if 'video_info' in ent:
                    continue
                else:
                    e.set_image(url=ent.media_url_https)
                e.url = ent.url

                embeds.append(e)
        else:
            embeds.append(self.create_twitter_embed(message, tweet))

        if with_text and len(embeds) > 0:
            e = embeds[0]

            e.set_author(name=f"{tweet.user.name} (@{tweet.user.screen_name})",
                         url=f"https://twitter.com/{tweet.user.screen_name}",
                         icon_url=tweet.user.profile_image_url)
            e.description = self.format_tweet_text(tweet)

        return embeds

    def format_quoted_tweet(self, message: Message, tweet: PeonyResponse):
        screen_name = "i"
        if 'user' in tweet:
            screen_name = tweet.user.screen_name or screen_name

        embed = ContentOnly(f"Quoted tweet: https://twitter.com/{screen_name}/status/{tweet.id_str}")
        return [embed]

    def format_tweet(self, message: Message, tweet: PeonyResponse):
        embeds = []

        if 'quoted_status' in tweet:
            embeds.extend(self.format_quoted_tweet(message, tweet.quoted_status))

        return embeds

    async def expand(self, message: Message, object_id):
        tweet = await self.twitter.fetch_tweet(object_id)

        log.debug(json.dumps(tweet.data))

        return self.format_tweet(message, tweet)

class DiscordExpander(Expander):
    def __init__(self, bot: commands.Bot):
        self.discord_bot = bot
        self.filter = re.compile(r"(?<!cdn\.)discord(app)?\.com")

    def format_message(self, link_message: Message, message: Message):
        embeds = []
        e = ContentEmbed()

        e.set_author(name=message.author.display_name, icon_url=message.author.avatar_url)
        e.timestamp = message.created_at
        e.url = message.jump_url
        e.colour = message.author.colour
        e.set_footer(text=f"Linked by {link_message.author.display_name}")

        if message.channel.nsfw and not link_message.channel.nsfw:
            e.title = "NSFW warning (Image removed)"
            e.description = f"||{message.content}||"
        else:
            e.description = message.content

            if len(message.attachments) > 0:
                e.set_image(url=message.attachments[0].url)

        embeds.append(e)

        if len(message.embeds) > 0:
            embeds.extend(message.embeds)

        return embeds

    async def expand(self, message: Message, object_id):
        target_guild = self.discord_bot.get_guild(object_id[0]) or await self.discord_bot.fetch_guild(object_id[0])
        target_channel: TextChannel = target_guild.get_channel(object_id[1])

        if target_channel is not None:
            try:
                target_message = await target_channel.fetch_message(object_id[2])
            except Forbidden:
                return []

            if target_message is not None:
                return self.format_message(message, target_message)

        return []

class EmbedExpansion(commands.Cog, name="Embeds"):
    link_regex = re.compile(r"http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*(),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+")

    def __init__(self, bot: commands.Bot, twitter_client: Twitter):
        self.twitter_expander = TwitterExpander(twitter_client)
        self.discord_expander = DiscordExpander(bot)

    @commands.Cog.listener()
    async def on_message(self, message: Message):
        if message.author.bot:
            return

        if "+noexpand" in message.content:
            return

        result = self.link_regex.search(message.content)
        if not result: return

        scheme, hostname, path, _, query, fragment = urlparse(result.group(0))

        log.debug(f"{hostname}; {path}")

        if self.twitter_expander.matches(hostname):
            tweet_id = int(path.split('/')[-1])

            embeds = await self.twitter_expander.expand(message, tweet_id)
        elif self.discord_expander.matches(hostname):
            if message.content.startswith("Replying to"):
                return  # disable when using discord's bad reply feature

            _, _, guild_str, channel_str, message_str = path.split('/')

            target = (int(guild_str), int(channel_str), int(message_str))

            try:
                embeds = await self.discord_expander.expand(message, target)
            except Forbidden:
                return
        else:
            return

        for e in embeds:
            if isinstance(e, ContentOnly):
                await message.channel.send(e.message_content)
            elif not isinstance(e, ContentEmbed):
                await message.channel.send(None, embed=e)
            elif e.message_content:
                await message.channel.send(e.message_content, embed=e)
            else:
                await message.channel.send(None, embed=e)


def setup(bot: commands.Bot):
    # TODO: Refactor cog to be more modular (so discord expansions can still work with twitter disabled)
    if hasattr(bot, 'twitter'):
        bot.add_cog(EmbedExpansion(bot, bot.twitter))
