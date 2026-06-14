import os
import pandas as pd
from clean_csv import clean_csv
from row_to_text import row_to_human_text

# Get project root directory
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

RAW_CSV_DIR = os.path.join(BASE_DIR, "data", "raw_csv")
OUTPUT_DIR = os.path.join(BASE_DIR, "data", "cleaned_text")

os.makedirs(OUTPUT_DIR, exist_ok=True)


def process_all_csvs():
    for file in os.listdir(RAW_CSV_DIR):
        if not file.endswith(".csv"):
            continue

        csv_path = os.path.join(RAW_CSV_DIR, file)
        df = clean_csv(csv_path)

        knowledge_blocks = []

        for _, row in df.iterrows():
            text = row_to_human_text(
                row.to_dict(),
                dataset_name=file.lower()
            )

            # ✅ COMPULSORY FIX FOR RAG
            # Do NOT filter by length
            if text and text.strip():
                knowledge_blocks.append(text)

        output_file = file.replace(".csv", ".txt")
        output_path = os.path.join(OUTPUT_DIR, output_file)

        with open(output_path, "w", encoding="utf-8") as f:
            f.write("\n\n---\n\n".join(knowledge_blocks))

        print(f"✅ Processed: {file}")


if __name__ == "__main__":
    process_all_csvs()
