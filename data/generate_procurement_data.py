
import pandas as pd
import random
from datetime import datetime, timedelta
from pathlib import Path

random.seed(42)

buyers = ["Buyer A", "Buyer B", "Buyer C", "Buyer D", "Buyer E"]

suppliers = [
    "Supplier Alpha",
    "Supplier Beta",
    "Supplier Gamma",
    "Supplier Delta",
    "Supplier Omega"
]

categories = [
    "IT Equipment",
    "Raw Materials",
    "Packaging",
    "Maintenance",
    "Logistics"
]

records = []

for i in range(1, 501):
    rfp_date = datetime(2025, 1, 1) + timedelta(
        days=random.randint(0, 500)
    )

    response_days = random.randint(2, 15)
    evaluation_days = random.randint(1, 10)
    negotiation_days = random.randint(1, 8)
    approval_days = random.randint(1, 7)

    proposal_date = rfp_date + timedelta(days=response_days)
    evaluation_date = proposal_date + timedelta(days=evaluation_days)
    negotiation_date = evaluation_date + timedelta(days=negotiation_days)
    po_date = negotiation_date + timedelta(days=approval_days)

    initial_estimate = round(random.uniform(5000, 100000), 2)
    final_amount = round(
        initial_estimate * random.uniform(0.85, 1.0), 2
    )

    records.append({
        "rfp_id": f"RFP-{i:04d}",
        "buyer": random.choice(buyers),
        "supplier": random.choice(suppliers),
        "category": random.choice(categories),
        "rfp_date": rfp_date.date(),
        "proposal_date": proposal_date.date(),
        "evaluation_date": evaluation_date.date(),
        "negotiation_date": negotiation_date.date(),
        "po_date": po_date.date(),
        "supplier_response_days": response_days,
        "evaluation_days": evaluation_days,
        "negotiation_days": negotiation_days,
        "approval_days": approval_days,
        "rfp_to_po_cycle_days": (po_date - rfp_date).days,
        "initial_estimate": initial_estimate,
        "final_po_amount": final_amount,
        "negotiated_savings": round(initial_estimate - final_amount, 2)
    })

df = pd.DataFrame(records)

output = Path(__file__).resolve().parent / "procurement_data.csv"
df.to_csv(output, index=False)

print("Procurement data generated successfully!")
print("Total RFP records:", len(df))
print("Saved to:", output)
