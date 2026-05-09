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


class EdisonBot(commands.Bot):
    async def setup_hook(self):
        database.init_db()
        for ext in ["cogs.help_command", "cogs.inventions"]:
            try:
                await self.load_extension(ext)
                print(f"[Edison] Loaded {ext}")
            except Exception as e:
                print(f"[Edison] ERROR loading {ext}: {e}")


bot = EdisonBot(
    command_prefix=["edison ", "edison", "Edison ", "Edison"],
    intents=intents,
    help_command=None,
)


@bot.event
async def on_ready():
    print(f"[Edison] Online as {bot.user} (ID: {bot.user.id})")
    print(f"[Edison] Prefix: edison  | Satellite 03 — Thinker")


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
