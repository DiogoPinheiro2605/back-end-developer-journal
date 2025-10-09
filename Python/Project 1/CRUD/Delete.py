import sys
import os


sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from Connection import get_connection

def main():
    conn = get_connection()
    cursor = conn.cursor()

    sale_id = 2

    # secure DELETE query
    query = "DELETE FROM sales WHERE idSales = %s"
    cursor.execute(query, (sale_id,))

    conn.commit()
    print(f"✅ Sale with ID {sale_id} deleted successfully!")

    cursor.close()
    conn.close()

if __name__ == "__main__":
    main()
