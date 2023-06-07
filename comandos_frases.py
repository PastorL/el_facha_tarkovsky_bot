import connection
import validations
from discord.ext import commands


@commands.command()
async def frase(ctx):
    conn = connection.get_connection()
    cursor = conn.cursor()
    server_name = ctx.message.guild.name
    try:
        cursor.execute(f"SELECT descripcion FROM frases WHERE server_name='{server_name}' ORDER BY RANDOM() LIMIT 1")
        #cursor.execute(f"SELECT descripcion FROM frases ORDER BY RANDOM() LIMIT 1")
        frase = cursor.fetchone()
        await ctx.send(frase[0])
    except Exception as exc:
        await ctx.send('No anda nada cuando traigo las frases: {}'.format(exc))
    finally:
        cursor.close()
        conn.close()

@commands.command()
async def addFrase(ctx,*,frase):
    autor = ctx.message.author.name
    await insert_frase(ctx, frase, autor)

@commands.command()
async def deleteFrase(ctx,*,frase):
    autor = ctx.message.author.name
    await delete_frase(ctx, frase, autor)

@commands.command()
async def buscarFrase(ctx, *, frase):
    conn = connection.get_connection()
    cursor = conn.cursor()
    server_name = ctx.message.guild.name
    try:
        cursor.execute(f"SELECT descripcion FROM frases WHERE server_name='{server_name}' AND LOWER(descripcion) LIKE '%{frase}%' ORDER BY RANDOM() LIMIT 1")
        frase = cursor.fetchone()
        await ctx.send(frase[0])
    except Exception as exc:
        await ctx.send('No existe esa frase peconchatumaquina.')
    finally:
        cursor.close()
        conn.close()

@commands.command()
async def quienFueElBurro(ctx,*,frase):
    if await validations.validate_pastor(ctx):
        conn = connection.get_connection()
        cursor = conn.cursor()
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
            conn.close()

@commands.command()
async def lastFrase(ctx):
    conn = connection.get_connection()
    cursor = conn.cursor()
    server_name = ctx.message.guild.name
    try:
        cursor.execute(f"SELECT descripcion FROM frases WHERE server_name='{server_name}' ORDER BY id_frase DESC LIMIT 1")
        frase = cursor.fetchone()
        await ctx.send(frase[0])
    except Exception as exc:
        await ctx.send('No anda nada cuando traigo las frases: {}'.format(exc))
    finally:
        cursor.close()
        conn.close()

async def insert_frase(ctx, frase, autor):
    if validate_frase(frase):
        conn = connection.get_connection()
        cursor = conn.cursor()
        server_name = ctx.message.guild.name
        sql = (f"INSERT INTO frases(descripcion, usuario, server_name) VALUES ('{get_frase(frase)}','{autor}','{server_name}')")
        try:
            result = cursor.execute(sql)
            conn.commit()
            await ctx.send("Frase agregada товарищ!")
        except Exception as exc:
            await ctx.send('No anda nada cuando guardo las frases: {}'.format(exc))
        finally:
            cursor.close()
            conn.close()
    else:
        await ctx.send("La frase ya existe сука блять!")

async def delete_frase(ctx, frase, autor):
    if not validate_frase(frase):
        conn = connection.get_connection()
        cursor = conn.cursor()
        server_name = ctx.message.guild.name
        sql = (f"DELETE FROM frases WHERE descripcion = '{get_frase(frase)}' AND server_name = '{server_name}'")
        try:
            result = cursor.execute(sql)
            await ctx.send("Frase borrada товарищ!")
            sql2 = (f"INSERT INTO frases_borradas(descripcion, autor_borrado) VALUES ('{get_frase(frase)}','{autor}')")
            result2 = cursor.execute(sql2)
            conn.commit()
        except Exception as exc:
            await ctx.send('No anda nada cuando borro las frases: {}'.format(exc))
        finally:
            cursor.close()
            conn.close()
    else:
        await ctx.send("La frase no existe сука блять!")
    
def validate_frase(frase):
    conn = connection.get_connection()
    cursor = conn.cursor()
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
        conn.close()

def get_frase(frase):
    return frase.replace("'", "´")

async def setup(bot):
    bot.add_command(frase)
    bot.add_command(addFrase)
    bot.add_command(deleteFrase)
    bot.add_command(buscarFrase)
    bot.add_command(quienFueElBurro)
    bot.add_command(lastFrase)