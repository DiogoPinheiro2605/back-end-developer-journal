import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from Connection import get_connection

# --- Código principal ---
conn = get_connection()
cursor = conn.cursor()

product_name = (input("What product do you want to add to the shop?\n"))
value = (input("How much will this product cost?\n"))

query = "INSERT INTO sales (product_name, value) VALUES (%s, %s)"
cursor.execute(query, (product_name, value))

conn.commit()
cursor.close()
conn.close()

print("Data inserted successfully!")
