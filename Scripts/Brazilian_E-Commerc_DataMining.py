#!/usr/bin/env python
# coding: utf-8

# # Import libraries

# In[1]:


import pandas as pd

from sqlalchemy import (
    create_engine, MetaData, Table, Column,
    String, Integer, ForeignKey
)


# ---
# # 1. Data Ingestion

# In[2]:


# Declare csv data types
dtypes_dict = {
    "customer_id": "string",
    "customer_unique_id": "string",
    "customer_zip_code_prefix": "Int64",
    "customer_city": "string",
    "customer_state": "string"
}

customers_df = pd.read_csv("../Data/csvs/olist_customers_dataset.csv", dtype=dtypes_dict)
customers_df.name = "customers"
# customers_df.dtypes


# In[3]:


# Declare csv data types
dtypes_dict = {
    "geolocation_zip_code_prefix": "Int64",
    "geolocation_lat": "Float64",
    "geolocation_lng": "Float64",
    "geolocation_city": "string",
    "geolocation_state": "string"
}

geolocation_df = pd.read_csv("../Data/csvs/olist_geolocation_dataset.csv", dtype=dtypes_dict)
geolocation_df.name = "geolocation"
# geolocation_df.dtypes


# In[4]:


# Declare csv data types
dtypes_dict = {
    "order_id": "string",
    "order_item_id": "Int64",
    "product_id": "string",
    "seller_id": "string",
    "shipping_limit_date": "string",
    "price": "Float64",
    "freight_value": "Float64"
}

# It is not expected to have wrong dates format, so the conversion can be at reading
dates_columns = [
        "shipping_limit_date"
    ]

order_items_df = pd.read_csv(
    "../Data/csvs/olist_order_items_dataset.csv", 
    dtype=dtypes_dict,
    parse_dates=dates_columns
)
order_items_df.name = "order_items"
# order_items_df.dtypes


# In[5]:


# Declare csv data types
dtypes_dict = {
    "order_id": "string",
    "payment_sequential": "Int64",
    "payment_type": "string",
    "payment_installments": "Int64",
    "payment_value": "Float64"
}

order_payments_df = pd.read_csv("../Data/csvs/olist_order_payments_dataset.csv", dtype=dtypes_dict)
order_payments_df.name = "order_payments"
# order_payments_df.dtypes


# In[6]:


# Declare csv data types
dtypes_dict = {
    "review_id": "string",
    "order_id": "string",
    "review_score": "Int64",
    "review_comment_title": "string",
    "review_comment_message": "string",
    "review_creation_date": "string",
    "review_answer_timestamp": "string"
}

# It is not expected to have wrong dates format, so the conversion can be at reading
dates_columns = [
        "review_creation_date", 
        "review_answer_timestamp"
    ]

order_reviews_df = pd.read_csv(
    "../Data/csvs/olist_order_reviews_dataset.csv", 
    dtype=dtypes_dict,
    parse_dates=dates_columns
)
order_reviews_df.name = "order_reviews"
# order_reviews_df.dtypes


# In[7]:


# Declare csv data types
dtypes_dict = {
    "order_id": "string",
    "customer_id": "string",
    "order_status": "string",
    "order_purchase_timestamp": "string",
    "order_approved_at": "string",
    "order_delivered_carrier_date": "string",
    "order_delivered_customer_date": "string",
    "order_estimated_delivery_date": "string"
}

# It is not expected to have wrong dates format, so the conversion can be at reading
dates_columns = [
        "order_purchase_timestamp",
        "order_approved_at", 
        "order_delivered_carrier_date", 
        "order_delivered_customer_date",
        "order_estimated_delivery_date"
    ]

orders_df = pd.read_csv(
    "../Data/csvs/olist_orders_dataset.csv", 
    dtype=dtypes_dict,
    parse_dates=dates_columns
)
orders_df.name = "orders"
# orders_df.dtypes


# In[8]:


# Declare csv data types
dtypes_dict = {
    "product_id": "string",
    "product_category_name": "string",
    "product_name_lenght": "Int64",
    "product_description_lenght": "Int64",
    "product_photos_qty": "Int64",
    "product_weight_g": "Int64",
    "product_length_cm": "Int64",
    "product_height_cm": "Int64",
    "product_width_cm": "Int64",
}

products_df = pd.read_csv("../Data/csvs/olist_products_dataset.csv", dtype=dtypes_dict)
products_df.name = "products"
# products_df.dtypes


# In[9]:


# Declare csv data types
dtypes_dict = {
    "seller_id": "string",
    "seller_zip_code_prefix": "Int64",
    "seller_city": "string",
    "seller_state": "string",
}

sellers_df = pd.read_csv("../Data/csvs/olist_sellers_dataset.csv", dtype=dtypes_dict)
sellers_df.name = "sellers"
# sellers_df.dtypes


# In[10]:


# Declare csv data types
dtypes_dict = {
    "product_category_name": "string",
    "product_category_name_english": "string"
}

product_category_name_translation_df = pd.read_csv("../Data/csvs/product_category_name_translation.csv", dtype=dtypes_dict)
product_category_name_translation_df.name = "product_category_name_translation"
# product_category_name_translation_df.dtypes


# In[11]:


# Create dataframes dictionary
dfs_dict = {
    customers_df.name: customers_df,
    geolocation_df.name: geolocation_df,
    order_items_df.name: order_items_df,
    order_payments_df.name: order_payments_df,
    order_reviews_df.name: order_reviews_df,
    orders_df.name: orders_df,
    products_df.name: products_df,
    sellers_df.name: sellers_df,
    product_category_name_translation_df.name: product_category_name_translation_df
}


# ---
# # 2. Data Quality Analysis

# ## 2.1. Missing data

# In[12]:


# Get what columns from which dataframes contains nulls
def check_nans(dfs_dict) -> None:
    for df in dfs_dict.values():
        nans_df = df.isna().sum()
        nans_df = nans_df[nans_df > 0]

        for column, quantity in nans_df.items():
            print(f"Nans in: {df.name} | Column: {column}. | Quantity: {quantity}")


# In[13]:


check_nans(dfs_dict)


# ## 2.2. Duplicates

# In[14]:


unique_fields_dict = {
    customers_df.name: ["customer_id"],
    geolocation_df.name: ["geolocation_zip_code_prefix"],
    order_reviews_df.name: ["review_id"],
    orders_df.name: ["order_id"],
    products_df.name: ["product_id"],
    sellers_df.name: ["seller_id"]
}

def find_duplicates(dfs_dict, unique_fields_dict) -> None:
    duplicated_dict = {}
    for name, columns in unique_fields_dict.items():
        for column in columns:
            temp_s = dfs_dict[name][column].duplicated(keep=False)
            temp_ar = temp_s[temp_s].index.array
            if (temp_ar.size > 0):
                duplicated_dict[name] = {column: temp_ar}

    return duplicated_dict


# In[15]:


duplicated_dict = find_duplicates(dfs_dict, unique_fields_dict)
duplicated_dict


# The tables **geolocation** and **order_reviews** seems to have duplicates. Now each one shall be inspected to decide the course of action.

# In[16]:


(
    dfs_dict["order_reviews"]
        .iloc[duplicated_dict["order_reviews"]["review_id"]]
        .sort_values(by="review_id")
        .head(15)
)


# In[17]:


(
    dfs_dict["geolocation"]
    .iloc[duplicated_dict["geolocation"]["geolocation_zip_code_prefix"]]
    .sort_values(by="geolocation_zip_code_prefix")
    .head(50)
)


# ---
# # 3. Data Cleaning and Transformation

# ## 3.1. Manage missing data
# In **orders** table is possible to have orders without comments, so values can stay null. For **products** with no category they are assigned "Unknown", the other fields values are set to -1 as a way to identify them in consults.

# In[18]:


def manage_nans(dfs_dict) -> None:
    dfs_dict[products_df.name] = dfs_dict[products_df.name].fillna({
        "product_category_name": "Unknown",
        "product_name_lenght": -1,
        "product_description_lenght": -1,
        "product_photos_qty": -1,
        "product_weight_g": -1,
        "product_length_cm": -1,
        "product_height_cm": -1,
        "product_width_cm": -1
    })


# In[19]:


manage_nans(dfs_dict)
check_nans(dfs_dict)


# ## 3.2. Manage Duplicates
# For these cases, duplicates seems to have the same information, so the first found value is kept and the rest deleted.

# In[20]:


dfs_dict["order_reviews"] = dfs_dict["order_reviews"].drop_duplicates(subset=["review_id"], keep="first")
dfs_dict["geolocation"] = dfs_dict["geolocation"].drop_duplicates(subset=["geolocation_zip_code_prefix"], keep="first")


# In[21]:


duplicated_dict = find_duplicates(dfs_dict, unique_fields_dict)
duplicated_dict


# ---
# # 4. Feature engineering
# 
# ## 4.1. Customers

# In[22]:


# Main dataframe where to read from in the next steps
main_customers_fe_df = (
    dfs_dict["customers"]
    .merge(dfs_dict["orders"], how="left", on="customer_id")
    .merge(dfs_dict["order_payments"], how="left", on="order_id")
    .merge(dfs_dict["order_items"], how="left", on="order_id")
    .merge(dfs_dict["order_reviews"], how="left", on="order_id")
)
main_customers_fe_df


# ### 4.1.1. Customer Lifetime Value (LTV) 
# It is the cumulative net value attributed to a customer from their first purchase to their last, including all transactions during that period.

# In[23]:


# Read orders money columns
temp_customers_fe_df = (
    main_customers_fe_df
    [["order_id", "order_item_id", "price", "freight_value", "payment_value"]]
    .copy()
)
# Create new columns and data
temp_customers_fe_df["order_value"] = (temp_customers_fe_df["price"] + temp_customers_fe_df["freight_value"]) * temp_customers_fe_df["order_item_id"]
temp_customers_fe_df["profit_based_LTV"] = (temp_customers_fe_df["payment_value"] - temp_customers_fe_df["order_value"])
temp_customers_fe_df = (
    temp_customers_fe_df[["order_id", "order_value", "payment_value", "profit_based_LTV"]]
    .groupby("order_id", as_index=False).sum()
    .sort_values(by="profit_based_LTV", ascending=False)
)
# Link the new data to its costumers
customers_fe_df = (
    temp_customers_fe_df[["order_id", "profit_based_LTV"]]
    .copy()
)
customers_fe_df = (
    customers_fe_df
    .merge(main_customers_fe_df[["order_id", "customer_unique_id"]], how="left", on="order_id")
    [["customer_unique_id", "profit_based_LTV"]]
    .groupby("customer_unique_id", as_index=False).mean()
    .sort_values(by="customer_unique_id", ascending=False)
)
customers_fe_df


# ### 4.1.2. Average order and payment value

# In[24]:


# Extract customers order and payment values 
temp_customers_fe_df = (
    temp_customers_fe_df
    .merge(main_customers_fe_df[["order_id", "customer_unique_id"]], how="left", on="order_id")
    [["customer_unique_id", "order_value", "payment_value"]]
    .groupby("customer_unique_id", as_index=False).sum()
    .sort_values(by="customer_unique_id", ascending=False)
)
customers_fe_df = (
    customers_fe_df
    .merge(temp_customers_fe_df, how="left", on="customer_unique_id")
)
customers_fe_df


# ### 4.1.3. Days since last purchase

# In[25]:


# Get last purchase per customer
temp_df = (
    main_customers_fe_df[["customer_unique_id", "order_purchase_timestamp"]]
    .groupby("customer_unique_id", as_index=False).max()
)
# Get last purchase
last_purchase_datetime = temp_df["order_purchase_timestamp"].max()
# Calculate costumers days
temp_df["days_since_purchase"] = (last_purchase_datetime - temp_df["order_purchase_timestamp"]).dt.days
temp_df = (
    temp_df[["customer_unique_id", "days_since_purchase"]]
    .groupby("customer_unique_id", as_index=False).min()
    .sort_values(by="customer_unique_id", ascending=False)
)
temp_df


# In[26]:


customers_fe_df = (
    customers_fe_df
    .merge(temp_df, how="left", on="customer_unique_id")
    .sort_values(by="customer_unique_id", ascending=False)
)
customers_fe_df


# ### 4.1.4. Average review score

# In[ ]:





# # Export to database
engine = create_engine("sqlite:///../Data/Brazilian_E-Commerc_Database.db")

for name, df in dfs_dict.items():
    df.to_sql(
        name=name,
        con=engine,
        if_exists="append",
        index=False
    )