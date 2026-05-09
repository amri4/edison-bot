import random
import discord
from discord.ext import commands
import database

EUREKA_IDEAS = [
    "A submarine that runs on laughter! The more the crew laughs, the faster it goes!",
    "Boots that let you walk on clouds — literally! Clouds! We could harvest rain too!",
    "A machine that translates animal sounds into human speech! Imagine what the Sea Kings are saying!",
    "Self-repairing sails made from spider silk and Sea Prism Stone weave!",
    "An alarm clock that only rings when you've had exactly the right amount of sleep!",
    "Edible packaging for all food supplies — zero waste AND delicious!",
    "A compass that points toward the nearest person who needs help! Revolutionary!",
    "Ink made from bioluminescent fish — write in the dark without a lantern!",
    "A ship hull coated in sharkskin texture to reduce drag by 40%!",
    "Goggles that let you see underwater currents and weather patterns simultaneously!",
]

RATINGS = [
    ("GENIUS!", "This is exactly the kind of idea that changes the world!"),
    ("BRILLIANT!", "Minor refinements needed but the core concept is extraordinary!"),
    ("Promising!", "It needs work, but the spark is there. Keep developing it!"),
    ("Interesting...", "I can see the vision. It needs more research before we proceed."),
    ("Needs work.", "The idea has merit, but the execution will be very difficult."),
    ("Rejected.", "I appreciate the submission but this one is not viable. Try again!"),
]

SIBLINGS = [
    ("Shaka", "01", "Good", "shaka"),
    ("Lilith", "02", "Evil", "lilith"),
    ("Edison", "03", "Thinker", "edison"),
    ("Pythagoras", "04", "Wisdom", "py"),
    ("Atlas", "05", "Violence", "atlas"),
    ("York", "06", "Greed", "york"),
]


class InventionsCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="idea")
    async def idea(self, ctx, *, content: str):
        idea_id = database.add_idea(ctx.guild.id, ctx.author.id, content)
        embed = discord.Embed(
            title="💡 Idea Submitted to Edison's Lab!",
            description=f"*\"{content}\"*",
            color=discord.Color.gold(),
        )
        embed.add_field(name="Idea ID", value=f"#{idea_id}", inline=True)
        embed.add_field(name="Submitted by", value=ctx.author.mention, inline=True)
        embed.set_footer(text="Pending review by Edison | Satellite 03")
        await ctx.send(embed=embed)

    @commands.command(name="ideas")
    async def ideas(self, ctx):
        rows = database.get_ideas(ctx.guild.id)
        if not rows:
            await ctx.send("No ideas submitted yet! Use `edison idea <your idea>` to submit one!")
            return
        embed = discord.Embed(
            title="💡 Recent Ideas — Edison's Lab",
            color=discord.Color.gold(),
        )
        for row in rows:
            idea_id, author_id, content, rating, timestamp = row
            rating_text = f"Rating: **{rating}**" if rating else "Rating: *pending*"
            embed.add_field(
                name=f"#{idea_id} — by <@{author_id}>",
                value=f"{content}\n{rating_text}",
                inline=False,
            )
        embed.set_footer(text="Satellite 03 — Edison (Thinker)")
        await ctx.send(embed=embed)

    @commands.command(name="rate")
    async def rate(self, ctx, idea_id: int):
        rows = database.get_ideas(ctx.guild.id, limit=9999)
        idea = next((r for r in rows if r[0] == idea_id), None)
        if not idea:
            await ctx.send(f"No idea found with ID `#{idea_id}` in this server.")
            return
        rating_label, rating_desc = random.choice(RATINGS)
        database.rate_idea(idea_id, rating_label)
        embed = discord.Embed(
            title=f"💡 Edison's Verdict on Idea #{idea_id}",
            color=discord.Color.gold(),
        )
        embed.add_field(name="Idea", value=idea[2], inline=False)
        embed.add_field(name="Rating", value=f"**{rating_label}**", inline=True)
        embed.add_field(name="Edison's Note", value=rating_desc, inline=False)
        embed.set_footer(text="Satellite 03 — Edison (Thinker)")
        await ctx.send(embed=embed)

    @commands.command(name="eureka")
    async def eureka(self, ctx):
        idea = random.choice(EUREKA_IDEAS)
        embed = discord.Embed(
            title="💡 EUREKA! Edison has a breakthrough!",
            description=f"*\"{idea}\"*",
            color=discord.Color.gold(),
        )
        embed.set_footer(text="Satellite 03 — Edison (Thinker) | A flash of inspiration!")
        await ctx.send(embed=embed)

    @commands.command(name="experiment")
    async def experiment(self, ctx, *, name: str):
        exp_id = database.add_experiment(ctx.guild.id, ctx.author.id, name)
        embed = discord.Embed(
            title="🔬 New Experiment Started!",
            description=f"**{name}**",
            color=discord.Color.gold(),
        )
        embed.add_field(name="Experiment ID", value=f"#{exp_id}", inline=True)
        embed.add_field(name="Status", value="Ongoing", inline=True)
        embed.add_field(name="Lead Researcher", value=ctx.author.mention, inline=True)
        embed.set_footer(text="Satellite 03 — Edison (Thinker)")
        await ctx.send(embed=embed)

    @commands.command(name="experiments")
    async def experiments(self, ctx):
        rows = database.get_experiments(ctx.guild.id)
        if not rows:
            await ctx.send("No experiments running! Start one with `edison experiment <name>`.")
            return
        embed = discord.Embed(
            title="🔬 Active Experiments — Edison's Lab",
            color=discord.Color.gold(),
        )
        for row in rows:
            exp_id, author_id, name, status, timestamp = row
            embed.add_field(
                name=f"#{exp_id} — {name}",
                value=f"Status: **{status.capitalize()}** | By: <@{author_id}> | Started: {timestamp[:10]}",
                inline=False,
            )
        embed.set_footer(text="Satellite 03 — Edison (Thinker)")
        await ctx.send(embed=embed)

    @commands.command(name="complete")
    async def complete(self, ctx, exp_id: int):
        database.complete_experiment(exp_id)
        embed = discord.Embed(
            title=f"✅ Experiment #{exp_id} Complete!",
            description="Outstanding work! Another success for the lab!",
            color=discord.Color.gold(),
        )
        embed.set_footer(text="Satellite 03 — Edison (Thinker)")
        await ctx.send(embed=embed)

    @commands.command(name="siblings")
    async def siblings(self, ctx):
        embed = discord.Embed(
            title="🤖 The Six Vegapunk Satellites",
            description="Oh! My siblings! We're all brilliant in our own ways! Well, mostly.",
            color=discord.Color.gold(),
        )
        for name, number, trait, prefix in SIBLINGS:
            marker = " ← you are here" if name == "Edison" else ""
            embed.add_field(
                name=f"Satellite {number} — {name} ({trait}){marker}",
                value=f"Prefix: `{prefix}`",
                inline=False,
            )
        await ctx.send(embed=embed)

    @idea.error
    async def idea_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("Usage: `edison idea <your idea>`")

    @experiment.error
    async def experiment_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("Usage: `edison experiment <name>`")

    @rate.error
    async def rate_error(self, ctx, error):
        if isinstance(error, (commands.MissingRequiredArgument, commands.BadArgument)):
            await ctx.send("Usage: `edison rate <idea id>`")

    @complete.error
    async def complete_error(self, ctx, error):
        if isinstance(error, (commands.MissingRequiredArgument, commands.BadArgument)):
            await ctx.send("Usage: `edison complete <experiment id>`")


async def setup(bot):
    await bot.add_cog(InventionsCog(bot))
