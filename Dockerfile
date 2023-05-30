FROM python:3.9-slim-buster

LABEL org.opencontainers.image.version="1.0"
LABEL org.opencontainers.image.maintainer="Wildpasta <chauve.richard@protonmail.com>"
LABEL org.opencontainers.image.description="Docker container HFR scraping"
LABEL org.opencontainers.image.source="https://github.com/WildPasta/discord_bot_hfr_scraper"

ENV DIR=/home/bot_hfr/
WORKDIR $DIR/bot_hfr

COPY bot $DIR/bot_hfr

RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "discord_bot_hfr_scraper.py"]
