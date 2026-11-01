
import csv
import random
from datetime import date, timedelta
from pathlib import Path

# Reproducible random data
random.seed(42)

# Project directories
PROJECT_ROOT = Path(__file__).resolve().parents[1]
OUTPUT_DIR = PROJECT_ROOT / "data" / "sample"
OUTPUT_FILE = OUTPUT_DIR / "production_data.csv"

# Industrial simulation settings
PLANT = "Plant_01"

PRODUCTION_LINES = {
    "Line_A": {"product": "Wine_Bottle_750ml", "unit_cost": 1.25},
    "Line_B": {"product": "Wine_Bottle_500ml", "unit_cost": 1.10},
    "Line_C": {"product": "Wine_Box_3L", "unit_cost": 2.40},
}

SHIFTS = ["Morning", "Afternoon", "Night"]

START_DATE = date(2025, 1, 1)
DAYS_TO_GENERATE = 365


def generate_production_data():
    """Generate simulated daily industrial production records."""

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    records = []

    for day in range(DAYS_TO_GENERATE):
        production_date = START_DATE + timedelta(days=day)

        for line, config in PRODUCTION_LINES.items():

            planned_units = random.randint(800, 1200)

            production_factor = random.uniform(0.85, 1.08)
            produced_units = int(planned_units * production_factor)

            rejected_units = int(
                produced_units * random.uniform(0.01, 0.05)
            )

            good_units = produced_units - rejected_units

            downtime_minutes = random.randint(0, 120)
            labor_hours = round(random.uniform(18, 24), 2)

            material_cost = produced_units * config["unit_cost"]
            labor_cost = labor_hours * 12
            energy_cost = random.uniform(80, 180)

            total_cost = (
                material_cost + labor_cost + energy_cost
            )

            records.append({
                "production_date": production_date.isoformat(),
                "plant": PLANT,
                "production_line": line,
                "product": config["product"],
                "shift": random.choice(SHIFTS),
                "planned_units": planned_units,
                "produced_units": produced_units,
                "rejected_units": rejected_units,
                "good_units": good_units,
                "downtime_minutes": downtime_minutes,
                "labor_hours": labor_hours,
                "material_cost": round(material_cost, 2),
                "labor_cost": round(labor_cost, 2),
                "energy_cost": round(energy_cost, 2),
                "total_cost": round(total_cost, 2),
            })

    fieldnames = records[0].keys()

    with open(OUTPUT_FILE, "w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(records)

    print(f"Data generated successfully: {OUTPUT_FILE}")
    print(f"Total records: {len(records)}")


if __name__ == "__main__":
    generate_production_data()
