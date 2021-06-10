import discord
import random
import imdb
import psycopg2
from discord.ext import commands

bot = commands.Bot(command_prefix = '.')
moviesDB = imdb.IMDb()
PG_PW = open("PG_PW.txt", 'r').read()
PG_DB = open("PG_DB.txt", 'r').read()
PG_US = open("PG_US.txt", 'r').read()
PG_HS = open("PG_HS.txt", 'r').read()
db = psycopg2.connect(host = PG_HS, database = PG_DB, user = PG_US, password = PG_PW)
frases_respuestas = []


@bot.event
async def on_message(message):
    ctx = await bot.get_context(message)
    if message.author == bot.user:
        return
    if message.author.name == 'PsiwareBot':
        psiware_bot_frase = message.content
        await insert_frase(ctx, psiware_bot_frase, 'PsiwareBot')
    if message.content in frases_respuestas:
        await frase(ctx)
    await bot.process_commands(message)



@bot.event
async def on_ready():
    cursor = db.cursor()
    try:
        cursor.execute("SELECT frase_respuesta FROM frases_respuestas")
        frases = cursor.fetchall()
        for frase in frases:
            frases_respuestas.append(frase[0])
    except Exception as exc:
        print(f"No pude obtener las frases a responder: {exc}")
    await bot.change_presence(activity=discord.Game('esculpir el tiempo'))
    print('Привет друзья!')



@bot.command()
async def addFrase(ctx,*,frase):
    autor = ctx.message.author.name
    await insert_frase(ctx, frase, autor)



@bot.command()
async def deleteFrase(ctx,*,frase):
    autor = ctx.message.author.name
    await delete_frase(ctx, frase, autor)



@bot.command()
async def frase(ctx):
    cursor = db.cursor()
    try:
        cursor.execute("SELECT descripcion FROM frases ORDER BY RANDOM() LIMIT 1")
        frase = cursor.fetchone()
        await ctx.send(frase[0])
    except Exception as exc:
        await ctx.send('No anda nada cuando traigo las frases: {}'.format(exc))
    cursor.close()



async def insert_frase(ctx, frase, autor):
    if validate_frase(frase):
        cursor = db.cursor()
        sql = (f"INSERT INTO frases(descripcion, usuario) VALUES ('{frase}','{autor}')")
        try:
            result = cursor.execute(sql)
            await ctx.send("Frase agregada товарищ!")
        except Exception as exc:
            await ctx.send('No anda nada cuando guarda las frases: {}'.format(exc))
        db.commit()
        cursor.close()
    else:
        await ctx.send("La frase ya existe сука блять!")



async def delete_frase(ctx, frase, autor):
    if not validate_frase(frase):
        cursor = db.cursor()
        sql = (f"DELETE FROM frases WHERE descripcion = '{frase}'")
        try:
            result = cursor.execute(sql)
            await ctx.send("Frase borrada товарищ!")
            sql2 = (f"INSERT INTO frases_borradas(descripcion, autor_borrado) VALUES ('{frase}','{autor}')")
            result2 = cursor.execute(sql2)
        except Exception as exc:
            await ctx.send('No anda nada cuando borro las frases: {}'.format(exc))
        db.commit()
        cursor.close()
    else:
        await ctx.send("La frase no existe сука блять!")



def validate_frase(frase):
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



@bot.command()
async def buscame(ctx,*,movie_to_search):
    movies = moviesDB.search_movie(movie_to_search)
    cont = 1
    await ctx.send("Estas son las que encontre: ")
    for movie in movies:
        if cont <= 5:
            try:
                title = movie['title']
                year = movie['year']
                await ctx.send(f'{title} - {year}')
            except:
                continue
            finally:
                cont += 1



@bot.command()
async def agregarTop(ctx,*,link_top):
    cursor = db.cursor()
    autor = ctx.message.author.name
    top = buscar_top(autor)
    if top == None:
        sql = (f"INSERT INTO tops(link, usuario) VALUES ('{link_top}','{autor}')")
        try:
            result = cursor.execute(sql)
            await ctx.send("Top agregado товарищ!")
        except Exception as exc:
            await ctx.send('No anda nada cuando guardo el top: {}'.format(exc))
    else:
        sql = (f"UPDATE tops SET link = '{link_top}' WHERE usuario = '{autor}'")
        try:
            result = cursor.execute(sql)
            await ctx.send('Top actualizado товарищ!')
        except Exception as exc:
            await ctx.send('No anda nada cuando guardo el top: {}'.format(exc))
    db.commit()
    cursor.close()


def buscar_top(autor):
    cursor = db.cursor()
    try:
        cursor.execute(f"SELECT link FROM tops WHERE usuario = '{autor}'")
        top_link = cursor.fetchone()
        if top_link == None:
            return None
        else:
            return top_link[0]
    except Exception as exc:
        print('Error al traer el top.')
    finally:
        cursor.close()



@bot.command()
async def miTop(ctx):
    autor = ctx.message.author.name
    top = buscar_top(autor)
    if top == None:
        await ctx.send("Todavia no existe un top para " + autor)
    else:
        await ctx.send(top)



@bot.command()
async def top(ctx,*,usuario):
    top = buscar_top(usuario)
    if top == None:
        await ctx.send("Todavia no existe un top para " + autor)
    else:
        await ctx.send(top)



@bot.command()
async def tasBien(ctx):
    await ctx.send(f'{round(bot.latency * 1000)}ms')


@bot.command()
async def stalker(ctx):
    await ctx.send("https://www.youtube.com/watch?v=TGRDYpCmMcM")


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
