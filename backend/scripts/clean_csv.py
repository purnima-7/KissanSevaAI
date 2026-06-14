import pandas as pd
import os
from unidecode import unidecode

RAW_CSV_DIR = "backend/data/raw_csv"
CLEAN_TEXT_DIR = "backend/data/cleaned_text"

os.makedirs(CLEAN_TEXT_DIR, exist_ok=True)

def clean_text(value):
    if pd.isna(value):
        return None
    value = str(value).strip()
    value = unidecode(value)          # remove weird unicode
    value = value.replace("_", " ")
    value = value.replace("-", " ")
    return value

def clean_csv(csv_path):
    df = pd.read_csv(csv_path)

    # Remove duplicate rows
    df = df.drop_duplicates()

    # Clean each column
    for col in df.columns:
        df[col] = df[col].apply(clean_text)

    return df
