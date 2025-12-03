from utils import *

headers = {
    "Authorization": f"Bearer {os.getenv('API_TOKEN')}",
    "Accept": "application/json"
}

def main():
    all_listings = []

    for value in get_items_by_collection("Magic", headers)["id"]:
        all_listings.append(get_expansion_id_listing(value, headers))

    all_listings_df = pd.concat(all_listings, ignore_index=True).drop_duplicates()

    all_listings_df.to_sql(
        "card_trader_products",   
        con = get_sql_engine("postgresql+psycopg2"),
        if_exists = "append",       
        index = False,             
        method = "multi"            
    )


    print(all_listings_df.info())

if __name__ == "__main__":
    main()