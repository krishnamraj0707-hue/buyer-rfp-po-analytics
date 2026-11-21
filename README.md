
# RFP-to-PO Buyer Procurement Analytics Dashboard

An interactive procurement analytics dashboard built using Python, SQL, Streamlit, and Plotly to analyze the Request for Proposal (RFP) to Purchase Order (PO) lifecycle.

## Live Dashboard

[View Interactive Dashboard](https://buyer-rfp-po-analytics-pw5mwwiyxt8mbuvfykhsn5.streamlit.app/)

## Project Overview

This project demonstrates how procurement data can be analyzed to monitor purchasing efficiency, supplier responsiveness, buyer productivity, and negotiated savings.

The dashboard uses 500 synthetically generated procurement records stored in a SQLite database.

**Procurement Workflow:**

RFP Creation → Supplier Response → Evaluation → Negotiation → Approval → Purchase Order

## Technology Stack

- Python
- Pandas
- SQLite / SQL
- Streamlit
- Plotly
- Git and GitHub

## Key Performance Indicators

1. Total RFPs
2. Average RFP-to-PO Cycle Time
3. Total Negotiated Savings
4. Average Supplier Response Time
5. SLA Compliance (25-Day Target)

## Dashboard Visualizations

1. Buyer Productivity Analysis — Bar Chart
2. Supplier Performance Analysis — Bar Chart
3. RFP-to-PO Cycle Time by Category — Bar Chart
4. Negotiated Savings by Category — Donut Chart
5. Monthly Procurement Cycle Time Trend — Line Chart
6. Procurement Value vs. Cycle Time — Scatter Plot
7. SLA Compliance — Gauge Chart

## Interactive Features

- Procurement category filter
- Buyer filter
- Supplier filter
- RFP date range filter
- Interactive Plotly visualizations
- Download filtered procurement records as CSV

## Data Pipeline

1. Generate synthetic procurement records using Python.
2. Save records to CSV.
3. Load procurement data into SQLite.
4. Query procurement records using SQL.
5. Calculate procurement KPIs using Pandas.
6. Visualize procurement performance using Streamlit and Plotly.

## Project Structure

```text
buyer-rfp-po-analytics/
├── dashboard/
│   └── app.py
├── data/
│   ├── generate_procurement_data.py
│   └── procurement_data.csv
├── database/
│   ├── create_database.py
│   └── procurement.db
├── processing/
├── requirements.txt
├── .gitignore
└── README.md
```

## Run Locally

Clone the repository:

```bash
git clone https://github.com/krishnamraj0707-hue/buyer-rfp-po-analytics.git
cd buyer-rfp-po-analytics
```

Install dependencies:

```bash
python -m pip install -r requirements.txt
```

Launch the dashboard:

```bash
python -m streamlit run dashboard/app.py
```

## Business Value

This dashboard demonstrates how procurement analytics can support:

- Monitoring procurement cycle efficiency
- Identifying supplier response delays
- Comparing buyer workloads
- Analyzing negotiated savings
- Tracking procurement SLA compliance
- Supporting data-driven purchasing decisions

## Data Disclaimer

All procurement records are synthetically generated for educational and portfolio demonstration purposes. They do not represent actual company transactions.

## Author

Krishnam Raj Jatoth

[GitHub Profile](https://github.com/krishnamraj0707-hue)
