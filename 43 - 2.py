from bs4 import BeautifulSoup
import json
import numpy as np
import os
import re
# ввод и вывод
input_dir = r"C:\Users\klimo\Desktop\Ycheba\engineering\prac 3\2"
output_dir = r"C:\Users\klimo\Desktop\Ycheba\engineering\prac 3\rezults"
os.makedirs(output_dir, exist_ok=True)

# типы экранов
screen_types = ["AMOLED", "IPS", "OLED"]


# парсинг из файла
def parse_html_file(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        soup = BeautifulSoup(file, "html.parser")

    products = []

    # строки с данными
    product_items = soup.find_all("div", class_="product-item")

    # каждый товар
    for item in product_items:
        product = {
            "nazvanie": item.find("span").text.strip(),
            "cena": int(item.find("price").text.strip().replace(" ₽", "").replace(" ", "")),
            "sim": item.find("li", type="sim").text.split()[0] if item.find("li", type="sim") else None,
            "razreshenie": item.find("li", type="resolution").text.strip() if item.find("li",
                                                                                        type="resolution") else None,
            "kamera": int(item.find("li", type="camera").text.split()[0]) if item.find("li", type="camera") else None,
        }

        # бонусы
        bonus_text = item.find("strong").text if item.find("strong") else ""
        bonus_match = re.search(r'(\d+)', bonus_text)
        if bonus_match:
            product["bonusy"] = int(bonus_match.group(1))
        else:
            product["bonusy"] = 0  #

        # экран
        screen_type = next((st for st in screen_types if st in item.text), None)
        if screen_type:
            product["screen"] = screen_type

        products.append(product)

    return products

file_paths = [os.path.join(input_dir, f"{i}.html") for i in range(1, 65)]

all_products = []

for file_path in file_paths:
    products = parse_html_file(file_path)
    all_products.extend(products)

# сохранение данных в json
output_json = os.path.join(output_dir, "second(парсинг).json")
with open(output_json, "w", encoding="utf-8") as json_file:
    json.dump(all_products, json_file, ensure_ascii=False, indent=4)

# цена
sorted_by_price = sorted(all_products, key=lambda x: x["cena"])

# sim
filtered_by_sim = [p for p in all_products if p.get("sim") == "2"]

# статистика по цене
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

# как часто встречаются одинаковые разрешения
resolutions = [p["razreshenie"] for p in all_products if "razreshenie" in p and p["razreshenie"]]
resolution_frequency = {res: resolutions.count(res) for res in set(resolutions)}

# сохранение в json
stats = {
    "sorted_by_price": sorted_by_price,
    "filtered_by_sim": filtered_by_sim,
    "price_stats": price_stats,
    "resolution_frequency": resolution_frequency,
}
output_stats_json = os.path.join(output_dir, "second(отфильтрованные).json")
with open(output_stats_json, "w", encoding="utf-8") as json_file:
    json.dump(stats, json_file, ensure_ascii=False, indent=4)

output_json, output_stats_json
