from bs4 import BeautifulSoup
import os
import json
import numpy as np
import re
import pandas as pd

# ввод и вывод
input_folder = r"C:\Users\klimo\Desktop\Ycheba\engineering\prac 3\5"
output_folder = r"C:\Users\klimo\Desktop\Ycheba\engineering\prac 3\rezults"
os.makedirs(output_folder, exist_ok=True)

html_files = [os.path.join(input_folder, f"{i}.html") for i in range(2, 16)]

# преобразование данных
def convert_int64_to_int(obj):
    if isinstance(obj, pd.Series):
        return obj.apply(lambda x: int(x) if isinstance(x, (np.int64, np.float64)) else x)
    elif isinstance(obj, dict):
        return {key: convert_int64_to_int(value) for key, value in obj.items()}
    elif isinstance(obj, list):
        return [convert_int64_to_int(item) for item in obj]
    elif isinstance(obj, (np.int64, np.float64)):
        return int(obj)
    return obj

# парсинг
def parse_object_page(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        soup = BeautifulSoup(file, "html.parser")
    try:
        # заголовок
        title_element = soup.find("title")
        meta_element = soup.find("meta", property="og:description")

        # поиск нужной информации
        if not title_element:
            print(f"Title не найден в файле {file_path}")
        else:
            print(f"Title: {title_element.text}")

        if not meta_element:
            print(f"Meta description не найдено в файле {file_path}")
        else:
            print(f"Meta description: {meta_element['content']}")

        # извлекаем данные
        name = title_element.text.strip().split("–")[0]
        price_text = meta_element["content"]
        price = int(price_text.split("по цене")[1].split("₽")[0].strip().replace(" ", ""))

        # масса
        mass_match = re.search(r"(\d+ ?(г|мл|л|кг))", name.lower())
        mass = mass_match.group(1) if mass_match else None


        if mass:
            name = name.replace(mass, "").strip()

        return {"name": name, "price": price, "mass": mass}
    except Exception as e:
        print(f"Ошибка при парсинге файла {file_path}: {e}")
        return None

# парсинг
all_objects = []
for file_path in html_files:
    data = parse_object_page(file_path)
    if data:
        all_objects.append(data)

# проверка наличия данных(не работал без этого код)
if not all_objects:
    print("Неверно")
else:
    # цена
    sorted_by_price = sorted(all_objects, key=lambda x: x["price"])

    # условие
    filtered_data = [obj for obj in all_objects if obj["price"] < 3000]

    # сортировка по ценам
    prices = [obj["price"] for obj in all_objects]
    price_stats = {
        "sum": np.sum(prices),
        "min": np.min(prices),
        "max": np.max(prices),
        "mean": np.mean(prices),
        "std_dev": np.std(prices),
    }

    # частота появления слов
    words = []
    for obj in all_objects:
        words.extend(obj["name"].split())
    word_frequency = {word: words.count(word) for word in set(words)}

    # преобразование данных
    all_objects = convert_int64_to_int(all_objects)
    price_stats = convert_int64_to_int(price_stats)
    sorted_by_price = convert_int64_to_int(sorted_by_price)
    filtered_data = convert_int64_to_int(filtered_data)

    # сохранение
    output_objects_file = os.path.join(output_folder, "fifth(парсинг).json")
    with open(output_objects_file, "w", encoding="utf-8") as json_file:
        json.dump(all_objects, json_file, ensure_ascii=False, indent=4)

    output_stats_file = os.path.join(output_folder, "fifth(отфильтрованный).json")
    with open(output_stats_file, "w", encoding="utf-8") as json_file:
        json.dump(
            {"sorted_by_price": sorted_by_price, "filtered_data": filtered_data,
             "price_stats": price_stats, "word_frequency": word_frequency},
            json_file, ensure_ascii=False, indent=4
        )

    print(f"Результаты сохранены в папке {output_folder}")
