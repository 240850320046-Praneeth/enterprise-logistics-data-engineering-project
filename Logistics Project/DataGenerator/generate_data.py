"""
Main script to generate and insert data into SQL Server
"""

import sys
import logging
from datetime import datetime

import pandas as pd

from data_generator import LogisticsDataGenerator
from database_connector import execute_many, get_current_counts


# ============================================================
# LOGGING
# ============================================================

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('generator_log.txt'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)


# ============================================================
# SAFE TYPE CONVERSION FUNCTIONS
# ============================================================

def safe_string(value):
    """
    Convert value to normal Python string.
    Pandas NaN becomes None.
    """
    if pd.isna(value):
        return None

    return str(value)


def safe_int(value):
    """
    Convert value to normal Python int.
    """
    if pd.isna(value):
        return None

    return int(value)


def safe_float(value):
    """
    Convert value to normal Python float.
    """
    if pd.isna(value):
        return None

    return float(value)


def safe_datetime(value):
    """
    Convert Pandas Timestamp to Python datetime.
    """
    if pd.isna(value):
        return None

    if isinstance(value, pd.Timestamp):
        return value.to_pydatetime()

    return value


def safe_date(value):
    """
    Convert Pandas Timestamp/datetime to Python date.
    SQL Server DATE columns require date values.
    """
    if pd.isna(value):
        return None

    if isinstance(value, pd.Timestamp):
        return value.date()

    if isinstance(value, datetime):
        return value.date()

    return value


# ============================================================
# MAIN
# ============================================================

def main():

    logger.info("=" * 60)

    logger.info(
        "🚀 Starting Logistics Data Generator"
    )

    logger.info(
        f"⏰ Start Time: "
        f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
    )

    logger.info("=" * 60)

    try:

        # ====================================================
        # INITIALIZE GENERATOR
        # ====================================================

        generator = LogisticsDataGenerator()

        # ====================================================
        # CURRENT COUNTS
        # ====================================================

        logger.info(
            "📊 Checking current record counts..."
        )

        current_counts = get_current_counts()

        for table, count in current_counts.items():

            logger.info(
                f"   {table}: {count} records"
            )

        # ====================================================
        # GENERATE ALL DATA
        # ====================================================

        logger.info(
            "\n📦 Generating new data..."
        )

        dataframes = generator.generate_all()

        logger.info(
            "\n💾 Inserting data into SQL Server..."
        )

        # ====================================================
        # CUSTOMERS
        # ====================================================

        if len(dataframes['customers']) > 0:

            logger.info(
                f"   Inserting "
                f"{len(dataframes['customers'])} "
                f"customers..."
            )

            query = """
                INSERT INTO dbo.customers
                (
                    first_name,
                    last_name,
                    email,
                    phone,
                    address_line1,
                    address_line2,
                    city,
                    state,
                    zip_code,
                    country,
                    customer_type,
                    created_date,
                    last_modified_date,
                    is_active
                )
                VALUES
                (
                    ?, ?, ?, ?, ?, ?, ?, ?,
                    ?, ?, ?, ?, ?, ?
                )
            """

            customer_data = []

            for _, row in dataframes['customers'].iterrows():

                customer_record = (

                    safe_string(
                        row['first_name']
                    ),

                    safe_string(
                        row['last_name']
                    ),

                    safe_string(
                        row['email']
                    ),

                    safe_string(
                        row['phone']
                    ),

                    safe_string(
                        row['address_line1']
                    ),

                    safe_string(
                        row['address_line2']
                    ),

                    safe_string(
                        row['city']
                    ),

                    safe_string(
                        row['state']
                    ),

                    safe_string(
                        row['zip_code']
                    ),

                    safe_string(
                        row['country']
                    ),

                    safe_string(
                        row['customer_type']
                    ),

                    safe_datetime(
                        row['created_date']
                    ),

                    safe_datetime(
                        row['last_modified_date']
                    ),

                    safe_int(
                        row['is_active']
                    )
                )

                customer_data.append(
                    customer_record
                )

            logger.info(
                "🔍 Checking first customer record..."
            )

            if len(customer_data) > 0:

                logger.info(
                    f"Customer values: "
                    f"{customer_data[0]}"
                )

                logger.info(
                    "🔍 Customer parameter types:"
                )

                for index, value in enumerate(
                    customer_data[0],
                    start=1
                ):

                    logger.info(
                        f"   Parameter {index}: "
                        f"value={value!r}, "
                        f"type={type(value).__name__}"
                    )

            execute_many(
                query,
                customer_data
            )

        # ====================================================
        # WAREHOUSES
        # ====================================================

        if len(dataframes['warehouses']) > 0:

            logger.info(
                f"   Inserting "
                f"{len(dataframes['warehouses'])} "
                f"warehouses..."
            )

            query = """
                INSERT INTO dbo.warehouses
                (
                    warehouse_name,
                    address_line1,
                    city,
                    state,
                    zip_code,
                    capacity_sqft,
                    current_utilization_percent,
                    warehouse_manager,
                    operating_hours,
                    created_date,
                    is_active
                )
                VALUES
                (
                    ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?
                )
            """

            warehouse_data = []

            for _, row in dataframes['warehouses'].iterrows():

                warehouse_record = (

                    safe_string(
                        row['warehouse_name']
                    ),

                    safe_string(
                        row['address_line1']
                    ),

                    safe_string(
                        row['city']
                    ),

                    safe_string(
                        row['state']
                    ),

                    safe_string(
                        row['zip_code']
                    ),

                    safe_int(
                        row['capacity_sqft']
                    ),

                    safe_float(
                        row[
                            'current_utilization_percent'
                        ]
                    ),

                    safe_string(
                        row['warehouse_manager']
                    ),

                    safe_string(
                        row['operating_hours']
                    ),

                    safe_datetime(
                        row['created_date']
                    ),

                    safe_int(
                        row['is_active']
                    )
                )

                warehouse_data.append(
                    warehouse_record
                )

            execute_many(
                query,
                warehouse_data
            )

        # ====================================================
        # DRIVERS
        # ====================================================

        if len(dataframes['drivers']) > 0:

            logger.info(
                f"   Inserting "
                f"{len(dataframes['drivers'])} "
                f"drivers..."
            )

            query = """
                INSERT INTO dbo.drivers
                (
                    first_name,
                    last_name,
                    driver_license_number,
                    phone,
                    email,
                    hire_date,
                    salary,
                    driver_status,
                    home_warehouse_id,
                    rating,
                    total_deliveries,
                    created_date,
                    last_modified_date,
                    is_active
                )
                VALUES
                (
                    ?, ?, ?, ?, ?, ?, ?, ?,
                    ?, ?, ?, ?, ?, ?
                )
            """

            driver_data = []

            for _, row in dataframes['drivers'].iterrows():

                driver_record = (

                    safe_string(
                        row['first_name']
                    ),

                    safe_string(
                        row['last_name']
                    ),

                    safe_string(
                        row[
                            'driver_license_number'
                        ]
                    ),

                    safe_string(
                        row['phone']
                    ),

                    safe_string(
                        row['email']
                    ),

                    safe_date(
                        row['hire_date']
                    ),

                    safe_float(
                        row['salary']
                    ),

                    safe_string(
                        row['driver_status']
                    ),

                    safe_int(
                        row['home_warehouse_id']
                    ),

                    safe_float(
                        row['rating']
                    ),

                    safe_int(
                        row['total_deliveries']
                    ),

                    safe_datetime(
                        row['created_date']
                    ),

                    safe_datetime(
                        row['last_modified_date']
                    ),

                    safe_int(
                        row['is_active']
                    )
                )

                driver_data.append(
                    driver_record
                )

            execute_many(
                query,
                driver_data
            )

        # ====================================================
        # VEHICLES
        # ====================================================

        if len(dataframes['vehicles']) > 0:

            logger.info(
                f"   Inserting "
                f"{len(dataframes['vehicles'])} "
                f"vehicles..."
            )

            query = """
                INSERT INTO dbo.vehicles
                (
                    vehicle_vin,
                    license_plate,
                    make,
                    model,
                    year,
                    vehicle_type,
                    capacity_cubic_ft,
                    max_weight_lbs,
                    fuel_type,
                    current_mileage,
                    last_service_date,
                    next_service_date,
                    vehicle_status,
                    assigned_driver_id,
                    created_date,
                    last_modified_date,
                    is_active
                )
                VALUES
                (
                    ?, ?, ?, ?, ?, ?, ?, ?, ?,
                    ?, ?, ?, ?, ?, ?, ?, ?
                )
            """

            vehicle_data = []

            # ------------------------------------------------
            # IMPORTANT:
            #
            # DO NOT use:
            #
            # dataframes['vehicles'].to_numpy()
            #
            # because Pandas/NumPy numeric types can cause
            # SQL Server TDS errors.
            #
            # Convert every field to a native Python type.
            # ------------------------------------------------

            for _, row in dataframes['vehicles'].iterrows():

                vehicle_record = (

                    # 1 - VARCHAR(17)
                    safe_string(
                        row['vehicle_vin']
                    ),

                    # 2 - VARCHAR(15)
                    safe_string(
                        row['license_plate']
                    ),

                    # 3 - VARCHAR(50)
                    safe_string(
                        row['make']
                    ),

                    # 4 - VARCHAR(50)
                    safe_string(
                        row['model']
                    ),

                    # 5 - INT
                    safe_int(
                        row['year']
                    ),

                    # 6 - VARCHAR(30)
                    safe_string(
                        row['vehicle_type']
                    ),

                    # 7 - INT
                    safe_int(
                        row['capacity_cubic_ft']
                    ),

                    # 8 - INT
                    safe_int(
                        row['max_weight_lbs']
                    ),

                    # 9 - VARCHAR(20)
                    safe_string(
                        row['fuel_type']
                    ),

                    # 10 - INT
                    safe_int(
                        row['current_mileage']
                    ),

                    # 11 - DATE
                    safe_date(
                        row['last_service_date']
                    ),

                    # 12 - DATE
                    safe_date(
                        row['next_service_date']
                    ),

                    # 13 - VARCHAR(20)
                    safe_string(
                        row['vehicle_status']
                    ),

                    # 14 - INT
                    safe_int(
                        row['assigned_driver_id']
                    ),

                    # 15 - DATETIME
                    safe_datetime(
                        row['created_date']
                    ),

                    # 16 - DATETIME
                    safe_datetime(
                        row['last_modified_date']
                    ),

                    # 17 - BIT
                    #
                    # CRITICAL FIX:
                    # Force this to native Python int.
                    #
                    safe_int(
                        row['is_active']
                    )
                )

                vehicle_data.append(
                    vehicle_record
                )

            # ------------------------------------------------
            # DEBUG FIRST VEHICLE
            # ------------------------------------------------

            logger.info(
                "🔍 Checking first vehicle record..."
            )

            if len(vehicle_data) > 0:

                logger.info(
                    f"Vehicle values: "
                    f"{vehicle_data[0]}"
                )

                logger.info(
                    "🔍 Vehicle parameter types:"
                )

                for index, value in enumerate(
                    vehicle_data[0],
                    start=1
                ):

                    logger.info(
                        f"   Parameter {index}: "
                        f"value={value!r}, "
                        f"type={type(value).__name__}"
                    )

            # ------------------------------------------------
            # INSERT VEHICLES
            # ------------------------------------------------

            execute_many(
                query,
                vehicle_data
            )

        # ====================================================
        # ORDERS
        # ====================================================

        if len(dataframes['orders']) > 0:

            logger.info(
                f"   Inserting "
                f"{len(dataframes['orders'])} "
                f"orders..."
            )

            query = """
                INSERT INTO dbo.orders
                (
                    order_number,
                    customer_id,
                    order_date,
                    total_amount,
                    tax_amount,
                    shipping_amount,
                    discount_amount,
                    order_status,
                    payment_status,
                    shipping_address,
                    shipping_city,
                    shipping_state,
                    shipping_zip,
                    shipping_method,
                    priority,
                    notes,
                    created_date,
                    last_modified_date,
                    is_active
                )
                VALUES
                (
                    ?, ?, ?, ?, ?, ?, ?, ?, ?, ?,
                    ?, ?, ?, ?, ?, ?, ?, ?, ?
                )
            """

            order_data = []

            for _, row in dataframes['orders'].iterrows():

                order_record = (

                    safe_string(
                        row['order_number']
                    ),

                    safe_int(
                        row['customer_id']
                    ),

                    safe_datetime(
                        row['order_date']
                    ),

                    safe_float(
                        row['total_amount']
                    ),

                    safe_float(
                        row['tax_amount']
                    ),

                    safe_float(
                        row['shipping_amount']
                    ),

                    safe_float(
                        row['discount_amount']
                    ),

                    safe_string(
                        row['order_status']
                    ),

                    safe_string(
                        row['payment_status']
                    ),

                    safe_string(
                        row['shipping_address']
                    ),

                    safe_string(
                        row['shipping_city']
                    ),

                    safe_string(
                        row['shipping_state']
                    ),

                    safe_string(
                        row['shipping_zip']
                    ),

                    safe_string(
                        row['shipping_method']
                    ),

                    safe_string(
                        row['priority']
                    ),

                    safe_string(
                        row['notes']
                    ),

                    safe_datetime(
                        row['created_date']
                    ),

                    safe_datetime(
                        row['last_modified_date']
                    ),

                    safe_int(
                        row['is_active']
                    )
                )

                order_data.append(
                    order_record
                )

            execute_many(
                query,
                order_data
            )

        # ====================================================
        # DELIVERIES
        # ====================================================

        if len(dataframes['deliveries']) > 0:

            logger.info(
                f"   Inserting "
                f"{len(dataframes['deliveries'])} "
                f"deliveries..."
            )

            query = """
                INSERT INTO dbo.deliveries
                (
                    delivery_number,
                    order_id,
                    driver_id,
                    vehicle_id,
                    warehouse_id,
                    assigned_date,
                    pickup_date,
                    delivery_date,
                    actual_delivery_date,
                    delivery_status,
                    delivery_address,
                    delivery_city,
                    delivery_state,
                    delivery_zip,
                    estimated_delivery_time_minutes,
                    actual_delivery_time_minutes,
                    delay_minutes,
                    delivery_notes,
                    customer_signature_url,
                    created_date,
                    last_modified_date,
                    is_active
                )
                VALUES
                (
                    ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?,
                    ?, ?, ?, ?, ?, ?, ?, ?, ?, ?
                )
            """

            delivery_data = []

            for _, row in dataframes['deliveries'].iterrows():

                delivery_record = (

                    safe_string(
                        row['delivery_number']
                    ),

                    safe_int(
                        row['order_id']
                    ),

                    safe_int(
                        row['driver_id']
                    ),

                    safe_int(
                        row['vehicle_id']
                    ),

                    safe_int(
                        row['warehouse_id']
                    ),

                    safe_datetime(
                        row['assigned_date']
                    ),

                    safe_datetime(
                        row['pickup_date']
                    ),

                    safe_datetime(
                        row['delivery_date']
                    ),

                    safe_datetime(
                        row['actual_delivery_date']
                    ),

                    safe_string(
                        row['delivery_status']
                    ),

                    safe_string(
                        row['delivery_address']
                    ),

                    safe_string(
                        row['delivery_city']
                    ),

                    safe_string(
                        row['delivery_state']
                    ),

                    safe_string(
                        row['delivery_zip']
                    ),

                    safe_int(
                        row[
                            'estimated_delivery_time_minutes'
                        ]
                    ),

                    safe_int(
                        row[
                            'actual_delivery_time_minutes'
                        ]
                    ),

                    safe_int(
                        row['delay_minutes']
                    ),

                    safe_string(
                        row['delivery_notes']
                    ),

                    safe_string(
                        row[
                            'customer_signature_url'
                        ]
                    ),

                    safe_datetime(
                        row['created_date']
                    ),

                    safe_datetime(
                        row['last_modified_date']
                    ),

                    safe_int(
                        row['is_active']
                    )
                )

                delivery_data.append(
                    delivery_record
                )

            execute_many(
                query,
                delivery_data
            )

        # ====================================================
        # VEHICLE LOCATIONS / GPS
        # ====================================================

        if len(
            dataframes['vehicle_locations']
        ) > 0:

            logger.info(
                f"   Inserting "
                f"{len(dataframes['vehicle_locations'])} "
                f"GPS locations..."
            )

            query = """
                INSERT INTO dbo.vehicle_locations
                (
                    vehicle_id,
                    driver_id,
                    latitude,
                    longitude,
                    speed_mph,
                    heading_degrees,
                    fuel_level_percent,
                    location_timestamp,
                    is_engine_on,
                    is_moving,
                    created_date
                )
                VALUES
                (
                    ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?
                )
            """

            gps_data = []

            for _, row in (
                dataframes[
                    'vehicle_locations'
                ].iterrows()
            ):

                gps_record = (

                    safe_int(
                        row['vehicle_id']
                    ),

                    safe_int(
                        row['driver_id']
                    ),

                    safe_float(
                        row['latitude']
                    ),

                    safe_float(
                        row['longitude']
                    ),

                    safe_float(
                        row['speed_mph']
                    ),

                    safe_float(
                        row['heading_degrees']
                    ),

                    safe_float(
                        row['fuel_level_percent']
                    ),

                    safe_datetime(
                        row['location_timestamp']
                    ),

                    safe_int(
                        row['is_engine_on']
                    ),

                    safe_int(
                        row['is_moving']
                    ),

                    safe_datetime(
                        row['created_date']
                    )
                )

                gps_data.append(
                    gps_record
                )

            execute_many(
                query,
                gps_data
            )

        # ====================================================
        # FINAL SUMMARY
        # ====================================================

        logger.info(
            "\n" + "=" * 60
        )

        logger.info(
            "✅ Data generation and insertion "
            "completed successfully!"
        )

        logger.info(
            "=" * 60
        )

        logger.info(
            "\n📊 Final record counts:"
        )

        final_counts = get_current_counts()

        total_records = 0

        for table, count in final_counts.items():

            logger.info(
                f"   {table}: {count} records"
            )

            total_records += count

        logger.info(
            f"\n📈 Total Records: "
            f"{total_records}"
        )

        logger.info(
            f"⏰ End Time: "
            f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        )

        logger.info(
            "=" * 60
        )

    except Exception as e:

        logger.error(
            f"❌ Error: {e}"
        )

        import traceback

        traceback.print_exc()

        sys.exit(1)


# ============================================================
# ENTRY POINT
# ============================================================

if __name__ == "__main__":
    main()