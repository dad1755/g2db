import os
from google.cloud.sql.connector import Connector, IPTypes
import sqlalchemy
import pymysql
import logging

# Set the environment variable for Google Cloud credentials
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "pro10-439001-fe04c9810437.json"

# Setup logging to display errors
logging.basicConfig(level=logging.INFO)

# Initialize Cloud SQL Connector
connector = Connector()

# SQLAlchemy database connection creator function
def getconn():
    try:
        logging.info("Attempting to connect to the Cloud SQL instance...")
        conn = connector.connect(
            "pro10-439001:us-central1:sql12741294",  # Cloud SQL Instance Connection Name
            "pymysql",  # MySQL driver
            user="sql12741294",  # Database user
            password="Lvu9cg9kGm",  # Database password
            db="12741294g10",  # Database name
            ip_type=IPTypes.PUBLIC  # Use IPTypes.PRIVATE for private IP if needed
        )
        logging.info("Successfully connected to the database!")
        return conn
    except Exception as e:
        logging.error(f"Failed to connect to the database: {e}")
        raise

# Create SQLAlchemy connection pool
pool = sqlalchemy.create_engine(
    "mysql+pymysql://",
    creator=getconn,
)

# Interact with Cloud SQL database using connection pool
try:
    with pool.connect() as db_conn:
        logging.info("Running SQL query...")
        result = db_conn.execute("SELECT * FROM STAFF LIMIT 10").fetchall()  # Replace `your_table` with actual table name

        # Do something with the results
        logging.info("Results fetched from the database:")
        for row in result:
            print(row)
except Exception as e:
    logging.error(f"Error while executing the query: {e}")

# Close Cloud SQL Connector
connector.close()
