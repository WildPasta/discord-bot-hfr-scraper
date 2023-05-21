"""
# hfr_scraper.py v 1.1
# Written by WildPasta
# Purpose: web scraper to retrieve hardware available on HFR website
"""

# Imports
import discord
import os
import requests
import sys

from bs4 import BeautifulSoup
from dotenv import load_dotenv
from discord.ext import commands
from discord.ext.commands import cooldown, BucketType

def get_ads(deep, keyword):
    """
    Retrieve all ads topics on HFR containing the keyword
    Deep is the number of pages scraped
    Keyword is the keyword to search for in the ads titles
    """

    # Empty dictionary containing the URL as key and title as value
    ads_dict = {}

    # Scrap the number of pages given in arg
    for i in range(0, deep, 1):
        url = f"https://forum.hardware.fr/hfr/AchatsVentes/Hardware/liste_sujet-{i}.htm"
        response = requests.get(url)

        # Parse HTML using BeautifulSoup
        soup = BeautifulSoup(response.content, 'html.parser')

        # Retrieve the title and URL of the ads in the specified column
        ads = soup.find_all("td", {"class": "sujetCase3"})

        # Iterate through all of the ads
        for ad in ads:
            # Find the cCatTopic element within the current ad
            cCatTopic = ad.find("a", {"class": "cCatTopic"})

            # Check if the cCatTopic element exists and its text contains the keyword
            if cCatTopic and keyword.lower() in cCatTopic.text.lower() and "vds" in cCatTopic.text.lower():
                url = "https://forum.hardware.fr" + cCatTopic["href"]
                # Check if the URL is unique in our dictionary
                if url not in ads_dict:
                    ads_dict[url] = cCatTopic.text

    return ads_dict

def main():
    # Load the environment variables
    load_dotenv()
    DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')

    # Deep variable for the scraper
    deep = 5

    # Load the Discord intents
    intents = discord.Intents.all()
    client = discord.Client(intents=intents)
    bot = commands.Bot(command_prefix='!', intents=intents, help_command=None)

    # Print a message when bot is ready
    @bot.event
    async def on_ready():
        print(f'The Discord_Bot is now ready!')   
    
    @bot.event
    async def on_command_error(ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            em = discord.Embed(title=f"Wait a second!",description=f"Réessaye dans {error.retry_after:.2f}s.")
            await ctx.send(embed=em, delete_after=10.0)

    @bot.command(name="search")
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def search(ctx, *keywords):
        search_query = " ".join(keywords)
        ads_dict = get_ads(deep, search_query)
        
        # Check if no ad is found
        if len(ads_dict) == 0:
            await ctx.send(f"No ad found containing the keyword '{search_query}'...")
        else:
            embed = discord.Embed(title=f"Search results for '{search_query}':", color=discord.Color.blue())

            count = 0
            for url, title in ads_dict.items():
                # Add the title and URL to the embed
                embed.add_field(name=title, value=url, inline=False)

                count += 1
                if count >= 10:
                    break

            await ctx.send(embed=embed)

    bot.run(DISCORD_TOKEN)

if __name__ == "__main__":
    sys.exit(main())
