import random
from discord.commands import SlashCommandGroup
from discord.ext import commands


class VkosenCog(commands.Cog):
    slash = SlashCommandGroup('vkosen', guild_ids=[542684644244586496])

    def __init__(self, bot):
        self.bot = bot

    @slash.command()
    async def amasita(self, ctx):
        '''雨下さんがママか確認'''
        if random.randint(1, 1000) % 5 == 0:
            await ctx.respond(f'雨下さんは{ctx.author.display_name}さんのママです。')
        elif random.randint(1, 1000) % 5 == 1:
            await ctx.respond(f'雨下さん{ctx.author.display_name}さんのママじゃないので......（冷静）')
        else:
            await ctx.respond(f'雨下さんは{ctx.author.display_name}さんのママではありません。')
