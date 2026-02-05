from database.db_setup import create_connection

def test_connection():
    """Test database connection."""
    conn = create_connection()
    if conn:
        print("Database connection successful.")
        cursor = conn.cursor()

        cursor.execute("SELECT table_name FROM information_schema.tables WHERE table_schema='public'")
        tables = cursor.fetchall()

        print("\n Tables in the database:")
        for table in tables:
            print(table[0])

        cursor.close()
        conn.close()
    else:
        print("Failed to connect to the database.")

if __name__ == "__main__":
    test_connection()