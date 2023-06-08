from discord.ext import commands
from table2ascii import table2ascii as t2a, PresetStyle
import validations
import connection
import discord
import DiscordUtils

@commands.command()
async def agregarAchi(ctx,*,achi_points):
    if await validations.validate_pastor(ctx):
        conn = connection.get_connection()
        cursor = conn.cursor()
        achi_points_list = achi_points.split(',')
        achi = achi_points_list[0]
        points = achi_points_list[1]
        server_name = ctx.message.guild.name
        sql = (f"INSERT INTO achievements(name, points, server) VALUES ('{get_achi(achi)}','{points}','{server_name}')")
        try:
            cursor.execute(sql)
            conn.commit()
            await ctx.send("Achivement agregado товарищ!")
        except Exception as exc:
            await ctx.send('No anda nada cuando guardo las frases: {}'.format(exc))
        finally:
            cursor.close()
            conn.close()

@commands.command()
async def achis(ctx):
    try:
        server_name = ctx.message.guild.name
        conn = connection.get_connection()
        cursor = conn.cursor()
        cursor.execute(f"SELECT id_achievement, name, points FROM achievements WHERE server='{server_name}'")
        achis = cursor.fetchall()
    except Exception as exc:
        await ctx.send('No anda nada cuando traigo la data: {}'.format(exc))
    finally:
        cursor.close()
        conn.close()

    achis_sets = []
    embeds = []
    while len(achis) > 10:
        achis_sets.append(achis[:5])
        del achis[:5]
    if len(achis) != 0:
        achis_sets.append(achis[:5])
        del achis[:5]

    for achis_set in achis_sets:
        body_data = []
        for data_achi in achis_set:
            number = data_achi[0]
            achi = data_achi[1]
            points = data_achi[2]
            body_data.append([number, achi, points])
        output = t2a(
            header = ['#', 'Achievement', 'Puntos'],
            body = body_data,
            style = PresetStyle.thin_compact
        )
        embed = discord.Embed(color=ctx.author.color).add_field(name="Achievements", value=f"```\n{output}```")
        embeds.append(embed)

    paginator = DiscordUtils.Pagination.CustomEmbedPaginator(ctx)
    paginator.add_reaction('⏮️', "first")
    paginator.add_reaction('⏪', "back")
    paginator.add_reaction('⏩', "next")
    paginator.add_reaction('⏭️', "last")
    embed = await paginator.run(embeds)
    await ctx.send(embed)

@commands.command()
async def misAchis(ctx):
    user_id = ctx.message.author.name
    try:
        conn = connection.get_connection()
        cursor = conn.cursor()
        sql = ("SELECT achi.name, achi.points "
                       "FROM user_achievements ua "
                       "INNER JOIN achievements achi ON achi.id_achievement = ua.id_achi "
                       f"WHERE ua.id_user='{user_id}'")
        cursor.execute(sql)
        user_achis = cursor.fetchall()
    except Exception as exc:
        await ctx.send('No anda nada cuando traigo la data: {}'.format(exc))
    finally:
        cursor.close()
        conn.close()

    user_achis_sets = []
    embeds = []
    total_points = 0
    while len(user_achis) > 10:
        user_achis_sets.append(user_achis[:5])
        del user_achis[:5]
    if len(user_achis) != 0:
        user_achis_sets.append(user_achis[:5])
        del user_achis[:5]

    for user_achi_set in user_achis_sets:
        body_data = []
        for user_achi in user_achi_set:
            achi = user_achi[0]
            points = user_achi[1]
            total_points += points
            body_data.append([achi, points, ''])
        body_data.append(['', '', total_points])
        output = t2a(
            header = ['Achievement', 'Puntos', 'Total'],
            body = body_data,
            style = PresetStyle.thin_compact
        )
        embed = discord.Embed(color=ctx.author.color).add_field(name="Achievements de "+user_id, value=f"```\n{output}```")
        embeds.append(embed)

    paginator = DiscordUtils.Pagination.CustomEmbedPaginator(ctx)
    paginator.add_reaction('⏮️', "first")
    paginator.add_reaction('⏪', "back")
    paginator.add_reaction('⏩', "next")
    paginator.add_reaction('⏭️', "last")
    embed = await paginator.run(embeds)
    await ctx.send(embed)

@commands.command()
async def darAchi(ctx,*,user_achi):
    if await validations.validate_pastor(ctx):
        try:
            user_achis = user_achi.split(',')
            user_id = user_achis[0]
            achi_id = user_achis[1]

            conn = connection.get_connection()
            cursor = conn.cursor()
            cursor.execute(f"SELECT id_achi FROM user_achievements WHERE id_user='{user_id}' AND id_achi = {achi_id}")
            achi = cursor.fetchone()

            if achi == None:
                sql = (f"INSERT INTO user_achievements(id_user, id_achi) VALUES ('{user_id}','{achi_id}')")
                cursor.execute(sql)
                conn.commit()
                await ctx.send("Achievement asignado товарищ.")
            else:
                await ctx.send("Disculpe maestro pero el usuario ya tiene ese achievement.")
        except Exception as exc:
            await ctx.send('No anda nada cuando asigno el achievement: {}'.format(exc))
        finally:
            cursor.close()
            conn.close()

@commands.command()
async def quitarAchi(ctx,*,user_achi):
    if await validations.validate_pastor(ctx):
        try:
            user_achis = user_achi.split(',')
            user_id = user_achis[0]
            achi_id = user_achis[1]

            conn = connection.get_connection()
            cursor = conn.cursor()
            cursor.execute(f"SELECT id_achi FROM user_achievements WHERE id_user='{user_id}' AND id_achi={achi_id}")
            achi = cursor.fetchone()

            if achi != None:
                sql = (f"DELETE FROM user_achievements WHERE id_user='{user_id}' AND id_achi={achi_id}")
                cursor.execute(sql)
                conn.commit()
                await ctx.send("Achievement borrado товарищ.")
            else:
                await ctx.send("Disculpe maestro pero el usuario no tiene ese achievement.")
        except Exception as exc:
            await ctx.send('No anda nada cuando borro el achievement: {}'.format(exc))
        finally:
            cursor.close()
            conn.close()

def get_achi(achi):
    return achi.replace("'", "´")

async def setup(bot):
    bot.add_command(agregarAchi)
    bot.add_command(achis)
    bot.add_command(misAchis)
    bot.add_command(darAchi)
    bot.add_command(quitarAchi)

