import pandas as pd
from datetime import datetime

ORDER_PATH = "data/orders.xlsx"

def save_order(customer, item, qty, price):
    df = pd.read_excel(ORDER_PATH)

    order = {
        "Order_ID": len(df) + 1,
        "Customer_Name": customer,
        "Item_Name": item,
        "Quantity": qty,
        "Total_Price": qty * price,
        "Time": datetime.now().strftime("%H:%M:%S")
    }

    df = pd.concat([df, pd.DataFrame([order])])
    df.to_excel(ORDER_PATH, index=False)

