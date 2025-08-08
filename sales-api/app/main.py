from fastapi import FastAPI
from app.services.analytics import (
    sale_data, sales_by_region, sales_in_date_range, top_customers,
    sales_by_product, avg_discount_by_category, monthly_sales_trend,
    best_selling_product_per_region, customer_purchase_history
)

app = FastAPI(title="Sales Data Analytics API", version="1.1")

@app.get("/")
def root():
    return {"message": "Sales API powered by FastAPI"}

@app.get("/api/sales/data")
def retrive_sale_data():
    return sale_data()

@app.get("/api/sales/regions")
def get_sales_by_region():
    return sales_by_region().to_dict(orient="records")

@app.get("/api/sales/top-customers")
def get_top_customers(limit: int = 5):
    return top_customers(limit).to_dict(orient="records")

@app.get("/api/sales/date-range")
def get_sales_in_range(start: str, end: str):
    return sales_in_date_range(start, end).to_dict(orient="records")

@app.get("/api/sales/products")
def get_sales_by_product():
    return sales_by_product().to_dict(orient="records")

@app.get("/api/sales/avg-discount")
def get_avg_discount_by_category():
    return avg_discount_by_category().to_dict(orient="records")

@app.get("/api/sales/monthly-trend")
def get_monthly_sales_trend():
    return monthly_sales_trend().to_dict(orient="records")

@app.get("/api/sales/best-product-region")
def get_best_selling_product_per_region():
    return best_selling_product_per_region().to_dict(orient="records")

@app.get("/api/sales/customer-history")
def get_customer_purchase_history(name: str):
    return customer_purchase_history(name)
