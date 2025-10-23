import pytest
import unittest
from unittest.mock import patch, Mock
from bs4 import BeautifulSoup
from src.scraper import Scraper


MOCK_HTML_CONTENT = """
<html>
<body>
    <div class="iVXPq">
        <span class="iyrAY">Бренд 1</span>
        <span class="kfy9O">Название продукта 1</span>
        <meta itemprop="price" content="6969">
        <meta itemprop="ratingValue" content="4.5">
        <div>
        <div>
    </div>
    <div class="iVXPq">
        <span class="iyrAY">Бренд 2</span>
        <span class="kfy9O">Название продукта 2</span>
        <meta itemprop="price" content="4545">
        <meta itemprop="ratingValue" content="2.5">
    </div>
</body>
</html>
"""
MOCK_HTML_zero = """
"""

class TestScraper(unittest.TestCase):

    def setUp(self):
        """Настройка, которая выполняется перед каждым тестом."""
        self.scraper = Scraper()
        self.mock_soup = BeautifulSoup(MOCK_HTML_CONTENT, 'html.parser')
        self.mock_soup_zero = BeautifulSoup(MOCK_HTML_zero, 'html.parser')
        self.base_url = "https://goldapple.ru"

    def test_product_successful(self):
        """Тест, тест продуктов га главной странице."""
        # Вызов тестируемого метода
        self.scraper.name_product(self.mock_soup)
        self.scraper.price_product(self.mock_soup)
        self.scraper.rating_product(self.mock_soup)


        # Проверка результатов
        self.assertEqual(self.scraper.product_brand, ['Бренд 1', 'Бренд 2'])
        self.assertEqual(self.scraper.product_name, ['Название продукта 1', 'Название продукта 2'])
        self.assertEqual(self.scraper.product_price, ['6969', '4545'])
        self.assertEqual(self.scraper.product_rating, ['4.5', '2.5'])


    # def test_description_product_success(requests_mock):
    #     """Тест успешного извлечения описаний для нескольких продуктов."""
    #     base_url = "https://goldapple.ru"
    #
    #     scraper = Scraper()
    #
    #     # Задаём фиктивные ссылки на страницы, которые будем мокировать
    #     scraper.product_links = [
    #         f"{base_url}/parfjumerija/product-one",
    #         f"{base_url}/parfjumerija/product-two"
    #     ]
    #
    #     # Настраиваем моки для каждого URL
    #     requests_mock.get(
    #         scraper.product_links[0],
    #         text=MOCK_PRODUCT_PAGE["/parfjumerija/product-one"]
    #     )
    #     requests_mock.get(
    #         scraper.product_links[1],
    #         text=MOCK_PRODUCT_PAGE["/parfjumerija/product-two"]
    #     )
    #
    #     # Вызываем тестируемый метод
    #     scraper.description_product()
    #
    #     # Проверяем, что результаты соответствуют ожиданиям
    #     assert scraper.product_description == [
    #         "Описание для продукта One.",
    #         "Описание не найдено"
    #     ]
    # def test_description(self):
    #     self.scraper.description_product()
    #
    #     for link, html in MOCK_PRODUCT_PAGE.items():
    #         m.get(f"{BASE_URL}{link}", text=html)
    #
    #     # Проверка результатов
    #     self.assertEqual(self.scraper.product_description, ["", ""])

        # на отсутствие
        # self.assertEqual(self.scraper.product_price, ['Цена отсутствует', 'Цена отсутствует'])
        # self.assertEqual(self.scraper.product_rating, ['Рейтинг отсутствует', 'Рейтинг отсутствует'])


