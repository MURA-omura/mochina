import random

import discord
import yaml

from cogs import ScheduleCog, VoiceCog


def main():
    bot = discord.Bot()


    @bot.event
    async def on_ready():
        print(f"{bot.user}としてログインしました！")


    @bot.slash_command(guild_ids=[683939861539192860, 542684644244586496])
    async def vping(ctx):
        await ctx.respond("pong")


    @bot.slash_command(guild_ids=[542684644244586496])
    async def vamasita(ctx):
        '''雨下さんがママか確認'''
        if random.randint(1, 10000) % 5 == 0:
            await ctx.respond(f'雨下さんは{ctx.author.display_name}さんのママです。')
        elif random.randint(1, 10000) % 5 == 1:
            await ctx.respond(f'雨下さん{ctx.author.display_name}さんのママじゃないので......（冷静）')
        else:
            await ctx.respond(f'雨下さんは{ctx.author.display_name}さんのママではありません。')


    bot.add_cog(ScheduleCog(bot))
    bot.add_cog(VoiceCog(bot))
    with open('config.yml', 'r') as f:
        cfg = yaml.safe_load(f)
    bot.get_cog('ScheduleCog').run_schedule.start()
    bot.run(cfg['TOKEN'])


if __name__ == '__main__':
    main()
