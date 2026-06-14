from backend.image_models.inference import load_model, predict_image

MODEL_TYPE = "disease"
CLASSES_PATH = "backend/image_models/disease_classes.json"
IMAGE_PATH = "backend/data/imagedata/disease/val/rice_blast/BLAST9_134.jpg"

model, class_names = load_model(MODEL_TYPE, CLASSES_PATH)

label, confidence = predict_image(
    image_path=IMAGE_PATH,
    model=model,
    class_names=class_names
)

print("Prediction:", label)
print("Confidence:", confidence)
