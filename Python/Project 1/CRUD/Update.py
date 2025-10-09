import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from Connection import get_connection

def main():
    conn = get_connection()
    cursor = conn.cursor()

    sale_id = 1 
    product_name = "Radio"
    value = 123

    # secure UPDATE query
    query = "UPDATE sales SET product_name = %s, value = %s WHERE idSales = %s"
    cursor.execute(query, (product_name, value, sale_id))

    conn.commit()
    print(f"✅ UPDATED SUCESSUFLY!")

    cursor.close()
    conn.close()

if __name__ == "__main__":
    main()
