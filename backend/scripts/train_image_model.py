import os
import sys
import json
import torch
import torch.nn as nn
from torchvision import datasets, transforms, models
from torch.utils.data import DataLoader
from tqdm import tqdm

# --------------------------------------------------
# CONFIG (OPTIMIZED FOR CPU)
# --------------------------------------------------

DEVICE = "cuda" if torch.cuda.is_available() else "cpu"

if len(sys.argv) != 2:
    print("Usage: python train_image_model.py [insect|disease]")
    sys.exit(1)

CATEGORY = sys.argv[1]  # insect or disease
assert CATEGORY in ["insect", "disease"]

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "..", "data", "imagedata", CATEGORY)
TRAIN_DIR = os.path.join(DATA_DIR, "train")
VAL_DIR = os.path.join(DATA_DIR, "val")
MODEL_DIR = os.path.join(BASE_DIR, "..", "image_models")
os.makedirs(MODEL_DIR, exist_ok=True)

EPOCHS = 8
BATCH_SIZE = 16
LR = 1e-3
IMG_SIZE = 224

# --------------------------------------------------
# FAST TRANSFORMS (NO AUGMENTATION)
# --------------------------------------------------

train_tfms = transforms.Compose([
    transforms.Resize((IMG_SIZE, IMG_SIZE)),
    transforms.ToTensor(),
    transforms.Normalize(
        mean=[0.485, 0.456, 0.406],
        std=[0.229, 0.224, 0.225]
    )
])

val_tfms = train_tfms

# --------------------------------------------------
# DATA
# --------------------------------------------------

train_ds = datasets.ImageFolder(TRAIN_DIR, transform=train_tfms)
val_ds = datasets.ImageFolder(VAL_DIR, transform=val_tfms)
train_loader = DataLoader(
    train_ds,
    batch_size=BATCH_SIZE,
    shuffle=True,
    num_workers=0
)

val_loader = DataLoader(
    val_ds,
    batch_size=BATCH_SIZE,
    shuffle=False,
    num_workers=0
)


num_classes = len(train_ds.classes)

print(f"Training {CATEGORY} model with {num_classes} classes")
print("Classes:", train_ds.classes)

# --------------------------------------------------
# MODEL (FREEZE BACKBONE)
# --------------------------------------------------

model = models.efficientnet_b0(weights=models.EfficientNet_B0_Weights.DEFAULT)

for param in model.features.parameters():
    param.requires_grad = False

model.classifier[1] = nn.Linear(
    model.classifier[1].in_features,
    num_classes
)

model = model.to(DEVICE)

criterion = nn.CrossEntropyLoss()
optimizer = torch.optim.Adam(
    model.classifier.parameters(),
    lr=LR
)

# --------------------------------------------------
# TRAINING LOOP
# --------------------------------------------------

for epoch in range(EPOCHS):
    model.train()
    running_loss = 0.0

    loop = tqdm(train_loader, desc=f"{CATEGORY.upper()} Epoch {epoch+1}/{EPOCHS}")

    for images, labels in loop:
        images = images.to(DEVICE)
        labels = labels.to(DEVICE)

        optimizer.zero_grad()
        outputs = model(images)
        loss = criterion(outputs, labels)
        loss.backward()
        optimizer.step()

        running_loss += loss.item()
        loop.set_postfix(loss=loss.item())

    avg_loss = running_loss / len(train_loader)
    print(f"{CATEGORY.upper()} | Epoch {epoch+1}/{EPOCHS} | Avg Loss: {avg_loss:.4f}")

# --------------------------------------------------
# SAVE MODEL + CLASS MAP
# --------------------------------------------------

model_path = os.path.join(MODEL_DIR, f"{CATEGORY}_model.pt")
torch.save(model.state_dict(), model_path)

class_map = {str(i): cls for i, cls in enumerate(train_ds.classes)}
with open(os.path.join(MODEL_DIR, f"{CATEGORY}_classes.json"), "w") as f:
    json.dump(class_map, f, indent=2)

print(f"✅ {CATEGORY} model saved to {model_path}")
