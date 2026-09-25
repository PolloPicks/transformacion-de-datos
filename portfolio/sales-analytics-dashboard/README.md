# Sales Analytics Dashboard & Automation

This project demonstrates a practical analytics workflow for a small or medium-sized business that manages sales in spreadsheets.

## Business problem

Many businesses collect sales transactions in Excel but still need to manually calculate monthly sales, profit, margins, top products and salesperson performance.

This project turns raw transactional data into a repeatable analytics workflow.

## What the solution calculates

- Total revenue
- Total cost
- Gross profit
- Gross margin
- Units sold
- Monthly sales trend
- Revenue by product
- Revenue by salesperson

## Sample results

Using the fictional dataset included in this repository:

- Revenue: **$61,467 MXN**
- Gross profit: **$27,973 MXN**
- Gross margin: **45.5%**
- Units sold: **589**
- Top product by revenue: **Limpiador Multiusos 1L**

## Project structure

```text
sales-analytics-dashboard/
├── README.md
├── data/
│   └── sample_sales.csv
├── src/
│   └── analyze_sales.py
└── output/
    └── .gitkeep
```

## How to run

```bash
python src/analyze_sales.py
```

The script reads the fictional sample dataset, validates the required columns, calculates business KPIs and exports summary CSV files into the `output/` directory.

## Why this matters for a business

The same logic can be adapted to a real client's Excel or CSV files to automate repetitive reporting and produce a management dashboard in Excel or Power BI.

Typical extensions include:

- customer profitability
- branch comparison
- budget vs. actual
- inventory rotation
- recurring monthly reporting
- automated ingestion of new files

## Data privacy

All data in this project is fictional and created only for demonstration purposes.
