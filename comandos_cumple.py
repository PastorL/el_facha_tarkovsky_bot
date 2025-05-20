import connection
from datetime import date
from discord.ext import commands

@commands.command()
async def cumple(ctx):
    discord_server = ctx.message.guild.name
    conn = connection.get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(f"SELECT discord_user, discord_id, fecha, cast(fecha + ((extract(year from age(fecha)) + 1) * interval '1' year) as date) as next_birthday from cumpleaños_fechas WHERE to_char(CURRENT_DATE,'MM') = to_char(cast(fecha + ((extract(year from age(fecha)) + 1) * interval '1' year) as date), 'MM') AND to_char(CURRENT_DATE,'DD') = to_char(cast(fecha + ((extract(year from age(fecha)) + 1) * interval '1' year) as date), 'DD')")
        cumpleañero_del_dia = cursor.fetchall()
        print(cumpleañero_del_dia)
        if cumpleañero_del_dia != []:
            for cumpleañero in cumpleañero_del_dia:
                cumpleañero_tag = f"<@{cumpleañero[1]}>"
                await ctx.send(f'Hoy es el cumpleaños de {cumpleañero_tag}! С днем ​​рождения товарищ!')
                await ctx.send("https://www.youtube.com/watch?v=UBGJOGNP0fI")
        else:
            print("asdasd")
            cursor.execute(f"SELECT discord_user, discord_id, fecha, cast(fecha + ((extract(year from age(fecha)) + 1) * interval '1' year) as date) as next_birthday from cumpleaños_fechas WHERE discord_server = '{discord_server}' ORDER BY next_birthday asc LIMIT 1")
            cumpleaños_data = cursor.fetchone()
            cumpleañero = cumpleaños_data[0]
            cumpleañero_id = cumpleaños_data[1]
            cumple = cumpleaños_data[3]
            await ctx.send(f'El próximo cumpleaños es el de {cumpleañero} el {cumple.day} del {cumple.month}.')
    except:
        await ctx.send(f'Error gravísimo al consultar los cumpleaños.')
    finally:
        cursor.close()
        conn.close()

@commands.command()
async def addMiCumple(ctx,*,fecha):
    autor_name = ctx.message.author.name
    server_name = ctx.message.guild.name
    autor_id = autor = ctx.message.author.id
    today = date.today()
    fecha_array = []
    if '/' in fecha or '-' in fecha:
        if '/' in fecha:
            fecha_array = fecha.split('/')
        if '-' in fecha:
            fecha_array = fecha.split('-')
    else:
        await ctx.send(f'Cuchame una cosa no te haga el vive y poné una fecha válida día/mes/año en ese exacto formato o te liquido.')
    if (len(fecha_array) == 3 and len(fecha_array[0]) != 0 and len(fecha_array[1]) != 0 and len(fecha_array[2]) != 0):
        dias = int(fecha_array[0])
        mes = int(fecha_array[1])
        año = int(fecha_array[2])
        if (dias > 31 or dias < 1):
            await ctx.send(f'No te haga el vive y poné un día válido.')
        else:
            if (mes > 12 or mes < 1):
                await ctx.send(f'No te haga el vive y poné un mes válido.')
            else:
                if (año > today.year or año < 1800):
                    await ctx.send(f'No te haga el vive y poné un año válido.')
                else:
                    if validate_cumpleanios_exists(server_name, autor_id):
                        conn = connection.get_connection()
                        cursor = conn.cursor()
                        date_cumpleaños = date(año, mes, dias)
                        sql = (f"INSERT INTO cumpleaños_fechas(discord_user, fecha, discord_server, discord_id) VALUES ('{autor_name}','{date_cumpleaños}','{server_name}','{autor_id}')")
                        try:
                            result = cursor.execute(sql)
                            conn.commit()
                            await ctx.send("Cumpleaños agregado товарищ!")
                        except Exception as exc:
                            await ctx.send('No anda nada cuando guardo el cumpleaños: {}'.format(exc))
                        finally:
                            cursor.close()
                            conn.close()
                    else:
                        await ctx.send(f'Vos ya cargaste tu cumpleaños payase vola de acá o te reviento la gorra.')
    else:
        await ctx.send(f'Cuchame una cosa no te haga el vive y poné una fecha válida día/mes/año en ese exacto formato o te liquido.')

def validate_cumpleanios_exists(server_name, autor_id):
    conn = connection.get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(f"SELECT COUNT (*) FROM cumpleaños_fechas WHERE discord_server = '{server_name}' AND discord_id = '{autor_id}'")
        result = 0
        result = cursor.fetchone()[0]
        if result == 0:
            return True
        else:
            return False
    except Exception as exc:
        print('Error al validar el cumpleaños.')
    finally:
        cursor.close()
        conn.close()
        
async def setup(bot):
    bot.add_command(cumple)
    bot.add_command(addMiCumple)
