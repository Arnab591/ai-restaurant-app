import pandas as pd

MENU_PATH = "data/menu.xlsx"

def get_menu():
    df = pd.read_excel(MENU_PATH)
    return df[df["Stock"] > 0]

def get_item(item_name):
    df = pd.read_excel(MENU_PATH)
    return df[df["Item_Name"].str.lower() == item_name.lower()]

def reduce_stock(item_name, qty):
    df = pd.read_excel(MENU_PATH)
    df.loc[
        df["Item_Name"].str.lower() == item_name.lower(),
        "Stock"
    ] -= qty
    df.to_excel(MENU_PATH, index=False)

