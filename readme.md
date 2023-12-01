# About Project
The project collects and processes data from CVmarket and CVonline. The project uses scrapy and playwright libraries. 

## Catalogs and files

- **Darbo_Rinkos_analiz-_-PBI:** General project catalog
- **CVmarket** CV market site scraper
    - **spiders** CV market spiders folder
        - **cvmarket_spider.py** CV market spider
- **CVonline** CV online site scraper
    - **scrap_cvonline.py** CV online site scraper
- **output** Scrap output data
    - **cvmarket_categories.json**
    - **cvmarket_categories.json**
    - **cvmarket_categories.json**
    - **cvmarket_categories.json**
- **config.py** Config module
- **processing.py** Data processing module
- **scrapy.cfg** scrapy scripts configurations 
- **requirements.txt** Python libraries list 
- **readme.md** Documentation 
# Installiation
Install requirements
```pip install -r requirements.txt```

# Run

Scrap CVmarket Data
```scrapy crawl cv_market_links_spider -o ../output/cvmarket.json``` 






# Docs

# PBI