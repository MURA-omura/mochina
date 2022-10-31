from datetime import datetime as dt
from pytz import timezone
from discord.commands import SlashCommandGroup
from discord.ext import commands, tasks


class ScheduleCog(commands.Cog):
    slash = SlashCommandGroup('vschedule', guild_ids=[683939861539192860, 542684644244586496])

    def __init__(self, bot):
        self.bot = bot
        self.tasks = []
        self.jst = timezone('Asia/Tokyo')
        self.guild_channel = {
            683939861539192860: 719443410062278746,
            542684644244586496: 715390348968329236,
        }

    @tasks.loop(seconds=5)
    async def run_schedule(self):
        await self.bot.wait_until_ready()
        datetime = dt.now(tz=self.jst)
        for gid, cid in self.guild_channel.items():
            channel = self.bot.get_channel(cid)
            for task in self.tasks.copy():
                if task['guild'] == gid and task['datetime'] <= datetime:
                    await channel.send(task['text'])
                    self.tasks.remove(task)
        print(self.tasks)

    @slash.command()
    async def add(self, ctx: commands.Context, text: str, datetime: str) -> None:
        '''スケジュールの追加'''
        task = {'guild': ctx.guild.id, 'datetime': dt.strptime(datetime, '%Y%m%d %H%M').replace(tzinfo=self.jst), 'text': text}
        self.tasks.append(task)
        await ctx.respond('Add schedule!')
