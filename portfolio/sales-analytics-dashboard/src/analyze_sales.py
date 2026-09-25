from pathlib import Path
import csv
from collections import defaultdict

BASE_DIR = Path(__file__).resolve().parents[1]
DATA_FILE = BASE_DIR / "data" / "sample_sales.csv"
OUTPUT_DIR = BASE_DIR / "output"

REQUIRED_COLUMNS = {
    "date",
    "order_id",
    "client",
    "salesperson",
    "product",
    "category",
    "units",
    "unit_price",
    "unit_cost",
}


def load_sales(path: Path):
    with path.open("r", encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)
        missing = REQUIRED_COLUMNS - set(reader.fieldnames or [])
        if missing:
            raise ValueError(f"Missing required columns: {sorted(missing)}")
        return list(reader)


def analyze(rows):
    totals = {
        "revenue": 0.0,
        "cost": 0.0,
        "profit": 0.0,
        "units": 0,
    }
    by_product = defaultdict(float)
    by_salesperson = defaultdict(float)
    by_month = defaultdict(float)

    for row in rows:
        units = int(row["units"])
        unit_price = float(row["unit_price"])
        unit_cost = float(row["unit_cost"])
        revenue = units * unit_price
        cost = units * unit_cost
        profit = revenue - cost

        totals["revenue"] += revenue
        totals["cost"] += cost
        totals["profit"] += profit
        totals["units"] += units

        by_product[row["product"]] += revenue
        by_salesperson[row["salesperson"]] += revenue
        by_month[row["date"][:7]] += revenue

    totals["margin"] = totals["profit"] / totals["revenue"] if totals["revenue"] else 0
    return totals, by_product, by_salesperson, by_month


def write_mapping(path: Path, key_name: str, value_name: str, mapping):
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([key_name, value_name])
        for key, value in sorted(mapping.items(), key=lambda x: x[1], reverse=True):
            writer.writerow([key, round(value, 2)])


def main():
    rows = load_sales(DATA_FILE)
    totals, by_product, by_salesperson, by_month = analyze(rows)

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    with (OUTPUT_DIR / "kpis.csv").open("w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["metric", "value"])
        writer.writerow(["revenue", round(totals["revenue"], 2)])
        writer.writerow(["cost", round(totals["cost"], 2)])
        writer.writerow(["profit", round(totals["profit"], 2)])
        writer.writerow(["margin", round(totals["margin"], 4)])
        writer.writerow(["units", totals["units"]])

    write_mapping(OUTPUT_DIR / "sales_by_product.csv", "product", "revenue", by_product)
    write_mapping(OUTPUT_DIR / "sales_by_salesperson.csv", "salesperson", "revenue", by_salesperson)

    with (OUTPUT_DIR / "sales_by_month.csv").open("w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["month", "revenue"])
        for month, value in sorted(by_month.items()):
            writer.writerow([month, round(value, 2)])

    print("Analysis complete")
    print(f"Revenue: ${totals['revenue']:,.2f}")
    print(f"Profit: ${totals['profit']:,.2f}")
    print(f"Margin: {totals['margin']:.1%}")
    print(f"Units: {totals['units']:,}")


if __name__ == "__main__":
    main()
