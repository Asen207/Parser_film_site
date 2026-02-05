import requests              # библиотека для HTTP-запросов
import json                  # работа с JSON (в этом коде не используется)
from bs4 import BeautifulSoup # парсинг HTML
import csv                   # работа с CSV-файлами

# URL страницы с зарубежными сериалами
html = "https://lordserialnew48.top/zarubezhnye/"

# Заголовки для имитации запроса из браузера
headers = {
   "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
   "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 YaBrowser/25.12.0.0 Safari/537.36"  
}

# Открываем локальный HTML-файл (предположительно сохранённую страницу)
with open("index.html") as file:
    src = file.read()

# Создаём объект BeautifulSoup для разбора HTML
soup = BeautifulSoup(src, "lxml")

page = []  # список для хранения номеров страниц

# Ищем блок навигации страниц
number_pages = ["navigation"]

# Получаем все ссылки внутри навигации
for item in soup.find(class_=number_pages).find_all("a"):
    page.append(item.get_text("href")) 

# Берём последний элемент — предполагаем, что это номер последней страницы
page = page[-1]

numbers = [1]       # список номеров страниц, начинается с 1
page_number = []    # отдельный список номеров страниц

# Генерируем номера страниц
for i in range(2, int(page) + 1):
    page_number.append(i)
    numbers.append(i + 1)

# Заголовки CSV-файла
title = ["name", "year", "rate_kinopoisk", "rate_imbd"]

# Названия колонок (переменные дублируют title)
name = "name"
year = "year"
rate_1 = "rate_kinopoisk"
rate_2 = "rate_imbd"

# Создаём CSV-файл и записываем заголовки
with open("serials.csv", "w", encoding="utf=8-sig") as file:
    writer = csv.writer(file, lineterminator="\r")
    for i in range(0, 4):
        writer.writerow(title[i]) 

i = 0
count = 0  # счётчик страниц

# Цикл обхода всех страниц
while count <= max(page_number):

    # Первая страница
    if count == 0:
        req = requests.get(html, headers=headers)  # HTTP-запрос
        src = req.text                             # HTML-код страницы
        print("1")
        
        soup = BeautifulSoup(src, "lxml")

        # CSS-классы элементов с данными сериалов
        class_serail = [
            "th-title",
            "th-year",
            "th-rate th-rate-kp",
            "th-rate th-rate-imdb"
        ]

        # Ищем все элементы с нужными классами
        all_serails_hrefs = soup.find_all(class_=class_serail)

        all_serials = []  # список сериалов
        for item in all_serails_hrefs:
            item_text = item.text                  # текст элемента
            item_text = item_text.replace("\n", " ")
            item_href = item.get_text("href")  
            all_serials.append(item_href)

        count += 1

    # Остальные страницы
    else:
        html = "https://lordserialnew48.top/zarubezhnye/" + "/page/" + str(page_number[count-1])
        
        req = requests.get(html, headers=headers)
        src = req.text
        soup = BeautifulSoup(src, "lxml")

        class_serail = [
            "th-title",
            "th-year",
            "th-rate th-rate-kp",
            "th-rate th-rate-imdb"
        ]

        all_serails_hrefs = soup.find_all(class_=class_serail)

        all_serials = []
        for item in all_serails_hrefs:
            item_text = item.text
            item_text = item_text.replace("\n", " ")
            item_href = item.get_text("href")
            all_serials.append(item_href)

        count += 1

    # Дописываем данные в CSV
    with open("serials.csv", "a", encoding="utf=8-sig") as file:
        writer = csv.writer(file)
        for i in range(0, len(all_serials)):
            writer.writerows(all_serials[i])  

    print(count)  # вывод текущего номера страницы
