import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from Connection import get_connection

def main():
    conn = get_connection()
    cursor = conn.cursor()

    sale_id = (input("Which is the id of the product that you want to change?\n")) 
    product_name = (input("What is the new name of the product?\n")) 
    value = (input("How much will this item cost ?\n")) 

    # secure UPDATE query
    query = "UPDATE sales SET product_name = %s, value = %s WHERE idSales = %s"
    cursor.execute(query, (product_name, value, sale_id))

    conn.commit()
    print(f"✅ UPDATED SUCESSUFLY!")

    cursor.close()
    conn.close()

if __name__ == "__main__":
    main()
