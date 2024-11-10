from google.cloud.sql.connector import Connector, IPTypes
import sqlalchemy
import pymysql

# Initialize Cloud SQL Connector
connector = Connector()

# SQLAlchemy database connection creator function
def getconn():
    conn = connector.connect(
        "pro10-439001:us-central1:sql12741294",  # Cloud SQL Instance Connection Name
        "pymysql",  # Database driver for MySQL
        user="sql12741294",  # Database user
        password="Lvu9cg9kGm",  # Database password
        db="12741294g10",  # Database name
        ip_type=IPTypes.PUBLIC  # Use IPTypes.PRIVATE for private IP if needed
    )
    return conn

# Create SQLAlchemy connection pool
pool = sqlalchemy.create_engine(
    "mysql+pymysql://",
    creator=getconn,
)

# Interact with Cloud SQL database using connection pool
with pool.connect() as db_conn:
    # Query database
    result = db_conn.execute("SELECT * FROM your_table LIMIT 10").fetchall()  # Replace `your_table` with actual table name

    # Do something with the results
    for row in result:
        print(row)

# Close Cloud SQL Connector
connector.close()
