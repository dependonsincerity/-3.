import re
from bs4 import BeautifulSoup
import json
import numpy as np
import os

# ввод и вывод
input_dir = r"C:\Users\klimo\Desktop\Ycheba\engineering\prac 3\1"
output_dir = r"C:\Users\klimo\Desktop\Ycheba\engineering\prac 3\rezults"
os.makedirs(output_dir, exist_ok=True)

def parse_html_file(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        soup = BeautifulSoup(file, "html.parser")

    products = []

    # извлечение данных из файла
    product = {
        "artikul": soup.find("span", string=lambda x: x and "Артикул" in x).string.split(":")[1].strip().split("\n")[0],
        # Убираем лишние символы новой строки
        "nalichie": "Нет" if "Нет" in soup.find("span", string=lambda x: x and "Наличие" in x).string else "Есть",
        "nazvanie": soup.find("h1", class_="title").string.split(":")[1].strip(),
        "gorod": soup.find("p", class_="address-price").string.split(":")[1].strip().split("Цена")[0].strip(),
        "cena": int(re.search(r'Цена[:\s]*(\d+)\s*руб', soup.find("p", class_="address-price").string).group(1)),
        "cvet": soup.find("span", class_="color").string.split(":")[1].strip() if soup.find("span",
                                                                                            class_="color") else None,
        "kolichestvo": int(soup.find("span", class_="quantity").string.split(":")[1].strip().replace(" шт", "")),
        "razmery": soup.find("span", string=lambda x: x and "Размеры" in x).string.split(":")[1].strip() if soup.find(
            "span", string=lambda x: x and "Размеры" in x) else None,
        "reiting": float(
            soup.find("span", string=lambda x: x and "Рейтинг" in x).string.split(":")[1].strip()) if soup.find("span",
                                                                                                                string=lambda
                                                                                                                    x: x and "Рейтинг" in x) else None,
        "prosmotry": int(
            soup.find("span", string=lambda x: x and "Просмотры" in x).string.split(":")[1].strip()) if soup.find(
            "span", string=lambda x: x and "Просмотры" in x) else None,
    }
    products.append(product)

    return products

file_paths = [os.path.join(input_dir, f"{i}.html") for i in range(2, 54)]

all_products = []

# парсинг
for file_path in file_paths:
    products = parse_html_file(file_path)
    all_products.extend(products)

# сохранение в json
output_json = os.path.join(output_dir, "first(парсинг).json")
with open(output_json, "w", encoding="utf-8") as json_file:
    json.dump(all_products, json_file, ensure_ascii=False, indent=4)

# сортировка по цене
sorted_by_price = sorted(all_products, key=lambda x: x["cena"])

# сортировка по наличию товара
filtered_by_availability = [p for p in all_products if p.get("nalichie") != "Нет"]

# цена
prices = [p["cena"] for p in all_products if "cena" in p]

if prices:
    price_stats = {
        "sum": int(np.sum(prices)),
        "min": int(np.min(prices)),
        "max": int(np.max(prices)),
        "mean": float(np.mean(prices)),
        "std_dev": float(np.std(prices)),
    }
else:
    price_stats = {
        "sum": 0,
        "min": 0,
        "max": 0,
        "mean": 0.0,
        "std_dev": 0.0,
    }

# частота рейтинга
ratings = [p["reiting"] for p in all_products if "reiting" in p]
rating_frequency = {rating: ratings.count(rating) for rating in set(ratings)}

# сохранение в json
stats = {
    "sorted_by_price": sorted_by_price,
    "filtered_by_availability": filtered_by_availability,
    "price_stats": price_stats,
    "rating_frequency": rating_frequency,
}
output_stats_json = os.path.join(output_dir, "first(отфильтрованные).json")
with open(output_stats_json, "w", encoding="utf-8") as json_file:
    json.dump(stats, json_file, ensure_ascii=False, indent=4)

print(f"Файлы сохранены: {output_json} и {output_stats_json}")
