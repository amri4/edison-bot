import discord
from discord.ext import commands

COMMANDS_DATA = {
    "💡 Inventions": {
        "edison idea <your idea>": "Submit an idea to Edison's lab database!",
        "edison ideas": "Show the 5 most recent ideas submitted in this server.",
        "edison rate <id>": "Edison rates an idea from the database (random rating).",
        "edison eureka": "Edison has a random flash of inspiration!",
        "edison experiment <name>": "Start a new experiment and log it.",
        "edison experiments": "Show ongoing experiments in this server.",
        "edison complete <id>": "Mark an experiment as complete.",
        "edison siblings": "List all six Vegapunk satellites.",
    },
    "❓ Help": {
        "edison?": "Show this help menu.",
    },
}


class CategorySelect(discord.ui.Select):
    def __init__(self):
        options = [
            discord.SelectOption(label=category, description=f"{len(cmds)} command(s)")
            for category, cmds in COMMANDS_DATA.items()
        ]
        super().__init__(placeholder="Select a command category...", options=options)

    async def callback(self, interaction: discord.Interaction):
        category = self.values[0]
        cmds = COMMANDS_DATA[category]
        embed = discord.Embed(
            title=f"Edison — {category}",
            color=discord.Color.gold(),
        )
        for name, desc in cmds.items():
            embed.add_field(name=f"`{name}`", value=desc, inline=False)
        embed.set_footer(text="Satellite 03 — Edison (Thinker) | Prefix: edison")
        await interaction.response.edit_message(embed=embed)


class HelpView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=60)
        self.add_item(CategorySelect())


class HelpCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="?")
    async def help_command(self, ctx):
        embed = discord.Embed(
            title="💡 Edison — Satellite 03 (Thinker)",
            description=(
                "Oh! Oh! A new visitor! Great timing — I just had a breakthrough!\n"
                "Select a category to see what I can do!\n\n"
                "**Prefix:** `edison`"
            ),
            color=discord.Color.gold(),
        )
        embed.set_footer(text="Use the menu below to explore commands.")
        await ctx.send(embed=embed, view=HelpView())


async def setup(bot):
    await bot.add_cog(HelpCog(bot))
