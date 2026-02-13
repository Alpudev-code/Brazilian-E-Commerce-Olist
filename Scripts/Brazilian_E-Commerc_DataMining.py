import pandas as pd

# Declare csv data types
dtypes_dict = {
    'customer_id': 'string',
    'customer_unique_id': 'string',
    'customer_zip_code_prefix': 'Int64',
    'customer_city': 'string',
    'customer_state': 'string'
}

customers_df = pd.read_csv("../Data/csvs/olist_customers_dataset.csv", dtype=dtypes_dict)
customers_df.name = "customers"
# customers_df.dtypes

# Declare csv data types
dtypes_dict = {
    'geolocation_zip_code_prefix': 'Int64',
    'geolocation_lat': 'Float64',
    'geolocation_lng': 'Float64',
    'geolocation_city': 'string',
    'geolocation_state': 'string'
}

geolocation_df = pd.read_csv("../Data/csvs/olist_geolocation_dataset.csv", dtype=dtypes_dict)
geolocation_df.name = "geolocation"
# geolocation_df.dtypes

# Declare csv data types
dtypes_dict = {
    'order_id': 'string',
    'order_item_id': 'Int64',
    'product_id': 'string',
    'seller_id': 'string',
    'shipping_limit_date': 'string',
    'price': 'Float64',
    'freight_value': 'Float64'
}

order_items_df = pd.read_csv("../Data/csvs/olist_order_items_dataset.csv", dtype=dtypes_dict)
order_items_df.name = "order_items"
# order_items_df.dtypes

# Declare csv data types
dtypes_dict = {
    'order_id': 'string',
    'payment_sequential': 'Int64',
    'payment_type': 'string',
    'payment_installments': 'Int64',
    'payment_value': 'Float64'
}

order_payments_df = pd.read_csv("../Data/csvs/olist_order_payments_dataset.csv", dtype=dtypes_dict)
order_payments_df.name = "order_payments"
# order_payments_df.dtypes

# Declare csv data types
dtypes_dict = {
    'review_id': 'string',
    'order_id': 'string',
    'review_score': 'Int64',
    'review_comment_title': 'string',
    'review_comment_message': 'string',
    'review_creation_date': 'string',
    'review_answer_timestamp': 'string'
}

order_reviews_df = pd.read_csv("../Data/csvs/olist_order_reviews_dataset.csv", dtype=dtypes_dict)
order_reviews_df.name = "order_reviews"
# order_reviews_df.dtypes

# Declare csv data types
dtypes_dict = {
    'order_id': 'string',
    'customer_id': 'string',
    'order_status': 'string',
    'order_purchase_timestamp': 'string',
    'order_approved_at': 'string',
    'order_delivered_carrier_date': 'string',
    'order_delivered_customer_date': 'string',
    'order_estimated_delivery_date': 'string'
}

orders_df = pd.read_csv("../Data/csvs/olist_orders_dataset.csv", dtype=dtypes_dict)
orders_df.name = "orders"
# orders_df.dtypes

# Declare csv data types
dtypes_dict = {
    'product_id': 'string',
    'product_category_name': 'string',
    'product_name_lenght': 'Int64',
    'product_description_lenght': 'Int64',
    'product_photos_qty': 'Int64',
    'product_weight_g': 'Int64',
    'product_length_cm': 'Int64',
    'product_height_cm': 'Int64',
    'product_width_cm': 'Int64',
}

products_df = pd.read_csv("../Data/csvs/olist_products_dataset.csv", dtype=dtypes_dict)
products_df.name = "products"
# products_df.dtypes

# Declare csv data types
dtypes_dict = {
    'seller_id': 'string',
    'seller_zip_code_prefix': 'Int64',
    'seller_city': 'string',
    'seller_state': 'string',
}

sellers_df = pd.read_csv("../Data/csvs/olist_sellers_dataset.csv", dtype=dtypes_dict)
sellers_df.name = "sellers"
# sellers_df.dtypes

# Declare csv data types
dtypes_dict = {
    'product_category_name': 'string',
    'product_category_name_english': 'string'
}

product_category_name_translation_df = pd.read_csv("../Data/csvs/product_category_name_translation.csv", dtype=dtypes_dict)
product_category_name_translation_df.name = "product_category_name_translation"
# product_category_name_translation_df.dtypes

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

# Get what columns from which dataframes contains nulls
def check_NaNs(dfs_dict) -> None:
    for df in dfs_dict.values():
        nans_df = df.isna().sum()
        nans_df = nans_df[nans_df > 0]

        for column, quantity in nans_df.items():
            print(f"Nans in: {df.name} | Column: {column}. | Quantity: {quantity}")

def manage_nans(dfs_dict) -> None:
    dfs_dict[order_reviews_df.name] = dfs_dict[order_reviews_df.name].fillna({
        "review_comment_title": "",
        "review_comment_message": ""
    })
    dfs_dict[orders_df.name] = dfs_dict[orders_df.name].fillna({
        "order_approved_at": "",
        "order_delivered_carrier_date": "",
        "order_delivered_customer_date": ""
    })
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

def manage_dates(dfs_dict, dates_dict) -> None:
    for df, columns in dates_dict.items():
        dfs_dict[df][columns] = dfs_dict[df][columns].apply(
            pd.to_datetime, 
            errors="coerce"
        )

manage_nans(dfs_dict)

dates_dict = {
    orders_df.name: [
        "order_approved_at", 
        "order_delivered_carrier_date", 
        "order_delivered_customer_date",
        "order_estimated_delivery_date"
    ],
    order_reviews_df.name: [
        "review_creation_date", 
        "review_answer_timestamp"
    ],
    order_items_df.name: [
        "shipping_limit_date"
    ]
}

manage_dates(dfs_dict, dates_dict)
