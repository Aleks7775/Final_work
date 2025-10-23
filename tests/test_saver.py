import os
import csv
import pytest
# import pandas as pd
from src.utils import CSVWriter


def test_write_to_csv_success(mocker):
    """
    Проверяет успешную запись данных в CSV-файл.
    """
    # Создаем фиктивный (mock) объект для имитации открытого файла
    mock_file = mocker.mock_open()
    # "Подменяем" встроенную функцию open() на наш фиктивный объект
    mocker.patch('builtins.open', mock_file)

    # Подготавливаем тестовые данные
    test_data = {
        'link': ['link1', 'link2'],
        'brand': ['brandA', 'brandB'],
        'name': ['name1', 'name2'],
        'price': [100, 200],
        'rating': [4.5, 4.0],
        'description': ['desc1', 'desc2'],
        'application': ['app1', 'app2'],
        'country': ['country1', 'country2']
    }

    # Создаем экземпляр класса и вызываем метод записи
    writer = CSVWriter('test_products.csv')
    writer.write_to_csv(
        test_data['link'],
        test_data['brand'],
        test_data['name'],
        test_data['price'],
        test_data['rating'],
        test_data['description'],
        test_data['application'],
        test_data['country']
    )

    # Проверяем, что open() был вызван с правильными аргументами
    mock_file.assert_called_once_with('test_products.csv', mode='w', newline='', encoding='utf-8')

    # # Получаем мок-объект, который имитирует csv-писателя.
    # mock_writer = mock_file().writerow
    #
    # # Проверяем, что были вызваны правильные методы writerow() с корректными данными.
    # expected_calls = [
    #     ['Ссылка', 'Бренд', 'Название продукта', 'Цена', 'Рейтинг', 'Описание', 'Инструкция', 'Страна-производитель'],
    #     ['link1', 'brandA', 'name1', 100, 4.5, 'desc1', 'app1', 'country1'],
    #     ['link2', 'brandB', 'name2', 200, 4.0, 'desc2', 'app2', 'country2']
    # ]
    #
    # for row in expected_calls:
    #     mock_writer.assert_any_call(row)