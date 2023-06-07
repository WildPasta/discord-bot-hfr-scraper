# Discord bot HFR scraper

This Discord bot has been developed to search and display ads from [hardware.fr](https://forum.hardware.fr/hfr/AchatsVentes/Hardware/liste_sujet-1.htm) website on a Discord server.

It uses web scraping to retrieve the ads and displays them in a user-friendly format.

## Features

- Search for ads from a specific website using keywords
- Display ads on the Discord server
- Store ads in a database to avoid duplicates (alert script only)

An extra script (new_alert.py) is available to lookup for specific ads and send a notification on the Discord server when a new ad is found. **It is recommended to use cron to run this script periodically.**

## Installation (CLI)

1. Clone this repository to your server.

```bash
git clone https://github.com/WildPasta/discord_bot_hfr_scraper.git
```

2. Install the required dependencies by running the following command:

```python
python pip install -r requirements.txt
```

3. Create a .env file in the `bot` directory and add the following information:

```
DISCORD_TOKEN=<your_discord_token>
DEEP=<number_of_pages_to_search>
```

Replace `<your_discord_token>` with the access token of your Discord bot. 
You can obtain this token by creating a bot application on the [Discord Developer Portal](https://discord.com/developers/applications).

Replace `<number_of_pages_to_search>` with the number of pages you want the bot to search for ads. 
*Note: Default value is 5.*

## Usage (CLI)

To launch the Discord bot, run the following command within the `bot` directory:

```python
python bot_hfr_scrap.py &
```

The bot will connect to Discord using the token provided in the `.env` file and will be ready to respond to commands.

## Installation (Docker)

Clone this repository to your server.

```bash
git clone https://github.com/WildPasta/discord_bot_hfr_scraper.git
```

Build the docker image:

```bash
docker build -t wildpasta/bot_hfr_scraper:1.0.0 .
```

## Usage (Docker)

You can run manually the docker using:
```bash
docker run -e DEEP="10" -e DISCORD_TOKEN="<your_discord_token>" wildpasta/bot_hfr_scraper:1.0.0
```

Or you can run the docker container using the docker-compose.yml file:
```bash
docker-compose up -d
```

## Discord Commands

The bot responds to the following commands:

- `!search` <keyword>: Search for ads containing the specified keyword

## New alert script

You can customize the `new_alert.py` by editing the following environment variables in the `.env`:

```
ALERT_CHANNEL=<alert_channel_id>
KEYWORD=<keyword>
```

Replace `<alert_channel_id>` with the ID of the channel where you want the bot to send alerts. 
You can obtain this ID by enabling the developer mode in Discord and right-clicking on the channel.

Replace `<keyword>` with the keyword you want the bot to search for.
