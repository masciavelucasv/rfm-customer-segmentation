# -*- coding: utf-8 -*-
"""
Created on Mon Nov 17 17:36:00 2025

@author: masci
"""

# -*- coding: utf-8 -*-
"""
RFM Customer Segmentation
Author: masciavelucasv
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# 1. LOAD DATA 
df = pd.read_csv("online_retail.csv", encoding="latin1")

# 2. DATA CLEANING
df.columns = df.columns.str.lower().str.strip().str.replace(" ", "_")

df = df.dropna(subset=["description"])
df = df.dropna(subset=["customerid"])
df = df[df["quantity"] > 0]

df["invoicedate"] = pd.to_datetime(df["invoicedate"])

# Create output folder
if not os.path.exists("images"):
    os.makedirs("images")

# 3. RFM CALCULATION
ref_date = df["invoicedate"].max() + pd.Timedelta(days=1)

df["totalamount"] = df["quantity"] * df["unitprice"]

rfm = (
    df.groupby("customerid")
    .agg(
        recency=("invoicedate", lambda x: (ref_date - x.max()).days),
        frequency=("invoiceno", "nunique"),
        monetary=("totalamount", "sum"),
    )
    .reset_index()
)

# 4. RFM SCORES
rfm["R_score"] = pd.qcut(rfm["recency"], 4, labels=[4, 3, 2, 1]).astype(int)
rfm["F_score"] = pd.qcut(rfm["frequency"].rank(method="first"), 4,
                         labels=[1, 2, 3, 4]).astype(int)
rfm["M_score"] = pd.qcut(rfm["monetary"].rank(method="first"), 4,
                         labels=[1, 2, 3, 4]).astype(int)

rfm["RFM_score"] = (
    rfm["R_score"].astype(str)
    + rfm["F_score"].astype(str)
    + rfm["M_score"].astype(str)
)

# 5. CUSTOMER SEGMENTATION
def segment_customer(r):
    R = r["R_score"]
    F = r["F_score"]
    M = r["M_score"]

    if R >= 3 and F >= 3 and M >= 3:
        return "Champions"
    elif R >= 3 and F >= 2:
        return "Loyal"
    elif R >= 2 and F <= 2:
        return "Potential Loyalist"
    elif R == 1 and F >= 3:
        return "At Risk"
    elif R == 1 and F <= 2:
        return "Lost"
    else:
        return "Others"


rfm["segment"] = rfm.apply(segment_customer, axis=1)

# 6. VISUALIZATIONS
plt.figure(figsize=(10, 5))
rfm["segment"].value_counts().plot(kind="bar")
plt.title("Customer Segments Distribution")
plt.ylabel("Number of Customers")
plt.savefig("images/segments_distribution.png")
plt.show()

plt.figure(figsize=(8, 6))
plt.scatter(rfm["recency"], rfm["frequency"], alpha=0.5)
plt.xlabel("Recency (days)")
plt.ylabel("Frequency")
plt.title("Recency vs Frequency")
plt.savefig("images/recency_vs_frequency.png")
plt.show()

plt.figure(figsize=(8, 6))
sns.heatmap(
    rfm.groupby("segment")[["recency", "frequency", "monetary"]].mean(),
    annot=True,
    cmap="Blues",
)
plt.title("RFM Metrics by Segment")
plt.savefig("images/rfm_heatmap.png")
plt.show()

# 7. EXPORT OUTPUT
rfm.to_csv("rfm_output.csv", index=False)

print("RFM analysis completed successfully.")
print("Output saved as rfm_output.csv")
print("Charts saved to /images folder.")
