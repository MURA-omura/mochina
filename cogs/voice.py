import discord
from discord.commands import SlashCommandGroup
from discord.ext import commands
import asyncio
import youtube_dl


ytdl_format_options = {
    'format': 'bestaudio/best',
    'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0' # bind to ipv4 since ipv6 addresses cause issues sometimes
}
ytdl = youtube_dl.YoutubeDL(ytdl_format_options)
ffmpeg_options = {'options': '-vn'}

class YTDLSource(discord.PCMVolumeTransformer):
    def __init__(self, source, *, data, volume=0.5):
        super().__init__(source, volume)

    @classmethod
    async def from_url(cls, url, *, loop=None, stream=False):
        loop = loop or asyncio.get_event_loop()
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=False))

        if 'entries' in data:
            # take first item from a playlist
            data = data['entries'][0]

        player = discord.FFmpegPCMAudio(data['url'], **ffmpeg_options)
        return player


class VoiceCog(commands.Cog):
    slash = SlashCommandGroup('vvoice', guild_ids=[683939861539192860, 542684644244586496])

    def __init__(self, bot):
        self.bot = bot
        self.vc = None
        self.music_queue = []

    def play_next(self, e=None):
        fut = asyncio.run_coroutine_threadsafe(self.play_queue(), self.bot.loop)
        try:
            fut.result()
        except Exception as e:
            print(e)

    async def play_queue(self):
        if self.music_queue:
            player = await YTDLSource.from_url(self.music_queue[0], loop=self.bot.loop)
            #await ctx.send(f'Play {self.music_queue[0]}')
            del self.music_queue[0]
            self.vc.play(player, after=self.play_next)

    @slash.command()
    async def join(self, ctx: commands.Context) -> None:
        '''ボイスチャンネルへ参加'''
        voice_state = ctx.author.voice
        if (not voice_state) or (not voice_state.channel):
            #もし送信者がどこのチャンネルにも入っていないなら
            await ctx.respond('ボイスチャンネルに参加してね')
            return
        channel = voice_state.channel
        self.vc = await channel.connect()
        await ctx.respond('Join!')

    @slash.command()
    async def bye(self, ctx: commands.Context) -> None:
        '''ボイスチャンネルから切断する'''
        if self.vc is None:
            await ctx.respond('Botはこのサーバーのボイスチャンネルに参加していないよ')
        else:
            await self.vc.disconnect()
            self.vc = None
            await ctx.respond('Bye!')

    @slash.command()
    async def play(self, ctx: commands.Context, url: str) -> None:
        '''音楽を再生する'''
        if self.vc is None:
            await self.join(ctx)
        if self.vc.is_playing():
            self.music_queue.append(url)
            await ctx.respond('Add url to queue!')
        else:
            player = await YTDLSource.from_url(url, loop=self.bot.loop)
            self.vc.play(player, after=self.play_next)
            await ctx.respond('Play!')

    def skip(self, ctx: commands.Context) -> None:
        '''次の音楽を再生する'''
        if self.vc.is_playing():
            self.vc.stop()
        if len(self.music_queue) > 0:
            next_url = self.music_queue[0]
            self.music_queue = self.music_queue[1:]
            asyncio.run(self.play(ctx, next_url))
        else:
            asyncio.run(ctx.respond('No music queue!'))

    @slash.command()
    async def stop(self, ctx: commands.Context) -> None:
        '''音楽を停止する'''
        if self.vc is None:
            await ctx.respond('ボイスチャンネルに入ってないよ')
            return
        self.vc.stop()
        await ctx.respond('Stop!')
