
import csv
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_FILE = PROJECT_ROOT / "data" / "sample" / "production_data.csv"


def validate_production_data():
    with open(DATA_FILE, "r", encoding="utf-8") as file:
        records = list(csv.DictReader(file))

    errors = []

    # Check 1: Empty dataset
    if not records:
        errors.append("Dataset is empty.")

    # Check 2: Duplicate records
    unique_records = set()

    for index, row in enumerate(records, start=2):

        # Check empty fields
        if any(not value.strip() for value in row.values()):
            errors.append(f"Empty field found at row {index}.")

        # Check duplicate records
        record_key = (
            row["production_date"],
            row["production_line"],
        )

        if record_key in unique_records:
            errors.append(f"Duplicate record at row {index}.")
        else:
            unique_records.add(record_key)

        produced = int(row["produced_units"])
        rejected = int(row["rejected_units"])
        good = int(row["good_units"])

        # Check production consistency
        if rejected > produced:
            errors.append(f"Rejected units exceed production at row {index}.")

        if good != produced - rejected:
            errors.append(f"Incorrect good units at row {index}.")

        # Check negative costs
        for field in ["material_cost", "labor_cost", "energy_cost", "total_cost"]:
            if float(row[field]) < 0:
                errors.append(f"Negative {field} at row {index}.")

    if errors:
        print("DATA QUALITY CHECK: FAILED")
        for error in errors:
            print(error)
    else:
        print("DATA QUALITY CHECK: PASSED")
        print(f"Records validated: {len(records)}")
        print("All checks passed successfully.")


if __name__ == "__main__":
    validate_production_data()

