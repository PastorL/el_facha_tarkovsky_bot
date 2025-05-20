import discord
import connection
from datetime import date
from discord.ext import commands
from table2ascii import table2ascii as t2a, PresetStyle

@commands.command()
async def addBolucompra(ctx,*,bolucompra):
    conn = connection.get_connection()
    cursor = conn.cursor()
    bolucompra_array = bolucompra.split(',')
    sql = (f"INSERT INTO bolucompras(descripcion, precio, ejecutada, link) VALUES ('{bolucompra_array[0]}','{bolucompra_array[1]}','0','{bolucompra_array[2]}')")
    try:
        result = cursor.execute(sql)
        conn.commit()
        await ctx.send("Bolucompra agregada товарищ!")
    except Exception as exc:
        await ctx.send('No anda nada cuando guardo las bolucompras: {}'.format(exc))
    finally:
        cursor.close()
        conn.close()

@commands.command()
async def ejecutarBolucompra(ctx,*,id):
    conn = connection.get_connection()
    cursor = conn.cursor()
    user = ctx.message.author.name
    print(user)
    today = date.today()
    print(today)
    sql = (f"UPDATE bolucompras SET ejecutada = '1', user_ejecutor = '{user}', fecha_ejecutada = '{today}' WHERE id_bolucompras = {id}")
    try:
        result = cursor.execute(sql)
        conn.commit()
        await ctx.send("Bolucompra ejecutada товарищ!")
    except Exception as exc:
        await ctx.send('No anda nada cuando ejecuto las bolucompras: {}'.format(exc))
    finally:
        cursor.close()
        conn.close()

@commands.command()
async def bolucompra(ctx,*,id):
    conn = connection.get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(f"SELECT * FROM bolucompras WHERE id_bolucompras = {id}")
        bolucompra = cursor.fetchone()
        conn.commit()
        hyper_link = f"[Link]({bolucompra[4]})"
        print(bolucompra)
        id_bolucompras = '#'+str(bolucompra[0]) if bool(bolucompra[0]) else '\u200b'
        descripcion = bolucompra[1] if bool(bolucompra[1]) else '\u200b'
        precio = bolucompra[2] if bool(bolucompra[2]) else '\u200b'
        ejecutada = bolucompra[3] if bool(bolucompra[3]) else '\u200b'
        link = hyper_link if bool(hyper_link) else '\u200b'
        user_ejecutor = bolucompra[5] if bool(bolucompra[5]) else '\u200b'
        fecha_ejecutada = bolucompra[6] if bool(bolucompra[6]) else '\u200b'

        embed = discord.Embed(
            title='Bolucompras',
            color=0xFF5733
        )
        try:
            embed.add_field(name='Id:', value=id_bolucompras, inline=True)
            embed.add_field(name='Descripción:', value=descripcion, inline=True)
            embed.add_field(name='Precio:', value=precio, inline=True)
            embed.add_field(name='Ejecutada:', value=ejecutada, inline=True)
            embed.add_field(name='Link:', value=link, inline=True)
            embed.add_field(name='Usuario Ejecutor:', value=user_ejecutor, inline=True)
            embed.add_field(name='Fecha Ejecutada:', value=fecha_ejecutada, inline=True)
        except Exception as exc:
            print(exc)
        await ctx.send(embed=embed)
    except Exception as exc:
        print(exc)
        await ctx.send(f"No pude traer la data de la bolucompra: {exc}")
    finally:
        cursor.close()
        conn.close()

@commands.command()
async def bolucompras(ctx):
    conn = connection.get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute(f"SELECT * FROM bolucompras")
        bolucompras_data = cursor.fetchall()
    except Exception as exc:
        await ctx.send('No anda nada cuando traigo la data: {}'.format(exc))
    try:
        body_data = []
        for bolucompra_data in bolucompras_data:
            id_bolucompras = bolucompra_data[0]
            descripcion = bolucompra_data[1]
            precio = bolucompra_data[2]
            ejecutada = bolucompra_data[3] 

            body_data.append([id_bolucompras, descripcion, precio, ejecutada])
    except Exception as exc:
        await ctx.send('No anda nada cuando traigo la data: {}'.format(exc))
    finally:
        cursor.close()
        conn.close()

    output = t2a(
        header = ['Id', 'Descripción', 'Precio', 'Ejecutada'],
        body = body_data,
        style = PresetStyle.thin_compact
    )
    embed = discord.Embed()
    embed.add_field(name="Bolucompras", value=f"```\n{output}```")
    await ctx.send(embed=embed)

async def setup(bot):
    bot.add_command(addBolucompra)
    bot.add_command(ejecutarBolucompra)
    bot.add_command(bolucompras)
    bot.add_command(bolucompra)