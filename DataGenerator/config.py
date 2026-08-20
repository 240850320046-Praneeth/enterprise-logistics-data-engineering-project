"""
Configuration file for Logistics Data Generator
"""

# SQL Server Connection Configuration
SQL_SERVER_CONFIG = {
    'server': 'localhost,1433',  # Use localhost or your server name
    'database': 'LogisticsDB',
    'driver': '{ODBC Driver 18 for SQL Server}',
    'trusted_connection': 'yes',  # Use Windows Authentication
    'encrypt': 'no'
}

# If using SQL Authentication instead of Windows Authentication:
# SQL_SERVER_CONFIG = {
#     'server': 'localhost,1433',
#     'database': 'LogisticsDB',
#     'driver': '{ODBC Driver 18 for SQL Server}',
#     'uid': 'sa',
#     'pwd': 'YourStrong!Passw0rd',
#     'encrypt': 'no'
# }

# Data Generation Configuration
DATA_CONFIG = {
    'num_customers': 500,          # Number of customers to generate
    'num_warehouses': 10,          # Number of warehouses
    'num_drivers': 50,             # Number of drivers
    'num_vehicles': 75,            # Number of vehicles
    'num_orders': 2000,            # Number of orders
    'num_deliveries': 2500,        # Number of deliveries
    'num_gps_locations': 1000,    # Number of GPS tracking points
    'days_of_data': 30,            # How many days back to generate
}

# Data Quality Issues to Inject
BAD_DATA_CONFIG = {
    'null_probability': 0.05,      # 5% chance of null values
    'duplicate_probability': 0.02, # 2% chance of duplicates
    'invalid_date_probability': 0.03,  # 3% chance of invalid dates
    'outlier_probability': 0.01,   # 1% chance of outliers
    'schema_drift_probability': 0.01, # 1% chance of schema drift
}

# Business Rules
BUSINESS_RULES = {
    'customer_types': ['REGULAR', 'PREMIUM', 'BUSINESS'],
    'customer_type_weights': [0.60, 0.25, 0.15],  # 60% Regular, 25% Premium, 15% Business
    
    'order_statuses': ['PENDING', 'PROCESSING', 'SHIPPED', 'DELIVERED', 'CANCELLED'],
    'order_status_weights': [0.10, 0.15, 0.20, 0.50, 0.05],
    
    'delivery_statuses': ['ASSIGNED', 'PICKED_UP', 'IN_TRANSIT', 'DELIVERED', 'FAILED', 'DELAYED'],
    'delivery_status_weights': [0.10, 0.15, 0.20, 0.45, 0.05, 0.05],
    
    'priorities': ['NORMAL', 'HIGH', 'URGENT'],
    'priority_weights': [0.70, 0.20, 0.10],
    
    'vehicle_types': ['VAN', 'TRUCK', 'CARGO', 'REFRIGERATED'],
    'vehicle_type_weights': [0.40, 0.30, 0.20, 0.10],
}

# Performance Testing Parameters
PERFORMANCE_CONFIG = {
    'batch_size': 1000,  # Records to insert per batch
    'enable_logging': True,  # Enable detailed logging
    'log_file': 'generator_log.txt'  # Log file location
}