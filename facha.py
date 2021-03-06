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
servers_availables = []
ignored_users = []



@bot.event
async def on_message(message):
    if message.author.name not in ignored_users:
        ctx = await bot.get_context(message)
        if validate_server(ctx):
            await process_message(ctx,message)
        else:
            if await validate_pastor(ctx):
                await process_message(ctx,message)
            else:
                await ctx.send('No te haga el loco y anda a escribir al servidor.')



async def process_message(ctx,message):
    if message.author == bot.user:
        return
    if (message.content in frases_respuestas) or custom_responses(message.content):
        await frase(ctx)
    await bot.process_commands(message)



def custom_responses(message):
    if ('Facha' in message) and ('deci' in message):
        return True
    if ('facha' in message) and ('deci' in message):
        return True
    if ('Facha' in message) and ('?' in message):
        return True
    if ('facha' in message) and ('?' in message):
        return True
    if ('Facha' in message) and ('conta' in message):
        return True
    if ('facha' in message) and ('conta' in message):
        return True



@bot.event
async def on_ready():
    cursor = db.cursor()
    try:
        cursor.execute("SELECT frase_respuesta FROM frases_respuestas")
        frases = cursor.fetchall()
        for frase in frases:
            frases_respuestas.append(frase[0])
        cursor.execute("SELECT description FROM available_servers")
        servers = cursor.fetchall()
        for server in servers:
            servers_availables.append(server[0])
        cursor.execute("SELECT user_name FROM ignored_users")
        ignored_users_db = cursor.fetchall()
        for user in ignored_users_db:
            ignored_users.append(user[0])
    except Exception as exc:
        print(f"No pude obtener las frases  y servidores a responder: {exc}")
    await bot.change_presence(activity=discord.Game('esculpir el tiempo'))
    print('???????????? ????????????!')



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
    server_name = ctx.message.guild.name
    try:
        #cursor.execute(f"SELECT descripcion FROM frases ORDER BY RANDOM() LIMIT 1")
        cursor.execute(f"SELECT descripcion FROM frases WHERE server_name='{server_name}' ORDER BY RANDOM() LIMIT 1")
        frase = cursor.fetchone()
        await ctx.send(frase[0])
    except Exception as exc:
        await ctx.send('No anda nada cuando traigo las frases: {}'.format(exc))
    cursor.close()



@bot.command()
async def review(ctx,*,movie):
    cursor = db.cursor()
    try:
        cursor.execute(f"SELECT movie_name FROM stalkers_movies WHERE movie_name = '{get_frase(movie)}'")
        movie = cursor.fetchone()
        if movie == None:
            await ctx.send('No que yo sepa')
        else:
            await ctx.send(f'{movie[0]} se hablo en el podcast, en un futuro te voy a decir en cual.')
    except Exception as exc:
        await ctx.send('No anda nada cuando busco el film: {}'.format(exc))
    cursor.close()



@bot.command()
async def tegobi(ctx):
    cursor = db.cursor()
    server_name = ctx.message.guild.name
    try:
        cursor.execute(f"SELECT tegobi_foto FROM tegobis ORDER BY RANDOM() LIMIT 1")
        frase = cursor.fetchone()
        await ctx.send(frase[0])
    except Exception as exc:
        await ctx.send('No anda nada cuando traigo las frases: {}'.format(exc))
    cursor.close()



async def insert_frase(ctx, frase, autor):
    if validate_frase(frase):
        cursor = db.cursor()
        server_name = ctx.message.guild.name
        sql = (f"INSERT INTO frases(descripcion, usuario, server_name) VALUES ('{get_frase(frase)}','{autor}','{server_name}')")
        try:
            result = cursor.execute(sql)
            await ctx.send("Frase agregada ??????????????!")
        except Exception as exc:
            await ctx.send('No anda nada cuando guarda las frases: {}'.format(exc))
        db.commit()
        cursor.close()
    else:
        await ctx.send("La frase ya existe ???????? ??????????!")



async def delete_frase(ctx, frase, autor):
    if not validate_frase(frase):
        cursor = db.cursor()
        server_name = ctx.message.guild.name
        sql = (f"DELETE FROM frases WHERE descripcion = '{get_frase(frase)}' AND server_name = '{server_name}'")
        try:
            result = cursor.execute(sql)
            await ctx.send("Frase borrada ??????????????!")
            sql2 = (f"INSERT INTO frases_borradas(descripcion, autor_borrado) VALUES ('{get_frase(frase)}','{autor}')")
            result2 = cursor.execute(sql2)
        except Exception as exc:
            await ctx.send('No anda nada cuando borro las frases: {}'.format(exc))
        db.commit()
        cursor.close()
    else:
        await ctx.send("La frase no existe ???????? ??????????!")



def validate_frase(frase):
    cursor = db.cursor()
    try:
        cursor.execute(f"SELECT COUNT (*) FROM frases WHERE descripcion = '{get_frase(frase)}'")
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
                print(movie)
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
            await ctx.send("Top agregado ??????????????!")
        except Exception as exc:
            await ctx.send('No anda nada cuando guardo el top: {}'.format(exc))
    else:
        sql = (f"UPDATE tops SET link = '{link_top}' WHERE usuario = '{autor}'")
        try:
            result = cursor.execute(sql)
            await ctx.send('Top actualizado ??????????????!')
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
async def quienFueElHijoDePuta(ctx,*,frase):
    if await validate_pastor(ctx):
        cursor = db.cursor()
        try:
            cursor.execute(f"SELECT usuario FROM frases WHERE descripcion = '{get_frase(frase)}'")
            culpable = cursor.fetchone()
            if culpable == None:
                await ctx.send("Disculpe maestro pero no encontre esa frase.")
            else:
                await ctx.send(f"El hije de pute fue: {culpable[0]}")
        except Exception as exc:
            await ctx.send(f"Error al traer al hijo de puta: {exc}")
        finally:
            cursor.close()



def validate_server(ctx):
    server_name = None
    try:
        server_name = ctx.message.guild.name
    except Exception as exc:
        print(f"{ctx.message.author.name} me esta hablando por privado")
    if (server_name == None) or (server_name not in servers_availables):
        return False
    else:
        return True



@bot.command()
async def ejecutar(ctx,*,sql):
    if await validate_pastor(ctx):
        cursor = db.cursor()
        try:
            cursor.execute(sql)
            db.commit()
            await ctx.send("Ejecutado master.")
        except Exception as exc:
            await ctx.send(f"No pude ejecutar el sql: {exc}")
        finally:
            cursor.close()



async def validate_pastor(ctx):
    autor = ctx.message.author.id
    if autor == 186664188750462977:
        return True
    else:
        await ctx.send("Quien te conoce pa? so boludo y no tene huevo.")
        return False



def get_frase(frase):
    return frase.replace("'", "??")



@bot.command()
async def koke(ctx,*,koke):
    if await validate_pastor(ctx):
        cursor = db.cursor()
        try:
            cursor.execute(f"SELECT * FROM pokemones WHERE poke_name = '{get_frase(koke)}'")
            kokemon = cursor.fetchone()
            db.commit()
            await show_pokemon_data(ctx,kokemon)
        except Exception as exc:
            await ctx.send(f"No pude traer la data del kokemon: {exc}")
        finally:
            cursor.close()



@bot.command()
async def pokedex(ctx,*,id_koke):
    if await validate_pastor(ctx):
        cursor = db.cursor()
        try:
            cursor.execute(f"SELECT * FROM pokemones WHERE id_pokedex = '{get_frase(id_koke)}'")
            kokemon = cursor.fetchone()
            db.commit()
            await show_pokemon_data(ctx,kokemon)
        except Exception as exc:
            await ctx.send(f"No pude traer la data del kokemon: {exc}")
        finally:
            cursor.close()



async def show_pokemon_data(ctx,kokemon):
    id_pokedex = '#'+str(kokemon[0]) if bool(kokemon[0]) else '\u200b'
    registrado = kokemon[2] if bool(kokemon[2]) else '\u200b'
    shiny_registrado = kokemon[3] if bool(kokemon[3]) else '\u200b'
    viviendo = kokemon[4] if bool(kokemon[4]) else '\u200b'
    shiny_viviendo = kokemon[5] if bool(kokemon[5]) else '\u200b'

    embed = discord.Embed(
        title=kokemon[1],
        url='https://pokemon.fandom.com/es/wiki/'+kokemon[1],
        color=0xFF5733
    )
    try:
        embed.add_field(name='Id Pokedex:', value=id_pokedex, inline=False)
        embed.add_field(name='Registrado:', value=registrado, inline=True)
        embed.add_field(name='Viviendo:', value=viviendo, inline=True)
        embed.add_field(name='\u200b', value='\u200b')
        embed.add_field(name='Shiny registrado:', value=shiny_registrado, inline=True)
        embed.add_field(name='Shiny viviendo:', value=shiny_viviendo, inline=True)
    except exc:
        print(exc)
    await ctx.send(embed=embed)



@bot.command()
async def shiny(ctx,*,koke):
    if await validate_koke(ctx,koke):
        cursor = db.cursor()
        try:
            cursor.execute(f"SELECT shiny_registered FROM pokemones WHERE poke_name = '{get_frase(koke)}'")
            shiny_registered = cursor.fetchone()
            if shiny_registered[0] == True:
                cursor.execute(f"UPDATE pokemones SET shiny_registered = 'false' WHERE poke_name = '{get_frase(koke)}'")
                await ctx.send(f"Actualizado: {koke} shiny no registrado.")
            else:
                cursor.execute(f"UPDATE pokemones SET shiny_registered = 'true' WHERE poke_name = '{get_frase(koke)}'")
                await ctx.send(f"Actualizado: {koke} shiny registrado.")
            db.commit()
        except Exception as exc:
            await ctx.send(f"No pude actualizar el koke shiny: {exc}")
        finally:
            cursor.close()



@bot.command()
async def registrado(ctx,*,koke):
    if await validate_koke(ctx,koke):
        cursor = db.cursor()
        try:
            cursor.execute(f"SELECT registered FROM pokemones WHERE poke_name = '{get_frase(koke)}'")
            shiny_registered = cursor.fetchone()
            if shiny_registered[0] == True:
                cursor.execute(f"UPDATE pokemones SET registered = 'false' WHERE poke_name = '{get_frase(koke)}'")
                await ctx.send(f"Actualizado: {koke} no registrado.")
            else:
                cursor.execute(f"UPDATE pokemones SET registered = 'true' WHERE poke_name = '{get_frase(koke)}'")
                await ctx.send(f"Actualizado: {koke} registrado.")
            db.commit()
        except Exception as exc:
            await ctx.send(f"No pude actualizar el koke: {exc}")
        finally:
            cursor.close()



@bot.command()
async def viviendo(ctx,*,koke_juego):
    split_koke_juego = koke_juego.split(" ", 1)
    koke = split_koke_juego[0]
    juego = split_koke_juego[1]
    if await validate_koke(ctx,koke):
        cursor = db.cursor()
        try:
            cursor.execute(f"UPDATE pokemones SET game_living = '{get_frase(juego)}' WHERE poke_name = '{get_frase(koke)}'")
            await ctx.send(f"Actualizado: {koke} ahora vive en Pokemon {juego}.")
            db.commit()
        except Exception as exc:
            await ctx.send(f"No pude actualizar donde vive el koke: {exc}")
        finally:
            cursor.close()



@bot.command()
async def shinyViviendo(ctx,*,koke_juego):
    split_koke_juego = koke_juego.split(" ", 1)
    koke = split_koke_juego[0]
    juego = split_koke_juego[1]
    if await validate_koke(ctx,koke):
        cursor = db.cursor()
        try:
            cursor.execute(f"UPDATE pokemones SET shiny_game_living = '{get_frase(juego)}' WHERE poke_name = '{get_frase(koke)}'")
            await ctx.send(f"Actualizado: {koke} shiny ahora vive en Pokemon {juego}.")
            db.commit()
        except Exception as exc:
            await ctx.send(f"No pude actualizar donde vive el koke shiny: {exc}")
        finally:
            cursor.close()



async def validate_koke(ctx, koke):
    cursor = db.cursor()
    try:
        cursor.execute(f"SELECT COUNT (*) FROM pokemones WHERE poke_name = '{get_frase(koke)}'")
        result = 0
        result = cursor.fetchone()[0]
        if result != 0:
            return True
        else:
            await ctx.send(f'Ese kokemon no existe rey.')
            return False
    except Exception as exc:
        await ctx.send(f'Error al validar el kokemon: {exc}')
    finally:
        cursor.close()



@bot.command()
async def holasanti(ctx):
    loc = ("xxx.xls")
    wb = xlrd.open_workbook(loc)
    sheet = wb.sheet_by_index(0)
    rows = sheet.nrows
    for i in range(rows):
        movie_name = sheet.cell_value(i, 5)
        imdb_link = sheet.cell_value(i, 6)
        imdb_id = sheet.cell_value(i, 1)
        cursor = db.cursor()
        sql = (f"INSERT INTO  stalkers_movies(movie_name, imdb_link, imdb_id) VALUES ('{get_frase(movie_name)}','{get_frase(imdb_link)}','{get_frase(imdb_id)}')")
        try:
            result = cursor.execute(sql)
            print(f"SE INSERTO EL KOKEMON: {movie_name}")
        except Exception as exc:
            print("EXPLOTO UN KOKEMON")
            print(exc)
        db.commit()
        cursor.close()



@bot.command()
async def tasBien(ctx):
    await ctx.send(f'{round(bot.latency * 1000)}ms')

@bot.command()
@commands.has_permissions(manage_messages=True)
async def limpiar(ctx, amount=2):
    await ctx.channel.purge(limit=amount)

@limpiar.error
async def limpiar_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send('Hermano no me pediste nada.')

bot.run('discord bot token')
