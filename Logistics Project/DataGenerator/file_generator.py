
import csv
import os
import random
from datetime import datetime, timedelta
from faker import Faker

fake = Faker()

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

FILE_SOURCE_DIR = os.path.join(
    BASE_DIR,
    "data",
    "file_source"
)

os.makedirs(FILE_SOURCE_DIR, exist_ok=True)


def generate_daily_orders(record_count=100):
    """
    Generate daily order data as a CSV file.
    This simulates an external partner/vendor file source.
    """

    file_path = os.path.join(
        FILE_SOURCE_DIR,
        f"daily_orders_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
    )

    headers = [
        "external_order_id",
        "customer_name",
        "product_name",
        "quantity",
        "unit_price",
        "total_amount",
        "order_date",
        "order_status"
    ]

    statuses = [
        "CREATED",
        "CONFIRMED",
        "PROCESSING",
        "SHIPPED",
        "DELIVERED",
        "CANCELLED"
    ]

    print(f"Generating {record_count} order records...")

    with open(file_path, "w", newline="", encoding="utf-8") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=headers)
        writer.writeheader()

        for _ in range(record_count):
            quantity = random.randint(1, 10)
            unit_price = round(random.uniform(10, 1000), 2)

            writer.writerow({
                "external_order_id": f"EXT-ORD-{random.randint(100000, 999999)}",
                "customer_name": fake.name(),
                "product_name": fake.word().capitalize(),
                "quantity": quantity,
                "unit_price": unit_price,
                "total_amount": round(quantity * unit_price, 2),
                "order_date": (
                    datetime.now()
                    - timedelta(days=random.randint(0, 30))
                ).strftime("%Y-%m-%d %H:%M:%S"),
                "order_status": random.choice(statuses)
            })

    print(f"CSV order file created: {file_path}")
    return file_path


def generate_warehouse_inventory(record_count=50):
    """
    Generate warehouse inventory data as CSV.
    """

    file_path = os.path.join(
        FILE_SOURCE_DIR,
        f"warehouse_inventory_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
    )

    headers = [
        "inventory_id",
        "warehouse_id",
        "product_code",
        "product_name",
        "quantity_available",
        "reorder_level",
        "last_updated"
    ]

    print(f"Generating {record_count} inventory records...")

    with open(file_path, "w", newline="", encoding="utf-8") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=headers)
        writer.writeheader()

        for inventory_id in range(1, record_count + 1):
            writer.writerow({
                "inventory_id": inventory_id,
                "warehouse_id": random.randint(1, 10),
                "product_code": f"PROD-{random.randint(1000, 9999)}",
                "product_name": fake.word().capitalize(),
                "quantity_available": random.randint(0, 1000),
                "reorder_level": random.randint(10, 100),
                "last_updated": datetime.now().strftime(
                    "%Y-%m-%d %H:%M:%S"
                )
            })

    print(f"CSV inventory file created: {file_path}")
    return file_path


if __name__ == "__main__":
    print("Starting CSV file generation...")

    generate_daily_orders(100)
    generate_warehouse_inventory(50)

    print("CSV file generation completed successfully!")

