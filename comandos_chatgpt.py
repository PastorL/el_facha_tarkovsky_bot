import openai
import os
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv('CHATGPT_API_KEY')

@commands.command()
async def chachi(ctx,*,prompt):
    response = chatgpt(prompt)
    await ctx.send(response)

def chatgpt(message):
    response = openai.Completion.create(
        engine="gpt-3.5-turbo-instruct",
        prompt=message,
        temperature=0.7,
        max_tokens=100
    )

    return response

async def setup(bot):
    bot.add_command(chachi)