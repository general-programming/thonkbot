from discord.ext import commands
from discord.utils import get
from discord import Member
from thonk import utils

import logging

log = logging.getLogger(__name__)

class Pronoun:
	def __init__(self, forms):
		self.subject = forms[0]
		self.object = forms[1]
		self.determiner = forms[2]
		self.posessive = forms[3]
		self.reflexive = forms[4]

	def short_form(self):
		return f"{self.subject}/{self.object}"

	def __str__(self):
		return f"{self.subject}/{self.object}/{self.determiner}" +\
			f"/{self.posessive}/{self.reflexive}"

	def matches(self, specifier: str):
		return str(self).startswith(specifier)

	def generate_link(self):
		return f"https://pronoun.is/{str(self)}"

class PronounRoles(commands.Cog):
	def __init__(self, pronouns):
		self.pronouns = pronouns
		self.role_cache = {}

	def find_pronoun(self, pronoun_part: str):
		guesses = filter(lambda p: p.matches(pronoun_part), self.pronouns)
		guesses = list(guesses)

		if len(guesses) > 1:
			raise Exception("That could mean too many pronouns! Try being more specific.")
		else:
			return guesses[0]

	@commands.command()
	async def iam(self, ctx: commands.Context, pronoun: str):
		p = self.find_pronoun(pronoun)
		full_pronoun = str(p)
		role = None

		if full_pronoun in self.role_cache:
			role_id = self.role_cache[full_pronoun]
			role = ctx.message.guild.get_role(role_id)

		if role is None:			
			role = get(ctx.message.guild.roles, name=full_pronoun)

		if role is None:
			role = await ctx.message.guild.create_role(name=full_pronoun)

		self.role_cache[full_pronoun] = role.id

		await ctx.message.author.add_roles(role)
		await ctx.send(f"\N{MEMO} *notes down* {ctx.message.author.display_name} uses **{p.short_form()}** pronouns")

	@commands.command()
	async def pronouns(self, ctx: commands.Context, user: Member):
		pronoun_roles = filter(lambda r: len(r.name.split("/")) == 5, user.roles)
		pronouns = map(lambda r: Pronoun(r.name), pronoun_roles)
		pronouns = list(pronouns)

		if len(pronouns) == 1:
			pronoun = pronouns[0]
			await ctx.send(f"**{user.display_name}** uses **{pronoun.short_form()}** pronouns ({pronoun.generate_link()})")
		else:
			formatted = ", ".join(map(lambda p: p.short_form(), pronouns[:-1])) +\
				f"and {pronouns[-1].short_form()}"
			
			await ctx.send(f"**{user.display_name}** uses **{formatted}** pronouns.")

def setup(bot: commands.Bot):
	pronouns = []
	
	with open("data/pronouns.tab", "rt", encoding="utf8") as fd:
		for line in fd:
			pronoun = Pronoun(line.strip().split("\t"))

			pronouns.append(pronoun)
	
	bot.add_cog(PronounRoles(pronouns))
