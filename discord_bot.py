import os
import discord
from discord.ext import commands
from dotenv import load_dotenv
from gpt_bot import get_legends, get_weapons, get_other
from embed_patch_notes import rag_system
import asyncio

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

PROGRESS_FRAMES = [
    "▱▱▱▱▱▱▱▱▱▱",
    "▰▱▱▱▱▱▱▱▱▱",
    "▰▰▱▱▱▱▱▱▱▱",
    "▰▰▰▱▱▱▱▱▱▱",
    "▰▰▰▰▱▱▱▱▱▱",
    "▰▰▰▰▰▱▱▱▱▱",
    "▰▰▰▰▰▰▱▱▱▱",
    "▰▰▰▰▰▰▰▱▱▱",
    "▰▰▰▰▰▰▰▰▱▱",
    "▰▰▰▰▰▰▰▰▰▱",
    "▰▰▰▰▰▰▰▰▰▰",
]

async def animate_progress(message, stop_event):
    i = 0
    while not stop_event.is_set():
        frame = PROGRESS_FRAMES[i % len(PROGRESS_FRAMES)]
        try:
            await message.edit(content=f"Processing... `{frame}`")
        except discord.HTTPException:
            pass
        i += 1
        await asyncio.sleep(0.6)

@bot.command(name="legends")
async def legends(ctx):
    progress = await ctx.send("Processing... `▱▱▱▱▱▱▱▱▱▱`")
    stop_event = asyncio.Event()
    
    task = asyncio.create_task(animate_progress(progress, stop_event))
    
    try:
        loop = asyncio.get_running_loop()
        response = await loop.run_in_executor(None, get_legends)
        stop_event.set()
        await task
        
        await progress.edit(content=f"**Legend Changes**\n\n{response}")
    except Exception as e:
        stop_event.set()
        await task
        await progress.edit(content=f"Error: {str(e)}")

@bot.command(name="weapons")
async def weapons(ctx):
    progress = await ctx.send("Processing... `▱▱▱▱▱▱▱▱▱▱`")
    stop_event = asyncio.Event()
    
    task = asyncio.create_task(animate_progress(progress, stop_event))
    
    try:
        loop = asyncio.get_running_loop()
        response = await loop.run_in_executor(None, get_weapons)
        stop_event.set()
        await task
        
        await progress.edit(content=f"**Weapon Changes**\n\n{response}")
    except Exception as e:
        stop_event.set()
        await task
        await progress.edit(content=f"Error: {str(e)}")

@bot.command(name="other")
async def other(ctx):
    progress = await ctx.send("Processing... `▱▱▱▱▱▱▱▱▱▱`")
    stop_event = asyncio.Event()
    
    task = asyncio.create_task(animate_progress(progress, stop_event))
    
    try:
        loop = asyncio.get_running_loop()
        response = await loop.run_in_executor(None, get_other)
        stop_event.set()
        await task
        
        await progress.edit(content=f"**Map & Gamemode Changes**\n\n{response}")
    except Exception as e:
        stop_event.set()
        await task
        await progress.edit(content=f"Error: {str(e)}")

@bot.command(name="ask")
async def ask(ctx, *, question: str):
    if not question.strip():
        await ctx.send("Please provide a question to ask about the patch notes.")
        return
    
    progress = await ctx.send("Processing... `▱▱▱▱▱▱▱▱▱▱`")
    stop_event = asyncio.Event()
    
    task = asyncio.create_task(animate_progress(progress, stop_event))
    
    try:
        loop = asyncio.get_running_loop()
        response = await loop.run_in_executor(None, rag_system.query, question)
        stop_event.set()
        await task
        
        await progress.edit(content=f"**Q: {question}**\n\n{response}")
    except Exception as e:
        stop_event.set()
        await task
        await progress.edit(content=f"Error: {str(e)}")

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")
    print("Apex Legends Meta Bot is ready!")
    print("Available commands: !legends, !weapons, !other, !ask")

bot.run(TOKEN)
