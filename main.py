import random
import yaml
import discord

bot = discord.Bot(prefix='$')

@bot.event
async def on_ready():
    print(f"{bot.user}としてログインしました！")


@bot.slash_command(guild_ids=[683939861539192860, 542684644244586496])
async def ping(ctx):
    await ctx.respond("pong")


@bot.slash_command(guild_ids=[542684644244586496])
async def amasita(ctx):
    '''雨下さんがママか確認'''
    if random.randint(1, 10000) % 5 == 0:
        await ctx.respond(f'雨下さんは{ctx.author.display_name}さんのママです。')
    elif random.randint(1, 10000) % 5 == 1:
        await ctx.respond(f'雨下さん{ctx.author.display_name}さんのママじゃないので......（冷静）')
    else:
        await ctx.respond(f'雨下さんは{ctx.author.display_name}さんのママではありません。')


@bot.slash_command(guild_ids=[683939861539192860, 542684644244586496])
async def join(ctx):
    '''ボイスチャンネルへ参加'''
    voice_state = ctx.author.voice
    if (not voice_state) or (not voice_state.channel):
        #もし送信者がどこのチャンネルにも入っていないなら
        await ctx.respond('ボイスチャンネルに参加してね')
        return
    channel = voice_state.channel
    await channel.connect()
    await ctx.respond('Join!')


@bot.slash_command(guild_ids=[683939861539192860, 542684644244586496])
async def bye(ctx):
    '''ボイスチャンネルから切断する'''
    voice_client = ctx.message.guild.voice_client
    if not voice_client:
        await ctx.respond('Botはこのサーバーのボイスチャンネルに参加していないよ')
        return
    await voice_client.disconnect()
    await ctx.respond('Bye!')


with open('config.yml', 'r') as f:
    cfg = yaml.safe_load(f)
bot.run(cfg['TOKEN'])
