import os
import random
import shutil

# Always resolve paths relative to THIS FILE
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "..", "data", "imagedata", "insect")

RAW_DIR = os.path.join(DATA_DIR, "raw", "farm_insects 3")
TRAIN_DIR = os.path.join(DATA_DIR, "train")
VAL_DIR = os.path.join(DATA_DIR, "val")

SPLIT = 0.8
EXTS = (".jpg", ".jpeg", ".png")

print("RAW_DIR:", RAW_DIR)

if not os.path.exists(RAW_DIR):
    raise FileNotFoundError(f"RAW_DIR not found: {RAW_DIR}")

os.makedirs(TRAIN_DIR, exist_ok=True)
os.makedirs(VAL_DIR, exist_ok=True)

for cls in os.listdir(RAW_DIR):
    cls_path = os.path.join(RAW_DIR, cls)
    if not os.path.isdir(cls_path):
        continue

    images = [i for i in os.listdir(cls_path) if i.lower().endswith(EXTS)]
    random.shuffle(images)

    cut = int(len(images) * SPLIT)
    train_imgs, val_imgs = images[:cut], images[cut:]

    os.makedirs(os.path.join(TRAIN_DIR, cls), exist_ok=True)
    os.makedirs(os.path.join(VAL_DIR, cls), exist_ok=True)

    for img in train_imgs:
        shutil.copy(
            os.path.join(cls_path, img),
            os.path.join(TRAIN_DIR, cls, img)
        )

    for img in val_imgs:
        shutil.copy(
            os.path.join(cls_path, img),
            os.path.join(VAL_DIR, cls, img)
        )

    print(f"{cls}: {len(train_imgs)} train | {len(val_imgs)} val")

print("✅ Insect dataset split complete.")
