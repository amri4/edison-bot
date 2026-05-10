import random
import discord
from discord.ext import commands
import shared_db

SUGGESTIONS = [
    "Allocate more server resources to encouraging daily berry claims — consistent engagement drives long-term retention.",
    "Users with York trust level 0 are the most disengaged. Target them with York feeding events to boost participation.",
    "Consider scheduling server events during peak hours based on when `atlas daily` is most frequently claimed.",
    "High warning counts correlate with lower berry activity. Address moderation issues to keep the economy healthy.",
    "The gap between top berry holders and the average is widening. A redistribution event via York feeding could rebalance.",
    "Pythagoras trivia participation is a strong predictor of server engagement. Promote it in announcement channels.",
    "York feeding frequency indicates emotional investment in the server. Focus growth efforts on users who feed York.",
    "Analyze which users have high trust but low berries — they are engaged but economically inactive. Target with bonuses.",
]

OPTIMIZATION_TIPS = [
    "Pin the York hunger alert channel so it's easily visible to all members.",
    "Set up a dedicated #economy channel for atlas commands to reduce channel clutter.",
    "Run weekly trivia nights in a dedicated channel to boost Pythagoras engagement scores.",
    "Use Lilith's warn system consistently — inconsistent moderation erodes server trust.",
    "Encourage users to claim daily berries every day; streaks could be a future feature to consider.",
    "Make sure all satellite bots share the same SHAKA_DB_PATH — data consistency is critical.",
]


class LogicCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="analyze")
    async def analyze(self, ctx):
        stats = shared_db.get_server_stats(ctx.guild.id)
        lb = shared_db.get_leaderboard(ctx.guild.id, by="berries", limit=1)
        top_berries = lb[0][1] if lb else 0
        avg = stats["total_berries"] / stats["total_users"] if stats["total_users"] else 0

        embed = discord.Embed(
            title="🧠 Edison — Server Analysis",
            description="*Analyzing Punk Records data...*",
            color=discord.Color.gold(),
        )
        embed.add_field(name="Registered Users", value=str(stats["total_users"]), inline=True)
        embed.add_field(name="Total Berries", value=f"{stats['total_berries']:,} 🍓", inline=True)
        embed.add_field(name="Avg. Berries/User", value=f"{avg:,.0f} 🍓", inline=True)
        embed.add_field(name="Top Balance", value=f"{top_berries:,} 🍓", inline=True)
        embed.add_field(name="York Feedings", value=str(stats["total_feeds"]), inline=True)
        embed.add_field(name="Total Warnings", value=str(stats["total_warnings"]), inline=True)
        embed.add_field(name="Avg. York Trust", value=str(stats["avg_trust"]), inline=True)

        if stats["total_users"] > 0:
            engagement = min(100, int((stats["total_feeds"] / stats["total_users"]) * 20))
            bar = "🟨" * (engagement // 10) + "⬛" * (10 - engagement // 10)
            embed.add_field(name="Engagement Index", value=f"`{bar}` {engagement}/100", inline=False)

        embed.set_footer(text="Satellite 03 — Edison (Analysis) | Data from SHAKA")
        await ctx.send(embed=embed)

    @commands.command(name="suggest")
    async def suggest(self, ctx):
        suggestion = random.choice(SUGGESTIONS)
        embed = discord.Embed(
            title="🧠 Edison — Strategic Suggestion",
            description=f"*\"{suggestion}\"*",
            color=discord.Color.gold(),
        )
        embed.set_footer(text="Satellite 03 — Edison | Thinking Unit")
        await ctx.send(embed=embed)

    @commands.command(name="report")
    async def report(self, ctx):
        stats = shared_db.get_server_stats(ctx.guild.id)
        lb_berries = shared_db.get_leaderboard(ctx.guild.id, by="berries", limit=3)
        lb_trust = shared_db.get_leaderboard(ctx.guild.id, by="trust", limit=3)
        trivia_lb = shared_db.get_trivia_leaderboard(ctx.guild.id, limit=3)

        embed = discord.Embed(
            title="🧠 Edison — Full System Report",
            description=f"**Server:** {ctx.guild.name}\n**Members:** {ctx.guild.member_count}",
            color=discord.Color.gold(),
        )

        if lb_berries:
            lines = [f"`{i+1}.` <@{uid}> — **{b:,}** 🍓" for i, (uid, b, _) in enumerate(lb_berries)]
            embed.add_field(name="Top Berry Holders", value="\n".join(lines), inline=True)

        if lb_trust:
            lines = [f"`{i+1}.` <@{uid}> — **{t}** 💜" for i, (uid, _, t) in enumerate(lb_trust)]
            embed.add_field(name="Most Trusted (York)", value="\n".join(lines), inline=True)

        if trivia_lb:
            lines = [f"`{i+1}.` <@{uid}> — **{s}** pts" for i, (uid, s) in enumerate(trivia_lb)]
            embed.add_field(name="Trivia Champions", value="\n".join(lines), inline=True)

        embed.add_field(name="Economy Summary", value=(
            f"Users: **{stats['total_users']}**\n"
            f"Berries in circulation: **{stats['total_berries']:,}** 🍓\n"
            f"York feedings: **{stats['total_feeds']}**\n"
            f"Total warnings: **{stats['total_warnings']}**"
        ), inline=False)

        tip = random.choice(OPTIMIZATION_TIPS)
        embed.add_field(name="💡 Edison's Tip", value=f"*{tip}*", inline=False)
        embed.set_footer(text="Satellite 03 — Edison | Full Report via SHAKA")
        await ctx.send(embed=embed)

    @commands.command(name="optimize")
    async def optimize(self, ctx):
        tip = random.choice(OPTIMIZATION_TIPS)
        embed = discord.Embed(
            title="🧠 Edison — Optimization Tip",
            description=f"*\"{tip}\"*",
            color=discord.Color.gold(),
        )
        embed.set_footer(text="Satellite 03 — Edison | Thinking Unit")
        await ctx.send(embed=embed)

    @commands.command(name="siblings")
    async def siblings(self, ctx):
        embed = discord.Embed(
            title="🤖 The Six Vegapunk Satellites",
            description="I've analyzed all sibling units. Here is the data:",
            color=discord.Color.gold(),
        )
        data = [
            ("Shaka", "01", "Central Brain / Database", "shaka"),
            ("Lilith", "02", "Moderation", "lilith"),
            ("Edison", "03", "Analysis & Strategy", "edison"),
            ("Pythagoras", "04", "Knowledge & Trivia", "py"),
            ("Atlas", "05", "Economy & Utility", "atlas"),
            ("York", "06", "Hunger & Trust", "york"),
        ]
        for name, num, role, prefix in data:
            marker = " ← you are here" if name == "Edison" else ""
            embed.add_field(name=f"Satellite {num} — {name}{marker}", value=f"Role: {role} | Prefix: `{prefix}`", inline=False)
        await ctx.send(embed=embed)


async def setup(bot):
    await bot.add_cog(LogicCog(bot))
