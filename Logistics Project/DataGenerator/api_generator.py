
import json
import os
import random
from datetime import datetime, timedelta
from faker import Faker

fake = Faker()

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

API_SOURCE_DIR = os.path.join(
    BASE_DIR,
    "data",
    "api_source"
)

os.makedirs(API_SOURCE_DIR, exist_ok=True)


def generate_delivery_events(record_count=100):
    """
    Simulate an external REST API response.
    The output is stored as JSON.
    """

    file_path = os.path.join(
        API_SOURCE_DIR,
        f"delivery_events_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    )

    events = []

    event_types = [
        "DELIVERY_CREATED",
        "DRIVER_ASSIGNED",
        "PICKED_UP",
        "OUT_FOR_DELIVERY",
        "DELIVERED",
        "DELIVERY_FAILED"
    ]

    for event_id in range(1, record_count + 1):

        event_time = (
            datetime.now()
            - timedelta(minutes=random.randint(0, 1440))
        )

        event = {
            "event_id": event_id,
            "event_type": random.choice(event_types),
            "delivery_id": random.randint(1, 2500),
            "order_id": random.randint(1, 2000),
            "driver_id": random.randint(1, 50),
            "event_timestamp": event_time.isoformat(),
            "source_system": "EXTERNAL_DELIVERY_API",
            "event_status": random.choice([
                "SUCCESS",
                "PENDING",
                "FAILED"
            ]),
            "message": fake.sentence()
        }

        events.append(event)

    api_response = {
        "source": "EXTERNAL_DELIVERY_API",
        "generated_at": datetime.now().isoformat(),
        "record_count": record_count,
        "data": events
    }

    with open(file_path, "w", encoding="utf-8") as json_file:
        json.dump(api_response, json_file, indent=4)

    print(f"API JSON response created: {file_path}")

    return file_path


if __name__ == "__main__":
    print("Starting API data generation...")

    generate_delivery_events(100)

    print("API data generation completed successfully!")

