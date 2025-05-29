import pyodbc

# Database connection parameters
# server = '192.168.1.226'  # Your SQL Server instance
# database = 'test_db'        # Target database
# username = 'climbing_user'  # Created SQL user
# password = 'hoosierheights' # Assigned password
# driver = '{ODBC Driver 18 for SQL Server}'  # Ensure this driver is installed

server = '127.0.0.1'         # Or your Docker container's IP
port = '1433'
database = 'test_db'
username = 'climbing_user'
password = 'hoosierheights'
# username = 'sa'
# password = 'H00S13Rheights'
driver = '/opt/homebrew/lib/libtdsodbc.so'  # FreeTDS .so driver

# Construct the connection string
# conn_str = f'''
#     DRIVER={driver};
#     SERVER={server};
#     DATABASE={database};
#     UID={username};
#     PWD={password};
#     TrustServerCertificate=yes;
#     Encrypt=yes;
# '''

conn_str = (
    f"DRIVER={driver};"
    f"SERVER={server};"
    f"PORT={port};"
    f"DATABASE={database};"
    f"UID={username};"
    f"PWD={password};"
    f"TDS_Version=7.4;"
)

try:
    # Establish the connection
    conn = pyodbc.connect(conn_str)
    cursor = conn.cursor()

    # Test the connection by retrieving the current user
    cursor.execute("SELECT USER_NAME();")
    row = cursor.fetchone()
    print(f"Connected successfully! Logged in as: {row[0]}")

    # Close the connection
    cursor.close()
    conn.close()
except Exception as e:
    print(f"Error: {e}")
