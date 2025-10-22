import csv

class CSVWriter:
    """
    Класс для записи данных из списков в CSV-файл.
    """
    def __init__(self, filename="products.csv"):
        self.filename = filename


    def write_to_csv(self, link, brand, name, price, rating, description, application, country):
        headers = ["Ссылка", "Бренд", "Название продукта", "Цена", "Рейтинг", "Описание", "Инструкция", "Страна-производитель"]

        try:
            with open(self.filename, mode='w', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)

                # Записываем заголовки
                writer.writerow(headers)

                # Записываем данные построчно
                for i in range(len(brand)):
                    writer.writerow([link[i], brand[i], name[i], price[i], rating[i], description[i], application[i], country[i]])
                    # writer.writerow([brand[i], name[i], price[i], link[i]])

            print(f"Данные успешно записаны в файл {self.filename}")

        except IOError as e:
            print(f"Ошибка при работе с файлом {self.filename}: {e}")
