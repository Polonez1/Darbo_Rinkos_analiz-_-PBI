# About Project

A project created for scraping dynamic websites using selenium and steal. 

- easy way to send a driver compatible with the Chrome version
- works on web with "incapsula"

# Installiation

Install requirements

```pip install -r requirements.txt```

# Config

general config file ```config.cfg```

## downloads config

1. run ```python run.py driver -e (--endpoints)``` open to see download endpoints
2. in config.cfg swap endpoints
3. After download driver

Manual download page:
https://googlechromelabs.github.io/chrome-for-testing/

If you use Chrome version 114 or older:
https://chromedriver.chromium.org/downloads

## Selenium config

1. All selenium configs in scraping_engine.py. For example: user_agent and other
2. Open scraping_engine.py and add or switch ScrapingEngine class __init__ args. 

# Doc

1. Download chrome driver

```python run.py driver -d (--download)```

driver downloaded by default ./driver/chromedriver-win32/chromedriver.exe








