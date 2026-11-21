
import streamlit as st
import pandas as pd
import sqlite3
from pathlib import Path

# Dashboard configuration
st.set_page_config(
    page_title="RFP-to-PO Procurement Analytics",
    page_icon="📊",
    layout="wide"
)

st.title("RFP-to-PO Buyer Procurement Analytics Dashboard")
st.write("Procurement cycle performance and supplier analytics")

# Connect to SQLite database
project_dir = Path(__file__).resolve().parent.parent
db_path = project_dir / "database" / "procurement.db"

with sqlite3.connect(db_path) as conn:
    df = pd.read_sql_query("SELECT * FROM procurement", conn)


# Interactive Procurement Category Filter
st.sidebar.header("Dashboard Filters")

selected_categories = st.sidebar.multiselect(
    "Select Procurement Categories",
    options=sorted(df["category"].unique()),
    default=sorted(df["category"].unique())
)


# Buyer Filter
selected_buyers = st.sidebar.multiselect(
    "Select Buyers",
    options=sorted(df["buyer"].unique()),
    default=sorted(df["buyer"].unique())
)

# Supplier Filter
selected_suppliers = st.sidebar.multiselect(
    "Select Suppliers",
    options=sorted(df["supplier"].unique()),
    default=sorted(df["supplier"].unique())
)


# RFP Date Range Filter
df["rfp_date"] = pd.to_datetime(df["rfp_date"])

min_date = df["rfp_date"].min().date()
max_date = df["rfp_date"].max().date()

selected_dates = st.sidebar.date_input(
    "Select RFP Date Range",
    value=(min_date, max_date),
    min_value=min_date,
    max_value=max_date
)

# Apply filter to dashboard data

df = df[
    df["category"].isin(selected_categories)
    & df["buyer"].isin(selected_buyers)
    & df["supplier"].isin(selected_suppliers)
].copy()


# Apply selected date range
if len(selected_dates) == 2:
    start_date, end_date = selected_dates

    df = df[
        (df["rfp_date"].dt.date >= start_date)
        & (df["rfp_date"].dt.date <= end_date)
    ].copy()


# Calculate procurement KPIs
total_rfps = len(df)
avg_cycle_time = df["rfp_to_po_cycle_days"].mean()
total_savings = df["negotiated_savings"].sum()
avg_supplier_response = df["supplier_response_days"].mean()


# SLA Compliance Calculation
SLA_TARGET_DAYS = 25

sla_compliant = (
    df["rfp_to_po_cycle_days"] <= SLA_TARGET_DAYS
).sum()

sla_compliance_rate = (
    sla_compliant / len(df) * 100
    if len(df) > 0 else 0
)


# Display KPI cards
col1, col2, col3, col4 = st.columns(4)

col1.metric("Total RFPs", f"{total_rfps:,}")
col2.metric("Avg RFP-to-PO Cycle", f"{avg_cycle_time:.2f} days")
col3.metric("Negotiated Savings", f"${total_savings:,.2f}")
col4.metric("Avg Supplier Response", f"{avg_supplier_response:.2f} days")


# SLA Compliance KPI
st.metric(
    "SLA Compliance (25-Day Target)",
    f"{sla_compliance_rate:.1f}%"
)

st.divider()

st.subheader("Procurement Records")
st.dataframe(df, use_container_width=True)

# Download Filtered Procurement Data
csv_data = df.to_csv(index=False).encode("utf-8")

st.download_button(
    label="📥 Download Procurement Data (CSV)",
    data=csv_data,
    file_name="filtered_procurement_data.csv",
    mime="text/csv",
    disabled=df.empty
)


# Buyer Productivity Chart
st.subheader("Buyer Productivity Analysis")

buyer_productivity = (
    df.groupby("buyer")
    .size()
    .reset_index(name="Total RFPs")
)

st.bar_chart(
    buyer_productivity,
    x="buyer",
    y="Total RFPs"
)


# Supplier Performance Analysis
st.subheader("Supplier Performance Analysis")

supplier_performance = (
    df.groupby("supplier")["supplier_response_days"]
    .mean()
    .round(2)
    .reset_index()
)

supplier_performance.columns = [
    "Supplier",
    "Average Response Days"
]

st.bar_chart(
    supplier_performance,
    x="Supplier",
    y="Average Response Days"
)


# RFP-to-PO Cycle Time Analysis
st.subheader("RFP-to-PO Cycle Time by Category")

cycle_time_analysis = (
    df.groupby("category")["rfp_to_po_cycle_days"]
    .mean()
    .round(2)
    .reset_index()
)

cycle_time_analysis.columns = [
    "Procurement Category",
    "Average Cycle Days"
]

st.bar_chart(
    cycle_time_analysis,
    x="Procurement Category",
    y="Average Cycle Days"
)


# Negotiated Savings Donut Chart
import plotly.express as px

st.subheader("Negotiated Savings by Procurement Category")

savings_analysis = (
    df.groupby("category", as_index=False)["negotiated_savings"]
    .sum()
)

fig_savings = px.pie(
    savings_analysis,
    names="category",
    values="negotiated_savings",
    hole=0.5,
    title="Distribution of Negotiated Savings",
    color="category"
)

fig_savings.update_traces(
    textinfo="percent+label",
    hovertemplate="%{label}<br>Savings: $%{value:,.2f}<extra></extra>"
)

st.plotly_chart(fig_savings, use_container_width=True)


# Monthly Procurement Cycle Time Trend
st.subheader("Monthly RFP-to-PO Cycle Time Trend")

# Convert RFP dates to datetime
df["rfp_date"] = pd.to_datetime(df["rfp_date"])

# Calculate average cycle time by month
monthly_cycle = (
    df.assign(month=df["rfp_date"].dt.to_period("M").astype(str))
    .groupby("month", as_index=False)["rfp_to_po_cycle_days"]
    .mean()
)

monthly_cycle["rfp_to_po_cycle_days"] = (
    monthly_cycle["rfp_to_po_cycle_days"].round(2)
)

# Create interactive line chart
fig_cycle = px.line(
    monthly_cycle,
    x="month",
    y="rfp_to_po_cycle_days",
    markers=True,
    title="Average Procurement Cycle Time by Month",
    labels={
        "month": "Month",
        "rfp_to_po_cycle_days": "Average Cycle Time (Days)"
    }
)

fig_cycle.update_layout(
    xaxis_tickangle=-45,
    hovermode="x unified"
)

st.plotly_chart(fig_cycle, use_container_width=True)


# Procurement Value vs Cycle Time Scatter Plot
st.subheader("Procurement Value vs. Cycle Time")

fig_scatter = px.scatter(
    df,
    x="final_po_amount",
    y="rfp_to_po_cycle_days",
    color="category",
    size="negotiated_savings",
    hover_data=["rfp_id", "buyer", "supplier"],
    title="Purchase Order Value vs. Procurement Cycle Time",
    labels={
        "final_po_amount": "Purchase Order Value ($)",
        "rfp_to_po_cycle_days": "RFP-to-PO Cycle Time (Days)",
        "category": "Procurement Category"
    },
    opacity=0.7
)

fig_scatter.update_layout(
    hovermode="closest"
)

st.plotly_chart(fig_scatter, use_container_width=True)


# SLA Compliance Gauge Chart
import plotly.graph_objects as go

st.subheader("Procurement SLA Compliance")

fig_sla = go.Figure(
    go.Indicator(
        mode="gauge+number",
        value=sla_compliance_rate,
        number={"suffix": "%", "valueformat": ".1f"},
        title={"text": "RFP-to-PO SLA Compliance"},
        gauge={
            "axis": {"range": [0, 100]},
            "bar": {"color": "#2563EB"},
            "steps": [
                {"range": [0, 60], "color": "#FEE2E2"},
                {"range": [60, 80], "color": "#FEF3C7"},
                {"range": [80, 100], "color": "#DCFCE7"}
            ],
            "threshold": {
                "line": {"color": "#DC2626", "width": 4},
                "thickness": 0.75,
                "value": 90
            }
        }
    )
)

fig_sla.update_layout(
    height=350,
    margin=dict(l=30, r=30, t=60, b=20)
)

st.plotly_chart(fig_sla, use_container_width=True)
