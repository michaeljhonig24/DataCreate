import psycopg2
from psycopg2 import sql

def create_connection():
    """Create a database connection."""
    try:
        conn = psycopg2.connect(
            host="localhost",
            database="boardgames_db",
            user="michael",
            password="test"
        )
        return conn
    except Exception as e:
        print(f"Error connecting to database: {e}")
        return None
    
def init_database():
    """" Initialize database tables"""
    conn = create_connection()
    if conn is None:
        return
    
    cursor = conn.cursor()

    # Create users table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tictactoe_stats (
                   id SERIAL PRIMARY KEY,
                   game_data TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                   difficulty VARCHAR(50),
                   winner VARCHAR(50),
                   total_moves INTEGER,
                   player_symbol VARCHAR(5)
                   );
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS checkers_stats (
                   id SERIAL PRIMARY KEY,
                   game_data TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                   difficulty VARCHAR(50),
                   winner VARCHAR(50),
                   total_moves INTEGER,
                   player_captures INTEGER,
                   bot_captures INTEGER,
                   player_king_captures INTEGER,
                   bot_king_captures INTEGER
                   );
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS connectfour_stats (
                   id SERIAL PRIMARY KEY,
                   game_data TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                   difficulty VARCHAR(50),
                   winner VARCHAR(50),
                   total_moves INTEGER,
                   player_color VARCHAR(10)
                   );
    """)

    conn.commit()
    cursor.close()
    conn.close()
    print("Database initialized successfully.")

if __name__ == "__main__":
    init_database()