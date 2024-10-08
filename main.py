from repo import get_data

import os
import asyncio
import markdownify
import discord
from discord.ext import commands
import yatg
import re

from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

intents = discord.Intents.all()

bot = commands.Bot(
    command_prefix=[";;"],
    intents=intents,
    help_command=None
    )

def table_converter(html: str) -> str:
    tables = re.findall(r'<table.*>.*</table>', html)
    if len(tables) == 0:
        return html
    
    for table in tables:
        ascii_table = yatg.html_2_ascii_table(html_content=table, output_style="orgmode")
        html = html.replace(table, "```" + ascii_table + "```")
    return html


def to_markdown(html: str) -> str:
    html = table_converter(html)
    html = html.replace("<span", "\t|\t<span")
    md = markdownify.markdownify(html=html)
    return md


async def search_data(ctx, search, table):
    data = get_data(table, search)
    if len(data) == 0:
        await ctx.send("Not found.")
        return
    elif len(data) == 1:
        title = data[0][1]
        description = to_markdown(data[0][2])
        source = description.split("Published in ")[-1]
        description = description.split("Published in ")[0]
        if len(description) > 2000:
            description = description[:2000] + "... (too long)"
        url = "https://www.dyasdesigns.com/dnd4e/?view={}".format(data[0][3])
        embed = discord.Embed(title=title, url=url, description=description)
        embed.set_footer(text=source)
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
            return (
                message.content.isnumeric() or message.content == "c"
            ) and message.author == ctx.message.author

        description = """Do you mean?\n{}""".format(list)
        embed = discord.Embed(title="Multiple Found", description=description)
        embed.set_footer(text="Type 1-10 to choose, or c to cancel.")
        option_message = await ctx.send(embed=embed)
        try:
            followup_message = await bot.wait_for(
                "message", timeout=60.0, check=followup
            )
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
            source = description.split("Published in ")[-1]
            description = description.split("Published in ")[0]
            if len(description) > 2000:
                description = description[:2000] + "\n\n... (too long)"
            url = "https://www.dyasdesigns.com/dnd4e/?view={}".format(data[3])
            embed = discord.Embed(title=title, url=url, description=description)
            embed.set_footer(text=source)
            await option_message.delete()
            await followup_message.delete()
            await ctx.send(embed=embed)
            return


@bot.command()
async def help(ctx):
    embed = discord.Embed(title="Help")
    embed.description = "`;;<command> <searched text>` - search for <command> with <searched text>\n"
    embed.add_field(name="List of Commands", value="`power`, `item`, `feat`, `poison`, `ritual`, `weapon`, \
                    `theme`, `disease`, `glossary`, `implement`, `trap`, `race`, `class`, `deity`, `background`, \
                    `monster`, `companion`, `paragonpath`, `epicdestiny`, `armor`")
    await ctx.send(embed=embed)


@bot.command(name="power")
async def power_search(ctx, *, search):
    await search_data(ctx, search, "power")


@bot.command(name="item")
async def item_search(ctx, *, search):
    await search_data(ctx, search, "item")


@bot.command(name="feat")
async def feat_search(ctx, *, search):
    await search_data(ctx, search, "feat")


@bot.command(name="poison")
async def poison_search(ctx, *, search):
    await search_data(ctx, search, "poison")


@bot.command(name="ritual")
async def ritual_search(ctx, *, search):
    await search_data(ctx, search, "ritual")


@bot.command(name="weapon")
async def weapon_search(ctx, *, search):
    await search_data(ctx, search, "weapon")


@bot.command(name="theme")
async def theme_search(ctx, *, search):
    await search_data(ctx, search, "theme")


@bot.command(name="disease")
async def disease_search(ctx, *, search):
    await search_data(ctx, search, "disease")


@bot.command(name="glossary")
async def glossary_search(ctx, *, search):
    await search_data(ctx, search, "glossary")


@bot.command(name="implement")
async def implement_search(ctx, *, search):
    await search_data(ctx, search, "implement")


@bot.command(name="armor")
async def armor_search(ctx, *, search):
    await search_data(ctx, search, "armor")


@bot.command(name="companion")
async def companion_search(ctx, *, search):
    await search_data(ctx, search, "companion")


@bot.command(name="trap")
async def trap_search(ctx, *, search):
    await search_data(ctx, search, "trap")


@bot.command(name="deity")
async def deity_search(ctx, *, search):
    await search_data(ctx, search, "deity")


@bot.command(name="background")
async def background_search(ctx, *, search):
    await search_data(ctx, search, "background")


@bot.command(name="epicdestiny")
async def epicdestiny_search(ctx, *, search):
    await search_data(ctx, search, "epicdestiny")


@bot.command(name="class")
async def class_search(ctx, *, search):
    await search_data(ctx, search, "class")


@bot.command(name="monster")
async def monster_search(ctx, *, search):
    await search_data(ctx, search, "monster")


@bot.command(name="paragonpath")
async def paragonpath_search(ctx, *, search):
    await search_data(ctx, search, "paragonpath")


@bot.command(name="race")
async def race_search(ctx, *, search):
    await search_data(ctx, search, "race")


bot.run(TOKEN)
