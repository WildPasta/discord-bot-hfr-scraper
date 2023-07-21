#!/bin/bash
service cron start
python bot_hfr_scraper.py &
