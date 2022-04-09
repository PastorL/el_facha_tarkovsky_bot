import discord
import random
import imdb
import psycopg2
from datetime import date
from discord.ext import commands
from random import randint
from table2ascii import table2ascii as t2a, PresetStyle

intents = discord.Intents.default()
intents.members = True
bot = commands.Bot(intents = intents, command_prefix = '.')
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
    if do_you_really(message.content):
        await ctx.send("if we don’t try 😐 then what the fuck 🤬 is stopping 🇻🇳 us 🇨🇳 from just throwing 👐🏿🙆🏻 ourselves off a bridge 🌉, and giving 👉 up ⬆, and saying 💬 “Yeah the planet 🌎 is dying ☠. The government 💩 hates 😡 us 🚶🏻🚶🏼. The animals 🐕 are leaving 🚫😔. The aliens 🌌👽 aren’t contacting 📞 us 🚶🏻🚶🏼. We might 🔍 be alone 😴. It just might 🤔 be you 👆 and me.” But 🍑 that’s okay 👌. Because do you 👆 really 💯 need 👉 anyone 👩 else 😩!?")
        await ctx.send("https://www.youtube.com/watch?v=Y4Fes8Up1tA")
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

def do_you_really(message):
    if ('Do you really need anyone else' in message) or ('do you really need anyone else' in message):
        return True
    else:
        return False


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
    server_name = ctx.message.guild.name
    try:
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
    if validate_psigang(server_name):
        try:
            cursor.execute(f"SELECT tegobi_foto FROM tegobis ORDER BY RANDOM() LIMIT 1")
            frase = cursor.fetchone()
            await ctx.send(frase[0])
        except Exception as exc:
            await ctx.send('No anda nada cuando traigo las frases: {}'.format(exc))
    cursor.close()



@bot.command()
async def lente(ctx):
    cursor = db.cursor()
    server_name = ctx.message.guild.name
    if validate_psigang(server_name):
        try:
            cursor.execute(f"SELECT lente_foto FROM lentes ORDER BY RANDOM() LIMIT 1")
            frase = cursor.fetchone()
            await ctx.send(frase[0])
        except Exception as exc:
            await ctx.send('No anda nada cuando traigo las frases: {}'.format(exc))
    cursor.close()



@bot.command()
async def pet(ctx):
    cursor = db.cursor()
    server_name = ctx.message.guild.name
    autor_name = ctx.message.author.name
    if validate_psigang(server_name):
        try:
            cursor.execute(f"SELECT pet_foto FROM pets ORDER BY RANDOM() LIMIT 1")
            frase = cursor.fetchone()
            await ctx.send(frase[0])
        except Exception as exc:
            await ctx.send('No anda nada cuando traigo las frases: {}'.format(exc))
    cursor.close()



@bot.command()
async def addPet(ctx, *, pet_foto):
    cursor = db.cursor()
    autor_name = ctx.message.author.name
    server_name = ctx.message.guild.name
    if validate_psigang(server_name):
        try:
            cursor.execute(f"SELECT pet_foto FROM pets WHERE pet_owner = '{autor_name}'")
            result = cursor.fetchone()
            if result == None:
                cursor.execute(f"INSERT INTO pets(pet_foto, pet_owner) VALUES('{pet_foto}', '{autor_name}')")
            else:
                cursor.execute(f"UPDATE pets SET pet_foto='{pet_foto}' WHERE pet_owner = '{autor_name}'")
            db.commit()
            await ctx.send('Pet agregada товарищ!')
        except Exception as exc:
            await ctx.send('No anda nada cuando actualizo las pets: {}'.format(exc))
    cursor.close()



@bot.command()
async def poetic(ctx):
    await ctx.send("https://media.discordapp.net/attachments/713987937892565052/928998748309295114/88e.png")



async def insert_frase(ctx, frase, autor):
    if validate_frase(frase):
        cursor = db.cursor()
        server_name = ctx.message.guild.name
        sql = (f"INSERT INTO frases(descripcion, usuario, server_name) VALUES ('{get_frase(frase)}','{autor}','{server_name}')")
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
        server_name = ctx.message.guild.name
        sql = (f"DELETE FROM frases WHERE descripcion = '{get_frase(frase)}' AND server_name = '{server_name}'")
        try:
            result = cursor.execute(sql)
            await ctx.send("Frase borrada товарищ!")
            sql2 = (f"INSERT INTO frases_borradas(descripcion, autor_borrado) VALUES ('{get_frase(frase)}','{autor}')")
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


@bot.command()
async def cargarPartida(ctx,*,data):
    if await validate_pastor(ctx):
        saved = 1
        cursor = db.cursor()
        game_data = data.split(',')
        cursor.execute(f"SELECT id_cs_game FROM cs_games GROUP BY id_cs_game ORDER BY id_cs_game DESC LIMIT 1")
        cs_games_quantity = int(cursor.fetchone()[0]) + 1
        print(cs_games_quantity)
        for player_data in game_data:
             player = player_data.split(' ')
             id_cs_player = player[0]
             kills = player[1]
             assists = player[2]
             deaths = player[3]
             score = player[4]
             win = player[5]

             try:
                 cursor.execute(f"SELECT total_kills, total_assists, total_deaths, total_score, total_wins FROM cs_ranking WHERE id_cs_player = '{id_cs_player}'")
                 result = cursor.fetchone()
                 ranking_kills = result[0]
                 ranking_assists = result[1]
                 ranking_deaths = result[2]
                 ranking_score = result[3]
                 ranking_wins = result[4]

                 total_kills = ranking_kills + int(kills)
                 total_assists = ranking_assists + int(assists)
                 total_deaths = ranking_deaths + int(deaths)
                 total_score = ranking_score + int(score)
                 total_wins = ranking_wins + int(win)


                 cursor.execute(f"INSERT INTO cs_games(id_cs_game, id_cs_player, kills, assists, deaths, score, win) VALUES ({cs_games_quantity},'{id_cs_player}',{kills},{assists},{deaths},{score},{win})")
                 cursor.execute(f"UPDATE cs_ranking SET total_kills = {total_kills}, total_assists = {total_assists}, total_deaths = {total_deaths}, total_score = {total_score}, total_wins = {total_wins} WHERE id_cs_player = '{id_cs_player}'")
                 db.commit()
             except Exception as exc:
                 saved = 0
                 await ctx.send('No anda nada cuando guardo el top: {}'.format(exc))
        cursor.close()
        if saved == 1:
            await ctx.send('Data de partidas actualizada.')


@bot.command()
async def myStats(ctx):
    id_cs_player = ctx.message.author.name
    cursor = db.cursor()
    try:
        cursor.execute(f"SELECT COUNT(*) FROM cs_games WHERE id_cs_player = '{id_cs_player}'")
        games_quantity = cursor.fetchone()[0]
        cursor.execute(f"SELECT total_kills, total_assists, total_deaths, total_score, total_wins FROM cs_ranking WHERE id_cs_player='{id_cs_player}'")
        player_data = cursor.fetchone()
    except Exception as exc:
        await ctx.send('No anda nada cuando traigo la data: {}'.format(exc))
    kills = player_data[0]
    assists = player_data[1]
    deaths = player_data[2]
    score = player_data[3]
    wins = player_data[4]

    media_kills = round(kills/games_quantity, 1)
    media_assists = round(assists/games_quantity, 1)
    media_deaths = round(deaths/games_quantity, 1)
    media_score = round(score/games_quantity, 1)
    media_wins = round(wins/games_quantity, 2)

    output = t2a(
        header = ['Games', 'Kills', 'Assists', 'Deaths', 'Score', 'Wins'],
        body = [[games_quantity, kills, assists, deaths, score, wins], ['Media', media_kills, media_assists, media_deaths, media_score, media_wins]],
        style=PresetStyle.thin_compact
    )
    embed = discord.Embed()
    embed.add_field(name=id_cs_player, value=f"```\n{output}```")
    await ctx.send(embed=embed)


@bot.command()
async def ranking(ctx):
    cursor = db.cursor()
    try:
        cursor.execute(f"SELECT id_cs_player, total_kills, total_assists, total_deaths, total_score, total_wins FROM cs_ranking ORDER BY total_kills DESC")
        players_data = cursor.fetchall()
    except Exception as exc:
        await ctx.send('No anda nada cuando traigo la data: {}'.format(exc))

    body_data = []
    for player_data in players_data:
        player = player_data[0]
        try:
            cursor.execute(f"SELECT COUNT(*) FROM cs_games WHERE id_cs_player = '{player}'")
            games_quantity = cursor.fetchone()[0]
        except Exception as exc:
            await ctx.send('No anda nada cuando traigo la data: {}'.format(exc))

        kills = player_data[1]
        assists = player_data[2]
        deaths = player_data[3]
        score = player_data[4]
        wins = player_data[5]

        body_data.append([player, kills, assists, deaths, score, games_quantity, wins])

    output = t2a(
        header = ['Rata', 'Kills', 'Assists', 'Deaths', 'Score', 'Games', 'Wins'],
        body = body_data,
        style = PresetStyle.thin_compact
    )
    embed = discord.Embed()
    embed.add_field(name="Ranking", value=f"```\n{output}```")
    await ctx.send(embed=embed)


def getMediaKills(elem):
    return elem[1]


@bot.command()
async def mediaRanking(ctx):
    cursor = db.cursor()
    try:
        cursor.execute(f"SELECT id_cs_player, total_kills, total_assists, total_deaths, total_score, total_wins FROM cs_ranking ORDER BY total_kills DESC")
        players_data = cursor.fetchall()
    except Exception as exc:
        await ctx.send('No anda nada cuando traigo la data: {}'.format(exc))

    body_data = []
    for player_data in players_data:
        player = player_data[0]
        try:
            cursor.execute(f"SELECT COUNT(*) FROM cs_games WHERE id_cs_player = '{player}'")
            games_quantity = cursor.fetchone()[0]
        except Exception as exc:
            await ctx.send('No anda nada cuando traigo la data: {}'.format(exc))

        kills = player_data[1]
        assists = player_data[2]
        deaths = player_data[3]
        score = player_data[4]
        wins = player_data[5]

        media_kills = 0
        media_assists = 0
        media_deaths = 0
        media_score = 0
        media_wins = 0

        if games_quantity != 0:
            media_kills = round(kills/games_quantity, 1)
            media_assists = round(assists/games_quantity, 1)
            media_deaths = round(deaths/games_quantity, 1)
            media_score = round(score/games_quantity, 1)
            media_wins = round(wins/games_quantity, 2)

        body_data.append([player, media_kills, media_assists, media_deaths, media_score, media_wins])

    body_data.sort(key=getMediaKills, reverse=True)
    output = t2a(
        header = ['Rata', 'Kills/g', 'Assists/g', 'Deaths/g', 'Score/g', 'Wins/g'],
        body = body_data,
        style = PresetStyle.thin_compact
    )
    embed = discord.Embed()
    embed.add_field(name="Ranking", value=f"```\n{output}```")
    await ctx.send(embed=embed)


@bot.command()
async def lastFrase(ctx):
    cursor = db.cursor()
    server_name = ctx.message.guild.name
    try:
        cursor.execute(f"SELECT descripcion FROM frases WHERE server_name='{server_name}' ORDER BY id_frase DESC LIMIT 1")
        frase = cursor.fetchone()
        await ctx.send(frase[0])
    except Exception as exc:
        await ctx.send('No anda nada cuando traigo las frases: {}'.format(exc))
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
        await ctx.send("Quien te conoce they? so bolude y no tene huevevarios.")
        return False



def get_frase(frase):
    return frase.replace("'", "´")



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
async def leon(ctx):
    today = date.today()
    remaining_days_to_agilucho = 0
    if ((date(today.year, 12, 15) < today) or (today < date(today.year, 6, 15))):
        if (date(today.year, 12,15) < today):
            june_agilucho = date(today.year + 1, 6, 15)
            remaining_days_to_agilucho_date = june_agilucho - today
            remaining_days_to_agilucho = remaining_days_to_agilucho_date.days
        else:
            june_agilucho = date(today.year, 6, 15)
            remaining_days_to_agilucho_date = june_agilucho - today
            remaining_days_to_agilucho = remaining_days_to_agilucho_date.days
    elif ((today.month == 7 and today.day == 15) or (today.month == 12 and today.day == 15)):
        await ctx.send("https://www.youtube.com/watch?v=7K1aiBmcMjQ")
        await ctx.send("https://www.youtube.com/watch?v=6vYnas6q3Sg")
        await ctx.send("https://media.discordapp.net/attachments/689515574669082794/878087380144361502/unknown.png")
        await ctx.send("https://media.discordapp.net/attachments/714897041825726466/873295536269172736/unknown.png")
        await ctx.send("https://media.discordapp.net/attachments/813481013618409582/860499861265580072/unknown.png")
        await ctx.send("https://cdn.discordapp.com/attachments/820570406921961482/837177739697192980/CliqjX0y9eRCM8fv1IFzkik0FyqS5LB6_7cfpmeqn2sjeXKDFoUghClmkEqA5TPaGwQgrzlJNE4SWIGT1QCuUDUh9t6nd1KOhhTX.png")
        await ctx.send("https://media.discordapp.net/attachments/820570406921961482/837176165223235594/qqTB3q3-0Muzfk7vgoYMoSl4mDLBb6__TQTyuP6Q4EklnBm0VgyfYnsrK50H5dtTgmnZna_JSI6rTSwaX0vVOc0r79xtnr-ggKuG.png")
        await ctx.send("https://images-ext-1.discordapp.net/external/Ih8IWq13q9KZST9ErFHBxBE0Ed_TCwZbVS0k-eaNTCg/%3Fwidth%3D1170%26height%3D676/https/media.discordapp.net/attachments/714897041825726466/870763075257651210/unknown.png")
        await ctx.send("https://images-ext-2.discordapp.net/external/dKS3FQH5nAGle6ysdYQYLV5O-cqx4Y7-ZIzmrq6RTn4/https/media.discordapp.net/attachments/689515574669082794/908784636375732224/unknown.png")
        await ctx.send("https://images-ext-1.discordapp.net/external/6BnmKn9MGKFJ5P4xmBRal15E1bUwiDz38-fXDZePPSo/https/media.discordapp.net/attachments/820570406921961482/850645707656527882/unknown.png")
        await ctx.send("https://images-ext-1.discordapp.net/external/WFjJlLxX0MEpNJ6pzt741G72omg2TFv7nWqT-8kGJVY/https/media.discordapp.net/attachments/689515574669082794/909364710909026345/unknown.png")
        await ctx.send("https://media.discordapp.net/attachments/689515574669082794/861035382807330886/CSGO_-_Discord_2021-07-03_00-34-53.mp4")
        await ctx.send("HOY SE COBRA EL LEON COMPAÑERES (o al menos eso deberíamos)")
    else:
        december_agilucho = date(today.year, 12, 15)
        remaining_days_to_agilucho_date = december_agilucho - today
        remaining_days_to_agilucho = remaining_days_to_agilucho_date.days
    if remaining_days_to_agilucho != 0 and remaining_days_to_agilucho == 1:
        agilucho = f"Falta {remaining_days_to_agilucho} día para que llegue el león compañeres."
        await ctx.send(agilucho + " https://www.youtube.com/watch?v=_LNd1y-8U_8")
    else:
        agilucho = f"Faltan {remaining_days_to_agilucho} días para que llegue el león compañeres."
        await ctx.send(agilucho + " https://www.youtube.com/watch?v=_LNd1y-8U_8")



@bot.command()
async def parmi(ctx):
    cursor = db.cursor()
    server_name = ctx.message.guild.name
    if validate_psigang(server_name):
        try:
            cursor.execute(f"SELECT parmi_frase FROM parmi_frases ORDER BY RANDOM() LIMIT 1")
            frase = cursor.fetchone()
            await ctx.send(frase[0])
        except Exception as exc:
            await ctx.send('No anda nada cuando traigo las frases: {}'.format(exc))
    cursor.close()



@bot.command()
async def addParmi(ctx,*,frase):
    autor = ctx.message.author.name
    server_name = ctx.message.guild.name
    if validate_psigang(server_name):
        if validate_parmi_frase(frase):
            cursor = db.cursor()
            server_name = ctx.message.guild.name
            sql = (f"INSERT INTO parmi_frases(parmi_frase) VALUES ('{get_frase(frase)}')")
            try:
                result = cursor.execute(sql)
                await ctx.send("Frase agregada товарищ!")
            except Exception as exc:
                await ctx.send('No anda nada cuando guarda las frases: {}'.format(exc))
            db.commit()
            cursor.close()
        else:
            await ctx.send("La frase ya existe сука блять!")



def validate_parmi_frase(frase):
    cursor = db.cursor()
    try:
        cursor.execute(f"SELECT COUNT (*) FROM parmi_frases WHERE parmi_frase = '{get_frase(frase)}'")
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
async def cumple(ctx):
    discord_server = ctx.message.guild.name
    cursor = db.cursor()
    try:
        cursor.execute(f"SELECT discord_user, discord_id, fecha, cast(fecha + ((extract(year from age(fecha)) + 1) * interval '1' year) as date) as next_birthday from cumpleaños_fechas WHERE to_char(CURRENT_DATE,'MM') = to_char(cast(fecha + ((extract(year from age(fecha)) + 1) * interval '1' year) as date), 'MM') AND to_char(CURRENT_DATE,'DD') = to_char(cast(fecha + ((extract(year from age(fecha)) + 1) * interval '1' year) as date), 'DD')")
        cumpleañero_del_dia = cursor.fetchone()
        if cumpleañero_del_dia != None:
            cumpleañero_tag = f"<@{cumpleañero_del_dia[1]}>"
            await ctx.send(f'Hoy es el cumpleaños de {cumpleañero_tag}! С днем ​​рождения товарищ!')
        else:
            cursor.execute(f"SELECT discord_user, discord_id, fecha, cast(fecha + ((extract(year from age(fecha)) + 1) * interval '1' year) as date) as next_birthday from cumpleaños_fechas WHERE discord_server = '{discord_server}' ORDER BY next_birthday asc LIMIT 1")
            cumpleaños_data = cursor.fetchone()
            cumpleañero = cumpleaños_data[0]
            cumpleañero_id = cumpleaños_data[1]
            cumple = cumpleaños_data[3]
            await ctx.send(f'El próximo cumpleaños es el de {cumpleañero} el {cumple.day} del {cumple.month}.')
    except:
        await ctx.send(f'Error gravísimo al consultar los cumpleaños.')




@bot.command()
async def addMiCumple(ctx,*,fecha):
    autor_name = ctx.message.author.name
    server_name = ctx.message.guild.name
    autor_id = autor = ctx.message.author.id
    today = date.today()
    fecha_array = []
    if '/' in fecha or '-' in fecha:
        if '/' in fecha:
            fecha_array = fecha.split('/')
        if '-' in fecha:
            fecha_array = fecha.split('-')
    else:
        await ctx.send(f'Cuchame una cosa no te haga el vive y poné una fecha válida día/mes/año en ese exacto formato o te liquido.')
    if (len(fecha_array) == 3 and len(fecha_array[0]) != 0 and len(fecha_array[1]) != 0 and len(fecha_array[2]) != 0):
        dias = int(fecha_array[0])
        mes = int(fecha_array[1])
        año = int(fecha_array[2])
        if (dias > 31 or dias < 1):
            await ctx.send(f'No te haga el vive y poné un día válido.')
        else:
            if (mes > 12 or mes < 1):
                await ctx.send(f'No te haga el vive y poné un mes válido.')
            else:
                if (año > today.year or año < 1800):
                    await ctx.send(f'No te haga el vive y poné un año válido.')
                else:
                    if validate_cumpleanios_exists(server_name, autor_id):
                        cursor = db.cursor()
                        date_cumpleaños = date(año, mes, dias)
                        sql = (f"INSERT INTO cumpleaños_fechas(discord_user, fecha, discord_server, discord_id) VALUES ('{autor_name}','{date_cumpleaños}','{server_name}','{autor_id}')")
                        try:
                            result = cursor.execute(sql)
                            await ctx.send("Cumpleaños agregado товарищ!")
                        except Exception as exc:
                            await ctx.send('No anda nada cuando guardo el cumpleaños: {}'.format(exc))
                        db.commit()
                        cursor.close
                    else:
                        await ctx.send(f'Vos ya cargaste tu cumpleaños payase vola de acá o te reviento la gorra.')
    else:
        await ctx.send(f'Cuchame una cosa no te haga el vive y poné una fecha válida día/mes/año en ese exacto formato o te liquido.')


def validate_cumpleanios_exists(server_name, autor_id):
    cursor = db.cursor()
    try:
        cursor.execute(f"SELECT COUNT (*) FROM cumpleaños_fechas WHERE discord_server = '{server_name}' AND discord_id = '{autor_id}'")
        result = 0
        result = cursor.fetchone()[0]
        if result == 0:
            return True
        else:
            return False
    except Exception as exc:
        print('Error al validar el cumpleaños.')
    finally:
        cursor.close()



@bot.command()
async def gartic(ctx):
    cursor = db.cursor()
    try:
        cursor.execute(f"SELECT gartic_image FROM gartics ORDER BY RANDOM() LIMIT 1")
        frase = cursor.fetchone()
        await ctx.send(frase[0])
    except Exception as exc:
        await ctx.send('No anda nada cuando traigo las frases: {}'.format(exc))
    cursor.close()



@bot.command()
async def addGartic(ctx,*,gartic_image):
    autor = ctx.message.author.name
    if validate_gartic_image(gartic_image):
        cursor = db.cursor()
        server_name = ctx.message.guild.name
        sql = (f"INSERT INTO gartics(gartic_image, gartic_user_added) VALUES ('{gartic_image}', '{autor}')")
        try:
            result = cursor.execute(sql)
            await ctx.send("Imagen agregada товарищ!")
        except Exception as exc:
            await ctx.send('No anda nada cuando guarda la imagen: {}'.format(exc))
        db.commit()
        cursor.close()
    else:
        await ctx.send("La imagen ya existe сука блять!")



def validate_gartic_image(gartic_image):
    cursor = db.cursor()
    try:
        cursor.execute(f"SELECT COUNT (*) FROM gartics WHERE gartic_image = '{gartic_image}'")
        result = 0
        result = cursor.fetchone()[0]
        if result == 0:
            return True
        else:
            return False
    except Exception as exc:
        print("Error al validar la imagen.")
    finally:
        cursor.close()



@bot.command()
async def addPorcel(ctx,film_name,film_link):
    added_user = ctx.message.author.name
    cursor = db.cursor()
    film_name_lc = film_name.lower()
    try:
        result = cursor.execute(f"INSERT INTO film_links(film_name, film_link, added_user) VALUES ('{film_name_lc}', '{film_link}', '{added_user}')")
        db.commit()
        await ctx.send("Link agregado товарищ!")
    except Exception as exc:
        print("Error al guardar el link.")
        await ctx.send('Error al guardar el link.: {}'.format(exc))
    finally:
        cursor.close()



@bot.command()
async def porcelLink(ctx,film_name):
    cursor = db.cursor()
    film_name_lc = film_name.lower()
    try:
        cursor.execute(f"SELECT film_name, film_link FROM film_links WHERE film_name LIKE '%{film_name_lc}%' LIMIT 5")
        links = cursor.fetchall()
        film_index = 1
        for link in links:
            print(link)
            await ctx.send(f"{film_index} - {link[0]} - {link[1]}")
            film_index = film_index + 1
    except Exception as exc:
        await ctx.send('Error al buscar el link.: {}'.format(exc))
    finally:
        cursor.close()



def validate_psigang(server_name):
    if server_name == 'Psigang':
        return True
    else:
        return False


@bot.command()
async def quienJuegaCS(ctx):
    players_pool = []
    players = []
    for member in ctx.guild.members:
        for role in member.roles:
            if (role.name == "CSGO"):
                players_pool.append(member)
    for _ in range(5):
        play = random.choice(players_pool)
        player_index = players_pool.index(play)
        players.append(play)
        players_pool.pop(player_index)
    for p in players:
        await ctx.send(p.name)


@bot.command()
async def holasanti(ctx):
    await ctx.send("test")


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

bot.run('Nzg4MTM2MDcxMzA1MjMyMzk0.X9fG6g.t-E01bK1FpsWzpJO-G6fSr_YcA4')
