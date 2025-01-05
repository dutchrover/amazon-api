# run_amazon_api_client.py
from amazon_api.amazon_api_client import load_all_orders, get_inventory, get_catalog_items, search_catalog_items
from datetime import datetime, timedelta

def get_orders(LastUpdatedAfter: datetime):
    for page in load_all_orders(LastUpdatedAfter=LastUpdatedAfter):
        for order in page.payload.get('Orders'):
            print(order)

if __name__ == "__main__":
    LastUpdatedAfter = (datetime.now() - timedelta(days=2)).isoformat()
    # get_orders(LastUpdatedAfter)

    # print(get_inventory(**{
    #     "details": False,
    #     "marketplaceIds": ["ATVPDKIKX0DER"],
    #     "startDateTime": (datetime.now() - timedelta(days=1)).isoformat()
    # }))

    # Search all catalog items
    catalog_items = search_catalog_items(
        MarketplaceId="ATVPDKIKX0DER",
        keywords="*",  # Search all items
        includedData=["summaries", "attributes", "identifiers"]
    )
    
    if catalog_items:
        print("\nCatalog Items:")
        for item in catalog_items.payload.get('items', []):
            asin = item.get('asin')
            title = item.get('summaries', [{}])[0].get('itemName', 'No Title')
            print(f"ASIN: {asin}")
            print(f"Title: {title}")
            print("---")
