import connection
import validations
from discord.ext import commands

@commands.command()
async def parmi(ctx):
    conn = connection.get_connection()
    cursor = conn.cursor()
    server_name = ctx.message.guild.name
    if validations.validate_psigang(server_name):
        try:
            cursor.execute(f"SELECT parmi_frase FROM parmi_frases ORDER BY RANDOM() LIMIT 1")
            frase = cursor.fetchone()
            await ctx.send(frase[0])
        except Exception as exc:
            await ctx.send('No anda nada cuando traigo la parmifrase: {}'.format(exc))
        finally:
            cursor.close()
            conn.close()

@commands.command()
async def addParmi(ctx,*,frase):
    autor = ctx.message.author.name
    server_name = ctx.message.guild.name
    if validations.validate_psigang(server_name):
        if validate_parmi_frase(frase):
            conn = connection.get_connection()
            cursor = conn.cursor()
            server_name = ctx.message.guild.name
            sql = (f"INSERT INTO parmi_frases(parmi_frase) VALUES ('{get_frase(frase)}')")
            try:
                result = cursor.execute(sql)
                conn.commit()
                await ctx.send("Parmifrase agregada товарищ!")
            except Exception as exc:
                await ctx.send('No anda nada cuando guardo la parmifrase: {}'.format(exc))
            finally:
                cursor.close()
                conn.close()
        else:
            await ctx.send("La frase ya existe сука блять!")

def validate_parmi_frase(frase):
    conn = connection.get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(f"SELECT COUNT (*) FROM parmi_frases WHERE parmi_frase = '{get_frase(frase)}'")
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

async def setup(bot):
    bot.add_command(parmi)
    bot.add_command(addParmi)