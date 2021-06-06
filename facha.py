import discord
from discord.ext import commands

bot = commands.Bot(command_prefix = '.')

@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Game('esculpir el tiempo'))
    print('Привет друзья!')

@bot.command()
async def hola(ctx):
    await ctx.send('Привет друзья!')

@bot.command()
async def lukilla(ctx):
    await ctx.send('.frase')

@bot.command()
async def chau(ctx):
    await ctx.send(f'{round(bot.latency * 1000)}ms')

@bot.command()
async def pastor(ctx):
    await ctx.send('Pastor es crack, nada más.')

@bot.command()
async def top(ctx):
    await ctx.send("https://letterboxd.com/pastorvsky/list/mejores-peliculas-de-la-historia-top-100/")

@bot.command()
async def topless(ctx):
    await ctx.send("https://i0.wp.com/lecturassumergidas.com/wp-content/uploads/2016/10/image.jpg?resize=450%2C630&ssl=1")

@bot.command()
async def stalker(ctx):
    await ctx.send("https://www.youtube.com/watch?v=TGRDYpCmMcM")

@bot.command()
async def zerkalo(ctx):
    await ctx.send("https://www.youtube.com/watch?v=CYZhXm02kN0")

@bot.command()
async def offret(ctx):
    await ctx.send("https://www.youtube.com/watch?v=PlV4k2GNGmo")

@bot.command()
async def nostalghia(ctx):
    await ctx.send("https://www.youtube.com/watch?v=-gH1cprEg0w")

@bot.command()
async def andreyrublev(ctx):
    await ctx.send("https://www.youtube.com/watch?v=OsEnNDr6YfA")

@bot.command()
async def ivanovo(ctx):
    await ctx.send("https://www.youtube.com/watch?v=aRkPoF7iVGc")

@bot.command()
async def frase(ctx):
    await ctx.send("Cierren el orto manga de puto")

@bot.command()
async def solyaris(ctx):
    await ctx.send("https://www.youtube.com/watch?v=6-4KydP92ss")
    await ctx.send("https://www.youtube.com/watch?v=xXa6XpaxBS0")

@bot.command()
async def infoChess(ctx):
    await ctx.send("https://drive.google.com/file/d/1CbPjXkNlE5d7gGXeoumgL-vfrG8T5Jkc/view")

@bot.command()
@commands.has_permissions(manage_messages=True)
async def limpiar(ctx, amount=2):
    await ctx.channel.purge(limit=amount)

@limpiar.error
async def limpiar_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send('Hermano no me pediste nada.')

bot.run('Nzg4MTM2MDcxMzA1MjMyMzk0.X9fG6g.9Cb3nIUNkXHUTvBkD_I6OW-jsBg')
