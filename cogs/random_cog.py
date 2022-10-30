import random
from discord.commands import SlashCommandGroup
from discord.ext import commands


class RandomCog(commands.Cog):
    slash = SlashCommandGroup('vschedule', guild_ids=[683939861539192860, 542684644244586496])

    def __init__(self, bot):
        self.bot = bot