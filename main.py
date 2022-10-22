from repo import get_data

import os
import re
import asyncio
import markdownify
import discord
from discord.ext import commands

from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

intents = discord.Intents.all()

bot = commands.Bot(command_prefix=[';;'], intents=intents)

def to_markdown(html: str) -> str:
    html = html.replace("<span", "\t|\t<span")
    md = markdownify.markdownify(html=html)
    return md

async def search_data(ctx, search, table):
    data = get_data(table, search)
    if len(data) == 0 :
        await ctx.send("Not found.")
        return
    elif len(data) == 1:
        title = data[0][1]
        description = to_markdown(data[0][2])
        embed = discord.Embed(title=title, description=description)
        await ctx.send(embed=embed)
        return
    else:
        idx = 1
        list = ""
        map = {}
        for x in data:
            map_key = "{}".format(idx)
            map[map_key] = x
            list = list + "`{0}. {1}`\n".format(idx, x[1])
            idx += 1
        def followup(message):
            return (message.content.isnumeric() or message.content == "c") and message.author == ctx.message.author
        description = """Do you mean?\n{}""".format(list)
        embed = discord.Embed(title="Multiple Found", description=description)
        embed.set_footer(text="Type 1-10 to choose, or c to cancel.")
        option_message = await ctx.send(embed=embed)
        try:
            followup_message = await bot.wait_for("message",timeout=60.0 ,check=followup)
        except asyncio.TimeoutError:
            await option_message.delete()
            await ctx.send("Time Out")
        else:
            if followup_message.content == "c":
                await option_message.delete()
                await followup_message.delete()
                return
            data = map[followup_message.content]
            title = data[1]
            description = to_markdown(data[2])
            embed = discord.Embed(title=title, description=description)
            await option_message.delete()
            await followup_message.delete()
            await ctx.send(embed=embed)
            return
        

@bot.command(name='power')
async def power_search(ctx, *, search):
    await search_data(ctx, search, "power")

@bot.command(name='item')
async def power_search(ctx, *, search):
    await search_data(ctx, search, "item")

@bot.command(name='feat')
async def power_search(ctx, *, search):
    await search_data(ctx, search, "feat")

@bot.command(name='poison')
async def power_search(ctx, *, search):
    await search_data(ctx, search, "poison")

@bot.command(name='ritual')
async def power_search(ctx, *, search):
    await search_data(ctx, search, "ritual")

@bot.command(name='weapon')
async def power_search(ctx, *, search):
    await search_data(ctx, search, "weapon")

@bot.command(name='theme')
async def power_search(ctx, *, search):
    await search_data(ctx, search, "theme")

@bot.command(name='disease')
async def power_search(ctx, *, search):
    await search_data(ctx, search, "disease")

@bot.command(name='glossary')
async def power_search(ctx, *, search):
    await search_data(ctx, search, "glossary")

bot.run(TOKEN)