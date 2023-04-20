from discord.ext import commands
import random

@commands.command()
async def piedra(ctx):
    result = piedra_papel_tijera()
    await ctx.send(result)

@commands.command()
async def papel(ctx):
    result = piedra_papel_tijera()
    await ctx.send(result)

@commands.command()
async def tijera(ctx):
    result = piedra_papel_tijera()
    await ctx.send(result)

def piedra_papel_tijera():
    options = ["piedra", "papel", "tijera"]
    result = random.choice(options)
    return result

async def setup(bot):
    bot.add_command(piedra)
    bot.add_command(papel)
    bot.add_command(tijera)