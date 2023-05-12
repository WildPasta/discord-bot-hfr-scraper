# Discord bot HFR scraper

This Discord bot has been developed to search and display ads from [hardware.fr](https://forum.hardware.fr/hfr/AchatsVentes/Hardware/liste_sujet-1.htm) website on a Discord server.

It uses web scraping to retrieve the ads and displays them in a user-friendly format.

An extra script is available to lookup for specific ads and send a notification on the Discord server when a new ad is found. It is recommended to use cron to run this script periodically.

## Features

- Search for ads from a specific website using keywords
- Display ads on the Discord server
- Store ads in a database to avoid duplicates (alert script only)

## Configuration

Before running the bot, make sure to complete the following steps:

1. Clone this repository to your server.
2. Install the required dependencies by running the following command:

```python
python pip install -r requirements.txt
```

3. Create a .env file in the root directory and add the following information:

```
DISCORD_TOKEN=<your_discord_token>
```

Replace `<your_discord_token>` with the access token of your Discord bot. You can obtain this token by creating a bot application on the [Discord Developer Portal](https://discord.com/developers/applications).

## Usage

To launch the Discord bot, run the following command on your server:

```python
python bot_hfr_scrap.py &
```

The bot will connect to Discord using the token provided in the `.env` file and will be ready to respond to commands.

## Discord Commands

The bot responds to the following commands:

- `!search` <keyword>: Search for ads containing the specified keyword

## Customize

You can customize the bot by editing the following variables in the `.py` files:

- deep: Number of pages to search for ads
- keywords (in new_alert.py): keywords to search for


