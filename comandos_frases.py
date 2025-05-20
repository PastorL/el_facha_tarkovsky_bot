import connection
import random
from discord.ext import commands


@commands.command()
async def frase(ctx):
    conn = connection.get_connection()
    cursor = conn.cursor()
    server_name = ctx.message.guild.name
    shiny = random.randint(0,8192)
    if shiny == 1:
        await ctx.send("https://media.discordapp.net/attachments/1102706675091259463/1238702230945665125/GNGQIHAW0AAF2oh.webp?ex=66403ed9&is=663eed59&hm=1f54fdcc219908fb4e1416db16862e491d09c1af09e9211acee263856711af85&=&format=webp&width=387&height=489")
        await ctx.send("Felicidades! un shiny!")
    else: 
        try:
            cursor.execute(f"SELECT descripcion FROM frases WHERE server_name='{server_name}' ORDER BY RANDOM() LIMIT 1")
            #cursor.execute(f"SELECT descripcion FROM frases ORDER BY RANDOM() LIMIT 1")
            frase = cursor.fetchone()
            await ctx.channel.purge(limit=1)
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
        cursor.execute(f"SELECT descripcion FROM frases WHERE server_name='{server_name}' AND LOWER(descripcion) LIKE '%{frase.lower()}%' ORDER BY RANDOM() LIMIT 1")
        frase = cursor.fetchone()
        await ctx.send(frase[0])
    except Exception as exc:
        await ctx.send('No existe esa frase peconchatumaquina.')
    finally:
        cursor.close()
        conn.close()

@commands.command()
async def quienFueElBurro(ctx,*,frase):
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

async def frase_custom(ctx, message):
    conn = connection.get_connection()
    cursor = conn.cursor()
    server_name = ctx.message.guild.name
    user = ctx.message.author.name
    shiny = random.randint(0,8192)
    if shiny == 1:
        await ctx.send("https://media.discordapp.net/attachments/1102706675091259463/1238702230945665125/GNGQIHAW0AAF2oh.webp?ex=66403ed9&is=663eed59&hm=1f54fdcc219908fb4e1416db16862e491d09c1af09e9211acee263856711af85&=&format=webp&width=387&height=489")
        await ctx.send("Felicidades! un shiny!")
    else: 
        try:
            message_words = message.split()
            
            cursor.execute(f"SELECT nickname FROM user_nicknames")
            nicknames = cursor.fetchall()
            nicknames_list = [item[0] for item in nicknames]
            nickname_matches = [element for element in message_words if element in nicknames_list]
            #nickname_to = list(message_words.intersection(nicknames_list))
            print("hola")
            print(nickname_matches)
            if not nickname_matches:
                query = f"SELECT descripcion FROM frases WHERE server_name='{server_name}' ORDER BY RANDOM() LIMIT 1"
            else:
                nicknames_to_find = ""
                for nickname in nickname_matches:
                    if nicknames_to_find == "":
                        nicknames_to_find = nicknames_to_find + f"nickname LIKE '%{nickname}%'"
                    else:
                        nicknames_to_find = nicknames_to_find + f" OR nickname LIKE '%{nickname}%'"
                cursor.execute(f"""SELECT nickname FROM user_nicknames un
                            INNER JOIN users u ON u.id_user=CAST(un.id_user as INTEGER)
                            WHERE u.id_user IN (SELECT DISTINCT CAST(id_user as INTEGER) FROM user_nicknames WHERE {nicknames_to_find})""")
                users_nicknames = cursor.fetchall()
                users_nicknames = [item[0] for item in users_nicknames]
                
                nicknames_to = ""
                for nickname in users_nicknames:
                    if nicknames_to == "":
                        nicknames_to = nicknames_to + f"descripcion LIKE '%{nickname}%'"
                    else:
                        nicknames_to = nicknames_to + f" OR descripcion LIKE '%{nickname}%'"
                query = f"SELECT descripcion FROM frases WHERE server_name='{server_name}' AND ({nicknames_to}) ORDER BY RANDOM() LIMIT 1"

            cursor.execute(query)
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