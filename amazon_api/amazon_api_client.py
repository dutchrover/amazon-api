from datetime import datetime, timedelta
from sp_api.api import Orders, Inventories, CatalogItems, Sellers
from sp_api.base import Marketplaces, ApiResponse
from sp_api.base.exceptions import SellingApiException
from sp_api.util import throttle_retry


@throttle_retry()
def load_all_orders(**kwargs):
    """
    a generator function to return all pages, obtained by NextToken
    """
    return Orders().get_orders(**kwargs)


@throttle_retry()
def get_listings_items(seller_id, **kwargs):
    """Get listings items using the Listings Items API"""
    try:
        listings_api = ListingsItems()
        
        # Initial parameters
        params = {
            'sellerId': seller_id,
            'marketplaceIds': ["ATVPDKIKX0DER"],  # US marketplace
            'includedData': ["summaries", "fulfillmentAvailability"],
            'pageSize': 10  # Start with smaller page size
        }
        
        # Add any additional parameters
        params.update(kwargs)
        
        # Make initial request
        response = listings_api.search_listings_items(**params)
        all_items = []
        
        while True:
            if response and hasattr(response, 'payload'):
                items = response.payload.get('items', [])
                if items:
                    all_items.extend(items)
                    print(f"Retrieved {len(items)} items (total: {len(all_items)})")
                
                # Check for next page
                pagination = response.payload.get('pagination', {})
                next_token = pagination.get('nextToken')
                if not next_token:
                    break
                
                # Get next page
                params['pageToken'] = next_token
                response = listings_api.search_listings_items(**params)
            else:
                break
        
        return all_items
    except SellingApiException as e:
        print(f"Error getting listings items: {e}")
        if hasattr(e, 'payload'):
            print(f"Error details: {e.payload}")
        return None
    except Exception as e:
        print(f"Unexpected error: {e}")
        return None


@throttle_retry()
def get_inventory(**kwargs):
    """Get inventory summary with pagination"""
    try:
        print("Creating Inventories API client...")
        inventories = Inventories()
        
        print("Making initial API request with params:", kwargs)
        response = inventories.get_inventory_summary_marketplace(**kwargs)
        
        if not response:
            print("No response received from API")
            return None
            
        if not hasattr(response, 'payload'):
            print("Response has no payload")
            return None
            
        print("Initial response payload:", response.payload)
        
        all_items = []
        page_count = 0
        
        while True:
            if response and response.payload:
                page_count += 1
                items = response.payload.get('inventorySummaries', [])
                print(f"Processing page {page_count} with {len(items)} items...")
                
                if not items:
                    print(f"No items found on page {page_count}")
                    print("Response payload:", response.payload)
                
                all_items.extend(items)
                
                # Check if there's a next token
                pagination = response.payload.get('pagination', {})
                next_token = pagination.get('nextToken')
                if not next_token:
                    print("No next token found - finished processing pages")
                    break
                    
                print(f"Found next token: {next_token[:20]}... - fetching next page")
                # Get next page using the token
                kwargs['nextToken'] = next_token
                response = inventories.get_inventory_summary_marketplace(**kwargs)
            else:
                print("Invalid response received")
                break
                
        print(f"Total pages processed: {page_count}")
        print(f"Total items collected: {len(all_items)}")
        return all_items
        
    except Exception as e:
        print(f"Error getting inventory: {str(e)}")
        import traceback
        print("Full error traceback:")
        print(traceback.format_exc())
        return None


def get_seller_id():
    """Get seller ID"""
    try:
        print("Creating Sellers API client...")
        sellers_api = Sellers(marketplace=Marketplaces.US)
        
        print("Getting marketplace participation...")
        response = sellers_api.get_marketplace_participation()
        
        if not response or not response.payload:
            print("No response or payload from Sellers API")
            return None
            
        print("Got response:", response.payload)
        
        for marketplace_data in response.payload:
            if marketplace_data.get('marketplace', {}).get('id') == 'ATVPDKIKX0DER':
                seller_id = marketplace_data.get('seller', {}).get('sellerId', 'VERICONIC')
                print(f"Found seller ID: {seller_id}")
                return seller_id
                
        print("No matching marketplace found for ATVPDKIKX0DER")
        return None
        
    except Exception as e:
        print(f"Error getting seller ID: {str(e)}")
        import traceback
        print("Full error traceback:")
        print(traceback.format_exc())
        return None


def get_catalog_item(asin, **kwargs):
    """Get catalog item details using v2022-04-01 API"""
    try:
        catalog = CatalogItems(marketplace=Marketplaces.US)
        return catalog.get_catalog_item(asin=asin, **kwargs)
    except Exception as e:
        print(f"Error getting catalog item: {e}")
        return None


def search_catalog_items(identifiers=None, **kwargs):
    """Search catalog items using v2022-04-01 API"""
    try:
        catalog = CatalogItems(marketplace=Marketplaces.US)
        params = {
            'marketplaceIds': ['ATVPDKIKX0DER'],  # US marketplace
            'includedData': ['summaries', 'identifiers', 'attributes'],
        }
        
        if identifiers:
            params.update({
                'identifiers': identifiers,
                'identifiersType': 'ASIN'
            })
            
        params.update(kwargs)
        return catalog.search_catalog_items(**params)
    except Exception as e:
        print(f"Error searching catalog: {e}")
        return None


@throttle_retry()
def get_inventory_count(seller_id):
    """Get total inventory count without retrieving all records"""
    try:
        print("Creating Inventories API client...")
        inventories = Inventories()
        
        # Initial parameters - request just one item to get pagination info
        params = {
            "marketplaceIds": ["ATVPDKIKX0DER"],
            "details": False,  # Don't need details for count
            "granularityType": "Marketplace",
            "granularityId": "ATVPDKIKX0DER",
            "sellerId": seller_id,
            "maxResultsPerPage": 1  # Minimum to get count
        }
        
        print("Making API request to get count...")
        response = inventories.get_inventory_summary_marketplace(**params)
        
        if not response or not hasattr(response, 'payload'):
            print("No response or payload from API")
            return None
            
        # Get total count from pagination
        total_count = response.payload.get('pagination', {}).get('totalResults', 0)
        print(f"Total inventory count: {total_count}")
        return total_count
        
    except Exception as e:
        print(f"Error getting inventory count: {str(e)}")
        import traceback
        print("Full error traceback:")
        print(traceback.format_exc())
        return None
