
import json
import os
import random
from datetime import datetime, timedelta

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

IOT_SOURCE_DIR = os.path.join(
    BASE_DIR,
    "data",
    "iot_source"
)

os.makedirs(IOT_SOURCE_DIR, exist_ok=True)


def generate_iot_events(record_count=100):
    """
    Generate IoT sensor events for logistics vehicles.
    """

    file_path = os.path.join(
        IOT_SOURCE_DIR,
        f"vehicle_sensor_events_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    )

    events = []

    for event_id in range(1, record_count + 1):

        timestamp = (
            datetime.now()
            - timedelta(seconds=random.randint(0, 3600))
        )

        event = {
            "event_id": event_id,
            "vehicle_id": random.randint(1, 75),
            "driver_id": random.randint(1, 50),

            "latitude": round(
                random.uniform(17.3000, 17.5000),
                6
            ),

            "longitude": round(
                random.uniform(78.3000, 78.6000),
                6
            ),

            "speed_kmph": round(
                random.uniform(0, 120),
                2
            ),

            "fuel_level_percent": round(
                random.uniform(5, 100),
                2
            ),

            "engine_temperature_celsius": round(
                random.uniform(70, 110),
                2
            ),

            "battery_voltage": round(
                random.uniform(11.5, 14.5),
                2
            ),

            "is_engine_on": random.choice([
                True,
                True,
                True,
                False
            ]),

            "is_moving": random.choice([
                True,
                False
            ]),

            "sensor_timestamp": timestamp.isoformat(),

            "source_system": "VEHICLE_IOT"
        }

        events.append(event)

    iot_payload = {
        "source": "VEHICLE_IOT",
        "generated_at": datetime.now().isoformat(),
        "record_count": record_count,
        "data": events
    }

    with open(file_path, "w", encoding="utf-8") as json_file:
        json.dump(iot_payload, json_file, indent=4)

    print(f"IoT sensor data created: {file_path}")

    return file_path


if __name__ == "__main__":
    print("Starting IoT data generation...")

    generate_iot_events(100)

    print("IoT data generation completed successfully!")

