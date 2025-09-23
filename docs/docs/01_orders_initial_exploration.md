*Orders* Initial Exploration Findings
====================================

Initial exploration steps of the *Orders* dataset, including all code and visualizations, can be found in [0.01-orders-initial-exploration.ipynb](../../notebooks/0.01-orders-initial-exploration.ipynb).

# Objective
The purpose of this initial exploration was to evaluate data integrity, gain an overall understanding of the data and its relationship to business logic, and investigate both time-based and customer-based patterns.

# Dataset Overview
- **Source:** Square
- **Shape:** Rows: 4028, Columns: 32
- **Granularity:** One row per menu item per order
- **Key Features:** *Item* columns provide item-based insights. *Recipient* columns provide information about customers. *Order* columns provide monetary and date information about each order.

# Data Quality Checks
## Missingness (%)
- **Order:** 2
- **Order Name:** 0.45
- **Order Date:** 0
- **Currency:** 0
- **Order Subtotal:** 0
- **Order Shipping Price:** 100
- **Order Tax Total:** 0
- **Order Total:** 0
- **Order Refunded Amount:** 100
- **Fulfillment Date:** 26
- **Fulfillment Type:** 26
- **Fulfillment Status:** 26
- **Channels:** 1
- **Fulfillment Location:** 0
- **Fulfillment Notes:** 87
- **Recipient Name:** 26
- **Recipient Email:** 50
- **Recipient Phone:** 26
- **Recipient Address:** 87
- **Recipient Address 2:** 98
- **Recipient Postal Code:** 87
- **Recipient City:** 87
- **Recipient Region:** 87
- **Recipient Country:** 77
- **Item Quantity:** 0
- **Item Name:** 0.04
- **Item SKU:** 100
- **Item Variation:** 0.04
- **Item Modifiers:** 42
- **Item Price:** 0
- **Item Options Total Price:** 0
- **Item Total Price:** 0
## Static Columns
Static columns have the same value for every row. Static features: **Currency**, **Fulfillment Location**, and **Recipient Region**.
## Duplicates
There are no duplicate rows.
## Outliers
Outlier detection is based on **IQR**.
### Order Total
- 6.23% are outliers.
- These constitute very large orders, such as catering orders, and **not** data entry mistakes.
### Item Price
- 2.83% are outliers.
- Include catering packages, platters, bundles, and expensive combos.
- **1** row is missing *Item Price* along with much other data.
- Outlier rows also have outlier *Item Options Total Price* values.
# Insights
## Customer-Level Insights
- **Unique Customers**: 822
### Repeat Customers
Repeat customers are categorized as customers who order more than once.
- **Repeat Customers:** 89
- **Percentage of Total Customers:** 10.87%
- **Order Rate:** 60% ordered 2 times, 80% ordered 4 or less times.
- **Days Between Orders:** Mean days: 54. Median days: 35.

## Product-Level Insights
- **Top Product Based on Quantity:** Glazed Baby Back Pork Ribs
- **Worst Product Based on Quantity:** Pineapple Coleslaw
- **Top Product Based on Revenue:** Glazed Baby Back Pork Ribs
- **Worst Product Based on Revenue:** Pickled Jalapenos

## Business-Level Insights
- **Total Sales:** $90,341.63
- **Total Orders:** 1,432
- **Average Sale Amount:** $63.08
- **Median Sale Amount:** $50.44
- **Maximum Sale Amount:** $1,158.75
- **Minimum Sale Amount:** $1.00

## Menu-Level Insights
- **Categories:** Combos, Sides, Ribs, Dips, Sips, Desserts, Sandwiches, Bites, and Party Packages.
- There are significant discrepencies in *Item Name* and *Item Variation* between orders of the same item. These features will need to be standardized.

# Time-Based Patterns
- **Day with Most Orders (mean and median):** Friday
- **Days with Least Orders (mean and median):** Wednesdays, Thursdays, and Saturdays
- **Peak Order Time (mean and median):** 7pm
- **Seasonality:** Weekly
- Not enough data to confirm *monthly* seasonality.

# Next Steps
Planned cleaning actions:
* Standardizing *Item Name* and *Item Variation*.
* Drop static columns.
* Drop fully empty columns.
* Features with significantly high missing rates will be dropped for modeling but kept for EDA.
* Features with low missing rates will be imputed.
* Drop insignificant columns
    * *Fulfillment Notes* does not contain valuable information for modeling or analysis.
    * *Recipient Country* because although it has multiple values, the business only serves food in the US.
* Aggregate rows to represent individual orders rather than individual menu items per order.
