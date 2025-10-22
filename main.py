from src.scraper import Scraper
from src.utils import CSVWriter


base_url = 'https://goldapple.ru'


"""Сбор данных"""
scraper = Scraper()
scraper.scrape(base_url, total_pages=2) # выбор количества страниц (total_pages ?)
scrape_links =scraper.product_links
scrape_brand =scraper.product_brand
scrape_name =scraper.product_name
scrape_price =scraper.product_price
scrape_rating = scraper.product_rating
scrape_description = scraper.product_description
scrape_application = scraper.product_application
scrape_country = scraper.product_country

"""Запись или перезапись продуктов"""
writer = CSVWriter("my_products.csv")
writer.write_to_csv(scrape_links, scrape_brand, scrape_name, scrape_price, scrape_rating,
                    scrape_description, scrape_application, scrape_country)