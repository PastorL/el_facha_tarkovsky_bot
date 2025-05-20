from discord.ext import commands
from table2ascii import table2ascii as t2a, PresetStyle
import validations
import connection
import discord
import DiscordUtils
import datetime


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
async def addObjetivo(ctx,*,goal):
    user_id = ctx.message.author.name
    today = datetime.date.today()
    year = today.year
    if len(goal) >= 35:
        await ctx.send('El objetivo es muy largo. Acortalo rata.')
    else:
        try:
            conn = connection.get_connection()
            cursor = conn.cursor()
            sql = (f"INSERT INTO goals(goal, id_user, done, year) VALUES ('{get_goal(goal)}','{user_id}', '0', '{year}')")
            cursor.execute(sql)
            conn.commit()
            await ctx.send("Objetivo agregado товарищ!")
        except Exception as exc:
            await ctx.send('No anda nada cuando guardo los objetivos: {}'.format(exc))
        finally:
            cursor.close()
            conn.close()

@commands.command()
async def misObjetivos(ctx, user_year: str=''):
    user_id = ctx.message.author.name
    print(user_year)
    if user_year != '':
        embed = await format_goals(ctx,user_id,user_year)
    else:
        today = datetime.date.today()
        year = today.year
        print(year)
        embed = await format_goals(ctx,user_id,year)
    await ctx.send(embed=embed)

@commands.command()
async def verObjetivosDe(ctx,*,user_id_year):
    user_id_years = user_id_year.split(',')
    user_id = user_id_years[0]
    user_year = user_id_years[1]
    if user_year != '':
        embed = await format_goals(ctx,user_id,user_year)
    else:
        today = datetime.date.today()
        year = today.year
        embed = await format_goals(ctx,user_id,year)
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

async def format_goals(ctx,user_id,year):
    try:
        conn = connection.get_connection()
        cursor = conn.cursor()
        cursor.execute(f"SELECT goal, done FROM goals WHERE id_user='{user_id}' AND year='{year}'")
        user_goals = cursor.fetchall()
    except Exception as exc:
        await ctx.send('No anda nada cuando traigo la data: {}'.format(exc))
    finally:
        cursor.close()
        conn.close()

    goal_sets = []
    embeds = []
    goal_number = 0
    while len(user_goals) > 10:
        goal_sets.append(user_goals[:10])
        del user_goals[:10]
    if len(user_goals) != 0:
        goal_sets.append(user_goals[:10])
        del user_goals[:10]

    for goal_set in goal_sets:
        body_data = []
        for goal in goal_set:
            if goal[1] == '0':
                done = "No"
            else:
                done = "✓"
            goal_number += 1
            body_data.append([goal_number, goal[0], done])
        output = t2a(
            header = ['N°','Objetivo','Listo'],
            body = body_data,
            style = PresetStyle.thin_compact
        )
        embed = discord.Embed(color=ctx.author.color).add_field(name="Objetivos "+str(year)+" de "+user_id, value=f"```\n{output}```")
        embeds.append(embed)

    paginator = DiscordUtils.Pagination.CustomEmbedPaginator(ctx)
    paginator.add_reaction('⏮️', "first")
    paginator.add_reaction('⏪', "back")
    paginator.add_reaction('⏩', "next")
    paginator.add_reaction('⏭️', "last")

    return await paginator.run(embeds)

def get_goal(goal):
    return goal.replace("'", "´")

async def setup(bot):
    bot.add_command(asignarObjetivo)
    bot.add_command(addObjetivo)
    bot.add_command(misObjetivos)
    bot.add_command(verObjetivosDe)
    bot.add_command(hecho)
    bot.add_command(deshecho)
