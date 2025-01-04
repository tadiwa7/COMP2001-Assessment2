import pyodbc

#connection details
server = 'dist-6-505.uopnet.plymouth.ac.uk'
database = 'COMP2001_TKandira'
username = 'TKandira'
password = 'NfkW662*'
driver = '{ODBC Driver 17 for SQL Server}'

#connection string
conn_str = (
   f'DRIVER={driver};'
   f'SERVER={server};'
   f'DATABASE={database};'
   f'UID={username};'
   f'PWD={password};'
   'Encrypt=Yes;'
   'TrustServerCertificate=Yes;'
   'Connection Timeout=30;'
   'Trusted_Connection=No'
)

# Establishing the connection
def get_db_connection():
    """
    Establish and return a new database connection.
    """
    try:
        conn = pyodbc.connect(conn_str)
        return conn
    except Exception as e:
        print("Error occurred while connecting to the database:", str(e))
        raise

# Test database connection function
def test_db_connection():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT 1")  # Simple query to test the connection
        result = cursor.fetchone()
        conn.close()
        return f"Database connection is working. Result: {result[0]}"
    except Exception as e:
        return f"Database connection failed: {str(e)}"

# Call the test function
print(test_db_connection())