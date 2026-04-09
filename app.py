import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="The Last Mile Logistics Auditor", layout="wide")

st.title("🚚 The Last Mile Logistics Auditor")
st.markdown("**Client:** Veridi Logistics | **Dataset:** Olist Brazilian E-Commerce")

# ── Load & cache data ──────────────────────────────────────
@st.cache_data
def load_data():
    orders = pd.read_csv("olist_orders_dataset.csv")
    reviews = pd.read_csv("olist_order_reviews_dataset.csv")
    customers = pd.read_csv("olist_customers_dataset.csv")
    products = pd.read_csv("olist_products_dataset.csv")
    order_items = pd.read_csv("olist_order_items_dataset.csv")
    translation = pd.read_csv("product_category_name_translation.csv")

    master = pd.merge(orders, reviews, on="order_id", how="left")
    master = pd.merge(master, customers, on="customer_id", how="left")

    master["order_estimated_delivery_date"] = pd.to_datetime(master["order_estimated_delivery_date"])
    master["order_delivered_customer_date"] = pd.to_datetime(master["order_delivered_customer_date"])

    delivered = master[master["order_status"] == "delivered"].copy()
    delivered["days_difference"] = (
        delivered["order_estimated_delivery_date"] - delivered["order_delivered_customer_date"]
    ).dt.days

    def classify(days):
        if days >= 0:
            return "On Time"
        elif days >= -5:
            return "Late"
        else:
            return "Super Late"

    delivered["delivery_status"] = delivered["days_difference"].apply(classify)

    products_t = pd.merge(products, translation, on="product_category_name", how="left")
    items = pd.merge(order_items, products_t[["product_id", "product_category_name_english"]], on="product_id", how="left")
    items_delivery = pd.merge(items, delivered[["order_id", "delivery_status"]], on="order_id", how="inner")

    return delivered, items_delivery

delivered, items_delivery = load_data()

# ── KPI Row ────────────────────────────────────────────────
st.markdown("---")
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Delivered Orders", f"{len(delivered):,}")
col2.metric("On Time", f"{(delivered['delivery_status'] == 'On Time').sum():,}")
col3.metric("Late", f"{(delivered['delivery_status'] == 'Late').sum():,}")
col4.metric("Super Late", f"{(delivered['delivery_status'] == 'Super Late').sum():,}")

st.markdown("---")

# ── Row 1: Delay Distribution & Sentiment ─────────────────
col1, col2 = st.columns(2)

with col1:
    st.subheader("Delivery Status Distribution")
    counts = delivered["delivery_status"].value_counts()
    fig, ax = plt.subplots()
    ax.bar(counts.index, counts.values, color=["#02C39A", "#F4A261", "#E63946"])
    ax.set_ylabel("Number of Orders")
    ax.set_title("On Time vs Late vs Super Late")
    st.pyplot(fig)

with col2:
    st.subheader("Average Review Score by Delivery Status")
    sentiment = delivered.groupby("delivery_status")["review_score"].mean().reindex(["On Time", "Late", "Super Late"])
    fig, ax = plt.subplots()
    ax.bar(sentiment.index, sentiment.values, color=["#02C39A", "#F4A261", "#E63946"])
    ax.set_ylim(0, 5)
    ax.set_ylabel("Average Review Score")
    ax.set_title("How Delays Affect Customer Satisfaction")
    for i, v in enumerate(sentiment.values):
        ax.text(i, v + 0.05, f"{v:.2f}", ha="center", fontweight="bold")
    st.pyplot(fig)

st.markdown("---")

# ── Row 2: Geographic ─────────────────────────────────────
st.subheader("Late Delivery Rate by State")
delivered["is_late"] = delivered["delivery_status"] != "On Time"
state_summary = delivered.groupby("customer_state").agg(
    total=("order_id", "count"),
    late=("is_late", "sum")
).reset_index()
state_summary["late_pct"] = (state_summary["late"] / state_summary["total"] * 100).round(2)
state_summary = state_summary.sort_values("late_pct", ascending=False)

fig, ax = plt.subplots(figsize=(14, 5))
ax.bar(state_summary["customer_state"], state_summary["late_pct"], color="#E63946")
ax.set_xlabel("State")
ax.set_ylabel("% Late Deliveries")
ax.set_title("Late Delivery Rate by Brazilian State")
plt.xticks(rotation=45)
plt.tight_layout()
st.pyplot(fig)

st.markdown("---")

# ── Row 3: Category ───────────────────────────────────────
st.subheader("Late Delivery Rate by Product Category")
items_delivery["is_late"] = items_delivery["delivery_status"] != "On Time"
cat_summary = items_delivery.groupby("product_category_name_english").agg(
    total=("order_id", "count"),
    late=("is_late", "sum")
).reset_index()
cat_summary["late_pct"] = (cat_summary["late"] / cat_summary["total"] * 100).round(2)
cat_summary = cat_summary[cat_summary["total"] >= 100].sort_values("late_pct", ascending=False).head(15)

fig, ax = plt.subplots(figsize=(12, 5))
ax.bar(cat_summary["product_category_name_english"], cat_summary["late_pct"], color="#F4A261")
ax.set_ylabel("% Late Deliveries")
ax.set_title("Top 15 Product Categories by Late Delivery Rate")
plt.xticks(rotation=45, ha="right")
plt.tight_layout()
st.pyplot(fig)