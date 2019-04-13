from discord.ext import commands
from discord import Message, Embed
from thonk.twitter import Twitter
from peony.data_processing import PeonyResponse

import re
import logging

log = logging.getLogger(__name__)

class ContentEmbed(Embed):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.message_content = None

class ContentOnly:
    def __init__(self):
        self.message_content = None

class EmbedExpansion(commands.Cog, name="Embeds"):
    tweet_regex = re.compile(r"https?://twitter\.com/.+/status/(\d+)/?")

    def __init__(self, twitter_client: Twitter):
        self.twitter = twitter_client

    def _create_embed(self, message: Message, tweet: PeonyResponse) -> ContentEmbed:
        e = ContentEmbed()

        e.set_footer(text=f"Posted to Discord by {message.author.display_name}",
                     icon_url=message.author.avatar_url)
        e.colour = int(tweet.user.profile_link_color, 16)

        return e

    def format_normal_tweet(self, message: Message, tweet: PeonyResponse):
        embeds = []

        if 'extended_entities' in tweet:
            for ent in tweet.extended_entities.media:
                e = self._create_embed(message, tweet)

                if 'video_info' in ent:
                    continue
                else:
                    e.set_image(url=ent.media_url_https)
                e.url = ent.url

                embeds.append(e)
        else:
            embeds.append(self._create_embed(message, tweet))

        if len(embeds) > 0 and not isinstance(embeds[0], ContentOnly):
            embeds[0].set_author(name=f"{tweet.user.name} (@{tweet.user.screen_name})",
                                 url=f"https://twitter.com/{tweet.user.screen_name}",
                                 icon_url=tweet.user.profile_image_url)
            embeds[0].description = tweet.text
            embeds[0].add_field(name="Retweets", value=tweet.retweet_count)
            embeds[0].add_field(name="Likes", value=tweet.favorite_count)

        return embeds

    def format_quoted_tweet(self, message: Message, tweet: PeonyResponse):
        embeds = self.format_tweet(message, tweet)
        if len(embeds) == 0:
            embeds.append(ContentOnly())

        embeds[0].message_content = f"Quoted tweet: https://twitter.com/i/status/{tweet.id_str}"

        return embeds

    def format_tweet(self, message: Message, tweet: PeonyResponse):
        embeds = []

        embeds.extend(self.format_normal_tweet(message, tweet))

        if 'quoted_status' in tweet:
            embeds.extend(self.format_quoted_tweet(message, tweet.quoted_status))

        return embeds

    @commands.Cog.listener()
    async def on_message(self, message: Message):
        if message.author.bot:
            return

        result = self.tweet_regex.search(message.content)

        if not result:
            return

        status_id = result.group(1)
        tweet = await self.twitter.fetch_tweet(status_id)

        embeds = self.format_tweet(message, tweet)
        if len(embeds) == 0:
            return

        embeds[0].message_content = message.content

        await message.delete()
        for e in embeds:
            if isinstance(e, ContentOnly):
                await message.channel.send(e.message_content)
            elif e.message_content:
                await message.channel.send(e.message_content, embed=e)
            else:
                await message.channel.send(None, embed=e)


def setup(bot: commands.Bot):
    bot.add_cog(EmbedExpansion(bot.twitter))
