import pandas as pd 
import requests
import json
from pandasql import sqldf
import os

def get_items_by_collection(coll_name, headers):
    coll_df = pd.DataFrame(
        requests.get(
            "https://api.cardtrader.com/api/v2/expansions"
            ,headers = headers
        ).json()
    )
    query = """SELECT DISTINCT id, name FROM coll_df WHERE name LIKE '%{}%'""".format(coll_name)
    return sqldf(query)

def get_expansion_id_listing(exp_id, headers):
    output = []
    response = requests.get(
        "https://api.cardtrader.com/api/v2/marketplace/products?expansion_id={}".format(exp_id)
        ,headers = headers
    ).json()
    for key, value in response.items():
        dict_data = {}   
        for item in value:
            dict_data["expansion_id"] = exp_id
            dict_data["expansion_name"] = item["expansion"]["name_en"]
            dict_data["blueprint_id"] = key
            dict_data["product_id"] = item["id"]
            dict_data["product_name"] = item["name_en"]
            dict_data["product_quantity"] = item["quantity"]
            dict_data["product_price_cents"] = item["price_cents"]
            dict_data["product_currency"] = item["price_currency"]
            dict_data["product_description"] = item["description"]
            dict_data["user_id"] = item["user"]["id"]
            dict_data["user_name"] = item["user"]["username"]
            dict_data["user_country"] = item["user"]["country_code"]
            dict_data["insert_timestamp"] = pd.Timestamp.utcnow()
            output.append(dict_data)
    return pd.DataFrame(output)