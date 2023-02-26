import connection
from discord.ext import commands

@commands.command()
async def gartic(ctx):
    conn = connection.get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(f"SELECT gartic_image FROM gartics ORDER BY RANDOM() LIMIT 1")
        frase = cursor.fetchone()
        await ctx.send(frase[0])
    except Exception as exc:
        await ctx.send('No anda nada cuando traigo el gartic art: {}'.format(exc))
    finally:
        cursor.close()
        conn.close()


@commands.command()
async def addGartic(ctx,*,gartic_image):
    autor = ctx.message.author.name
    if validate_gartic_image(gartic_image):
        conn = connection.get_connection()
        cursor = conn.cursor()
        server_name = ctx.message.guild.name
        sql = (f"INSERT INTO gartics(gartic_image, gartic_user_added) VALUES ('{gartic_image}', '{autor}')")
        try:
            result = cursor.execute(sql)
            conn.commit()
            await ctx.send("Imagen agregada товарищ!")
        except Exception as exc:
            await ctx.send('No anda nada cuando guardo el gartic art: {}'.format(exc))
        finally:
            cursor.close()
            conn.close()
    else:
        await ctx.send("La imagen ya existe сука блять!")


def validate_gartic_image(gartic_image):
    conn = connection.get_connection()
    cursor = conn.cursor()
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
        conn.close()


async def setup(bot):
    bot.add_command(gartic)
    bot.add_command(addGartic)