*Catalog* Initial Exploration Findings
=====================================

Initial exploration steps of the *Catalog* dataset, including all code and visualizations, can be found in [0.02-catalog-initial-exploration.ipynb](../../notebooks/0.02-catalog-initial-exploration.ipynb)

# Objective
The purpose of this initial exploration is to gain an understanding of the catalog dataset, verify data, and build catalog-level insights.

# Dataset Overview
- **Source:** Square
- **Shape:** 66 rows. 75 columns.
- **Granularity:** One row per variation of menu item.
- **Key Features:** *Item Name* is the name of the menu item. *Variation Name* lists which variation of the item the row represents. *Categories* lists the category under which the item falls.

# Data Quality Checks
## Missingness (%)
- **Token:** 0
- **Item Name:** 0
- **Variation Name:** 0
- **SKU:** 100
- **Description:** 44
- **Categories:** 8
- **Reporting Category:** 8
- **SEO Title:** 33
- **SEO Description:** 32
- **Permalink:** 33
- **GTIN:** 100
- **Square Online Item Visibility:** 0
- **Item Type:** 0
- **Weight (lb):** 98
- **Social Media Link Title:** 100
- **Social Media Link Description:** 100
- **Shipping Enabled:** 14
- **Self-serve Ordering Enabled:** 17
- **Delivery Enabled:** 17
- **Pickup Enabled:** 17
- **Price:** 0
- **Online Sale Price:** 100
- **Archived:** 0
- **Sellable:** 100
- **Contains Alcohol:** 17
- **Stockabled:** 100
- **Auto Add Item to Check:** 0
- **Option Name 1:** 88
- **Option Value 1:** 88
- **Current Quantity:** 86
- **New Quantity:** 100
- **Stock Alert Enabled:** 97
- **Stock Alert Count:** 97
- **All Modifier Set Features:** 0
## Missingness Correlations
- Reporting Category and Categories
- Delivery-related columns: Shipping Enabled, Pickup Enabled, Delivery Enabled
## Static Columns
Static features have the same value for all rows.
- Weight (lb)
- Self-serve Ordering Enabled
- Archived
- Contains Alcohol
- Stock Alert Enabled BELLY RUBB - BBQ Ribs To Go & Catering
- Stock Alert Count BELLY RUBB - BBQ Ribs To Go & Catering
- Modifier Set - Are you OK with spicy food?
- Modifier Set - Choose the glaze for rack 4
- Modifier Set - Extra Toppings
- Modifier Set - Glazed Belly Bites
- Modifier Set - Half Rack Glaze
- Modifier Set - How about Pork Rib Bites (off the bone rib meat)?
- Modifier Set - How about some cheese on top?
- Modifier Set - Spicy sauce?
## Duplicates
There are no duplicate rows.

# Categories
**List of Categories:** Combos, Sides, Ribs, Dips, Sips, Desserts, Sandwiches, Bites, Party Package
**Category with Most Items:** Dips (14)
**Category with Least Items:** Desserts (2)
**Greatest Range in Category:** $187 (Party Package)

# Data Integrity Checks
* Variations representing greater quantity of items are priced higher.
* Prices for *side* version of items are less than prices of *full* version of same item.

# Next Steps
* This data will be used when standardizing *Item Name* and *Item Variation* while cleaning the *Orders* dataset.