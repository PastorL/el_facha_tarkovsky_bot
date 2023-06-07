import connection
import discord
import asyncio
from discord.ext import commands
from gtts import gTTS


@commands.command()
async def habla(ctx):
    conn = connection.get_connection()
    cursor = conn.cursor()
    server_name = ctx.message.guild.name
    try:
        cursor.execute(f"SELECT descripcion FROM frases WHERE server_name='{server_name}' AND descripcion NOT LIKE '%https%' ORDER BY RANDOM() LIMIT 1")
        frase = cursor.fetchone()

        language = 'es'
        tts = gTTS(frase[0], lang=language)
        audio_file = 'hablacion.mp3'
        tts.save(audio_file)

        await ctx.send(file=discord.File(audio_file))    
    except Exception as exc:
        await ctx.send('No anda nada cuando traigo las frases: {}'.format(exc))
    finally:
        cursor.close()
        conn.close()

@commands.command()
async def contame(ctx):
    conn = connection.get_connection()
    cursor = conn.cursor()
    server_name = ctx.message.guild.name
    try:
        cursor.execute(f"SELECT descripcion FROM frases WHERE server_name='{server_name}' AND descripcion NOT LIKE '%https%' ORDER BY RANDOM() LIMIT 1")
        frase = cursor.fetchone()

        if ctx.author.voice is None or ctx.author.voice.channel is None:
            await ctx.send("No estás conectado a ningún canal.")
            return

        channel = ctx.author.voice.channel
        await channel.connect()

        language = 'es'
        tts = gTTS(frase[0], lang=language)
        audio_path = 'hablacion.mp3'
        tts.save(audio_path)
        FFMPEG_OPTIONS = {
            "options": "-vn",
        }
        ctx.voice_client.play(discord.FFmpegOpusAudio(audio_path))

        while ctx.voice_client.is_playing():
            await asyncio.sleep(1)  
        await ctx.voice_client.disconnect()
    except Exception as exc:
        await ctx.send('No anda nada cuando traigo las frases: {}'.format(exc))
    finally:
        cursor.close()
        conn.close()

@commands.command()
async def andate(ctx):
    await ctx.voice_client.disconnect()

@commands.command()
async def buscarHabla(ctx, *, frase):
    conn = connection.get_connection()
    cursor = conn.cursor()
    server_name = ctx.message.guild.name
    try:
        cursor.execute(f"SELECT descripcion FROM frases WHERE server_name='{server_name}' AND LOWER(descripcion) LIKE '%{frase}%' AND descripcion NOT LIKE '%https%' ORDER BY RANDOM() LIMIT 1")
        frase = cursor.fetchone()
        language = 'es'
        tts = gTTS(frase[0], lang=language)
        audio_file = 'hablacion.mp3'
        tts.save(audio_file)

        await ctx.send(file=discord.File(audio_file))    
    except Exception as exc:
        await ctx.send('No existe esa frase peconchatumaquina.')
    finally:
        cursor.close()
        conn.close()

async def setup(bot):
    bot.add_command(habla)
    bot.add_command(buscarHabla)
    bot.add_command(contame)
    bot.add_command(andate)