"""
# hfr_scraper.py v 1.1
# Written by WildPasta
# Purpose: web scraper to retrieve hardware available on HFR website
"""

# Python standard libraries
import os
import requests
from requests.exceptions import RequestException
import sys

# Third-party libraries
from bs4 import BeautifulSoup
from dotenv import load_dotenv
import discord
from discord.ext import commands

def get_ads(deep: int, keyword: str) -> dict:
    """
    Retrieve all ads topics on HFR containing the keyword
    deep: The number of pages to scrape
    keyword: The keyword to search for in the ads titles
    Returns: A dictionary containing the ads URLs and titles
    """

    ads_dict = {}

    # Scrap the number of pages given in arg
    for i in range(deep):
        url = f"https://forum.hardware.fr/hfr/AchatsVentes/Hardware/liste_sujet-{i}.htm"
        try:
            response = requests.get(url)
            response.raise_for_status()
        except RequestException as e:
            print(f"Error occurred while making the request: {e}")
            continue

        try:
            # Parse HTML
            soup = BeautifulSoup(response.content, 'html.parser')

            # Retrieve the title and URL of the ads
            ads = soup.find_all("td", {"class": "sujetCase3"})

            # Iterate through all of the ads
            for ad in ads:
                # Find the cCatTopic element within the current ad
                cCatTopic = ad.find("a", {"class": "cCatTopic"})

                # Check if the cCatTopic element exists and its text contains the keyword
                if cCatTopic and keyword.lower() in cCatTopic.text.lower():
                    url = "https://forum.hardware.fr" + cCatTopic["href"]
                    # Check if the URL is unique in our dictionary
                    if url not in ads_dict:
                        ads_dict[url] = cCatTopic.text
        except Exception as e:
            print(f"Error occurred while parsing the HTML: {e}")
            continue

    return ads_dict

def main() -> None:
    try:
        # Load the environment variables
        load_dotenv()
        DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
        if DISCORD_TOKEN is None:
            raise ValueError("DISCORD_TOKEN environment variable is not set.")
        
        DEEP = int(os.getenv('DEEP', '5'))
        if DEEP > 20:
            DEEP = 20

        # Load the Discord intents
        intents = discord.Intents.all()
        bot = commands.Bot(command_prefix='!', intents=intents, help_command=None)

        # Print a message when bot is ready
        @bot.event
        async def on_ready():
            print(f'The Discord_Bot is now ready!')
        
        # Print a retry message
        @bot.event
        async def on_command_error(ctx, error):
            if isinstance(error, commands.CommandOnCooldown):
                em = discord.Embed(title=f"Wait a second!",description=f"Please retry in {error.retry_after:.2f}s.")
                await ctx.send(embed=em, delete_after=10.0)

        # Search command
        @bot.command(name="search")
        @commands.cooldown(1, 10, commands.BucketType.user)
        async def search(ctx, *keywords):
            search_query = " ".join(keywords)
            ads_dict = get_ads(DEEP, search_query)
            
            if not ads_dict:
                await ctx.send(f"No ad found containing the keyword '{search_query}'...")
            else:
                embed = discord.Embed(title=f"Search results for '{search_query}':", color=discord.Color.blue())
                count = 0
                for url, title in ads_dict.items():
                    embed.add_field(name=title, value=url, inline=False)
                    count += 1
                    if count >= 10:
                        break

                await ctx.send(embed=embed)

        bot.run(DISCORD_TOKEN)
    except Exception as e:
        print(f"An error occurred in the main function: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(main())
