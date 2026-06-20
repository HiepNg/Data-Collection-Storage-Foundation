from pymongo import MongoClient
from pathlib import Path
import IP2Location
import csv

client = MongoClient("mongodb://localhost:27017")

db = client["countly"]

# Kiểm tra kết nối
client.admin.command("ping")
print("Connected!")

collection = db["summary"]

'''
# View_product_detail
with open(
    "view_product_detail.csv",
    "w",
    newline="",
    encoding="utf-8-sig"
) as f:

    writer = csv.writer(f)
    writer.writerow(["_id","product_id ","viewing_product_id","current_url"])
    
    count = 0

    query_vpd = {"collection":"view_product_detail"}
    projection_vpd = {
        "_id": 1,
        "product_id": 1,
        "viewing_product_id": 1,
        "current_url": 1
    }
    cursor_vpd = collection.find(
        query_vpd,
        projection_vpd,
        no_cursor_timeout=True

    ).limit(10000).batch_size(10000)

    for doc in cursor:
        writer.writerow([
            doc.get('_id'),
            doc.get('product_id'),
            doc.get('viewing_product_id'),
            doc.get('current_url'),
        ])

        count+=1
        
        if count % 10000 ==0:
            print(f"Processed {count:,}")
print(f"Done! Exported {count:,} rows")
'''

'''
# select_product_option
with open(
    "select_product_option.csv",
    "w",
    newline="",
    encoding="utf-8-sig"
) as f:

    writer = csv.writer(f)
    writer.writerow(["_id","product_id ","viewing_product_id","current_url"])
    
    count = 0

    query_spo = {"collection":"select_product_option"}
    projection_spo = {
        "_id": 1,
        "product_id": 1,
        "viewing_product_id": 1,
        "current_url": 1
    }
    cursor_spo = collection.find(
        query_spo,
        projection_spo,
        no_cursor_timeout=True

    ).limit(100000).batch_size(10000)

    for doc in cursor_spo:
        writer.writerow([
            doc.get('_id'),
            doc.get('product_id'),
            doc.get('viewing_product_id'),
            doc.get('current_url'),
        ])

        count+=1
        
        if count % 10000 ==0:
            print(f"Processed {count:,}")
print(f"Done! Exported {count:,} rows")
'''

'''
# select_product_option_quality
with open(
    "select_product_option_quality.csv",
    "w",
    newline="",
    encoding="utf-8-sig"
) as f:

    writer = csv.writer(f)
    writer.writerow(["_id","product_id ","viewing_product_id","current_url"])
    
    count = 0

    query_spoq = {"collection":"select_product_option_quality"}
    projection_spoq = {
        "_id": 1,
        "product_id": 1,
        "viewing_product_id": 1,
        "current_url": 1
    }
    cursor_spoq = collection.find(
        query_spoq,
        projection_spoq,
        no_cursor_timeout=True

    ).limit(100000).batch_size(10000)

    for doc in cursor_spoq:
        writer.writerow([
            doc.get('_id'),
            doc.get('product_id'),
            doc.get('viewing_product_id'),
            doc.get('current_url'),
        ])

        count+=1
        
        if count % 10000 ==0:
            print(f"Processed {count:,}")
print(f"Done! Exported {count:,} rows")

'''

'''
#product_detail_recommendation_visible

with open(
    "product_detail_recommendation_visible.csv",
    "w",
    newline="",
    encoding="utf-8-sig"
) as f:

    writer = csv.writer(f)
    writer.writerow(["_id","product_id ","viewing_product_id","current_url"])
    
    count = 0

    query_pdrs = {"collection":"product_detail_recommendation_visible"}
    projection_pdrs = {
        "_id": 1,
        "product_id": 1,
        "viewing_product_id": 1,
        "current_url": 1
    }
    cursor_pdrs = collection.find(
        query_pdrs,
        projection_pdrs,
        no_cursor_timeout=True

    ).limit(100000).batch_size(10000)

    for doc in cursor_pdrs:
        writer.writerow([
            doc.get('_id'),
            doc.get('product_id'),
            doc.get('viewing_product_id'),
            doc.get('current_url'),
        ])

        count+=1
        
        if count % 10000 ==0:
            print(f"Processed {count:,}")
print(f"Done! Exported {count:,} rows")

'''

'''
#product_detail_recommendation_noticed
with open(
    "product_detail_recommendation_noticed.csv",
    "w",
    newline="",
    encoding="utf-8-sig"
) as f:

    writer = csv.writer(f)
    writer.writerow(["_id","product_id ","viewing_product_id","current_url"])
    
    count = 0

    query_pdrn = {"collection":"product_detail_recommendation_noticed"}
    projection_pdrn = {
        "_id": 1,
        "product_id": 1,
        "viewing_product_id": 1,
        "current_url": 1
    }
    cursor_pdrn = collection.find(
        query_pdrn,
        projection_pdrn,
        no_cursor_timeout=True

    ).limit(100000).batch_size(10000)

    for doc in cursor_pdrn:
        writer.writerow([
            doc.get('_id'),
            doc.get('product_id'),
            doc.get('viewing_product_id'),
            doc.get('current_url'),
        ])

        count+=1
        
        if count % 10000 ==0:
            print(f"Processed {count:,}")
print(f"Done! Exported {count:,} rows")
'''

#product_view_all_recommend_clicked
with open(
    "product_view_all_recommend_clicked .csv",
    "w",
    newline="",
    encoding="utf-8-sig"
) as f:

    writer = csv.writer(f)
    writer.writerow(["_id","viewing_product_id","referrer_url"])
    
    count = 0

    query_pvarc = {"collection":"product_view_all_recommend_clicked"}
    projection_pvarc = {
        "_id": 1,
        "viewing_product_id": 1,
        "referrer_url": 1
    }
    cursor_pvarc = collection.find(
        query_pvarc,
        projection_pvarc,
        no_cursor_timeout=True

    ).limit(100000).batch_size(10000)

    for doc in cursor_pvarc:
        writer.writerow([
            doc.get('_id'),
            doc.get('viewing_product_id'),
            doc.get('referrer_url'),
        ])

        count+=1
        
        if count % 10000 ==0:
            print(f"Processed {count:,}")
print(f"Done! Exported {count:,} rows")


# statuses = collection.distinct("collection")

# for s in statuses:
#     print(s)
#     add_to_cart_action
# back_to_product_action
# checkout
# checkout_success
# landing_page_recommendation_clicked
# landing_page_recommendation_noticed
# landing_page_recommendation_visible
# listing_page_recommendation_clicked
# listing_page_recommendation_noticed
# listing_page_recommendation_visible
# product_detail_recommendation_clicked
# product_detail_recommendation_noticed
# product_detail_recommendation_visible
# product_view_all_recommend_clicked
# search_box_action
# select_product_option
# select_product_option_quality
# sorting_relevance_click_action
# view_all_recommend
# view_home_page
# view_landing_page
# view_listing_page
# view_my_account
# view_product_detail
# view_shopping_cart
# view_sorting_relevance
# view_static_page