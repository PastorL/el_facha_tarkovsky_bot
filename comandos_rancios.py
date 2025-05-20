import connection
import validations
import urllib
import json
import re
from bs4 import BeautifulSoup
from datetime import date
from discord.ext import commands

@commands.command()
async def poetic(ctx):
    await ctx.send("https://media.discordapp.net/attachments/713987937892565052/928998748309295114/88e.png")

@commands.command()
async def doYouReally(ctx):
    await ctx.send("if we don’t try 😐 then what the fuck 🤬 is stopping 🇻🇳 us 🇨🇳 from just throwing 👐🏿🙆🏻 ourselves off a bridge 🌉, and giving 👉 up ⬆, and saying 💬 “Yeah the planet 🌎 is dying ☠. The government 💩 hates 😡 us 🚶🏻🚶🏼. The animals 🐕 are leaving 🚫😔. The aliens 🌌👽 aren’t contacting 📞 us 🚶🏻🚶🏼. We might 🔍 be alone 😴. It just might 🤔 be you 👆 and me.” But 🍑 that’s okay 👌. Because do you 👆 really 💯 need 👉 anyone 👩 else 😩!?")
    await ctx.send("https://www.youtube.com/watch?v=Y4Fes8Up1tA")

@commands.command()
async def borralo(ctx):
    await ctx.send(f"https://www.twitch.tv/nikozfps/clip/RefinedSwissTofuSpicyBoy-8tn0bytoyf4xHczc?filter=clips&range=all&sort=time")

@commands.command()
async def tatakae(ctx):
    await ctx.send("Susumi Tsuzukerunda. Shindemo, shinda atomo... Kore wa ... Tou san ga hajimeta ... Monogatari daro?")

@commands.command()
async def tegobi(ctx):
    conn = connection.get_connection()
    cursor = conn.cursor()
    server_name = ctx.message.guild.name
    if validations.validate_psigang(server_name):
        try:
            cursor.execute(f"SELECT tegobi_foto FROM tegobis ORDER BY RANDOM() LIMIT 1")
            frase = cursor.fetchone()
            await ctx.send(frase[0])
        except Exception as exc:
            await ctx.send('No anda nada cuando traigo el tegobi: {}'.format(exc))
        finally:
            cursor.close()
            conn.close()

@commands.command()
async def lente(ctx):
    conn = connection.get_connection()
    cursor = conn.cursor()
    server_name = ctx.message.guild.name
    if validations.validate_psigang(server_name):
        try:
            cursor.execute(f"SELECT lente_foto FROM lentes ORDER BY RANDOM() LIMIT 1")
            frase = cursor.fetchone()
            await ctx.send(frase[0])
        except Exception as exc:
            await ctx.send('No anda nada cuando traigo el lente: {}'.format(exc))
        finally:
            cursor.close()
            conn.close()

@commands.command()
async def pet(ctx):
    conn = connection.get_connection()
    cursor = conn.cursor()
    server_name = ctx.message.guild.name
    autor_name = ctx.message.author.name
    if validations.validate_psigang(server_name):
        try:
            cursor.execute(f"SELECT pet_foto FROM pets ORDER BY RANDOM() LIMIT 1")
            frase = cursor.fetchone()
            await ctx.send(frase[0])
        except Exception as exc:
            await ctx.send('No anda nada cuando traigo la pet: {}'.format(exc))
        finally:
            cursor.close()
            conn.close()

@commands.command()
async def addPet(ctx, *, pet_foto):
    conn = connection.get_connection()
    cursor = conn.cursor()
    autor_name = ctx.message.author.name
    server_name = ctx.message.guild.name
    if validations.validate_psigang(server_name):
        try:
            cursor.execute(f"SELECT pet_foto FROM pets WHERE pet_owner = '{autor_name}'")
            result = cursor.fetchone()
            if result == None:
                cursor.execute(f"INSERT INTO pets(pet_foto, pet_owner) VALUES('{pet_foto}', '{autor_name}')")
            else:
                cursor.execute(f"UPDATE pets SET pet_foto='{pet_foto}' WHERE pet_owner = '{autor_name}'")
            conn.commit()
            await ctx.send('Pet agregada товарищ!')
        except Exception as exc:
            await ctx.send('No anda nada cuando actualizo las pets: {}'.format(exc))
        finally:
            cursor.close()
            conn.close()

@commands.command()
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
    elif ((today.month == 6 and today.day == 15) or (today.month == 12 and today.day == 15)):
        await printRanciadasDelLeon(ctx)
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

@commands.command()
async def perdonSantiBrueraQueTeCagoElLeonYNoContestoComoEsDebido(ctx):
    await printRanciadasDelLeon(ctx)

@commands.command()
async def fudanshiItsCocoFriday(ctx):
    await ctx.send("https://media.discordapp.net/attachments/689515574669082794/1103456041351528518/image.png?width=539&height=539")

@commands.command()
async def coco(ctx):
    await ctx.send("https://www.youtube.com/watch?v=6vYnas6q3Sg")

@commands.command()
async def limone(ctx):
    await ctx.send("https://www.youtube.com/watch?v=0xOoJaA2OHk")

@commands.command()
async def limon(ctx):
    url = 'https://app.ripio.com/api/v3/rates/USDC_ARS/'
    hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11'}
    req = urllib.request.Request(url, headers=hdr)
    resp = urllib.request.urlopen(req)
    ripio_data = resp.read().decode('utf-8')
    ripio_json = json.loads(ripio_data)
    await ctx.send(f"USDC para la compra: {ripio_json['buy_rate']}")
    await ctx.send(f"USDC para la venta: {ripio_json['sell_rate']}")
    await ctx.send(f"USDC variación: {ripio_json['variation']}")

@commands.command()
async def blue(ctx):
    url = 'https://www.valordolarblue.com.ar/'
    hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11'}
    req = urllib.request.Request(url, headers=hdr)
    resp = urllib.request.urlopen(req)
    blue_data = resp.read().decode('utf-8')
    soup = BeautifulSoup(blue_data, 'html.parser')
    compra_div = soup.find('div', {'title': 'Precio de compra del Dólar Blue en la Argentina'})
    venta_div = soup.find('div', {'title': 'Precio de venta del Dólar Blue en la Argentina'})
    compra = compra_div.find('strong')
    venta = venta_div.find('strong')
    await ctx.send(f"Dolar Blue para la compra: {venta.text}")
    await ctx.send(f"Dolar Blue para la venta: {compra.text}")

@commands.command()
async def tarea(ctx):
    conn = connection.get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(f"SELECT tarea FROM tareas ORDER BY tarea DESC LIMIT 1")
        frase = cursor.fetchone()
        await ctx.send(frase[0])
    except Exception as exc:
        await ctx.send('No anda nada cuando traigo la tarea: {}'.format(exc))
    finally:
        cursor.close()
        conn.close()

@commands.command()
async def addTarea(ctx,*,tarea):
    conn = connection.get_connection()
    cursor = conn.cursor()
    if await validations.validate_pastor(ctx):
        try:
            cursor.execute(f"INSERT INTO tareas(tarea) VALUES('{tarea}')")
            conn.commit()
            await ctx.send('Tarea agregada товарищ!')
        except Exception as exc:
            await ctx.send('No anda nada cuando guardo la tarea: {}'.format(exc))
        finally:
            cursor.close()
            conn.close()

@commands.command()
async def addGoles(ctx, *, goles):
    conn = connection.get_connection()
    cursor = conn.cursor()
    id_user = ctx.message.author.name
    try:
        cursor.execute(f"SELECT id_user FROM goles WHERE id_user = '{id_user}'")
        result = cursor.fetchone()
        if result == None:
            cursor.execute(f"INSERT INTO goles(id_user, goles) VALUES('{id_user}', '{goles}')")
        else:
            cursor.execute(f"SELECT goles FROM goles WHERE id_user = '{id_user}'")
            goles_user = cursor.fetchone()[0]
            goles_totales = goles_user + int(goles)
            cursor.execute(f"UPDATE goles SET goles='{goles_totales}' WHERE id_user = '{id_user}'")
        conn.commit()
        await ctx.send('Goles sumados товарищ!')
    except Exception as exc:
        await ctx.send('No anda nada cuando actualizo los goles: {}'.format(exc))
    finally:
        cursor.close()
        conn.close()

@commands.command()
async def misGoles(ctx):
    conn = connection.get_connection()
    cursor = conn.cursor()
    id_user = ctx.message.author.name
    try:
        cursor.execute(f"SELECT goles FROM goles WHERE id_user = '{id_user}'")
        result = cursor.fetchone()[0]
        await ctx.send(result)
    except Exception as exc:
        await ctx.send('No anda nada cuando traigo los goles: {}'.format(exc))
    finally:
        cursor.close()
        conn.close()

async def printRanciadasDelLeon(ctx):
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

async def setup(bot):
    bot.add_command(poetic)
    bot.add_command(doYouReally)
    bot.add_command(borralo)
    bot.add_command(tatakae)
    bot.add_command(tegobi)
    bot.add_command(lente)
    bot.add_command(pet)
    bot.add_command(addPet)
    bot.add_command(leon)
    bot.add_command(perdonSantiBrueraQueTeCagoElLeonYNoContestoComoEsDebido)
    bot.add_command(coco)
    bot.add_command(limone)
    bot.add_command(limon)
    bot.add_command(blue)
    bot.add_command(addTarea)
    bot.add_command(tarea)
    bot.add_command(addGoles)
    bot.add_command(misGoles)
