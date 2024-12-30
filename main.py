# run_amazon_api_client.py
from amazon_api.amazon_api_client import load_all_orders
from datetime import datetime, timedelta

def get_orders(LastUpdatedAfter: datetime):
    for page in load_all_orders(LastUpdatedAfter=LastUpdatedAfter):
        for order in page.payload.get('Orders'):
            print( order)

if __name__ == "__main__":
    LastUpdatedAfter = (datetime.now() - timedelta(days=2)).isoformat()
    get_orders(LastUpdatedAfter)