import os
import re

BASE_DIR = os.path.join(
    os.path.dirname(__file__),
    "..", "data", "imagedata", "disease"
)

def normalize(name):
    name = name.lower()
    name = re.sub(r"[()]", "", name)
    name = re.sub(r"\s+on\s+", "_", name)
    name = re.sub(r"\s+in\s+", "_", name)
    name = re.sub(r"\s+", "_", name)
    name = re.sub(r"_+", "_", name)
    return name.strip("_")

for split in ["train", "val"]:
    split_dir = os.path.join(BASE_DIR, split)
    for cls in os.listdir(split_dir):
        old = os.path.join(split_dir, cls)
        if not os.path.isdir(old):
            continue
        new_name = normalize(cls)
        new = os.path.join(split_dir, new_name)
        if old != new:
            print(f"{cls} → {new_name}")
            os.rename(old, new)

print("✅ Disease labels normalized.")
