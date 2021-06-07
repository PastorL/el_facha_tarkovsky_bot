import discord
import sqlite3
import random
from discord.ext import commands

bot = commands.Bot(command_prefix = '.')

@bot.event
async def on_message(message):
    ctx = await bot.get_context(message)
    if message.author == bot.user:
        return
    if message.author.name == 'PsiwareBot':
        psiware_bot_frase = message.content
        await insert_frase(ctx, psiware_bot_frase, 'PsiwareBot')
    await bot.process_commands(message)



@bot.event
async def on_ready():
    db = sqlite3.connect('main.sqlite')
    cursor = db.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS frases(
            id_frase INTEGER NOT NULL UNIQUE,
            descripcion TEXT,
            usuario TEXT,
            PRIMARY KEY(id_frase AUTOINCREMENT)
        )
    ''')
    await bot.change_presence(activity=discord.Game('esculpir el tiempo'))
    print('Привет друзья!')



@bot.command()
async def addFrase(ctx,*,frase):
    autor = ctx.message.author.name
    await insert_frase(ctx, frase, autor)



@bot.command()
async def frase(ctx):
    db = sqlite3.connect('main.sqlite')
    cursor = db.cursor()
    try:
        cursor.execute("SELECT COUNT (*) FROM frases")
        result = cursor.fetchone()
        id_frase = random.randint(1, result[0])
        cursor.execute(f"SELECT descripcion FROM frases WHERE id_frase = {id_frase}")
        frase_descripcion = cursor.fetchone()
        await ctx.send(frase_descripcion[0])
    except Exception as exc:
        await ctx.send('No anda nada cuando traigo las frases: {}'.format(exc))
    cursor.close()
    db.close()



async def insert_frase(ctx, frase, autor):
    if validate_frase(frase):
        db = sqlite3.connect('main.sqlite')
        cursor = db.cursor()
        sql = ("INSERT INTO frases(descripcion, usuario) VALUES (?,?)")
        val = (frase, autor)
        try:
            result = cursor.execute(sql, val)
            await ctx.send("Frase agregada товарищ!")
        except Exception as exc:
            await ctx.send('No anda nada cuando guarda las frases: {}'.format(exc))
        db.commit()
        cursor.close()
        db.close()
    else:
        await ctx.send("La frase ya existe сука блять!")



def validate_frase(frase):
    db = sqlite3.connect('main.sqlite')
    cursor = db.cursor()
    try:
        cursor.execute(f"SELECT COUNT (*) FROM frases WHERE descripcion = '{frase}'")
        result = 0
        result = cursor.fetchone()[0]
        if result == 0:
            return True
        else:
            return False
    except Exception as exc:
        print('Error al validar la frase.')
    finally:
        cursor.close()
        db.close()



@bot.command()
async def tasBien(ctx):
    await ctx.send(f'{round(bot.latency * 1000)}ms')

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

bot.run('Nzg4MTM2MDcxMzA1MjMyMzk0.X9fG6g.8fyxKV5848JeWTjvk_Y8QCk046I')
