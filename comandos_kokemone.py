import discord
import validations
import connection
from discord.ext import commands

@commands.command()
async def koke(ctx,*,koke):
    if await validations.validate_pastor(ctx):
        conn = connection.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(f"SELECT * FROM pokemones WHERE poke_name = '{validations.get_frase(koke)}'")
            kokemon = cursor.fetchone()
            conn.commit()
            await show_pokemon_data(ctx,kokemon)
        except Exception as exc:
            await ctx.send(f"No pude traer la data del kokemon: {exc}")
        finally:
            cursor.close()
            conn.close()

@commands.command()
async def pokedex(ctx,*,id_koke):
    if await validations.validate_pastor(ctx):
        conn = connection.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(f"SELECT * FROM pokemones WHERE poke_name = '{validations.get_frase(id_koke)}'")
            kokemon = cursor.fetchone()
            conn.commit()
            await show_pokemon_data(ctx,kokemon)
        except Exception as exc:
            await ctx.send(f"No pude traer la data del kokemon: {exc}")
        finally:
            cursor.close()
            conn.close()

@commands.command()
async def shiny(ctx,*,koke):
    if await validate_koke(ctx,koke):
        conn = connection.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(f"SELECT shiny_registered FROM pokemones WHERE poke_name = '{validations.get_frase(koke)}'")
            shiny_registered = cursor.fetchone()
            if shiny_registered[0] == True:
                cursor.execute(f"UPDATE pokemones SET shiny_registered = 'false' WHERE poke_name = '{validations.get_frase(koke)}'")
                await ctx.send(f"Actualizado: {koke} shiny no registrado.")
            else:
                cursor.execute(f"UPDATE pokemones SET shiny_registered = 'true' WHERE poke_name = '{validations.get_frase(koke)}'")
                await ctx.send(f"Actualizado: {koke} shiny registrado.")
            conn.commit()
        except Exception as exc:
            await ctx.send(f"No pude actualizar el koke shiny: {exc}")
        finally:
            cursor.close()
            conn.close()

@commands.command()
async def registrado(ctx,*,koke):
    if await validate_koke(ctx,koke):
        conn = connection.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(f"SELECT registered FROM pokemones WHERE poke_name = '{validations.get_frase(koke)}'")
            shiny_registered = cursor.fetchone()
            if shiny_registered[0] == True:
                cursor.execute(f"UPDATE pokemones SET registered = 'false' WHERE poke_name = '{validations.get_frase(koke)}'")
                await ctx.send(f"Actualizado: {koke} no registrado.")
            else:
                cursor.execute(f"UPDATE pokemones SET registered = 'true' WHERE poke_name = '{validations.get_frase(koke)}'")
                await ctx.send(f"Actualizado: {koke} registrado.")
            conn.commit()
        except Exception as exc:
            await ctx.send(f"No pude actualizar el koke: {exc}")
        finally:
            cursor.close()
            conn.close()

@commands.command()
async def viviendo(ctx,*,koke_juego):
    split_koke_juego = koke_juego.split(" ", 1)
    koke = split_koke_juego[0]
    juego = split_koke_juego[1]
    if await validate_koke(ctx,koke):
        conn = connection.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(f"UPDATE pokemones SET game_living = '{validations.get_frase(juego)}' WHERE poke_name = '{validations.get_frase(koke)}'")
            await ctx.send(f"Actualizado: {koke} ahora vive en Pokemon {juego}.")
            conn.commit()
        except Exception as exc:
            await ctx.send(f"No pude actualizar donde vive el koke: {exc}")
        finally:
            cursor.close()
            conn.close()

@commands.command()
async def shinyViviendo(ctx,*,koke_juego):
    split_koke_juego = koke_juego.split(" ", 1)
    koke = split_koke_juego[0]
    juego = split_koke_juego[1]
    if await validate_koke(ctx,koke):
        conn = connection.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(f"UPDATE pokemones SET shiny_game_living = '{validations.get_frase(juego)}' WHERE poke_name = '{validations.get_frase(koke)}'")
            conn.commit()
            await ctx.send(f"Actualizado: {koke} shiny ahora vive en Pokemon {juego}.")
        except Exception as exc:
            await ctx.send(f"No pude actualizar donde vive el koke shiny: {exc}")
        finally:
            cursor.close()
            conn.close()

async def validate_koke(ctx, koke):
    conn = connection.get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(f"SELECT COUNT (*) FROM pokemones WHERE poke_name = '{validations.get_frase(koke)}'")
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
        conn.close()

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
    except Exception as exc:
        print(exc)
    await ctx.send(embed=embed)

async def setup(bot):
    bot.add_command(koke)
    bot.add_command(pokedex)
    bot.add_command(shiny)
    bot.add_command(registrado)
    bot.add_command(viviendo)
    bot.add_command(shinyViviendo)