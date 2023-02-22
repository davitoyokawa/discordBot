import datetime
import nextcord
import nextwave
from nextcord.ext import commands


class ControlPanel(nextcord.ui.View):
    def __init__(self, vc, ctx):
        super().__init__()
        self.vc = vc
        self.ctx = ctx

    @nextcord.ui.button(label="Retomar/Pausar", style=nextcord.ButtonStyle.blurple)
    async def resume_pause(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        if not interaction.user == self.ctx.author:
            return await interaction.response.send_message(
                "Você não pode fazer isso. Use o comando você mesmo para utiliza-los", ephemeral=False)
        for child in self.children:
            child.disabled = False
        if self.vc.is_paused():
            await self.vc.resume()
            await interaction.message.edit(content="Retomado", view=self)
        else:
            await self.vc.pause()
            await interaction.message.edit(content="Pausado", view=self)

    @nextcord.ui.button(label="Fila", style=nextcord.ButtonStyle.blurple)
    async def fila(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        if not interaction.user == self.ctx.author:
            return await interaction.response.send_message(
                "Você não pode fazer isso. Use o comando você mesmo para utiliza-los", ephemeral=True)
        for child in self.children:
            child.disabled = False
        button.disabled = True
        if self.vc.queue.is_empty:
            return await interaction.response.send_message("A fila está vazia", ephemeral=True)

        em = nextcord.Embed(title="Fila")
        queue = self.vc.queue.copy()
        cont_songs = 0

        for song in queue:
            cont_songs += 1
            em.add_field(name=f"Número {cont_songs}", value=f"'{song.title}'")
        await interaction.message.edit(embed=em, view=self)

    @nextcord.ui.button(label="Pular", style=nextcord.ButtonStyle.blurple)
    async def skip(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        if not interaction.user == self.ctx.author:
            return await interaction.response.send_message(
                "Você não pode fazer isso. Use o comando você mesmo para utiliza-los", ephemeral=True)
        for child in self.children:
            child.disabled = False
        button.disabled = True
        if self.vc.queue.is_empty:
            return await interaction.response.send_message("A fila está vazia", ephemeral=True)

        try:
            next_song = self.vc.queue.get()
            await self.vc.play(next_song)
            await interaction.message.edit(content=f"Tocando {next_song}", view=self)
        except Exception:
            return await interaction.response.send_message("A fila está vazia", ephemeral=True)

    @nextcord.ui.button(label="SAIR", style=nextcord.ButtonStyle.red)
    async def sair(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        if not interaction.user == self.ctx.author:
            return await interaction.response.send_message(
                "Você não pode fazer isso. Use o comando você mesmo para utiliza-los", ephemeral=True)
        for child in self.children:
            child.disabled = True
        await interaction.message.edit(content=":middle_finger:", view=self)
        await self.vc.disconnect()


class Music(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_nextwave_track_end(self, player: nextwave.Player, track: nextwave.Track, reason: str):
        ctx = player.ctx
        vc: player = ctx.voice_client

        if not reason.endswith("CED") and not reason.endswith("PED"):
            next_song = vc.queue.get()
            await vc.play(next_song)
            tocando_embed = nextcord.Embed(title=f"Tocando {next_song.title}", color=nextcord.Color.gold())
            tocando_embed.add_field(name=f"Duração:",
                                    value=f"{str(datetime.timedelta(seconds=next_song.duration))} segundos")
            tocando_embed.add_field(name=f"Url: ", value=f"{next_song.uri}")
            await ctx.send(embed=tocando_embed)

    @commands.command()
    async def painel(self, ctx: commands.Context):
        if not ctx.voice_client:
            vc: nextwave.Player = await ctx.author.voice.channel.connect(cls=nextwave.Player)
        elif not getattr(ctx.author.voice, "channel", None):
            return await ctx.send('É preciso estar em canal para usar esse comando :middle_finger:')
        elif not ctx.author.voice.channel == ctx.me.voice.channel:
            return await ctx.send('É preciso que eu esteja no mesmo canal que voce :joy: ')
        else:
            vc: nextwave.Player = ctx.voice_client
        if not vc.is_playing():
            return await ctx.send("Tem que ter uma musica tocando :zany_face: ")
        song = vc.track

        em = nextcord.Embed(title="Painel", description="Controle a música usando os botões")
        view = ControlPanel(vc, ctx)
        await ctx.send(view=view, embed=em)
        await view.wait()

    @commands.command()
    async def play(self, ctx: commands.Context, *, search: nextwave.YouTubeTrack):
        if not ctx.voice_client:
            vc: nextwave.Player = await ctx.author.voice.channel.connect(cls=nextwave.Player)
        elif not ctx.author.voice.channel == ctx.me.voice.channel:
            return await ctx.send('É preciso que eu esteja no mesmo canal que voce :joy: ')
        else:
            vc: nextwave.Player = ctx.voice_client
        try:
            if vc.queue.is_empty and not vc.is_playing():
                await vc.play(search)
                tocando_embed = nextcord.Embed(title=f"Tocando {search.title}", color=nextcord.Color.gold())
                tocando_embed.add_field(name=f"Duração:",
                                        value=f"{str(datetime.timedelta(seconds=search.duration))}")
                tocando_embed.add_field(name=f"Url: ", value=f"{search.uri}")
                tocando_embed.add_field(name=f"Pedido por: ", value=f"{ctx.author.mention}")
                await ctx.send(embed=tocando_embed)
            else:
                await vc.queue.put_wait(search)
                embed_fila = nextcord.Embed(title=f"'{search.title}'", description="Adicionado na fila")
                embed_fila.add_field(name=f"Numero na fila: {vc.queue.find_position(search) + 1}", value="")
                embed_fila.add_field(name="Pedido por:", value=ctx.author.mention)
                message = await ctx.send(embed=embed_fila)
            vc.ctx = ctx

        except Exception:
            await vc.disconnect(force=True)

    @commands.command()
    async def pause(self, ctx: commands.Context):
        if not ctx.voice_client:
            return await ctx.send('Não estou em nenhum canal de voz :face_exhaling: ')
        elif not getattr(ctx.author.voice, "channel", None):
            return await ctx.send('É preciso estar em canal para usar esse comando :middle_finger:')
        elif not ctx.author.voice.channel == ctx.me.voice.channel:
            return await ctx.send('É preciso que eu esteja no mesmo canal que voce')
        else:
            vc: nextwave.Player = ctx.voice_client

        await vc.pause()
        await ctx.send("Pausado!")

    @commands.command()
    async def resume(self, ctx: commands.Context):
        if not ctx.voice_client:
            return await ctx.send('Não estou em nenhum canal de voz :face_exhaling: ')
        elif not getattr(ctx.author.voice, "channel", None):
            return await ctx.send('É preciso estar em canal para usar esse comando :middle_finger:')
        elif not ctx.author.voice.channel == ctx.me.voice.channel:
            return await ctx.send('É preciso que eu esteja no mesmo canal que voce')
        else:
            vc: nextwave.Player = ctx.voice_client

        await vc.resume()
        await ctx.send("Tocando novamente!")

    @commands.command()
    async def stop(self, ctx: commands.Context):
        if not ctx.voice_client:
            return await ctx.send('Não estou em nenhum canal de voz :face_exhaling: ')
        elif not getattr(ctx.author.voice, "channel", None):
            return await ctx.send('É preciso estar em canal para usar esse comando :middle_finger:')
        elif not ctx.author.voice.channel == ctx.me.voice.channel:
            return await ctx.send('É preciso que eu esteja no mesmo canal que voce')
        else:
            vc: nextwave.Player = ctx.voice_client

        await vc.stop()
        await ctx.send(":skull: ")

    @commands.command()
    async def leave(self, ctx: commands.Context):
        if not getattr(ctx.author.voice, "channel", None):
            return await ctx.send('É preciso estar em canal para usar esse comando :middle_finger:')
        else:
            vc: nextwave.Player = ctx.voice_client

        await vc.disconnect()
        await ctx.send(':middle_finger:')

    @commands.command()
    async def skip(self, ctx: commands.Context):
        if not ctx.voice_client:
            return await ctx.send('Não estou em nenhum canal de voz :face_exhaling: ')
        elif not getattr(ctx.author.voice, "channel", None):
            return await ctx.send('É preciso estar em um canal para usar esse comando :middle_finger:')
        elif not ctx.author.voice.channel == ctx.voice_client.channel:
            return await ctx.send('É preciso que eu esteja no mesmo canal que voce')
        else:
            vc: nextwave.Player = ctx.voice_client

        if vc.queue.is_empty:
            await ctx.send('Não tem mais nada na fila :skull:')
            return await vc.stop()
        else:
            try:
                next_song = vc.queue.get()
                await vc.play(next_song)
                await ctx.send(f"Musica pulada por {ctx.author.mention}")
                tocando_embed = nextcord.Embed(title=f"Tocando {next_song.title}", color=nextcord.Color.gold())
                tocando_embed.add_field(name=f"Duração:",
                                        value=f"{str(datetime.timedelta(seconds=next_song.duration))} segundos")
                tocando_embed.add_field(name=f"Url: ", value=f"{next_song.uri}")
                tocando_embed.add_field(name=f"Pedido por: ", value=f"{ctx.author.mention}")
                return await ctx.send(embed=tocando_embed)
            except Exception as e:
                print(e)

    @commands.command()
    async def fila(self, ctx: commands.Context):
        if not ctx.voice_client:
            return await ctx.send('Não estou em nenhum canal de voz :face_exhaling: ')
        elif not getattr(ctx.author.voice, "channel", None):
            return await ctx.send('É preciso estar em um canal para usar esse comando :middle_finger:')
        elif not ctx.author.voice.channel == ctx.voice_client.channel:
            return await ctx.send('É preciso que eu esteja no mesmo canal que voce')
        else:
            vc: nextwave.Player = ctx.voice_client

        if vc.queue.is_empty:
            return await ctx.send("A fila está vazia")

        em = nextcord.Embed(title="Queue")
        queue = vc.queue.copy()
        cont_songs = 0
        for song in queue:
            cont_songs += 1
            em.add_field(name=f"Número {cont_songs}", value=f"'{song.title}'", inline=False)
        return await ctx.send(embed=em)

    @commands.command()
    async def volume(self, ctx: commands.Context, vol: int):
        if not ctx.voice_client:
            return await ctx.send('Não estou em nenhum canal de voz :face_exhaling: ')
        elif not getattr(ctx.author.voice, "channel", None):
            return await ctx.send('É preciso estar em um canal para usar esse comando :middle_finger:')
        elif not ctx.author.voice.channel == ctx.voice_client.channel:
            return await ctx.send('É preciso que eu esteja no mesmo canal que voce')
        else:
            vc: nextwave.Player = ctx.voice_client

        if vol < 0:
            await ctx.send("Volume negativo ??!? :middle_finger:")
        await ctx.send(f"Volume alterado para {vol}%")
        return await vc.set_volume(vol)

    @commands.command()
    async def emb(self, ctx: commands.Context):
        if not ctx.voice_client:
            return await ctx.send('Não estou em nenhum canal de voz :face_exhaling: ')
        elif not getattr(ctx.author.voice, "channel", None):
            return await ctx.send('É preciso estar em um canal para usar esse comando :middle_finger:')
        elif not ctx.author.voice.channel == ctx.voice_client.channel:
            return await ctx.send('É preciso que eu esteja no mesmo canal que voce')
        else:
            vc: nextwave.Player = ctx.voice_client
            vc.queue.shuffle()
            await ctx.send('Fila embaralhada!')



def setup(bot):
    bot.add_cog(Music(bot))
