from pymongo import MongoClient
from pathlib import Path
import IP2Location
import csv


db = client["countly"]

# Kiểm tra kết nối
client.admin.command("ping")
print("Connected!")

collection = db["summary"]

# Đọc và đếm số lượng IP duy nhất

result = list(
    collection.aggregate(
        [
            {"$group": {"_id": "$ip"}},
            {"$count": "unique_ips"}
        ],
        allowDiskUse=True
    )
)

print(result)

ip_db = IP2Location.IP2Location(
    r"d:\dec_data\IP-COUNTRY-REGION-CITY.BIN"
)
query = {"ip": {"$exists": True, "$nin": [None, ""]}}
projection = {"ip": 1, "_id": 0}

cursor = collection.find(
    query,
    projection,
    no_cursor_timeout=True
).sort("ip", 1).batch_size(10000)

last_ip = None
count = 0

with open("ip_locations.csv", "w", newline="", encoding="utf-8-sig") as f:
    writer = csv.writer(f)
    writer.writerow(["ip", "country", "region", "city"])

    for doc in cursor:
        ip = doc.get("ip")

        if ip == last_ip:
            continue

        last_ip = ip

        record = ip_db.get_all(ip)

        writer.writerow([
            ip,
            record.country_long,
            record.region,
            record.city
        ])

        count += 1

        if count % 10000 == 0:
            print(f"Processed {count:,} unique IPs")

cursor.close()
print(f"Done! Total unique IPs: {count:,}")


r"c:\ubuntu\Poetry\Project5\all_product_ids.csv"