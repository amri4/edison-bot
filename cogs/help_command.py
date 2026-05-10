import discord
from discord.ext import commands

COMMANDS_DATA = {
    "🧠 Analysis": {
        "edison analyze": "Analyze server stats from the SHAKA database.",
        "edison report": "Full system report: economy, trust, trivia, tips.",
        "edison suggest": "Get a strategic suggestion based on server data.",
        "edison optimize": "Get a server optimization tip.",
    },
    "🤖 Satellite Info": {
        "edison siblings": "List all six Vegapunk satellites and their roles.",
    },
    "❓ Help": {
        "edison help": "Show this help menu.",
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
            title=f"🧠 Edison — {category}",
            color=discord.Color.gold(),
        )
        for name, desc in cmds.items():
            embed.add_field(name=f"`{name}`", value=desc, inline=False)
        embed.set_footer(text="Satellite 03 — Edison (Thinker) | Analysis & Strategy | Prefix: edison")
        await interaction.response.edit_message(embed=embed)


class HelpView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=60)
        self.add_item(CategorySelect())


class HelpCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="help", aliases=["?"])
    async def help_command(self, ctx):
        embed = discord.Embed(
            title="🧠 EDISON — Satellite 03 (Thinker)",
            description=(
                "PUNK-03 // Edison — Thinking Unit of Dr. Vegapunk.\n"
                "Built for ideas, strategy, and problem solving.\n"
                "I analyze SHAKA's data to give you insights and suggestions.\n\n"
                "**Prefix:** `edison`"
            ),
            color=discord.Color.gold(),
        )
        embed.set_footer(text="Select a category below to view commands.")
        await ctx.send(embed=embed, view=HelpView())


async def setup(bot):
    await bot.add_cog(HelpCog(bot))
