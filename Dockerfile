FROM python:3.9-slim-buster

LABEL org.opencontainers.image.version="1.0"
LABEL org.opencontainers.image.maintainer="Wildpasta <chauve.richard@protonmail.com>"
LABEL org.opencontainers.image.description="Docker container HFR scraping"
LABEL org.opencontainers.image.source="https://github.com/WildPasta/discord_bot_hfr_scraper"

ENV DIR=/home/bot/
WORKDIR $DIR

COPY bot $DIR

RUN pip install --no-cache-dir -r requirements.txt
RUN apt-get update && apt-get install -y cron

COPY cronjob /etc/cron.d/cronjob
RUN chmod 0644 /etc/cron.d/cronjob
RUN crontab /etc/cron.d/cronjob
RUN touch /var/log/cron.log

COPY entrypoint.sh $DIR
RUN chmod +x $DIR/entrypoint.sh

CMD ["./entrypoint.sh"]
