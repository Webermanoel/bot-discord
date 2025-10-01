import discord
from discord.ext import commands, tasks
from datetime import datetime
import os
from dotenv import load_dotenv
import random
import asyncio
import pytz

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

intents = discord.Intents.default()
intents.message_content = True
intents.members = True



bot = commands.Bot(command_prefix='!', intents=intents)

def load_phrases(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return [line.strip() for line in file.readlines()]

TRIGGERS = load_phrases('triggers.txt')
RESPONSES = load_phrases('responses.txt')

timezone = pytz.timezone('America/Sao_Paulo')

@bot.event
async def on_ready():
    print(f'Bot {bot.user.name} has connected to Discord!')
    if not daily_greetings.is_running():
        daily_greetings.start()

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    content_lower = message.content.lower()

    for trigger, response in zip(TRIGGERS, RESPONSES):
        if trigger in content_lower:
            formatted_response = response.replace("{author}", message.author.mention)
            await send_typing_message(message.channel, formatted_response)
            break

    await bot.process_commands(message)

async def send_typing_message(channel, message):
    async with channel.typing():
        await asyncio.sleep(2)
        await channel.send(message)

@bot.command(name='kratos')
async def ajuda(ctx):
    responses = [
        f"{ctx.author.mention}. Sou o deus da guerra.",
        f"O que foi garoto, {ctx.author.mention}.",
        f"Sou Kratos deus da guerra, {ctx.author.mention}.",
    ]
    await send_typing_message(ctx.channel, random.choice(responses))

@tasks.loop(minutes=60)
async def daily_greetings():
    now = datetime.now(timezone)
    channel_id = int(os.getenv("ID_CHANNEL"))
    channel = bot.get_channel(channel_id)

    if now.hour == 6:
        await channel.send("Bom dia!")
    elif now.hour == 12:
        await channel.send("Boa tarde!")
    elif now.hour == 16:
        await channel.send("Boa tarde!")
    elif now.hour == 18:
        await channel.send("Boa noite!")


@daily_greetings.before_loop
async def before_daily_greetings():
    await bot.wait_until_ready()


bot.run(TOKEN)