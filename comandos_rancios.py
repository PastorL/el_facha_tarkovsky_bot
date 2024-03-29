import connection
import validations
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
