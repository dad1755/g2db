import mysql.connector
from mysql.connector import Error

# Define connection parameters
db_config = {
    'host': '34.67.211.206',  # Public IP address of the MySQL server
    'database': '12741294g10',  # Database name
    'user': 'sql12741294',  # MySQL username
    'password': 'Lvu9cg9kGm'  # MySQL password
}

try:
    # Establish the connection to the MySQL database
    connection = mysql.connector.connect(**db_config)
    
    if connection.is_connected():
        print("Connected to MySQL database")
    
    # Example: Execute a simple query to verify the connection
    cursor = connection.cursor()
    cursor.execute("SELECT DATABASE();")
    record = cursor.fetchone()
    print(f"You're connected to database: {record}")

except Error as e:
    print(f"Error while connecting to MySQL: {e}")

finally:
    if connection.is_connected():
        cursor.close()
        connection.close()
        print("MySQL connection is closed.")
