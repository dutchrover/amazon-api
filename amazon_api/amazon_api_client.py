from datetime import datetime, timedelta
from sp_api.api import Orders, Inventories, Catalog
from sp_api.base import Marketplaces
from sp_api.util import throttle_retry, load_all_pages


@throttle_retry()
@load_all_pages()
def load_all_orders(**kwargs):
    """
    a generator function to return all pages, obtained by NextToken
    """
    return Orders().get_orders(**kwargs)


def get_inventory(**kwargs):
    return Inventories().get_inventory_summary_marketplace(**kwargs)


@throttle_retry()
def get_catalog_items(**kwargs):
    """
    Get catalog items for the specified marketplace
    """
    try:
        catalog = Catalog(marketplace=Marketplaces.US)
        return catalog.get_catalog_item(**kwargs)
    except Exception as e:
        print(f"Error fetching catalog items: {e}")
        return None


@throttle_retry()
@load_all_pages()
def search_catalog_items(**kwargs):
    """
    Search catalog items and return all pages of results
    """
    try:
        catalog = Catalog(marketplace=Marketplaces.US)
        return catalog.search_catalog_items(**kwargs)
    except Exception as e:
        print(f"Error searching catalog: {e}")
        return None
