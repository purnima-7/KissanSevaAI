def row_to_human_text(row: dict, dataset_name: str = "") -> str:
    lines = []

    # ---------------------------
    # Normalize column names ONCE
    # ---------------------------
    normalized = {}
    for k, v in row.items():
        if v is None or v == "":
            continue
        key = k.strip().lower().replace("_", " ")
        normalized[key] = v

    # Remove non-semantic junk
    for junk in ["index", "row", "unnamed: 0"]:
        normalized.pop(junk, None)

    # ---------------------------
    # Crop production dataset
    # ---------------------------
    if "crop" in dataset_name:
        FIELD_MAP = {
            "state name": "State",
            "district name": "District",
            "crop year": "Year",
            "season": "Season",
            "crop": "Crop",
            "area": "Area cultivated",
            "production": "Total production",
        }

        for key, label in FIELD_MAP.items():
            if key not in normalized:
                continue

            value = normalized[key]

            if key == "area":
                lines.append(f"{label}: {value} hectares")
            elif key == "production":
                lines.append(f"{label}: {value} tonnes")
            else:
                lines.append(f"{label}: {value}")

    # ---------------------------
    # Safe fallback for other datasets
    # ---------------------------
    else:
        for key, value in normalized.items():
            label = key.title()
            lines.append(f"{label}: {value}")

    return "\n".join(lines)
