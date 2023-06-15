"""
# new_alert.py v 1.0
# Written by WildPasta
# Purpose: get update on HFR ads containing the keyword
"""

# Python standard libraries
import os
import sys

# Third-party libraries
import discord 
from dotenv import load_dotenv  
import sqlite3

# Local modules
import bot_hfr_scraper

database = "hardware.db"

def sql_additem(item_type: str, item_name: str, item_url: str) -> None:
    """
    Add an item to the database.
    item_type: Type of the item.
    item_name: Name of the item.
    item_url: URL of the item.
    """

    dbSocket = sqlite3.connect(database)
    cursor = dbSocket.cursor()

    req = "INSERT INTO items (item_type, item_name, item_url) VALUES (?, ?, ?)"
    data = (item_type, item_name, item_url)
    cursor.execute(req, data)
    dbSocket.commit()
    cursor.close()

def is_url_in_database(url: str) -> bool:
    """
    Check if the URL is already present in the database.
    url: URL to check.
    Returns: True if the URL is in the database, False otherwise.
    """

    dbSocket = sqlite3.connect(database)
    cursor = dbSocket.cursor()

    req = "SELECT COUNT(*) FROM items WHERE item_url = ?"
    cursor.execute(req, (url,))
    count = cursor.fetchone()[0]

    cursor.close()

    return count > 0

def retrieve_new_ads(ads: dict) -> list:
    """
    Retrieve new ads by comparing with the database.
    ads: Dictionary of ads {url: title}.
    Returns: List of new ads [(title, url)].
    """

    new_ads = []
    for url, title in ads.items():
        if not is_url_in_database(url):
            new_ads.append((title, url))
    return new_ads

async def send_message(client: discord.Client, message: str, ALERT_CHANNEL: str) -> None:
    """
    Send a message to the alert channel.
    client: Discord client object.
    message: Message to send.
    """

    embed = discord.Embed(
        title="Nouvelles annonces de serveurs HFR",
        description=message,
        color=discord.Color.green()
    )
    channel = client.get_channel(ALERT_CHANNEL)
    await channel.send(embed=embed)

def main():
    try:
        load_dotenv()
        DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
        ALERT_CHANNEL = int(os.getenv('ALERT_CHANNEL'))
        KEYWORD = os.getenv('KEYWORD')
        DEEP = int(os.getenv('DEEP', '5'))
        if DEEP > 20:
            DEEP = 20
        
        if not DISCORD_TOKEN:
            raise ValueError("DISCORD_TOKEN environment variable is not set.")
        
        if not ALERT_CHANNEL:
            raise ValueError("ALERT_CHANNEL environment variable is not set.")
        
        if not KEYWORD:
            raise ValueError("KEYWORD environment variable is not set.")
        
        intents = discord.Intents.all()
        client = discord.Client(intents=intents)

        @client.event
        async def on_ready():
            ads = bot_hfr_scraper.get_ads(DEEP, KEYWORD)
            new_ads = retrieve_new_ads(ads)
            if not new_ads:
                message="**Aucune nouvelle annonce !**"
                channel = client.get_channel(ALERT_CHANNEL)
                await channel.send(message)
            else:
                message = ""
                for title, url in new_ads:
                    message += f"{title} ({url})\n"
                    sql_additem("serveur", title, url)

                await send_message(client, message, ALERT_CHANNEL)

            await client.close()

        client.run(DISCORD_TOKEN)
    except Exception as e:
        print(f"An error occurred in the main function: {e}")
        return 1
    
if __name__ == "__main__":
    sys.exit(main())
