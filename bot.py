import os
import nextcord
import nextwave
from nextcord.ext import commands
from nextwave.ext import spotify
from nextcord import FFmpegPCMAudio

FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}


def run_discord_bot():
    TOKEN = 'DISCORD_TOKEN'
    intents = nextcord.Intents.default()
    intents.message_content = True
    bot = commands.Bot(command_prefix='*', intents=intents)
    bot.remove_command('help')

    @bot.event
    async def on_ready():
        bot.loop.create_task(node_connect())
        print(f'{bot.user} is running!')

    for fn in os.listdir('./cogs'):
        if fn.endswith(".py"):
            bot.load_extension(f"cogs.{fn[:-3]}")

    @bot.event
    async def on_nextwave_node_ready(node: nextwave.Node):
        print(f"Node {node.identifier} is ready")

    async def node_connect():
        await bot.wait_until_ready()
        await nextwave.NodePool.create_node(bot=bot, host='lavalink.mariliun.ml', port=443,
                                            password="lavaliun", https=True,
                                            spotify_client=spotify.SpotifyClient(
                                                client_id="SPOTIFY_ID",
                                                client_secret="SPOTIFY_Password"))

    @bot.command()
    async def s(ctx):
        voice = nextcord.utils.get(bot.voice_clients, guild=ctx.guild)
        await voice.disconnect(force=True)

    @bot.command()
    async def p(ctx, arg):
        if not ctx.guild.voice_client:
            if ctx.author.voice:
                channel = ctx.author.voice.channel
                await channel.connect()
            else:
                await ctx.send('É preciso estar no canal para usar esse comando :middle_finger:')

        voice = ctx.guild.voice_client
        arg = 'aud/' + arg + '.mp3'
        source = FFmpegPCMAudio(arg)

        if voice.is_playing():
            await ctx.send("k")
        else:
            await voice.play(source)

    bot.run(TOKEN, reconnect=True)
