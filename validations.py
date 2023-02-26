def validate_psigang(server_name):
    if server_name == 'Psigang':
        return True
    else:
        return False

async def validate_pastor(ctx):
    autor = ctx.message.author.id
    if autor == 186664188750462977:
        return True
    else:
        await ctx.send("Quien te conoce they? so bolude y no tene huevevarios.")
        return False

def validate_server(ctx, servers_availables):
    server_name = None
    try:
        server_name = ctx.message.guild.name
    except Exception as exc:
        print(f"{ctx.message.author.name} me esta hablando por privado")
    if (server_name == None) or (server_name not in servers_availables):
        return False
    else:
        return True

def get_frase(frase):
    return frase.replace("'", "´")