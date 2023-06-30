import psycopg2
from psycopg2 import sql
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
# from time import sleep 

# sleep(10)

# Connect to the PostgreSQL server
conn = psycopg2.connect(
    host="db",
    port=5432,
    dbname="hudsondb",
    user="hudsondb",
    password="HouseOfTemplates"
)

# Set isolation level to autocommit
conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)

# Create a cursor
cursor = conn.cursor()

# Define the SQL statement to create the table
create_table_query = """
CREATE TABLE Template (
  id SERIAL PRIMARY KEY,
  name VARCHAR(50),
  content TEXT,
  created_at TIMESTAMP DEFAULT NOW()
);
"""

# Execute the SQL statement
cursor.execute(create_table_query)

# Close the cursor and the connection
cursor.close()
conn.close()