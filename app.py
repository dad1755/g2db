from google.cloud.sql.connector import Connector
import sqlalchemy
import pymysql  # Required for MySQL connections

# Initialize the Google Cloud SQL Connector
connector = Connector()

# Function to return the database connection using the SQL Connector
def getconn() -> pymysql.connections.Connection:
    conn = connector.connect(
        "pro10-439001:us-central1:sql12741294",  # Replace with your instance name in the format project:region:instance
        "pymysql",  # Use pymysql for MySQL, psycopg2 for PostgreSQL
        user="sql12741294",  # Your database username
        password="Lvu9cg9kGm",  # Your database password
        db="12741294g10"  # Your database name
    )
    return conn

# Create a connection pool with SQLAlchemy
pool = sqlalchemy.create_engine(
    "mysql+pymysql://",  # Use 'mysql+pymysql' for MySQL, 'postgresql+psycopg2' for PostgreSQL
    creator=getconn,  # Function to provide connection from Cloud SQL Connector
)

# Example query to test the connection
try:
    # Example of interacting with the database using SQLAlchemy
    with pool.connect() as connection:
        result = connection.execute("SELECT 1")
        print(f"Query result: {result.fetchone()}")
except Exception as e:
    print(f"Error: {e}")
