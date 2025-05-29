import pyodbc
import pandas as pd

# conn = pyodbc.connect(
#     "DRIVER={ODBC Driver 18 for SQL Server};"
#     "SERVER=ZAPDOS\\MOLTRES;"
#     "DATABASE=test_db;"
#     "UID=climbing_user;"
#     "PWD=hoosierheights;"
#     "TrustServerCertificate=yes;"
#     "Encrypt=yes;"
# )
# cursor = conn.cursor()



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


# df = pd.read_csv("sales.csv")

# Quick validation
# print(df.info())                 # types, null counts
# print(df.head())

# # Check for invalid prices
# df['price'] = pd.to_numeric(df['price'], errors='coerce')
# print(df[df['price'].isnull()])
# print('no nulls')
# breakpoint()

# Drop foreign keys safely
cursor.execute("""
DECLARE @sql NVARCHAR(MAX) = '';
SELECT @sql += 'ALTER TABLE ' + QUOTENAME(OBJECT_NAME(parent_object_id)) +
               ' DROP CONSTRAINT ' + QUOTENAME(name) + '; '
FROM sys.foreign_keys;
IF @sql <> ''
    EXEC sp_executesql @sql;
""")

cursor.execute("""
DROP TABLE IF EXISTS Sales, Visits, Day_Passes, Members, Customers;
""")
conn.commit()

# Table creation
cursor.execute("""
CREATE TABLE Customers (customer_id INT PRIMARY KEY, name VARCHAR(50), age INT);
CREATE TABLE Members (member_id INT PRIMARY KEY, customer_id INT, name VARCHAR(50), age INT, join_date DATE, 
                      is_active BIT, FOREIGN KEY (customer_id) REFERENCES Customers(customer_id));
CREATE TABLE Visits (visit_id INT PRIMARY KEY, member_id INT, date DATE, time TIME, duration INT, 
                     FOREIGN KEY (member_id) REFERENCES Members(member_id));
CREATE TABLE Day_Passes (day_pass_id INT PRIMARY KEY, purchaser_id INT, date DATE, pass_type VARCHAR(20), 
                         group_ages VARCHAR(100), FOREIGN KEY (purchaser_id) REFERENCES Customers(customer_id));
CREATE TABLE Sales (sale_id INT PRIMARY KEY, customer_id INT, member_id INT NULL, date DATE, item VARCHAR(50), 
                    price DECIMAL(10,2), FOREIGN KEY (customer_id) REFERENCES Customers(customer_id));
""")
conn.commit()

# Load CSV Data
for table, filename in [
    ("Customers", "customers.csv"), ("Members", "members.csv"),
                         ("Visits", "visits.csv"), ("Day_Passes", "day_passes.csv"),
                        ("Sales", "sales.csv")]:
    df = pd.read_csv(filename)
    print(f'Loading {table}')
    for row in df.itertuples(index=False, name=None):
        cursor.execute(f"INSERT INTO {table} VALUES ({', '.join(['?' for _ in row])})", row)
    conn.commit()

print("✅ Data successfully loaded into SQL Server.")
cursor.close()
conn.close()