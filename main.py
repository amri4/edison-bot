import os
import random
import discord
from discord.ext import commands
from dotenv import load_dotenv
import database

load_dotenv()

SIBLING_NAMES = ["Shaka", "Lilith", "Pythagoras", "Atlas", "York"]

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix=["edison ", "edison", "Edison ", "Edison"], intents=intents, help_command=None)


@bot.event
async def on_ready():
    database.init_db()
    await bot.load_extension("cogs.help_command")
    await bot.load_extension("cogs.inventions")
    print(f"[Edison] Online as {bot.user} (ID: {bot.user.id})")
    print(f"[Edison] Prefix: edison | Satellite 03 — Thinker")


@bot.event
async def on_message(message):
    if message.author.bot:
        return

    content_lower = message.content.lower()
    for name in SIBLING_NAMES:
        if name.lower() in content_lower:
            responses = [
                f"Oh! {name} just sparked a new idea in me! What if they collaborated on an invention?!",
                f"{name}! Hearing that name gives me energy! So much potential!",
                f"Mentioning {name} reminds me — I had a breakthrough idea inspired by their work!",
            ]
            await message.channel.send(random.choice(responses))
            break

    await bot.process_commands(message)


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        return
    raise error


if __name__ == "__main__":
    token = os.getenv("DISCORD_TOKEN")
    if not token:
        raise RuntimeError("DISCORD_TOKEN not set in .env")
    bot.run(token)
