import os
import re

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
INSECT_DIR = os.path.join(BASE_DIR, "..", "data", "imagedata", "insect")

def normalize(name):
    name = name.lower()
    name = re.sub(r"\(.*?\)", "", name)     # remove parentheses
    name = re.sub(r"[^a-z\s_]", "", name)   # remove symbols
    name = re.sub(r"\s+", "_", name.strip())
    name = name.replace("__", "_")

    # singularize common plurals
    if name.endswith("ies"):
        name = name[:-3] + "y"
    elif name.endswith("s"):
        name = name[:-1]

    return name

for split in ["train", "val"]:
    split_path = os.path.join(INSECT_DIR, split)
    if not os.path.exists(split_path):
        continue

    for folder in os.listdir(split_path):
        old = os.path.join(split_path, folder)
        new_name = normalize(folder)
        new = os.path.join(split_path, new_name)

        if old != new:
            os.rename(old, new)
            print(f"{folder} → {new_name}")

print("✅ Insect labels normalized.")
