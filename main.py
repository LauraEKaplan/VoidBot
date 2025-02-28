# from threading import Thread
import discord
import os
from discord.ext import commands

import psutil   #for mem monitoring
import asyncio  #for mem monitoring
import signal   #for graceful shutdown

#--------ESTABLISH BOT ACCESS--------#
#load bot token via environment variables
TOKEN = os.getenv("DISCORD_BOT_TOKEN")
#confirm token exists
if not TOKEN:
    raise ValueError("Bot token is missing! Please add it in a secure fashion.")
#set bot's required intents
intents = discord.Intents.default()
intents.message_content = True  #permit message reading
bot = commands.Bot(command_prefix="!", intents=intents)

#--------SHUTDOWN BEHAVIOR--------#
async def shutdown():
    print("VoidBot shutting down gracefully...")
    await bot.close()
def handle_shutdown(signum, frame):
    asyncio.create_task(shutdown()) 
    
#catch termination signals before running bot
signal.signal(signal.SIGINT, handle_shutdown)
signal.signal(signal.SIGTERM, handle_shutdown)

#--------MEMORY MONITORING--------#
async def monitor_memory():
    while True:
        mem_usage = psutil.virtual_memory().percent
        if mem_usage > 80:  #restart if mem usage >80%
            print(f"High memory usage detected ({mem_usage}%), restarting bot...")
            await bot.close()  #graceful shutdown
        await asyncio.sleep(60)  #check mem every 60sec
        
@bot.event
async def on_ready():
    print(f'Void_Bot is online! Logged in as {bot.user}')
    bot.loop.create_task(monitor_memory()) #start memory monitoring

@bot.event
async def on_message(message):
    if message.author.bot:
        return  #ignore bot messages

    if message.channel.name == "scream-into-the-void":
        user = message.author.name
        word_count = len(message.content.split())

        await message.delete()
        if word_count == 1:
            await message.channel.send(
                f"{user} has screamed {word_count} word into the void."
            )
        else:
            await message.channel.send(
                f"{user} has screamed {word_count} words into the void."
            )

#--------RUN BOT--------#
bot.run(TOKEN)
