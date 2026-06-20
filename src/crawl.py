from pymongo import MongoClient
import pandas as pd
import csv
import asyncio
import json
import random
import re
import os
from datetime import datetime
from curl_cffi.requests import AsyncSession

client = MongoClient("mongodb://localhost:27017")

db = client["countly"]

# Kiểm tra kết nối
client.admin.command("ping")
print("Connected!")

collection = db["summary"]

# product_ids = set(collection.distinct("product_id"))
# viewing_ids = set(collection.distinct("viewing_product_id"))

# all_ids = product_ids | viewing_ids

# with open("all_product_ids.csv", "w", newline="", encoding="utf-8-sig") as f:
#     writer = csv.writer(f)

#     writer.writerow(["product_id"])

#     for product_id in all_ids:
#         writer.writerow([product_id])
# print(len(all_ids))



# =========================
# CONFIG
# =========================

INPUT_IDS_FILE = r"c:\ubuntu\Poetry\Project5\all_product_ids.csv"

OUTPUT_CSV = "products_infomation.csv"
FAILED_FILE = "failed_ids.txt"
LOG_FILE = f"crawler_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"

BASE_DOMAIN = "www.glamira.com"

ENGLISH_DOMAINS = [
    "www.glamira.co.uk",
    "www.glamira.com.au",
    "www.glamira.ca",
    "www.glamira.ie",
    "www.glamira.co.nz",
    "www.glamira.sg",
    "www.glamira.hk",
    "www.glamira.in",
    "www.glamira.com.ph",
    "www.glamira.com.my",
    "www.glamira.ae",
    "www.glamira.co.za",
    "www.glamira.co.id",
    "www.glamira.co.th",
    "www.glamira.com.kw",
    "www.glamira.africa",
]

CONCURRENCY = 20
TIMEOUT = 20

FIELDS = [
    "product_id",
    "name",
    "sku",
    "attribute_set_id",
    "attribute_set",
    "type_id",
    "price",
    "min_price",
    "max_price",
    "min_price_format",
    "max_price_format",
    "gold_weight",
    "none_metal_weight",
    "fixed_silver_weight",
    "material_design",
    "qty",
    "collection",
    "collection_id",
    "product_type",
    "product_type_value",
    "category",
    "category_name",
    "store_code",
    "platinum_palladium_info_in_alloy",
    "bracelet_without_chain",
    "show_popup_quantity_eternity",
    "visible_contents",
    "gender",
]


csv_lock = asyncio.Lock()
failed_lock = asyncio.Lock()
log_lock = asyncio.Lock()


# =========================
# UTILS
# =========================

def build_url(domain, product_id):
    return f"https://{domain}/catalog/product/view/id/{product_id}"


def init_csv():
    if not os.path.exists(OUTPUT_CSV):
        with open(OUTPUT_CSV, "w", newline="", encoding="utf-8-sig") as f:
            writer = csv.DictWriter(f, fieldnames=FIELDS)
            writer.writeheader()


def load_ids():
    df = pd.read_csv(INPUT_IDS_FILE)

    return (
        df["product_id"]
        .dropna()
        .astype(int)
        .astype(str)
        .tolist()
    )


def load_done_ids():
    if not os.path.exists(OUTPUT_CSV):
        return set()

    try:
        df = pd.read_csv(OUTPUT_CSV, usecols=["product_id"])
        return set(
            df["product_id"]
            .dropna()
            .astype(int)
            .astype(str)
            .tolist()
        )
    except Exception:
        return set()


async def log(message):
    print(message)

    async with log_lock:
        with open(LOG_FILE, "a", encoding="utf-8") as f:
            f.write(message + "\n")


def extract_react_data(html):
    patterns = [
        r"var\s+react_data\s*=\s*(\{.*?\});",
        r"window\.react_data\s*=\s*(\{.*?\});",
        r"react_data\s*=\s*(\{.*?\});",
    ]

    for pattern in patterns:
        match = re.search(pattern, html, re.DOTALL)

        if match:
            try:
                return json.loads(match.group(1))
            except Exception:
                return None

    return None


def build_csv_row(react_data):
    row = {}

    for field in FIELDS:
        value = react_data.get(field)

        if isinstance(value, list):
            value = "|".join(map(str, value))

        elif isinstance(value, dict):
            value = json.dumps(value, ensure_ascii=False)

        row[field] = value

    return row


# =========================
# CRAWLER
# =========================

async def fetch_product(session, product_id, sem):
    domains = [BASE_DOMAIN] + ENGLISH_DOMAINS

    async with sem:
        for domain in domains:
            url = build_url(domain, product_id)

            try:
                await asyncio.sleep(random.uniform(0.2, 0.8))

                response = await session.get(url, timeout=TIMEOUT)
                status = response.status_code

                if status != 200:
                    await log(f"[{status}] {product_id} -> {domain}")
                    continue

                react_data = extract_react_data(response.text)

                if not react_data:
                    await log(f"[NO DATA] {product_id} -> {domain}")
                    continue

                react_data["source_domain"] = domain
                react_data["source_url"] = url

                await log(f"[OK] {product_id} -> {domain}")
                return react_data

            except Exception as e:
                await log(f"[ERROR] {product_id} -> {domain} | {e}")
                continue

    await log(f"[FAILED ALL DOMAINS] {product_id}")
    return None


async def save_to_csv(react_data):
    row = build_csv_row(react_data)

    async with csv_lock:
        with open(OUTPUT_CSV, "a", newline="", encoding="utf-8-sig") as f:
            writer = csv.DictWriter(f, fieldnames=FIELDS)
            writer.writerow(row)


async def save_failed(product_id):
    async with failed_lock:
        with open(FAILED_FILE, "a", encoding="utf-8") as f:
            f.write(str(product_id) + "\n")


async def worker(session, product_id, sem):
    react_data = await fetch_product(session, product_id, sem)

    if react_data:
        await save_to_csv(react_data)
    else:
        await save_failed(product_id)


async def main():
    init_csv()

    all_ids = load_ids()
    done_ids = load_done_ids()

    product_ids = [
        product_id
        for product_id in all_ids
        if product_id not in done_ids
    ]

    await log("=" * 60)
    await log(f"Total IDs     : {len(all_ids)}")
    await log(f"Done IDs      : {len(done_ids)}")
    await log(f"Remaining IDs : {len(product_ids)}")
    await log(f"Base domain   : {BASE_DOMAIN}")
    await log(f"Fallbacks     : {len(ENGLISH_DOMAINS)}")
    await log(f"Concurrency   : {CONCURRENCY}")
    await log("=" * 60)

    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/136.0.0.0 Safari/537.36"
        ),
        "Accept": (
            "text/html,application/xhtml+xml,application/xml;q=0.9,"
            "image/avif,image/webp,image/apng,*/*;q=0.8"
        ),
        "Accept-Language": "en-US,en;q=0.9",
        "Referer": "https://www.glamira.com/",
    }

    sem = asyncio.Semaphore(CONCURRENCY)

    async with AsyncSession(
        headers=headers,
        impersonate="chrome136"
    ) as session:
        tasks = [
            worker(session, product_id, sem)
            for product_id in product_ids
        ]

        await asyncio.gather(*tasks)

    await log("=" * 60)
    await log("DONE")
    await log(f"Output CSV : {OUTPUT_CSV}")
    await log(f"Failed IDs : {FAILED_FILE}")
    await log("=" * 60)


if __name__ == "__main__":
    asyncio.run(main())