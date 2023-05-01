import discord
import connection
import validations
import comandos_frases
import os
from discord.ext import commands
from deep_translator import GoogleTranslator
from dotenv import load_dotenv

load_dotenv()
BOT_TOKEN = os.getenv('BOT_TOKEN')

intents = discord.Intents.default()
intents.members = True
intents.message_content = True
bot = commands.Bot(intents = intents, command_prefix = '.')
frases_respuestas = []
servers_availables = []
ignored_users = []

async def command_extensions():
    await bot.load_extension('comandos_frases')
    await bot.load_extension('comandos_csgo')
    await bot.load_extension('comandos_cumple')
    await bot.load_extension('comandos_films')
    await bot.load_extension('comandos_gartic')
    await bot.load_extension('comandos_kokemone')
    await bot.load_extension('comandos_parmi')
    await bot.load_extension('comandos_rancios')
    await bot.load_extension('comandos_piedra')
    await bot.load_extension('comandos_achievements')
    await bot.load_extension('comandos_objetivos')

@bot.event
async def on_ready():
    await command_extensions()
    conn = connection.get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT frase_respuesta FROM frases_respuestas")
        frases = cursor.fetchall()
        for frase in frases:
            frases_respuestas.append(frase[0])
        cursor.execute("SELECT description FROM available_servers")
        servers = cursor.fetchall()
        for server in servers:
            servers_availables.append(server[0])
        cursor.execute("SELECT user_name FROM ignored_users")
        ignored_users_db = cursor.fetchall()
        for user in ignored_users_db:
            ignored_users.append(user[0])
    except Exception as exc:
        print(f"No pude obtener las frases  y servidores a responder: {exc}")
    finally:
        cursor.close()
        conn.close()
    await bot.change_presence(activity=discord.Game('esculpir el tiempo'))
    print('Привет друзья!')

@bot.event
async def on_message(message):
    if message.author.name not in ignored_users:
        ctx = await bot.get_context(message)
        if (validations.validate_server(ctx, servers_availables)):
            await process_message(ctx,message)
        else:
            if await validations.validate_pastor(ctx):
                await process_message(ctx,message)
            else:
                await ctx.send('No te haga el loco y anda a escribir al servidor.')

async def process_message(ctx,message):
    if message.author == bot.user:
        return     
    #if (message.content == '<@&789730850707079230>'):
        #await ctx.send('https://www.instagram.com/p/CpnItRHP5hv/')
    if (message.content in frases_respuestas) or custom_responses(message.content):
        await comandos_frases.frase(ctx)
    await bot.process_commands(message)

def custom_responses(message):
    if ('Facha' in message) and ('deci' in message):
        return True
    if ('facha' in message) and ('deci' in message):
        return True
    if ('Facha' in message) and ('?' in message):
        return True
    if ('facha' in message) and ('?' in message):
        return True
    if ('Facha' in message) and ('conta' in message):
        return True
    if ('facha' in message) and ('conta' in message):
        return True

@bot.command()
async def ejecutar(ctx,*,sql):
    if await validations.validate_pastor(ctx):
        conn = connection.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(sql)
            conn.commit()
            await ctx.send("Ejecutado master.")
        except Exception as exc:
            await ctx.send(f"No pude ejecutar el sql: {exc}")
        finally:
            cursor.close()
            conn.close()

@bot.command()
async def traduci(ctx,*,text):
    translated = GoogleTranslator(source='auto', target='portuguese').translate(text)
    await ctx.send(translated)

@bot.command()
async def traduciAl(ctx,*,text):
    language_text = text.split(',')
    language = language_text[0]
    translated = GoogleTranslator(source='auto', target=f'{language}').translate(text[3:])
    await ctx.send(translated)

@bot.command()
async def say(ctx,*,message):
    await ctx.channel.purge(limit=1)
    await ctx.send(message)

@bot.command()
async def tasBien(ctx):
    await ctx.send(f'{round(bot.latency * 1000)}ms')

@bot.command()
@commands.has_permissions(manage_messages=True)
async def limpiar(ctx, amount=2):
    await ctx.channel.purge(limit=amount)

@bot.command()
@commands.has_permissions(manage_messages=True)
async def megaLimpiar(ctx, amount):
    await ctx.channel.purge(limit=int(amount))

@limpiar.error
async def limpiar_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send('Hermano no me pediste nada.')

bot.run(BOT_TOKEN)
