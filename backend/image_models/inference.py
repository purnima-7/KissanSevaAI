import json
import torch
import torch.nn as nn
from torchvision import models, transforms
from PIL import Image

# --------------------------------------------------
# CONFIG
# --------------------------------------------------

DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")
IMAGE_SIZE = 224

TRANSFORM = transforms.Compose([
    transforms.Resize((IMAGE_SIZE, IMAGE_SIZE)),
    transforms.ToTensor(),
    transforms.Normalize(
        mean=[0.485, 0.456, 0.406],
        std=[0.229, 0.224, 0.225]
    )
])

# --------------------------------------------------
# LOAD MODEL
# --------------------------------------------------

def load_model(model_type: str, classes_path: str):
    """
    model_type: 'disease' or 'insect'
    classes_path: path to disease_classes.json or insect_classes.json
    """

    with open(classes_path, "r") as f:
        class_names = json.load(f)

    # Number of classes
    if isinstance(class_names, dict):
        num_classes = len(class_names)
    else:
        num_classes = len(class_names)

    # Build EfficientNet
    model = models.efficientnet_b0(weights=None)
    model.classifier[1] = nn.Linear(
        model.classifier[1].in_features,
        num_classes
    )

    model_path = f"backend/image_models/{model_type}_model.pt"

    model.load_state_dict(
        torch.load(model_path, map_location=DEVICE)
    )

    model.to(DEVICE)
    model.eval()

    return model, class_names

# --------------------------------------------------
# IMAGE PREDICTION
# --------------------------------------------------

def predict_image(image_path: str, model, class_names):
    """
    Returns:
        label (str)
        confidence (float %)
    """

    image = Image.open(image_path).convert("RGB")
    image = TRANSFORM(image).unsqueeze(0).to(DEVICE)

    with torch.no_grad():
        outputs = model(image)
        probs = torch.softmax(outputs, dim=1)
        confidence, index = torch.max(probs, dim=1)

    idx = index.item()

    # Handle both list & dict class mappings
    if isinstance(class_names, dict):
        label = class_names[str(idx)]
    else:
        label = class_names[idx]

    confidence = round(confidence.item() * 100, 2)
    return label, confidence
