"""
# new_alert.py v 1.0
# Written by WildPasta
# Purpose: get update on HFR ads containing the keyword
"""

import discord
import os
import sqlite3
import sys

from dotenv import load_dotenv

import bot_hfr_scrap

database = "hardware.db"

def sql_additem(item_type, item_name, item_url):
    dbSocket = sqlite3.connect(database)
    cursor = dbSocket.cursor()

    req = "INSERT INTO items (item_type, item_name, item_url) VALUES (?, ?, ?)"
    data = (item_type, item_name, item_url)
    cursor.execute(req, data)
    dbSocket.commit()
    cursor.close()

def is_url_in_database(url):
    """
    Vérifie si l'URL est déjà présente dans la base de données
    """
    dbSocket = sqlite3.connect(database)
    cursor = dbSocket.cursor()

    req = "SELECT COUNT(*) FROM items WHERE item_url = ?"
    cursor.execute(req, (url,))
    count = cursor.fetchone()[0]

    cursor.close()

    return count > 0

def retrieve_new_ads(ads):
    new_ads = []
    for url, title in ads.items():
        if not is_url_in_database(url):
            new_ads.append((title, url))
    return new_ads

async def send_message(client, message):
    embed = discord.Embed(
        title="Nouvelles annonces de serveurs HFR",
        description=message,
        color=discord.Color.green()
    )
    channel = client.get_channel(1052934887100915763)
    await channel.send(embed=embed)

def main():
    load_dotenv()
    DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
    
    intents = discord.Intents.all()
    client = discord.Client(intents=intents)

    @client.event
    async def on_ready():
        keyword = "serveur"
        deep = 10
        ads = bot_hfr_scrap.get_ads(deep, keyword)
        new_ads = retrieve_new_ads(ads)
        if not new_ads:
            message="**Aucune nouvelle annonce !**"
            channel = client.get_channel(1052934887100915763)
            await channel.send(message)
        else:
            message = ""
            for title, url in new_ads:
                message += f"{title} ({url})\n"
                sql_additem("serveur", title, url)

            await send_message(client, message)

        await client.close()

    client.run(DISCORD_TOKEN)

if __name__ == "__main__":
    sys.exit(main())
