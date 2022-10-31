from datetime import datetime as dt, timedelta, timezone
import random

import discord
from discord.commands import SlashCommandGroup
from discord.ext import commands, tasks


class ScheduleCog(commands.Cog):
    slash = SlashCommandGroup('vschedule', guild_ids=[683939861539192860, 542684644244586496])

    def __init__(self, bot):
        self.bot = bot
        self.tasks = []
        self.jst = timezone(timedelta(hours=+9), 'JST')
        self.guild_channel = {
            683939861539192860: 719443410062278746,
            542684644244586496: 715390348968329236,
        }
        self.activity_list = [
            'YouTube',
            'Twitter',
            'Discord',
        ]

    @tasks.loop(seconds=10)
    async def run_schedule(self):
        await self.bot.wait_until_ready()
        datetime = dt.now(tz=self.jst)
        # ステータスの変更
        if datetime.minute == 0 and datetime.second < 10:
            await self.bot.change_presence(activity=discord.Game(name=random.choice(self.activity_list)))

        # タスクの送信
        for gid, cid in self.guild_channel.items():
            channel = self.bot.get_channel(cid)
            for task in self.tasks.copy():
                if task['guild'] == gid and task['datetime'] <= datetime:
                    await channel.send(f"<@{task['user']}> {task['text']}")
                    self.tasks.remove(task)

    @slash.command()
    async def add(self, ctx: commands.Context, text: str, datetime: str) -> None:
        '''スケジュールの追加'''
        datetime = dt.strptime(datetime, '%Y%m%d %H%M').replace(tzinfo=self.jst)
        if datetime <= dt.now(tz=self.jst):
            await ctx.respond('現在時刻より後を指定してね')
        else:
            task = {'guild': ctx.guild.id, 'user': ctx.user.id, 'datetime': datetime, 'text': text}
            self.tasks.append(task)
            await ctx.respond('スケジュールを追加したよ')

    @slash.command()
    async def show(self, ctx: commands.Context) -> None:
        '''スケジュールの確認'''
        respond_text = ''
        for task in self.tasks:
            if task['guild'] == ctx.guild.id:
                respond_text += f"{task['datetime'].strftime('%Y/%m/%d %H:%M')}  {task['text']}\n"
        if respond_text == '':
            await ctx.respond('タスクは無いよ')
        else:
            await ctx.respond(respond_text[:-1])
