import discord
import connection
import random
import validations
from table2ascii import table2ascii as t2a, PresetStyle
from discord.ext import commands

@commands.command()
async def quienJuegaCS(ctx):
    players_pool = []
    players = []
    for member in ctx.guild.members:
        for role in member.roles:
            if (role.name == "CSGO"):
                players_pool.append(member)
    for _ in range(5):
        play = random.choice(players_pool)
        player_index = players_pool.index(play)
        players.append(play)
        players_pool.pop(player_index)
    for p in players:
        await ctx.send(p.name)

@commands.command()
async def cargarPartida(ctx,*,data):
    if await validations.validate_pastor(ctx):
        saved = 1
        conn = connection.get_connection()
        cursor = conn.cursor()
        game_data = data.split(',')
        cursor.execute(f"SELECT id_cs_game FROM cs_games GROUP BY id_cs_game ORDER BY id_cs_game DESC LIMIT 1")
        cs_games_quantity = int(cursor.fetchone()[0]) + 1
        print(cs_games_quantity)
        for player_data in game_data:
            player = player_data.split(' ')
            id_cs_player = player[0]
            kills = player[1]
            assists = player[2]
            deaths = player[3]
            score = player[4]
            win = player[5]
            try:
                cursor.execute(f"SELECT total_kills, total_assists, total_deaths, total_score, total_wins FROM cs_ranking WHERE id_cs_player = '{id_cs_player}'")
                result = cursor.fetchone()
                ranking_kills = result[0]
                ranking_assists = result[1]
                ranking_deaths = result[2]
                ranking_score = result[3]
                ranking_wins = result[4]

                total_kills = ranking_kills + int(kills)
                total_assists = ranking_assists + int(assists)
                total_deaths = ranking_deaths + int(deaths)
                total_score = ranking_score + int(score)
                total_wins = ranking_wins + int(win)

                cursor.execute(f"INSERT INTO cs_games(id_cs_game, id_cs_player, kills, assists, deaths, score, win) VALUES ({cs_games_quantity},'{id_cs_player}',{kills},{assists},{deaths},{score},{win})")
                cursor.execute(f"UPDATE cs_ranking SET total_kills = {total_kills}, total_assists = {total_assists}, total_deaths = {total_deaths}, total_score = {total_score}, total_wins = {total_wins} WHERE id_cs_player = '{id_cs_player}'")
                conn.commit()
            except Exception as exc:
                saved = 0
                await ctx.send('No anda nada cuando guardo la data de la partida: {}'.format(exc))
            finally:
                cursor.close()
                conn.close()
        if saved == 1:
            await ctx.send('Data de partidas actualizada.')

@commands.command()
async def myStats(ctx):
    id_cs_player = ctx.message.author.name
    conn = connection.get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(f"SELECT COUNT(*) FROM cs_games WHERE id_cs_player = '{id_cs_player}'")
        games_quantity = cursor.fetchone()[0]
        cursor.execute(f"SELECT total_kills, total_assists, total_deaths, total_score, total_wins FROM cs_ranking WHERE id_cs_player='{id_cs_player}'")
        player_data = cursor.fetchone()
    except Exception as exc:
        await ctx.send('No anda nada cuando traigo la data: {}'.format(exc))
    finally:
        cursor.close()
        conn.close()

    kills = player_data[0]
    assists = player_data[1]
    deaths = player_data[2]
    score = player_data[3]
    wins = player_data[4]

    media_kills = round(kills/games_quantity, 1)
    media_assists = round(assists/games_quantity, 1)
    media_deaths = round(deaths/games_quantity, 1)
    media_score = round(score/games_quantity, 1)
    media_wins = round(wins/games_quantity, 2)

    output = t2a(
        header = ['Games', 'Kills', 'Assists', 'Deaths', 'Score', 'Wins'],
        body = [[games_quantity, kills, assists, deaths, score, wins], ['Media', media_kills, media_assists, media_deaths, media_score, media_wins]],
        style=PresetStyle.thin_compact
    )
    embed = discord.Embed()
    embed.add_field(name=id_cs_player, value=f"```\n{output}```")
    await ctx.send(embed=embed)

@commands.command()
async def ranking(ctx):
    conn = connection.get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(f"SELECT id_cs_player, total_kills, total_assists, total_deaths, total_score, total_wins FROM cs_ranking ORDER BY total_kills DESC")
        players_data = cursor.fetchall()
    except Exception as exc:
        await ctx.send('No anda nada cuando traigo la data: {}'.format(exc))

    try:
        body_data = []
        for player_data in players_data:
            player = player_data[0]
            cursor.execute(f"SELECT COUNT(*) FROM cs_games WHERE id_cs_player = '{player}'")
            games_quantity = cursor.fetchone()[0]

            kills = player_data[1]
            assists = player_data[2]
            deaths = player_data[3]
            score = player_data[4]
            wins = player_data[5]

            body_data.append([player, kills, assists, deaths, score, games_quantity, wins])
    except Exception as exc:
        await ctx.send('No anda nada cuando traigo la data: {}'.format(exc))
    finally:
        cursor.close()
        conn.close()

    output = t2a(
        header = ['Rata', 'Kills', 'Assists', 'Deaths', 'Score', 'Games', 'Wins'],
        body = body_data,
        style = PresetStyle.thin_compact
    )
    embed = discord.Embed()
    embed.add_field(name="Ranking", value=f"```\n{output}```")
    await ctx.send(embed=embed)

@commands.command()
async def mediaRanking(ctx):
    conn = connection.get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(f"SELECT id_cs_player, total_kills, total_assists, total_deaths, total_score, total_wins FROM cs_ranking ORDER BY total_kills DESC")
        players_data = cursor.fetchall()
    except Exception as exc:
        await ctx.send('No anda nada cuando traigo la data: {}'.format(exc))

    try:
        body_data = []
        for player_data in players_data:
            player = player_data[0]
            cursor.execute(f"SELECT COUNT(*) FROM cs_games WHERE id_cs_player = '{player}'")
            games_quantity = cursor.fetchone()[0]

            kills = player_data[1]
            assists = player_data[2]
            deaths = player_data[3]
            score = player_data[4]
            wins = player_data[5]

            media_kills = 0
            media_assists = 0
            media_deaths = 0
            media_score = 0
            media_wins = 0

            if games_quantity != 0:
                media_kills = round(kills/games_quantity, 1)
                media_assists = round(assists/games_quantity, 1)
                media_deaths = round(deaths/games_quantity, 1)
                media_score = round(score/games_quantity, 1)
                media_wins = round(wins/games_quantity, 2)

            body_data.append([player, media_kills, media_assists, media_deaths, media_score, media_wins])
    except Exception as exc:
            await ctx.send('No anda nada cuando traigo la data: {}'.format(exc))
    finally:
        cursor.close()
        conn.close()

    body_data.sort(key=getMediaKills, reverse=True)
    output = t2a(
        header = ['Rata', 'Kills/g', 'Assists/g', 'Deaths/g', 'Score/g', 'Wins/g'],
        body = body_data,
        style = PresetStyle.thin_compact
    )
    embed = discord.Embed()
    embed.add_field(name="Ranking", value=f"```\n{output}```")
    await ctx.send(embed=embed)

@commands.command()
async def lastestMediaRanking(ctx):
    conn = connection.get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(f"SELECT id_cs_player, total_kills, total_assists, total_deaths, total_score, total_wins FROM cs_ranking ORDER BY total_kills DESC")
        players_data = cursor.fetchall()
    except Exception as exc:
        await ctx.send('No anda nada cuando traigo la data: {}'.format(exc))

    try:
        body_data = []
        games_quantity = 30
        for player_data in players_data:
            player = player_data[0]
            cursor.execute(f"SELECT SUM(kills), SUM(assists), SUM(deaths), SUM(score), SUM(win) FROM cs_games WHERE id_cs_player = '{player}' AND id_cs_game IN (SELECT id_cs_game FROM cs_games WHERE id_cs_player = '{player}' ORDER BY id_cs_game DESC LIMIT 30)")
            data = cursor.fetchone()

            kills = data[0]
            assists = data[1]
            deaths = data[2]
            score = data[3]
            wins = data[4]

            media_kills = 0
            media_assists = 0
            media_deaths = 0
            media_score = 0
            media_wins = 0

            if games_quantity != 0:
                media_kills = round(kills/games_quantity, 1)
                media_assists = round(assists/games_quantity, 1)
                media_deaths = round(deaths/games_quantity, 1)
                media_score = round(score/games_quantity, 1)
                media_wins = round(wins/games_quantity, 2)

            body_data.append([player, media_kills, media_assists, media_deaths, media_score, media_wins])
    except Exception as exc:
        await ctx.send('No anda nada cuando traigo la data: {}'.format(exc))
    finally:
        cursor.close()
        conn.close()

    body_data.sort(key=getMediaKills, reverse=True)
    output = t2a(
        header = ['Rata', 'Kills/g', 'Assists/g', 'Deaths/g', 'Score/g', 'Wins/g'],
        body = body_data,
        style = PresetStyle.thin_compact
    )
    embed = discord.Embed()
    embed.add_field(name="Ranking", value=f"```\n{output}```")
    await ctx.send(embed=embed)

def getMediaKills(elem):
    return elem[1]

async def setup(bot):
    bot.add_command(quienJuegaCS)
    bot.add_command(cargarPartida)
    bot.add_command(myStats)
    bot.add_command(ranking)
    bot.add_command(mediaRanking)
    bot.add_command(lastestMediaRanking)