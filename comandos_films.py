import connection
import random
import validations
from imdb import Cinemagoer
from discord.ext import commands

moviesDB = Cinemagoer()

@commands.command()
async def review(ctx,*,movie):
    conn = connection.get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(f"SELECT movie_name FROM stalkers_movies WHERE movie_name = '{validations.get_frase(movie)}'")
        movie = cursor.fetchone()
        if movie == None:
            await ctx.send('No que yo sepa')
        else:
            await ctx.send(f'{movie[0]} se hablo en el podcast, en un futuro te voy a decir en cual.')
    except Exception as exc:
        await ctx.send('No anda nada cuando busco el film: {}'.format(exc))
    finally:
        cursor.close()
        conn.close()

@commands.command()
async def buscame(ctx,*,movie_to_search):
    try:
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
    except Exception as exc:
        await ctx.send("Algo falló mientras buscaba el filme: {}".format(exc))

@commands.command()
async def agregarTop(ctx,*,link_top):
    conn = connection.get_connection()
    cursor = conn.cursor()
    autor = ctx.message.author.name
    top = buscar_top(autor)
    try:
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
        cursor.commit()
    except Exception as exc:
        await ctx.send("Error al agregar top: {}".format(exc))
    finally:
        cursor.close()
        conn.close()

@commands.command()
async def miTop(ctx):
    autor = ctx.message.author.name
    top = buscar_top(autor)
    if top == None:
        await ctx.send("Todavia no existe un top para " + autor)
    else:
        await ctx.send(top)

@commands.command()
async def top(ctx,*,usuario):
    top = buscar_top(usuario)
    if top == None:
        await ctx.send("Todavia no existe un top para " + usuario)
    else:
        await ctx.send(top)

@commands.command()
async def addPorcel(ctx,film_name,film_link):
    added_user = ctx.message.author.name
    conn = connection.get_connection()
    cursor = conn.cursor()
    film_name_lc = film_name.lower()
    try:
        result = cursor.execute(f"INSERT INTO film_links(film_name, film_link, added_user) VALUES ('{film_name_lc}', '{film_link}', '{added_user}')")
        conn.commit()
        await ctx.send("Link agregado товарищ!")
    except Exception as exc:
        print("Error al guardar el link.")
        await ctx.send('Error al guardar el link.: {}'.format(exc))
    finally:
        cursor.close()
        conn.close()

@commands.command()
async def porcel(ctx,film_name):
    conn = connection.get_connection()
    cursor = conn.cursor()
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
        conn.close()

def buscar_top(autor):
    conn = connection.get_connection()
    cursor = conn.cursor()
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
        conn.close()

async def setup(bot):
    bot.add_command(review)
    bot.add_command(buscame)
    bot.add_command(agregarTop)
    bot.add_command(miTop)
    bot.add_command(top)
    bot.add_command(addPorcel)
    bot.add_command(porcel)