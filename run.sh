#!/bin/bash
scrapy crawl cv_market_links_spider -o ../output/cvmarket.json
python crawl.py cv_online_links_spider