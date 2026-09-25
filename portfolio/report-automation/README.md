# Automated Monthly Business Report

This project demonstrates how a repetitive monthly Excel/CSV reporting process can be automated with Python.

## Business problem

Small and medium-sized companies often spend hours every month copying sales files, recalculating KPIs and rebuilding the same management report.

## Solution

The script in this project:

1. loads all CSV files from an input folder,
2. validates the required columns,
3. combines monthly files,
4. calculates revenue, cost, profit and margin,
5. summarizes performance by month, customer and product,
6. exports management-ready CSV summaries.

## Typical client use cases

- recurring monthly sales report
- customer profitability report
- product performance report
- consolidation of files from multiple branches
- budget vs actual preparation
- preparation of clean data for Excel or Power BI

## Structure

```text
report-automation/
├── README.md
├── src/
│   └── build_monthly_report.py
├── input/
│   └── sample_month.csv
└── output/
    └── .gitkeep
```

## Run

```bash
python src/build_monthly_report.py
```

## Business value

The goal is to replace repetitive manual spreadsheet work with a repeatable process that can be run every month in seconds and then connected to an Excel or Power BI dashboard.

All sample data is fictional.
