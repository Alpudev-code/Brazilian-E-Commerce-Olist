# Study Case: Brazilian E-Commerce
## Overview
This project involves analyzing a public [dataset](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce?select=olist_customers_dataset.csv) from Brazil's e-commerce platform, Olist. The goal is to develop a comprehensive data pipeline that ensures high-quality data for analysis and to develop a BI dashboard with useful insights.

---
## Table of contents
1. Data Ingestion
2. Data Quality Analysis
3. Data Cleaning and Transformation

---
## 1. Data Ingestion
The data ingestion phase involved downloading CSV files from Kaggle and defining a logic model schema for the dataset. The schema includes primary keys, foreign keys and relations.

![Brazilian_E-Commerc_Diagram.jpg](https://github.com/Alpudev-code/Brazilian-E-Commerce-Olist/blob/dev/Readme/Brazilian_E-Commerc_Diagram.jpg?raw=true)

---
## 2. Data Quality Analysis
Data quality analysis was performed to identify issues such as missing values, invalid dates format and duplicates.
### Date fields
Upon inspection, there is no need for dates management as they come already in a valid format.
### Missing data
There are a couple of tables with missing values in one or more columns:

```
Nans in: order_reviews | Column: review_comment_title. | Quantity: 87656
Nans in: order_reviews | Column: review_comment_message. | Quantity: 58247
Nans in: products | Column: product_category_name. | Quantity: 610
Nans in: products | Column: product_name_lenght. | Quantity: 610
Nans in: products | Column: product_description_lenght. | Quantity: 610
Nans in: products | Column: product_photos_qty. | Quantity: 610
Nans in: products | Column: product_weight_g. | Quantity: 2
Nans in: products | Column: product_length_cm. | Quantity: 2
Nans in: products | Column: product_height_cm. | Quantity: 2
Nans in: products | Column: product_width_cm. | Quantity: 2
```
 
 - **order_reviews** values can be null, it's possible to have orders without comments.
 - **products** with no category are assigned to "Unknown", the other fields values are set to -1 as a way to identify them in consults.
### Duplicates
 Duplicates are only checked for tables with values of primary key or not nullable in the database. 
 
 The tables **geolocation** and **order_reviews** seems to have duplicates. The indexes of the duplicated data were extracted to later inspect them.
 
 ![Order_reviews_Duplicates.png](https://github.com/Alpudev-code/Brazilian-E-Commerce-Olist/blob/dev/Readme/Order_reviews_Duplicates.png?raw=true)

![Geolocation_Duplicates.png](https://github.com/Alpudev-code/Brazilian-E-Commerce-Olist/blob/dev/Readme/Geolocation_Duplicates.png?raw=true)

---
## 3. Data Cleaning and Transformation
### Missing data
In **order_reviews** in **orders** table, it is possible to have orders without comments so values can stay null. For **products** with no category are assigned to "Unknown", the other fields values are set to -1 as a way to identify them in consults.
### Duplicates
Duplicated values from **geolocation** and **order_reviews** tables contains their own repeated data, so the decision was to keep the first found row.

## Technology stack:
- Python
	- Jupyter
	- Pandas
	- Numpy
	- SQLAlquemy
- SQLite
	- sqlitebrowser
- Metabase
