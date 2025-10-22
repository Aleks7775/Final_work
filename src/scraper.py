from urllib.parse import urljoin
import time
import requests
from bs4 import BeautifulSoup


class Scraper:
    """Класс для веб-скрапинга"""

    def __init__(self):
        self.product_brand = []
        self.product_name = []
        self.product_price = []
        self.product_links = []
        self.product_rating = []
        self.product_description = []
        self.product_application = []
        self.product_country = []

    def scrape(self, base_url, total_pages):
        """Скрапинг total_pages страниц из раздела Парфюмерия и извлечение данных"""
        for page_num in range(1, total_pages + 1):
            url = f"{base_url}/parfjumerija?p={page_num}"
            try:
                response = requests.get(url)
                response.raise_for_status()  # Проверка на успешный ответ (200 OK)
                soup = BeautifulSoup(response.text, 'html.parser')

                self.name_product(soup)
                self.price_product(soup)
                self.links_product(soup, base_url)
                self.rating_product(soup)
                self.description_product()
                self.application_product()
                self.country_product()

                time.sleep(1)

            except requests.exceptions.RequestException as e:
                print(f"Ошибка при загрузке URL {url}: {e}")
                break

    def name_product(self, soup):
        """Извлекает бренд и наименование продукта"""
        name_containers = soup.find_all(class_="iVXPq")

        for container in name_containers:
            brand_span = container.find('span', class_="iyrAY")
            name_span = container.find('span', class_='kfy9O')
            if brand_span and name_span:
                self.product_brand.append(brand_span.get_text(strip=True))
                self.product_name.append(name_span.get_text(strip=True))

    def price_product(self, soup):
        """Извлекает цены продуктов"""
        price_containers = soup.find_all(class_="iVXPq")

        for container in price_containers:
            price = container.find('meta', itemprop='price')
            if price:
                self.product_price.append(price['content'])
            else:
                self.product_price.append("Цена отсутствует")


    def links_product(self, soup, base_url):
        """Извлекает ссылки продуктов"""
        links_containers = soup.find_all(class_="iVXPq")

        for container in links_containers:
            links = container.find('a')['href']
            if links:
                link_connect = urljoin(base_url, links)
                self.product_links.append(link_connect)
            else:
                self.product_links.append(None)


    def rating_product(self, soup):
        """Извлекает рейтинг продуктов"""
        rating_containers = soup.find_all(class_="iVXPq")

        for container in rating_containers:
            rating = container.find('meta', itemprop='ratingValue')
            if rating:
                self.product_rating.append(rating['content'])
            else:
                self.product_rating.append('Рейтинг отсутствует')


    def description_product(self):
        """Извлекает описание продуктов"""
        for link in self.product_links:
            link_request = requests.get(link)
            description_soup = BeautifulSoup(link_request.text, 'html.parser')
            description = description_soup.find('div', itemprop="description")
            if description:
                self.product_description.append(description.get_text(strip=True))
            else:
                self.product_description.append('Описание не найдено')


    def application_product(self):
        """Извлекает инструкцию продуктов"""
        for link in self.product_links:
            link_request = requests.get(link)
            application_soup = BeautifulSoup(link_request.text, 'html.parser')
            application = application_soup.find('div', attrs={'text': 'Применение'})
            if application:
                self.product_application.append(application.get_text(strip=True))
            else:
                self.product_application.append("Инструкция отсутствует")



    def country_product(self):
        """Извлекает Страна-производитель продуктов"""
        for link in self.product_links:
            link_request = requests.get(link)
            country_soup = BeautifulSoup(link_request.text, 'html.parser')
            country = country_soup.find('div', attrs={'text': 'Дополнительная информация'})
            if country:
                self.product_country.append(country.get_text(separator=' ', strip=True))
            else:
                self.product_country.append("Страна-производитель не указана")
