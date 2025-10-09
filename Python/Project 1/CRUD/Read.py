import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from Connection import get_connection

def main():
    conn = get_connection()
    cursor = conn.cursor()

    query = ("SELECT * FROM sales")
    cursor.execute(query)

    rows = cursor.fetchall()
    for row in rows:
        print(row)

    cursor.close()
    conn.close()

if __name__ == "__main__":
    main()
