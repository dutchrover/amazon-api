from datetime import datetime, timedelta
from sp_api.api import Orders, Inventories
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
