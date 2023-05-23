import connection
import discord
import DiscordUtils
from table2ascii import table2ascii as t2a, PresetStyle
from imdb import Cinemagoer
from discord.ext import commands

@commands.command()
async def ayuda(ctx):
    try:
        conn = connection.get_connection()
        cursor = conn.cursor()
        cursor.execute(f"SELECT command, help FROM helps")
        helps = cursor.fetchall()
    except Exception as exc:
        await ctx.send('No anda nada cuando traigo la data: {}'.format(exc))
    finally:
        cursor.close()
        conn.close()

    help_sets = []
    embeds = []
    while len(helps) > 10:
        help_sets.append(helps[:5])
        del helps[:5]
    if len(helps) != 0:
        help_sets.append(helps[:5])
        del helps[:5]

    for help_set in help_sets:
        body_data = []
        for help in help_set:
            body_data.append([help[0], help[1]])
        output = t2a(
            header = ['Comando','Ayuda'],
            body = body_data,
            style = PresetStyle.thin_compact
        )
        embed = discord.Embed(color=ctx.author.color).add_field(name="Lista de comandos", value=f"```\n{output}```")
        embeds.append(embed)

    paginator = DiscordUtils.Pagination.CustomEmbedPaginator(ctx)
    paginator.add_reaction('⏮️', "first")
    paginator.add_reaction('⏪', "back")
    paginator.add_reaction('⏩', "next")
    paginator.add_reaction('⏭️', "last")
    embed = await paginator.run(embeds)
    await ctx.send(embed)

@commands.command()
async def ayudaDe(ctx,command):
    conn = connection.get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(f"SELECT help FROM helps WHERE command='{command}'")
        help = cursor.fetchone()
        await ctx.send(help[0])
    except Exception as exc:
        await ctx.send('Error al buscar la ayuda: {}'.format(exc))
    finally:
        cursor.close()
        conn.close()

async def setup(bot):
    bot.add_command(ayuda)
    bot.add_command(ayudaDe)