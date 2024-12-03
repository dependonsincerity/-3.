import os
import json
import numpy as np
import xml.etree.ElementTree as ET

# ввод и вывод
input_dir = r"C:\Users\klimo\Desktop\Ycheba\engineering\prac 3\4"
output_dir = r"C:\Users\klimo\Desktop\Ycheba\engineering\prac 3\rezults"  
os.makedirs(output_dir, exist_ok=True)

# парсинг файла
def parse_xml_file(file_path):
    tree = ET.parse(file_path)
    root = tree.getroot()
    items = []
    for clothing in root.findall("clothing"):
        item = {
            "id": clothing.findtext("id", default="").strip(),
            "name": clothing.findtext("name", default="").strip(),
            "category": clothing.findtext("category", default="").strip(),
            "size": clothing.findtext("size", default="").strip(),
            "color": clothing.findtext("color", default="").strip(),
            "material": clothing.findtext("material", default="").strip(),
            "price": float(clothing.findtext("price", default="0").strip()) if clothing.findtext("price") else None,
            "rating": float(clothing.findtext("rating", default="0").strip()) if clothing.findtext("rating") else None,
            "reviews": int(clothing.findtext("reviews", default="0").strip()) if clothing.findtext("reviews") else None,
            "new": clothing.findtext("new", default="").strip(),
            "exclusive": clothing.findtext("exclusive", default="").strip(),
            "sporty": clothing.findtext("sporty", default="").strip(),
        }
        items.append(item)
    return items

file_paths = [os.path.join(input_dir, f) for f in os.listdir(input_dir) if f.endswith(".xml")]

all_items = []

for file_path in file_paths:
    items = parse_xml_file(file_path)
    all_items.extend(items)

# сохранение в json
output_json = os.path.join(output_dir, "fourth(парсинг).json")
with open(output_json, "w", encoding="utf-8") as json_file:
    json.dump(all_items, json_file, ensure_ascii=False, indent=4)

# цена
sorted_by_price = sorted(all_items, key=lambda x: x.get("price", 0))

# только новые товары
filtered_by_new = [item for item in all_items if item.get("new") == "+"]

# выборка по рейтингу
ratings = [item["rating"] for item in all_items if "rating" in item and item["rating"] is not None]
rating_stats = {
    "sum": float(np.sum(ratings)),
    "min": float(np.min(ratings)),
    "max": float(np.max(ratings)),
    "mean": float(np.mean(ratings)),
    "std_dev": float(np.std(ratings)),
}

# частота появления категорий
categories = [item["category"] for item in all_items if "category" in item and item["category"]]
category_frequency = {category: categories.count(category) for category in set(categories)}

# сохранение в json
stats = {
    "sorted_by_price": sorted_by_price,
    "filtered_by_new": filtered_by_new,
    "rating_stats": rating_stats,
    "category_frequency": category_frequency,
}
output_stats_json = os.path.join(output_dir, "fourth(отфильтрованные).json")
with open(output_stats_json, "w", encoding="utf-8") as json_file:
    json.dump(stats, json_file, ensure_ascii=False, indent=4)

print(f"Файлы сохранены: {output_json} и {output_stats_json}")
