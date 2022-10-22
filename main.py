from repo import get_data

import os
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
    embed = discord.Embed(title=data[1], description=to_markdown(data[2]))
    await ctx.send(embed=embed)

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