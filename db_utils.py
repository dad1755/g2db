import mysql.connector
from mysql.connector import Error
import pandas as pd

# Database connection details
DB_CONFIG = {
    'host': 'sql12.freemysqlhosting.net',
    'database': 'sql12741294',
    'user': 'sql12741294',
    'password': 'Lvu9cg9kGm',
    'port': 3306
}

def execute_query(query, params=None):
    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        cursor = connection.cursor()
        cursor.execute(query, params)
        connection.commit()
        return cursor
    except Error as e:
        return e
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

def fetch_data(query):
    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        df = pd.read_sql(query, connection)
        return df
    except Error as e:
        return pd.DataFrame()  # Return empty DataFrame on error
    finally:
        if connection.is_connected():
            connection.close()
