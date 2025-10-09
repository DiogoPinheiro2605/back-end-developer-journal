import sys
import os


sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from Connection import get_connection

def main():
    conn = get_connection()
    cursor = conn.cursor()

    sale_id = (input("Which is the id of the product that you want to delete from the shop?"))

    # secure DELETE query
    query = "DELETE FROM sales WHERE idSales = %s"
    cursor.execute(query, (sale_id,))

    conn.commit()
    print(f"✅ Sale with ID {sale_id} deleted successfully!")

    cursor.close()
    conn.close()

if __name__ == "__main__":
    main()
