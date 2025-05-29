import pyodbc

conn = pyodbc.connect(
    "DRIVER=/opt/homebrew/lib/libtdsodbc.so;"
    "SERVER=127.0.0.1;"  # or your IP like '192.168.1.xxx'
    "PORT=1433;"
    "DATABASE=test_db;"
    "UID=climbing_user;"
    "PWD=hoosierheights;"
    "TDS_Version=7.4;"
)
cursor = conn.cursor()

cursor.execute("""
DROP TABLE Sales;
DROP TABLE Day_Passes;
DROP TABLE Visits;
DROP TABLE Members;
DROP TABLE Customers;
""")
conn.commit()