import nextcord
from nextcord.ext import commands
import aiohttp


class Aleatorio(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def trollface(self, ctx):
        file = open("trollface.txt", encoding="utf8")
        t = ""
        for line in file.readlines():
            t += line
        file.close()
        await ctx.send(t)

    @commands.command()
    async def mostra(self, ctx):
        file = open("mostra.txt", encoding="utf8")
        t = ""
        for line in file.readlines():
            t += line
        file.close()
        await ctx.send(t)

    @commands.command()
    async def eval(self, ctx, e):
        novo = e.replace("x", "*")
        await ctx.send(eval(novo))

    @commands.command()
    async def gpt(self, ctx: commands.command(), *, prompt: str):
        token = "GPT_token"
        async with aiohttp.ClientSession() as session:
            payload = {
                'model': "text-davinci-003",
                'prompt': prompt,
                'temperature': 0.7,
                'max_tokens': 2500,
                'top_p': 1,
                'frequency_penalty': 0,
                'presence_penalty': 0,
                'best_of': 1,
            }
            headers = {"Authorization": f"Bearer {token}"}
            async with session.post('https://api.openai.com/v1/completions', headers=headers, json=payload) as resp:
                response = await resp.json()
                embed = nextcord.Embed(title=f"Eu acho que ...", description=response['choices'][0]["text"])
            await ctx.send(embed=embed)

    @commands.command()
    async def mover(self, ctx: commands.Context, membro: nextcord.Member, canal: nextcord.VoiceChannel):
        try:
            await membro.move_to(canal)
        except nextcord.ext.commands.errors.ChannelNotFound:
            await ctx.send(f"Não existe nenhum canal '{canal}'")
        except nextcord.ext.commands.errors.UserNotFound:
            await ctx.send(f"Não existe nenhum usuario chamado '{membro.name}'")

    @commands.command()
    async def mover2(self, ctx: commands.Context, membro: nextcord.Member, canal: nextcord.VoiceChannel, canal2: nextcord.VoiceChannel, n):
        n = int(n)
        for i in range(n):
            await membro.move_to(canal)
            await membro.move_to(canal2)

    @commands.command()
    async def movert(self, ctx: commands.Context, *membros: nextcord.Member):
        try:
            canal = ctx.author.voice.channel
            for membro in membros:
                if not isinstance(membro, nextcord.Member):
                    await ctx.send(f"Não existe {membro}!")
                else:
                    await membro.move_to(canal)
        except Exception as e:
            print(e)


def setup(bot):
    bot.add_cog(Aleatorio(bot))
