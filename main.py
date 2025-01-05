# run_amazon_api_client.py
import json
from amazon_api.amazon_api_client import get_inventory, get_seller_id, get_inventory_count
import csv
import sys
from collections import defaultdict

if __name__ == "__main__":
    try:
        MAX_RECORDS = 2000
        
        print("\nStarting inventory retrieval process...")
        
        # First get seller ID
        seller_id = get_seller_id()
        if not seller_id:
            print("Failed to get seller ID")
            sys.exit(1)
            
        # Get total count first
        print("\nGetting total inventory count...")
        total_count = get_inventory_count(seller_id)
        if total_count is None:
            print("Failed to get inventory count")
            sys.exit(1)
            
        print(f"\nTotal inventory items available: {total_count}")
        proceed = input("\nDo you want to proceed with retrieving all items? (y/n): ")
        if proceed.lower() != 'y':
            print("Operation cancelled by user")
            sys.exit(0)
            
        print(f"\nGetting inventory for seller: {seller_id}")
        
        # Get inventory items
        print("\nFetching inventory items...")
        inventory_params = {
            "marketplaceIds": ["ATVPDKIKX0DER"],
            "details": True,
            "granularityType": "Marketplace",
            "granularityId": "ATVPDKIKX0DER",
            "sellerId": seller_id
        }
        
        print("Using inventory parameters:", json.dumps(inventory_params, indent=2))
        inventory_items = get_inventory(**inventory_params)
        
        if not inventory_items:
            print("No inventory items found or error occurred")
            sys.exit(1)
        
        print(f"Found {len(inventory_items)} total items")
        
        # Process items
        seen_skus = set()
        all_items = []
        skus_processed = 0
        
        print("\nProcessing items...")
        for item in inventory_items:
            skus_processed += 1
            
            # Debug every 100 items
            if skus_processed % 100 == 0:
                print(f"\nProcessed {skus_processed} items so far...")
                print(f"Current item structure: {json.dumps(item, indent=2)}")
            
            sku = item.get('sellerSku', '')
            asin = item.get('asin', '')
            quantity = item.get('totalQuantity', 0)
            condition = item.get('condition', '')
            
            # Skip if SKU doesn't start with '3'
            if not sku.startswith('3'):
                if skus_processed % 100 == 0:  # Print every 100th skipped SKU
                    print(f"Skipping SKU (not starting with 3): {sku}")
                continue
            
            # Only add if we haven't seen this SKU before
            if sku not in seen_skus and len(all_items) < MAX_RECORDS:
                seen_skus.add(sku)
                all_items.append({
                    'asin': asin,
                    'seller_sku': sku,
                    'item_condition': condition,
                    'quantity': quantity
                })
                print(f"Found SKU starting with 3: {sku}")
            
            # Safety check - stop if we reach max records
            if len(all_items) >= MAX_RECORDS:
                print(f"\nReached maximum of {MAX_RECORDS} records. Stopping processing.")
                break
        
        print(f"\nTotal SKUs processed: {skus_processed}")
        print(f"Total unique SKUs found (starting with 3): {len(all_items)}")
        
        if len(all_items) > 0:
            # Sort items by SKU
            all_items.sort(key=lambda x: x['seller_sku'])
            
            # Write to CSV
            output_file = 'inventory.csv'
            print(f"\nWriting data to {output_file}...")
            
            with open(output_file, 'w', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(['asin', 'seller-sku', 'item-condition', 'quantity'])
                for item in all_items:
                    writer.writerow([
                        item['asin'],
                        item['seller_sku'],
                        item['item_condition'],
                        item['quantity']
                    ])
            
            print(f"\nData successfully written to {output_file}")
        else:
            print("\nNo SKUs found starting with '3' - no CSV file written")
            
    except Exception as e:
        print(f"\nUnexpected error occurred: {str(e)}")
        import traceback
        print("\nFull error traceback:")
        print(traceback.format_exc())
        sys.exit(1)
