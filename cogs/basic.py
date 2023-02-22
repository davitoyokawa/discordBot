import os

from nextcord.ext import commands
import nextcord
import responses


class Basic(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def join(self, ctx):
        if ctx.author.voice:
            channel = ctx.author.voice.channel
            await channel.connect()
        else:
            await ctx.send('É preciso estar no canal para usar esse comando :middle_finger:')

    @commands.command()
    async def help(self, ctx):
        embed = nextcord.Embed(
            title='Comandos gerais',
            description='',
            color=nextcord.Color.blue()
        )
        embed.add_field(
            name='*help',
            value='Lista de todos os comandos',
            inline=True
        )
        embed.add_field(
            name='*imp',
            value='Vídeo/Imagem aleatória "importante"',
            inline=False
        )
        embed.add_field(
            name='*info',
            value='Id, nome e avatar de alguém',
            inline=False
        )
        embed.add_field(
            name='*lista',
            value='Mostra todos os áudios que o bot tem',
            inline=False
        )
        embed.add_field(
            name='*p',
            value='Toca algum áudio da *lista',
            inline=False
        )
        embed.add_field(
            name='*leave',
            value='Expulsa o bot da call',
            inline=False
        )
        embed_music = nextcord.Embed(
            title='Comandos de musica',
            description='',
            color=nextcord.Color.blurple()
        )
        embed_music.add_field(
            name='*volume',
            value='Altera o volume do bot',
            inline=False
        )
        embed_music.add_field(
            name='*play',
            value='Coloca algo na fila para tocar',
            inline=False
        )
        embed_music.add_field(
            name='*skip',
            value='Pula para a próxima música',
            inline=False
        )
        embed_music.add_field(
            name='*stop',
            value='Para o que o bot esta tocando',
            inline=False
        )
        embed_music.add_field(
            name='*pause',
            value='Pausa o que o bot esta tocando',
            inline=False
        )
        embed_music.add_field(
            name='*resume',
            value='Retoma o áudio pausado',
            inline=False
        )
        embed_music.add_field(
            name='*fila',
            value='Mostra as próximas musicas na fila',
            inline=False
        )
        embed_music.add_field(
            name='*painel',
            value='Mostra um painel para controlar as musicas',
            inline=False
        )
        embed_music.add_field(
            name='*emb',
            value='Embaralha as musicas da fila',
            inline=False
        )
        await ctx.channel.send(embed=embed)
        await ctx.channel.send(embed=embed_music)

    @commands.command()
    async def imp(self, ctx):
        response = responses.handle_response("")
        await ctx.channel.send(response)

    @commands.command()
    async def imp_vid(self, ctx):
        response = responses.handle_response("vid")
        await ctx.channel.send(response)

    @commands.command()
    async def imp_img(self, ctx):
        response = responses.handle_response("img")
        await ctx.channel.send(response)

    @commands.command()
    async def kick(self, ctx: commands.Context, membro: nextcord.Member):
        try:
            await membro.disconnect()
            await ctx.send(f"{ctx.author.mention} kickou {membro.mention}")
        except nextcord.ext.commands.errors.UserNotFound:
            await ctx.send(f"Não existe nenhum usuario chamado '{membro.name}'")

    @commands.command()
    async def mute(self, ctx, membro: nextcord.Member):
        await membro.edit(mute=True)
        await membro.edit(deafen=True)

    @commands.command()
    async def unmute(self, ctx, membro: nextcord.Member):
        await membro.edit(mute=False)
        await membro.edit(deafen=False)

    @commands.command()
    async def lista(self, ctx):
        embed2 = nextcord.Embed(
            title='Alguns Audios',
            color=nextcord.Color.blue(),
            colour=nextcord.Color.dark_blue()
        )
        embed2.add_field(
            name='Doentes',
            value='-bemlembrado'
                  '\n-botconlow '
                  '\n-calaboca '
                  '\n-eai '
                  '\n-fabio1 '
                  '\n-falacara '
                  '\n-gatofdp '
                  '\n-grito1 '
                  '\n-grito2 '
                  '\n-gustavocarro '
                  '\n-gustavogemendo '
                  '\n-jon '
                  '\n-misugue '
                  '\n-misugui '
                  '\n-misuguiputo '
                  '\n-pqp '
                  '\n-pqvc '
                  '\n-tefude '
                  '\n-valeu '
                  '\n-xbyyg',
            inline=True
        )
        embed2.add_field(
            name='Minecraft',
            value='-bau'
                  '\n-bau2'
                  '\n-cow '
                  '\n-uh'
                  '\n-villager1'
                  '\n-villager2'
                  '\n-villager3'
                  '\n-villager4'
                  '\n-zombie',
            inline=True
        )
        embed2.add_field(
            name='Memes',
            value='-buraco'
                  '\n-errou'
                  '\n-eugostumm'
                  '\n-rapaz'
                  '\n-receba'
                  '\n-tiraessemlk'
                  '\n-bob',
            inline=True
        )
        await ctx.channel.send(embed=embed2)

    @commands.command()
    async def lista_total(self, ctx):
        lista_2 = ''
        lista = [item[:len(item)-4] for item in os.listdir('aud/')]
        for nome in lista:
            lista_2 += '-'+nome+'\n'
        embed = nextcord.Embed(
            title='Audios',
            color=nextcord.Color.blue(),
            colour=nextcord.Color.dark_blue(),
            description=lista_2
        )
        await ctx.channel.send(embed=embed)

    @commands.command()
    async def c(self, ctx, amount=5):
        if amount <= 20:
            await ctx.channel.purge(limit=amount)
        else:
            await ctx.send('Máx. 20 ')

    @commands.command()
    async def info(self, ctx: commands.Context, user: nextcord.User):
        try:
            user_id = user.id
            username = user.name
            avatar = user.display_avatar.url
            await ctx.send(f'Id: {user_id} - {username}\n{avatar}')
        except nextcord.ext.commands.errors.MissingRequiredArgument:
            await ctx.send('Use *info @user')

    @info.error
    async def userinfo_error(self: commands.Context, error: commands.CommandError):
        if isinstance(error, commands.BadArgument):
            return await self.send('Não foi possivel achar esse usuário.')

    @commands.Cog.listener()
    async def on_message(self, message):
        if 'kkkkkk' in message.content or message.content == 'boa':
            await message.add_reaction('\U0001F602')
            await message.add_reaction('\U0001F923')
            await message.add_reaction('\U0001F595')
            await message.add_reaction('\U0001F90F')
            await message.add_reaction('\U0001F924')
            await message.add_reaction('\U0001F480')

        if 'xbyyg' in message.content:
            await message.add_reaction('\U0001F1FB')
            await message.add_reaction('\U0001F1EE')
            await message.add_reaction('\U0001F1E6')
            await message.add_reaction('\U0001F1E9')
            await message.add_reaction('\U0001F1F4')
            await message.add_reaction('\U00002757')

    @commands.Cog.listener()
    async def on_reaction_add(self, reaction, user):
        if reaction.message:
            message = reaction.message
            if reaction.emoji == "😂":
                await message.add_reaction('\U0001F923')
                await message.add_reaction('\U0001F595')
                await message.add_reaction('\U0001F90F')
                await message.add_reaction('\U0001F924')
                await message.add_reaction('\U0001F480')


def setup(bot):
    bot.add_cog(Basic(bot))
