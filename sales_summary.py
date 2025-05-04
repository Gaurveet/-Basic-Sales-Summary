
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt

# Step 1: Connect to (or create) the SQLite database
conn = sqlite3.connect("sales_data.db")
cursor = conn.cursor()

# Step 2: Create sales table (if it doesn't already exist)
cursor.execute("""
    CREATE TABLE IF NOT EXISTS sales (
        id INTEGER PRIMARY KEY,
        product TEXT,
        quantity INTEGER,
        price REAL
    )
""")

# Step 3: Insert sample data (skip if already populated)
sample_data = [
    ('Apple', 10, 0.5),
    ('Banana', 5, 0.3),
    ('Apple', 15, 0.5),
    ('Orange', 8, 0.7),
    ('Banana', 12, 0.3),
    ('Orange', 4, 0.7),
]
cursor.executemany("INSERT INTO sales (product, quantity, price) VALUES (?, ?, ?)", sample_data)
conn.commit()

# Step 4: Run SQL query to get total quantity and revenue per product
query = """
    SELECT 
        product, 
        SUM(quantity) AS total_qty, 
        SUM(quantity * price) AS revenue 
    FROM sales 
    GROUP BY product
"""
df = pd.read_sql_query(query, conn)

# Step 5: Print the result
print("Sales Summary:")
print(df)

# Step 6: Plot bar chart
df.plot(kind='bar', x='product', y='revenue', legend=False, color='skyblue')
plt.ylabel("Revenue")
plt.title("Revenue by Product")
plt.tight_layout()

# Save the chart (optional)
plt.savefig("sales_chart.png")

# Show plot
plt.show()

# Step 7: Close the connection
conn.close()
