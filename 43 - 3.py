import os
import json
import numpy as np
import xml.etree.ElementTree as ET

# ввод и вывод
input_dir = r"C:\Users\klimo\Desktop\Ycheba\engineering\prac 3\3"
output_dir = r"C:\Users\klimo\Desktop\Ycheba\engineering\prac 3\rezults"  
os.makedirs(output_dir, exist_ok=True)

# парсинг одного файла
def parse_xml_file(file_path):
    tree = ET.parse(file_path)
    root = tree.getroot()
    star_data = {
        "name": root.find("name").text.strip(),
        "constellation": root.find("constellation").text.strip(),
        "spectral_class": root.find("spectral-class").text.strip(),
        "radius": float(root.find("radius").text.strip()),
        "rotation": float(root.find("rotation").text.strip().replace(" days", "")),
        "age": float(root.find("age").text.strip().replace(" billion years", "")),
        "distance": float(root.find("distance").text.strip().replace(" million km", "")),
        "absolute_magnitude": float(root.find("absolute-magnitude").text.strip().replace(" million km", "")),
    }
    return star_data

file_paths = [os.path.join(input_dir, f) for f in os.listdir(input_dir) if f.endswith(".xml")]

all_stars = []

for file_path in file_paths:
    star_data = parse_xml_file(file_path)
    all_stars.append(star_data)

# сохранение в json
output_json = os.path.join(output_dir, "third(парсинг).json")
with open(output_json, "w", encoding="utf-8") as json_file:
    json.dump(all_stars, json_file, ensure_ascii=False, indent=4)

# радиус
sorted_by_radius = sorted(all_stars, key=lambda x: x["radius"])

# созвездия
filtered_by_constellation = [star for star in all_stars if star["constellation"] == "Близнецы"]

# выборка по радиусу
radii = [star["radius"] for star in all_stars]
radius_stats = {
    "sum": float(np.sum(radii)),
    "min": float(np.min(radii)),
    "max": float(np.max(radii)),
    "mean": float(np.mean(radii)),
    "std_dev": float(np.std(radii)),
}

# частота появления спектральных классов
spectral_classes = [star["spectral_class"] for star in all_stars]
spectral_frequency = {cls: spectral_classes.count(cls) for cls in set(spectral_classes)}

# сохранение в json
stats = {
    "sorted_by_radius": sorted_by_radius,
    "filtered_by_constellation": filtered_by_constellation,
    "radius_stats": radius_stats,
    "spectral_class_frequency": spectral_frequency,
}
output_stats_json = os.path.join(output_dir, "third(отфильтрованные).json")
with open(output_stats_json, "w", encoding="utf-8") as json_file:
    json.dump(stats, json_file, ensure_ascii=False, indent=4)

print(f"Файлы сохранены: {output_json} и {output_stats_json}")
