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
    - **cvmarket_categories.json** Category dim data
    - **cvonline_category.json** Category dim data
    - **cvmarket.json** General cvmarket data
    - **cvonline.json** General cvonline data
- **config.py** Config module
- **processing.py** Data processing module
- **scrapy.cfg** scrapy scripts configurations 
- **requirements.txt** Python libraries list 
- **readme.md** Documentation 
# Installiation
Install requirements
```pip install -r requirements.txt```

# Run

## Scraping

Scrap CVmarket Data
```scrapy crawl cv_market_links_spider -o ../output/cvmarket.json``` 

Scrap CVonline Data
```python -m CVonline.crawl```

Save transformed data in .xlsx format

Category data:
```python run.py cat -o``` (by default folder: xlsx_output)
or 
```python run.py cat -o ./you_directory/```

Vacancies data:
```python run.py data -o``` (by default folder: xlsx_output)
or 
```python run.py data -o ./you_directory/```

without '-o' I'll just show firs dataframes rows

## Complex Scraping

Run all scrapers:
```.\parse.bat```

Transform .json data to .xlsx 
```.\save_data.bat```

# PBI