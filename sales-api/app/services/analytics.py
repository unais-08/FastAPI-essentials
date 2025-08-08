import pandas as pd

df = pd.read_csv("app/data/sales_data.csv")
df["order_date"] = pd.to_datetime(df["order_date"])
df["total_price"] = df["quantity"] * df["unit_price"] * (1 - df["discount"])

def sale_data():
    return df.to_dict(orient="records")

def sales_by_region():
    return df.groupby("region")[["quantity", "total_price"]].sum().reset_index()

def top_customers(limit=5):
    return (
        df.groupby("customer_name")["total_price"]
        .sum()
        .sort_values(ascending=False)
        .head(limit)
        .reset_index()
    )

def sales_in_date_range(start, end):
    mask = (df["order_date"] >= start) & (df["order_date"] <= end)
    filtered = df[mask]
    return filtered.groupby("product")[["quantity", "total_price"]].sum().reset_index()


def sales_by_product():
    """Total quantity & revenue per product"""
    return df.groupby("product")[["quantity", "total_price"]].sum().reset_index()

def avg_discount_by_category():
    """Average discount by category"""
    return df.groupby("category")["discount"].mean().reset_index()

def monthly_sales_trend():
    """Total sales per month"""
    monthly = df.resample("M", on="order_date")[["total_price"]].sum().reset_index()
    monthly["month"] = monthly["order_date"].dt.strftime("%Y-%m")
    return monthly[["month", "total_price"]]

def best_selling_product_per_region():
    """Best-selling product in each region by revenue"""
    idx = df.groupby("region")["total_price"].idxmax()
    return df.loc[idx, ["region", "product", "total_price"]]

def customer_purchase_history(customer_name):
    """All purchases for a given customer"""
    filtered = df[df["customer_name"].str.lower() == customer_name.lower()]
    return filtered.to_dict(orient="records")
