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
MOCK_HTML_two = """
        <html>
        <body>
            <div itemprop="description">Описание для продукта One.</div>
            <div text="Применение">Применение: Нанести на кожу.</div>
            <div text="Дополнительная информация">Франция </div>
        </body>
        </html>
        <html>
    """

MOCK_HTML_zero = """
<body>
    <div class="iVXPq">
        <div>
        <div>
    </div>
    <div class="iVXPq">
    </div>
</body>
</html>
"""

class TestScraper(unittest.TestCase):

    def setUp(self):
        """Настройка, которая выполняется перед каждым тестом."""
        self.scraper = Scraper()
        self.mock_soup = BeautifulSoup(MOCK_HTML_CONTENT, 'html.parser')
        self.mock_soup_two = BeautifulSoup(MOCK_HTML_two, 'html.parser')
        self.mock_soup_zero = BeautifulSoup(MOCK_HTML_zero, 'html.parser')
        self.base_url = "https://goldapple.ru"

    def test_product_successful(self):
        """Тест, тест продуктов на главной странице."""
        self.scraper.name_product(self.mock_soup)
        self.scraper.price_product(self.mock_soup)
        self.scraper.rating_product(self.mock_soup)


        # Проверка результатов
        self.assertEqual(self.scraper.product_brand, ['Бренд 1', 'Бренд 2'])
        self.assertEqual(self.scraper.product_name, ['Название продукта 1', 'Название продукта 2'])
        self.assertEqual(self.scraper.product_price, ['6969', '4545'])
        self.assertEqual(self.scraper.product_rating, ['4.5', '2.5'])


    def test_missing_goods(self):

        self.scraper.name_product(self.mock_soup_zero)
        self.scraper.price_product(self.mock_soup_zero)
        self.scraper.rating_product(self.mock_soup_zero)

        self.assertEqual(self.scraper.product_brand, [])
        self.assertEqual(self.scraper.product_name, [])
        self.assertEqual(self.scraper.product_price, ['Цена отсутствует', 'Цена отсутствует'])
        self.assertEqual(self.scraper.product_rating, ['Рейтинг отсутствует', 'Рейтинг отсутствует'])


    @patch('requests.get')
    def test_information_one_product(self, mock_get):
        """Тесты на странице продукта"""

        self.scraper.product_links = ["http://goldapple.ru/product-1"]

        mock_response = Mock()
        mock_response.text = MOCK_HTML_two
        mock_get.return_value = mock_response

        self.scraper.description_product()
        self.scraper.application_product()
        self.scraper.country_product()

        # Проверка результатов
        self.assertEqual(self.scraper.product_description, [
            "Описание для продукта One."])
        self.assertEqual(self.scraper.product_application, [
            "Применение: Нанести на кожу."])
        self.assertEqual(self.scraper.product_country, [
            "Франция"])
