#!/bin/bash
scrapy crawl cv_market_links_spider -o ../output/cvmarket.json
python -m CVonline.crawl
