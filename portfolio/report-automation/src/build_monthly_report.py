from pathlib import Path
import pandas as pd

REQUIRED_COLUMNS = {
    "date", "customer", "product", "units", "unit_price", "unit_cost"
}

INPUT_DIR = Path(__file__).resolve().parents[1] / "input"
OUTPUT_DIR = Path(__file__).resolve().parents[1] / "output"


def load_monthly_files() -> pd.DataFrame:
    files = sorted(INPUT_DIR.glob("*.csv"))
    if not files:
        raise FileNotFoundError("No CSV files found in the input folder.")

    frames = []
    for file in files:
        df = pd.read_csv(file)
        missing = REQUIRED_COLUMNS - set(df.columns)
        if missing:
            raise ValueError(f"{file.name} is missing columns: {sorted(missing)}")
        frames.append(df)

    data = pd.concat(frames, ignore_index=True)
    data["date"] = pd.to_datetime(data["date"])
    data["revenue"] = data["units"] * data["unit_price"]
    data["cost"] = data["units"] * data["unit_cost"]
    data["profit"] = data["revenue"] - data["cost"]
    data["margin"] = data["profit"] / data["revenue"].replace(0, pd.NA)
    return data


def build_report(data: pd.DataFrame) -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    monthly = (
        data.assign(month=data["date"].dt.to_period("M").astype(str))
        .groupby("month", as_index=False)
        .agg(revenue=("revenue", "sum"), cost=("cost", "sum"), profit=("profit", "sum"), units=("units", "sum"))
    )
    monthly["margin"] = monthly["profit"] / monthly["revenue"]

    customers = (
        data.groupby("customer", as_index=False)
        .agg(revenue=("revenue", "sum"), profit=("profit", "sum"), units=("units", "sum"))
        .sort_values("revenue", ascending=False)
    )

    products = (
        data.groupby("product", as_index=False)
        .agg(revenue=("revenue", "sum"), profit=("profit", "sum"), units=("units", "sum"))
        .sort_values("revenue", ascending=False)
    )

    monthly.to_csv(OUTPUT_DIR / "monthly_summary.csv", index=False)
    customers.to_csv(OUTPUT_DIR / "customer_summary.csv", index=False)
    products.to_csv(OUTPUT_DIR / "product_summary.csv", index=False)

    total_revenue = data["revenue"].sum()
    total_profit = data["profit"].sum()
    total_margin = total_profit / total_revenue if total_revenue else 0

    print(f"Revenue: ${total_revenue:,.2f}")
    print(f"Profit: ${total_profit:,.2f}")
    print(f"Margin: {total_margin:.1%}")
    print(f"Rows processed: {len(data):,}")


if __name__ == "__main__":
    build_report(load_monthly_files())
