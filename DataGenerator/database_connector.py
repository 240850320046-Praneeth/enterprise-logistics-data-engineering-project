"""
Database connection and utility functions
"""

import pyodbc
import pandas as pd
from config import SQL_SERVER_CONFIG
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def get_connection():
    """
    Create and return a connection to SQL Server
    
    Returns:
        pyodbc.Connection: Database connection object
    """
    try:
        connection_string = (
            f"DRIVER={SQL_SERVER_CONFIG['driver']};"
            f"SERVER={SQL_SERVER_CONFIG['server']};"
            f"DATABASE={SQL_SERVER_CONFIG['database']};"
        )
        
        # Use Windows Authentication
        if SQL_SERVER_CONFIG.get('trusted_connection'):
            connection_string += f"Trusted_Connection={SQL_SERVER_CONFIG['trusted_connection']};"
        
        # Use SQL Authentication if provided
        if SQL_SERVER_CONFIG.get('uid') and SQL_SERVER_CONFIG.get('pwd'):
            connection_string += f"UID={SQL_SERVER_CONFIG['uid']};PWD={SQL_SERVER_CONFIG['pwd']};"
        
        # Encryption settings
        if SQL_SERVER_CONFIG.get('encrypt'):
            connection_string += f"Encrypt={SQL_SERVER_CONFIG['encrypt']};"
        
        conn = pyodbc.connect(connection_string)
        logger.info("✅ Connected to SQL Server successfully!")
        return conn
    
    except Exception as e:
        logger.error(f"❌ Failed to connect to SQL Server: {e}")
        raise

def execute_query(query, params=None):
    """
    Execute a SQL query and return results as DataFrame
    
    Args:
        query (str): SQL query to execute
        params (tuple, optional): Query parameters
    
    Returns:
        pd.DataFrame: Query results
    """
    conn = get_connection()
    try:
        if params:
            df = pd.read_sql_query(query, conn, params=params)
        else:
            df = pd.read_sql_query(query, conn)
        return df
    finally:
        conn.close()

def execute_many(query, data, batch_size=1000):
    """
    Execute a batch insert using executemany
    
    Args:
        query (str): SQL insert query
        data (list): List of tuples containing data
        batch_size (int): Number of records per batch
    
    Returns:
        int: Number of records inserted
    """
    conn = get_connection()
    cursor = conn.cursor()
    total_inserted = 0
    
    try:
        # Insert in batches for better performance
        for i in range(0, len(data), batch_size):
            batch = data[i:i + batch_size]
            cursor.executemany(query, batch)
            conn.commit()
            total_inserted += len(batch)
            logger.info(f"Inserted {total_inserted} records so far...")
        
        logger.info(f"✅ Inserted {total_inserted} records successfully!")
        return total_inserted
    
    except Exception as e:
        logger.error(f"❌ Error inserting data: {e}")
        conn.rollback()
        raise
    finally:
        cursor.close()
        conn.close()

def get_current_counts():
    """
    Get current record counts from all tables
    
    Returns:
        dict: Dictionary of table names and record counts
    """
    conn = get_connection()
    cursor = conn.cursor()
    
    tables = ['customers', 'warehouses', 'drivers', 'vehicles', 'orders', 'deliveries', 'vehicle_locations']
    counts = {}
    
    try:
        for table in tables:
            cursor.execute(f"SELECT COUNT(*) FROM {table}")
            counts[table] = cursor.fetchone()[0]
        return counts
    finally:
        cursor.close()
        conn.close()