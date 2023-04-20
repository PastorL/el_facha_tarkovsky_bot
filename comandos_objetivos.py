from discord.ext import commands
from table2ascii import table2ascii as t2a, PresetStyle
import validations
import connection
import discord

@commands.command()
async def asignarObjetivo(ctx,*,user_goal):
    if await validations.validate_pastor(ctx):
        user_goals = user_goal.split(',')
        user_id = user_goals[0]
        goal = user_goals[1]
        try:
            conn = connection.get_connection()
            cursor = conn.cursor()
            sql = (f"INSERT INTO goals(goal, id_user, done) VALUES ('{get_goal(goal)}','{user_id}', '0')")
            cursor.execute(sql)
            conn.commit()
            await ctx.send("Objetivo agregado товарищ!")
        except Exception as exc:
            await ctx.send('No anda nada cuando guardo los objetivos: {}'.format(exc))
        finally:
            cursor.close()
            conn.close()
        
@commands.command()
async def agregarObjetivo(ctx,*,goal):
    user_id = ctx.message.author.name
    try:
        conn = connection.get_connection()
        cursor = conn.cursor()
        sql = (f"INSERT INTO goals(goal, id_user, done) VALUES ('{get_goal(goal)}','{user_id}', '0')")
        cursor.execute(sql)
        conn.commit()
        await ctx.send("Objetivo agregado товарищ!")
    except Exception as exc:
        await ctx.send('No anda nada cuando guardo los objetivos: {}'.format(exc))
    finally:
        cursor.close()
        conn.close()

@commands.command()
async def misObjetivos(ctx):
    user_id = ctx.message.author.name
    embed = await format_goals(ctx,user_id)
    await ctx.send(embed=embed)

@commands.command()
async def verObjetivosDe(ctx,*,user_id):
    embed = await format_goals(ctx,user_id)
    await ctx.send(embed=embed)

@commands.command()
async def hecho(ctx,*,goal):
    user_id = ctx.message.author.name
    try:
        conn = connection.get_connection()
        cursor = conn.cursor()
        cursor.execute(f"SELECT id_user FROM goals WHERE goal='{goal}' AND id_user='{user_id}'")
        result = cursor.fetchone()
        if result != None:
            cursor.execute(f"UPDATE goals SET done ='1' WHERE goal='{goal}' AND id_user='{user_id}'")
            conn.commit()
            await ctx.send("Objetivo actualizado товарищ!")
        else:
            await ctx.send("No parece que tengas ese objetivo товарищ!")
    except Exception as exc:
        await ctx.send('No anda nada cuando actualizo la data: {}'.format(exc))
    finally:
        cursor.close()
        conn.close()

@commands.command()
async def deshecho(ctx,*,goal):
    user_id = ctx.message.author.name
    try:
        conn = connection.get_connection()
        cursor = conn.cursor()
        cursor.execute(f"SELECT id_user FROM goals WHERE goal='{goal}' AND id_user='{user_id}'")
        result = cursor.fetchone()
        if result != None:
            cursor.execute(f"UPDATE goals SET done ='0' WHERE goal='{goal}' AND id_user='{user_id}'")
            conn.commit()
            await ctx.send("Objetivo actualizado товарищ!")
        else:
            await ctx.send("No parece que tengas ese objetivo товарищ!")
    except Exception as exc:
        await ctx.send('No anda nada cuando actualizo la data: {}'.format(exc))
    finally:
        cursor.close()
        conn.close()

async def format_goals(ctx,user_id):
    try:
        conn = connection.get_connection()
        cursor = conn.cursor()
        cursor.execute(f"SELECT goal, done FROM goals WHERE id_user='{user_id}'")
        user_goals = cursor.fetchall()
    except Exception as exc:
        await ctx.send('No anda nada cuando traigo la data: {}'.format(exc))
    finally:
        cursor.close()
        conn.close()

    body_data = []
    for user_achi in user_goals:
        goal = user_achi[0]
        if user_achi[1] == '0':
            done = "No"
        else:
            done = "✓"
        body_data.append([goal, done])
    output = t2a(
        header = ['Objetivo','Listo'],
        body = body_data,
        style = PresetStyle.thin_compact
    )
    embed = discord.Embed()
    embed.add_field(name="Objetivos 2023 de "+user_id, value=f"```\n{output}```")
    return embed

def get_goal(goal):
    return goal.replace("'", "´")

async def setup(bot):
    bot.add_command(asignarObjetivo)
    bot.add_command(agregarObjetivo)
    bot.add_command(misObjetivos)
    bot.add_command(verObjetivosDe)
    bot.add_command(hecho)
    bot.add_command(deshecho)
