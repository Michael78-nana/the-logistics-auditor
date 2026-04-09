# The "Last Mile" Logistics Auditor

**Client:** Veridi Logistics (Global E-Commerce Aggregator)  
**Deliverable:** Code Notebook & Insight Presentation

---

## A. Executive Summary
An audit of Veridi Logistics' delivery data reveals that approximately 8.8% of all delivered orders across Brazil arrived late. The impact on customer satisfaction is severe — Super Late deliveries (more than 5 days past the estimated date) averaged a review score of just 1.79 out of 5, compared to 4.29 for on-time orders. The problem is not nationwide: northeastern states, particularly Alagoas (AL) and Maranhão (MA), show disproportionately high late delivery rates of 24% and 20% respectively. Product categories such as audio equipment and seasonal supplies also emerge as consistently hard to ship on time, pointing to specific seller relationships that need urgent attention.

## B. Project Links
- **Link to Notebook:** *(logistics_auditor.ipynb)*
- **Link to HTML Export:** *(logistics_auditor.html)*
- **Link to Presentation:** *(https://docs.google.com/presentation/d/1Vdb9yv-kIyPHiRxsOxP6NDQZaIRJTKNh/edit?usp=sharing&ouid=105077676706585141384&rtpof=true&sd=true)*
- **Link to Dashboard:** (https://the-logistics-auditor-jnrkf8yde6ayvzcrq6jtfd.streamlit.app/)

## C. Technical Explanation

**Data Cleaning:**  
Date columns (`order_estimated_delivery_date` and `order_delivered_customer_date`) were converted to datetime format before any calculations. Orders with a status of `cancelled` or `unavailable` were excluded from the delay analysis since they were never delivered. For the category-level analysis, categories with fewer than 100 orders were filtered out to ensure statistical reliability.

**Candidate's Choice — Late Delivery Rate by Product Category:**  
Beyond geography, we investigated whether certain product categories are harder to ship on time than others. Audio equipment, fashion/underwear/beach items, and christmas supplies topped the list at around 13% late delivery rate. This adds direct business value — if specific categories consistently underperform, Veridi can work with sellers in those categories to improve lead times, packaging, or fulfilment processes, rather than treating the problem as purely a regional logistics issue.

---

## 1. Business Context
**Veridi Logistics** manages shipping for thousands of online sellers. Recently, the CEO has noticed a spike in negative customer reviews. She has a "gut feeling" that the problem isn't just that packages are late, but that the estimated delivery dates provided to customers are wildly inaccurate (i.e., we are over-promising and under-delivering).

She needs you to audit the delivery data to find the root cause. She specifically wants to know: **"Are we failing specific regions, or is this a nationwide problem?"**

Your job is to build a "Delivery Performance" audit tool that connects the dots between **Logistics Data** (when a package arrived) and **Customer Sentiment** (how they rated the experience).

## 2. The Data
You will use the **Olist E-Commerce Dataset**, a real commercial dataset from a Brazilian marketplace. This is a relational database dump, meaning the data is split across multiple CSV files.

* **Source:** [Kaggle - Olist Brazilian E-Commerce Dataset](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce)
* **Key Files Used:**
    * `olist_orders_dataset.csv`
    * `olist_order_reviews_dataset.csv`
    * `olist_customers_dataset.csv`
    * `olist_products_dataset.csv`
    * `olist_order_items_dataset.csv`
    * `product_category_name_translation.csv`

## 3. Tooling
- **Environment:** Jupyter Notebook (Anaconda)
- **Language:** Python 3
- **Libraries:** pandas, matplotlib

---

## 4. User Stories Completed

### Story 1: The Schema Builder
Loaded the Orders, Reviews, and Customers CSVs and joined them into a single master dataset of 99,992 rows. Verified that duplicate `order_id` values (551 found) were expected due to the one-to-many relationship between orders and reviews.

### Story 2: The "Real" Delay Calculator
Calculated `days_difference` between estimated and actual delivery dates. Classified orders as On Time (89,134), Late (3,631), and Super Late (4,242). Cancelled and unavailable orders were excluded.

### Story 3: The Geographic Heatmap
Calculated late delivery percentage per Brazilian state. Alagoas (AL) topped the list at 23.94%, followed by Maranhão (MA) at 19.56% — both northeastern states far from the main distribution centres.

### Story 4: The Sentiment Correlation
On Time orders averaged a review score of 4.29, Late orders 3.46, and Super Late orders just 1.79 — confirming that late deliveries are directly driving negative customer reviews.

### Bonus: The Translation Challenge
Mapped Portuguese product category names to English using `product_category_name_translation.csv`, enabling category-level analysis accessible to a global audience.

### Candidate's Choice: Late Delivery Rate by Product Category
Identified the top 15 product categories with the highest late delivery rates. Audio, fashion_underwear_beach, and christmas_supplies led at ~13%, giving Veridi actionable insight beyond regional patterns.

---

## 🛑 Pre-Submission Checklist

### 1. Repository & Code Checks
- [ ] My GitHub Repo is Public.
- [ ] I have uploaded the `.ipynb` notebook file.
- [ ] I have ALSO uploaded an HTML export of the notebook.
- [ ] I have NOT uploaded the raw dataset CSVs.
- [ ] My code uses Relative Paths.

### 2. Deliverable Checks
- [ ] My Presentation link is publicly accessible.
- [ ] I have updated this `README.md` file with my Executive Summary and technical notes.

### 3. Completeness
- [ ] I have completed User Stories 1–4.
- [ ] I have completed the Candidate's Choice challenge and explained it above.