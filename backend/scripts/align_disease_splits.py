import os
import shutil

BASE = os.path.join(
    os.path.dirname(__file__),
    "..", "data", "imagedata", "disease"
)

train_dir = os.path.join(BASE, "train")
val_dir = os.path.join(BASE, "val")

train_classes = set(os.listdir(train_dir))
val_classes = set(os.listdir(val_dir))

# Classes missing in val
missing_in_val = train_classes - val_classes
# Classes missing in train
missing_in_train = val_classes - train_classes

print("Missing in val:", missing_in_val)
print("Missing in train:", missing_in_train)

# Remove unmatched classes (safe for first version)
for cls in missing_in_val:
    shutil.rmtree(os.path.join(train_dir, cls))
    print(f"Removed train/{cls}")

for cls in missing_in_train:
    shutil.rmtree(os.path.join(val_dir, cls))
    print(f"Removed val/{cls}")

print("✅ Train/Val alignment complete.")
