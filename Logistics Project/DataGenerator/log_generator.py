
import logging
import os
import random
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

LOG_SOURCE_DIR = os.path.join(
    BASE_DIR,
    "data",
    "logs"
)

os.makedirs(LOG_SOURCE_DIR, exist_ok=True)

LOG_FILE = os.path.join(
    LOG_SOURCE_DIR,
    "logistics_application.log"
)


def setup_logger():

    logger = logging.getLogger("logistics_application")

    logger.setLevel(logging.INFO)

    logger.handlers.clear()

    file_handler = logging.FileHandler(LOG_FILE)

    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)s | %(message)s"
    )

    file_handler.setFormatter(formatter)

    logger.addHandler(file_handler)

    return logger


def generate_application_logs(record_count=100):

    logger = setup_logger()

    log_messages = [
        "Order created successfully",
        "Order status updated",
        "Driver assigned to delivery",
        "Vehicle location received",
        "Delivery started",
        "Delivery completed",
        "Warehouse inventory updated",
        "Payment processed successfully",
        "API request completed",
        "Database connection successful",
        "Data validation completed"
    ]

    error_messages = [
        "Failed to process delivery event",
        "Database connection timeout",
        "Invalid vehicle location received",
        "External API request failed"
    ]

    for _ in range(record_count):

        log_type = random.choices(
            ["INFO", "WARNING", "ERROR"],
            weights=[80, 15, 5],
            k=1
        )[0]

        if log_type == "INFO":
            logger.info(
                random.choice(log_messages)
            )

        elif log_type == "WARNING":
            logger.warning(
                f"Warning detected: {random.choice(log_messages)}"
            )

        else:
            logger.error(
                random.choice(error_messages)
            )

    print(
        f"{record_count} application logs generated successfully"
    )

    print(
        f"Log file: {LOG_FILE}"
    )


if __name__ == "__main__":

    print("Starting application log generation...")

    generate_application_logs(100)

    print("Application log generation completed successfully!")

