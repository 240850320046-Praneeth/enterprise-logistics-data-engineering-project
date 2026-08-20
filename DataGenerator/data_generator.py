"""
Logistics Data Generator
Generates realistic enterprise-style logistics data
"""

import random
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from faker import Faker

from config import (
    DATA_CONFIG,
    BAD_DATA_CONFIG,
    BUSINESS_RULES
)


# ============================================================
# Faker
# ============================================================

fake = Faker()


class LogisticsDataGenerator:

    def __init__(self, config=DATA_CONFIG):

        self.config = config
        self.fake = Faker()

        # Reproducible data
        random.seed(42)
        np.random.seed(42)
        Faker.seed(42)

        print("🚀 Logistics Data Generator initialized!")
        print(f"📊 Configuration: {config}")

    # ========================================================
    # DATE GENERATOR
    # ========================================================

    def _generate_date_range(self, days_back):

        start_date = datetime.now() - timedelta(
            days=days_back
        )

        random_days = random.randint(
            0,
            days_back
        )

        random_hours = random.randint(
            0,
            23
        )

        random_minutes = random.randint(
            0,
            59
        )

        return start_date + timedelta(
            days=random_days,
            hours=random_hours,
            minutes=random_minutes
        )

    # ========================================================
    # BAD DATA GENERATOR
    # ========================================================

    def _apply_bad_data(
        self,
        value,
        column_type
    ):

        # NULL injection
        if random.random() < BAD_DATA_CONFIG[
            'null_probability'
        ]:

            return None

        # Invalid date
        if (
            column_type == 'date'
            and random.random()
            < BAD_DATA_CONFIG[
                'invalid_date_probability'
            ]
        ):

            return '2026-13-32'

        # Numeric outlier
        if (
            column_type == 'number'
            and random.random()
            < BAD_DATA_CONFIG[
                'outlier_probability'
            ]
        ):

            if isinstance(
                value,
                (int, float)
            ):

                return value * random.randint(
                    5,
                    20
                )

        return value

    # ========================================================
    # CUSTOMERS
    # ========================================================

    def generate_customers(
        self,
        count=None
    ):

        if count is None:
            count = self.config[
                'num_customers'
            ]

        customers = []

        customer_types = BUSINESS_RULES[
            'customer_types'
        ]

        customer_weights = BUSINESS_RULES[
            'customer_type_weights'
        ]

        for _ in range(count):

            first_name = fake.first_name()

            last_name = fake.last_name()

            email = (
                f"{first_name.lower()}."
                f"{last_name.lower()}@"
                f"{fake.domain_name()}"
            )

            customer = (
                first_name,
                last_name,
                email,
                fake.phone_number()[:20],
                fake.street_address()[:200],

                (
                    fake.secondary_address()[:200]
                    if random.random() > 0.7
                    else None
                ),

                fake.city()[:50],

                fake.state_abbr()[:2],

                fake.zipcode()[:10],

                'USA',

                random.choices(
                    customer_types,
                    weights=customer_weights
                )[0],

                self._generate_date_range(365),

                self._generate_date_range(30),

                1
            )

            customer = list(customer)

            # email is NOT NULL in SQL Server.
            # Therefore we do not inject NULL into email.

            # Country is nullable.
            customer[9] = self._apply_bad_data(
                customer[9],
                'string'
            )

            customers.append(
                tuple(customer)
            )

        return customers

    # ========================================================
    # WAREHOUSES
    # ========================================================

    def generate_warehouses(
        self,
        count=None
    ):

        if count is None:
            count = self.config[
                'num_warehouses'
            ]

        warehouses = []

        warehouse_names = [
            'North Distribution Center',
            'South Logistics Hub',
            'East Fulfillment Center',
            'West Regional Warehouse',
            'Central Mega Warehouse',
            'Metro Logistics',
            'Express Hub',
            'Regional Distribution Center',
            'Fulfillment Center',
            'Logistics Park'
        ]

        cities = [
            'Seattle',
            'Austin',
            'New York',
            'Los Angeles',
            'Chicago',
            'Houston',
            'Phoenix',
            'Philadelphia',
            'San Antonio',
            'San Diego'
        ]

        states = [
            'WA',
            'TX',
            'NY',
            'CA',
            'IL',
            'TX',
            'AZ',
            'PA',
            'TX',
            'CA'
        ]

        for i in range(count):

            warehouse = (
                warehouse_names[
                    i % len(warehouse_names)
                ],

                fake.street_address()[:200],

                cities[
                    i % len(cities)
                ],

                states[
                    i % len(states)
                ],

                fake.zipcode()[:10],

                random.randint(
                    30000,
                    150000
                ),

                round(
                    random.uniform(
                        10,
                        95
                    ),
                    2
                ),

                fake.name()[:100],

                (
                    f"{random.randint(6, 9)}:00 - "
                    f"{random.randint(17, 21)}:00"
                ),

                self._generate_date_range(365),

                1
            )

            warehouses.append(
                warehouse
            )

        return warehouses

    # ========================================================
    # DRIVERS
    # ========================================================

    def generate_drivers(
        self,
        count=None,
        warehouse_count=None
    ):

        if count is None:
            count = self.config[
                'num_drivers'
            ]

        if warehouse_count is None:
            warehouse_count = self.config[
                'num_warehouses'
            ]

        drivers = []

        for _ in range(count):

            first_name = fake.first_name()

            last_name = fake.last_name()

            driver = (
                first_name,

                last_name,

                f"DL{random.randint(100000, 999999)}",

                fake.phone_number()[:20],

                (
                    f"{first_name.lower()}."
                    f"{last_name.lower()}"
                    f"@delivery.com"
                )[:100],

                self._generate_date_range(730),

                round(
                    random.uniform(
                        45000,
                        85000
                    ),
                    2
                ),

                random.choices(
                    [
                        'ACTIVE',
                        'INACTIVE',
                        'ON_LEAVE'
                    ],
                    weights=[
                        0.85,
                        0.10,
                        0.05
                    ]
                )[0],

                random.randint(
                    1,
                    warehouse_count
                ),

                round(
                    random.uniform(
                        3.5,
                        5.0
                    ),
                    2
                ),

                random.randint(
                    0,
                    1000
                ),

                self._generate_date_range(365),

                self._generate_date_range(30),

                1
            )

            drivers.append(
                driver
            )

        return drivers

    # ========================================================
    # VEHICLES
    # ========================================================

    def generate_vehicles(
        self,
        count=None,
        driver_count=None
    ):

        if count is None:
            count = self.config[
                'num_vehicles'
            ]

        if driver_count is None:
            driver_count = self.config[
                'num_drivers'
            ]

        vehicles = []

        makes = [
            'Ford',
            'Chevrolet',
            'Mercedes',
            'GMC',
            'Ram',
            'Dodge',
            'Honda'
        ]

        models = [
            'Transit',
            'Express',
            'Sprinter',
            'Silverado',
            'ProMaster',
            'Sierra',
            'Odyssey'
        ]

        vehicle_types = BUSINESS_RULES[
            'vehicle_types'
        ]

        fuel_types = [
            'GASOLINE',
            'DIESEL',
            'ELECTRIC',
            'HYBRID'
        ]

        for _ in range(count):

            vehicle_vin = ''.join(
                random.choices(
                    'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789',
                    k=17
                )
            )

            license_plate = ''.join(
                random.choices(
                    'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789',
                    k=6
                )
            )

            vehicle = (

                vehicle_vin,

                license_plate,

                random.choice(
                    makes
                ),

                random.choice(
                    models
                ),

                random.randint(
                    2018,
                    2025
                ),

                random.choices(
                    vehicle_types,
                    weights=BUSINESS_RULES[
                        'vehicle_type_weights'
                    ]
                )[0],

                random.randint(
                    300,
                    1000
                ),

                random.randint(
                    3000,
                    15000
                ),

                random.choices(
                    fuel_types,
                    weights=[
                        0.40,
                        0.45,
                        0.05,
                        0.10
                    ]
                )[0],

                random.randint(
                    10000,
                    150000
                ),

                self._generate_date_range(
                    180
                ),

                self._generate_date_range(
                    90
                ),

                random.choices(
                    [
                        'AVAILABLE',
                        'IN_TRANSIT',
                        'MAINTENANCE',
                        'RETIRED'
                    ],
                    weights=[
                        0.60,
                        0.25,
                        0.10,
                        0.05
                    ]
                )[0],

                (
                    random.randint(
                        1,
                        driver_count
                    )
                    if random.random() > 0.3
                    else None
                ),

                self._generate_date_range(
                    365
                ),

                self._generate_date_range(
                    30
                ),

                1
            )

            vehicles.append(
                vehicle
            )

        return vehicles

    # ========================================================
    # ORDERS
    # ========================================================

    def generate_orders(
        self,
        count=None,
        customer_count=None
    ):

        if count is None:
            count = self.config[
                'num_orders'
            ]

        if customer_count is None:
            customer_count = self.config[
                'num_customers'
            ]

        orders = []

        statuses = BUSINESS_RULES[
            'order_statuses'
        ]

        status_weights = BUSINESS_RULES[
            'order_status_weights'
        ]

        priorities = BUSINESS_RULES[
            'priorities'
        ]

        priority_weights = BUSINESS_RULES[
            'priority_weights'
        ]

        for i in range(count):

            order_date = (
                self._generate_date_range(
                    30
                )
            )

            total_amount = round(
                random.uniform(
                    50,
                    1000
                ),
                2
            )

            tax_amount = round(
                total_amount * 0.08,
                2
            )

            shipping_amount = round(
                random.uniform(
                    5,
                    30
                ),
                2
            )

            discount_amount = round(
                random.uniform(
                    0,
                    20
                ),
                2
            )

            order = (

                f"ORD-2026-"
                f"{str(i + 1).zfill(5)}",

                random.randint(
                    1,
                    customer_count
                ),

                order_date,

                total_amount,

                tax_amount,

                shipping_amount,

                discount_amount,

                random.choices(
                    statuses,
                    weights=status_weights
                )[0],

                random.choices(
                    [
                        'PENDING',
                        'PAID',
                        'FAILED',
                        'REFUNDED'
                    ],
                    weights=[
                        0.10,
                        0.80,
                        0.05,
                        0.05
                    ]
                )[0],

                fake.street_address()[:200],

                fake.city()[:50],

                fake.state_abbr()[:2],

                fake.zipcode()[:10],

                random.choices(
                    [
                        'Standard',
                        'Express',
                        'Overnight'
                    ],
                    weights=[
                        0.60,
                        0.30,
                        0.10
                    ]
                )[0],

                random.choices(
                    priorities,
                    weights=priority_weights
                )[0],

                (
                    fake.text(
                        max_nb_chars=500
                    )
                    if random.random() > 0.7
                    else None
                ),

                order_date,

                self._generate_date_range(
                    15
                ),

                1
            )

            orders.append(
                order
            )

        return orders

    # ========================================================
    # DELIVERIES
    # ========================================================

    def generate_deliveries(
        self,
        count=None,
        order_count=None,
        driver_count=None,
        vehicle_count=None,
        warehouse_count=None
    ):

        if count is None:
            count = self.config[
                'num_deliveries'
            ]

        if order_count is None:
            order_count = self.config[
                'num_orders'
            ]

        if driver_count is None:
            driver_count = self.config[
                'num_drivers'
            ]

        if vehicle_count is None:
            vehicle_count = self.config[
                'num_vehicles'
            ]

        if warehouse_count is None:
            warehouse_count = self.config[
                'num_warehouses'
            ]

        deliveries = []

        for i in range(count):

            assigned_date = (
                self._generate_date_range(
                    30
                )
            )

            estimated_time = random.randint(
                30,
                180
            )

            if random.random() < 0.6:

                pickup_date = (
                    assigned_date
                    + timedelta(
                        hours=random.randint(
                            1,
                            4
                        )
                    )
                )

                delivery_date = (
                    pickup_date
                    + timedelta(
                        hours=random.randint(
                            1,
                            6
                        )
                    )
                )

                actual_delivery_date = (
                    delivery_date
                    + timedelta(
                        minutes=random.randint(
                            -30,
                            60
                        )
                    )
                )

                delivery_status = random.choices(
                    [
                        'DELIVERED',
                        'FAILED',
                        'DELAYED'
                    ],
                    weights=[
                        0.70,
                        0.10,
                        0.20
                    ]
                )[0]

                actual_time = random.randint(
                    30,
                    240
                )

                delay_minutes = max(
                    0,
                    actual_time
                    - estimated_time
                )

            else:

                pickup_date = None
                delivery_date = None
                actual_delivery_date = None

                delivery_status = random.choice(
                    [
                        'ASSIGNED',
                        'PICKED_UP',
                        'IN_TRANSIT'
                    ]
                )

                actual_time = None
                delay_minutes = 0

            delivery = (

                f"DEL-"
                f"{str(i + 1).zfill(5)}",

                random.randint(
                    1,
                    order_count
                ),

                random.randint(
                    1,
                    driver_count
                ),

                random.randint(
                    1,
                    vehicle_count
                ),

                random.randint(
                    1,
                    warehouse_count
                ),

                assigned_date,

                pickup_date,

                delivery_date,

                actual_delivery_date,

                delivery_status,

                fake.street_address()[:200],

                fake.city()[:50],

                fake.state_abbr()[:2],

                fake.zipcode()[:10],

                estimated_time,

                actual_time,

                delay_minutes,

                (
                    fake.text(
                        max_nb_chars=500
                    )
                    if random.random() > 0.7
                    else None
                ),

                (
                    f"https://signatures.delivery.com/"
                    f"{fake.uuid4()}"
                    if delivery_status == 'DELIVERED'
                    else None
                ),

                assigned_date,

                self._generate_date_range(
                    15
                ),

                1
            )

            deliveries.append(
                delivery
            )

        return deliveries

    # ========================================================
    # GPS LOCATIONS
    # ========================================================

    def generate_gps_locations(
        self,
        count=None,
        vehicle_count=None,
        driver_count=None
    ):

        if count is None:
            count = self.config[
                'num_gps_locations'
            ]

        if vehicle_count is None:
            vehicle_count = self.config[
                'num_vehicles'
            ]

        if driver_count is None:
            driver_count = self.config[
                'num_drivers'
            ]

        locations = []

        cities = {

            'Seattle': (
                47.6062,
                -122.3321
            ),

            'Austin': (
                30.2672,
                -97.7431
            ),

            'New York': (
                40.7128,
                -74.0060
            ),

            'Los Angeles': (
                34.0522,
                -118.2437
            ),

            'Chicago': (
                41.8781,
                -87.6298
            ),

            'Houston': (
                29.7604,
                -95.3698
            ),

            'Phoenix': (
                33.4484,
                -112.0740
            ),

            'Philadelphia': (
                39.9526,
                -75.1652
            ),

            'San Antonio': (
                29.4241,
                -98.4936
            ),

            'San Diego': (
                32.7157,
                -117.1611
            )
        }

        for _ in range(count):

            city_name = random.choice(
                list(cities.keys())
            )

            base_lat, base_lon = cities[
                city_name
            ]

            latitude = (
                base_lat
                + random.uniform(
                    -0.5,
                    0.5
                )
            )

            longitude = (
                base_lon
                + random.uniform(
                    -0.5,
                    0.5
                )
            )

            location = (

                random.randint(
                    1,
                    vehicle_count
                ),

                random.randint(
                    1,
                    driver_count
                ),

                round(
                    latitude,
                    8
                ),

                round(
                    longitude,
                    8
                ),

                round(
                    random.uniform(
                        0,
                        75
                    ),
                    2
                ),

                round(
                    random.uniform(
                        0,
                        360
                    ),
                    2
                ),

                round(
                    random.uniform(
                        5,
                        100
                    ),
                    2
                ),

                self._generate_date_range(
                    7
                ),

                # FIXED:
                # Added the missing ] here.
                random.choice([
                    0,
                    1
                ]),

                random.choice([
                    0,
                    1
                ]),

                self._generate_date_range(
                    7
                )
            )

            locations.append(
                location
            )

        return locations

    # ========================================================
    # GENERATE ALL
    # ========================================================

    def generate_all(self):

        print("📊 Generating data...")

        customers = self.generate_customers()

        warehouses = self.generate_warehouses()

        drivers = self.generate_drivers()

        vehicles = self.generate_vehicles()

        orders = self.generate_orders()

        deliveries = self.generate_deliveries()

        gps_locations = (
            self.generate_gps_locations()
        )

        dataframes = {

            'customers': pd.DataFrame(
                customers,
                columns=[
                    'first_name',
                    'last_name',
                    'email',
                    'phone',
                    'address_line1',
                    'address_line2',
                    'city',
                    'state',
                    'zip_code',
                    'country',
                    'customer_type',
                    'created_date',
                    'last_modified_date',
                    'is_active'
                ]
            ),

            'warehouses': pd.DataFrame(
                warehouses,
                columns=[
                    'warehouse_name',
                    'address_line1',
                    'city',
                    'state',
                    'zip_code',
                    'capacity_sqft',
                    'current_utilization_percent',
                    'warehouse_manager',
                    'operating_hours',
                    'created_date',
                    'is_active'
                ]
            ),

            'drivers': pd.DataFrame(
                drivers,
                columns=[
                    'first_name',
                    'last_name',
                    'driver_license_number',
                    'phone',
                    'email',
                    'hire_date',
                    'salary',
                    'driver_status',
                    'home_warehouse_id',
                    'rating',
                    'total_deliveries',
                    'created_date',
                    'last_modified_date',
                    'is_active'
                ]
            ),

            'vehicles': pd.DataFrame(
                vehicles,
                columns=[
                    'vehicle_vin',
                    'license_plate',
                    'make',
                    'model',
                    'year',
                    'vehicle_type',
                    'capacity_cubic_ft',
                    'max_weight_lbs',
                    'fuel_type',
                    'current_mileage',
                    'last_service_date',
                    'next_service_date',
                    'vehicle_status',
                    'assigned_driver_id',
                    'created_date',
                    'last_modified_date',
                    'is_active'
                ]
            ),

            'orders': pd.DataFrame(
                orders,
                columns=[
                    'order_number',
                    'customer_id',
                    'order_date',
                    'total_amount',
                    'tax_amount',
                    'shipping_amount',
                    'discount_amount',
                    'order_status',
                    'payment_status',
                    'shipping_address',
                    'shipping_city',
                    'shipping_state',
                    'shipping_zip',
                    'shipping_method',
                    'priority',
                    'notes',
                    'created_date',
                    'last_modified_date',
                    'is_active'
                ]
            ),

            'deliveries': pd.DataFrame(
                deliveries,
                columns=[
                    'delivery_number',
                    'order_id',
                    'driver_id',
                    'vehicle_id',
                    'warehouse_id',
                    'assigned_date',
                    'pickup_date',
                    'delivery_date',
                    'actual_delivery_date',
                    'delivery_status',
                    'delivery_address',
                    'delivery_city',
                    'delivery_state',
                    'delivery_zip',
                    'estimated_delivery_time_minutes',
                    'actual_delivery_time_minutes',
                    'delay_minutes',
                    'delivery_notes',
                    'customer_signature_url',
                    'created_date',
                    'last_modified_date',
                    'is_active'
                ]
            ),

            'vehicle_locations': pd.DataFrame(
                gps_locations,
                columns=[
                    'vehicle_id',
                    'driver_id',
                    'latitude',
                    'longitude',
                    'speed_mph',
                    'heading_degrees',
                    'fuel_level_percent',
                    'location_timestamp',
                    'is_engine_on',
                    'is_moving',
                    'created_date'
                ]
            )
        }

        print("✅ Data generation complete!")

        return dataframes


# ============================================================
# END OF FILE
# ============================================================