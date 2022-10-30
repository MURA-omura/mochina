import discord
import yaml

from cogs import ScheduleCog, VkosenCog, VoiceCog


def main():
    bot = discord.Bot()


    @bot.event
    async def on_ready():
        print(f"{bot.user}としてログインしました！")


    @bot.slash_command(guild_ids=[683939861539192860, 542684644244586496])
    async def vping(ctx):
        await ctx.respond(f"pong {round(bot.latency, 2)}ms")


    bot.add_cog(ScheduleCog(bot))
    bot.add_cog(VkosenCog(bot))
    bot.add_cog(VoiceCog(bot))
    with open('config.yml', 'r') as f:
        cfg = yaml.safe_load(f)
    bot.get_cog('ScheduleCog').run_schedule.start()
    bot.run(cfg['TOKEN'])


if __name__ == '__main__':
    main()
