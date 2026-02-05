from database.db_setup import create_connection

def save_tictactoe_game(difficulty, winner, total_moves, player_symbol):
    """Save Tic-Tac-Toe game stats"""
    conn = create_connection()
    if not conn:
        return
    
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO tictactoe_stats(difficulty, winner, total_moves, player_symbol)
        VALUES (%s, %s, %s, %s)
    """, (difficulty, winner, total_moves, player_symbol))

    conn.commit()
    cursor.close()
    conn.close()

def save_checkers_game(difficulty, winner, total_moves, player_captures, bot_captures, player_king_captures, bot_king_captures):
    """Save Checkers game stats"""
    conn = create_connection()
    if not conn:
        return
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO checkers_stats(difficulty, winner, total_moves, player_captures, bot_captures, player_king_captures, bot_king_captures)
                   VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, (difficulty, winner, total_moves, player_captures, bot_captures, player_king_captures, bot_king_captures)) 
    conn.commit()
    cursor.close()
    conn.close()

def save_connectfour_game(difficulty, winner, total_moves, player_color):
    """Save Connect Four game stats"""
    conn = create_connection()
    if not conn:
        return
    
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO connectfour_stats(difficulty, winner, total_moves, player_color)
        VALUES (%s, %s, %s, %s)
    """, (difficulty, winner, total_moves, player_color))

    conn.commit()
    cursor.close()
    conn.close()

def get_tictactoe_stats():
    """Get Tic-Tac-Toe game stats"""
    conn = create_connection()
    if not conn:
        return {}
    
    cursor = conn.cursor()
    # total number of games
    cursor.execute("SELECT COUNT(*) FROM tictactoe_stats")
    total_games = cursor.fetchone()[0]

    # win rates
    cursor.execute("SELECT winner, COUNT(*) FROM tictactoe_stats GROUP BY winner")
    wins = dict(cursor.fetchall())

    # win rate by difficulty
    cursor.execute("""SELECT difficulty, winner, COUNT(*) 
                   FROM tictactoe_stats
                   GROUP BY difficulty, winner
    """)
    difficulty_stats = {}
    for difficulty, winner, count in cursor.fetchall():
        difficulty_stats.setdefault(difficulty, {})
        difficulty_stats[difficulty][winner] = int(count)

    cursor.execute("""SELECT AVG(total_moves)
                   FROM tictactoe_stats
    """)
    avg_moves = cursor.fetchone()[0] or 0

    cursor.close()
    conn.close()

    return {
        "total_games": int(total_games),
        "player_wins": int(wins.get("Player", 0)),
        "bot_wins": int(wins.get("Bot", 0)),
        "ties": int(wins.get("Tie", 0)),
        "avg_moves": float(avg_moves),
        "difficulty_stats":difficulty_stats
    }

def get_checkers_stats():
    """Get Checkers Stats"""
    conn = create_connection()
    if not conn:
        return {}
    
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM checkers_stats")
    total_games = cursor.fetchone()[0]

    cursor.execute("""SELECT winner, COUNT(*)
                   FROM checkers_stats
                   GROUP BY winner""")
    wins = dict(cursor.fetchall())

    cursor.execute("""SELECT SUM(player_captures), SUM(bot_captures), SUM(player_king_captures), SUM(bot_king_captures)
                   FROM checkers_stats""")
    captures = cursor.fetchone()

    cursor.execute("""SELECT AVG(total_moves)
                   FROM checkers_stats
    """)
    avg_moves = cursor.fetchone()[0] or 0

    cursor.close()
    conn.close()

    return {
        "total_games": total_games,
        "player_wins": wins.get("Player", 0),
        "bot_wins": wins.get("Bot", 0),
        "player_captures": captures[0] or 0,
        "bot_captures": captures[1] or 0,
        "player_king_captures": captures[2] or 0,
        "bot_king_captures": captures[3] or 0,
        "avg_moves": round(float(avg_moves), 1)
    }


def get_connectfour_stats():
    """Get Connect Four Stats"""
    conn = create_connection()
    if not conn:
        return {}
    
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM connectfour_stats")
    total_games = cursor.fetchone()[0]

    cursor.execute("""SELECT winner, COUNT(*)
                   FROM connectfour_stats
                   GROUP BY winner""")
    wins = dict(cursor.fetchall())

    cursor.execute("""SELECT AVG(total_moves)
                   FROM connectfour_stats
    """)
    avg_moves = cursor.fetchone()[0] or 0

    cursor.close()
    conn.close()

    return {
        "total_games": total_games,
        "player_wins": wins.get("Player", 0),
        "bot_wins": wins.get("Bot", 0),
        "ties": wins.get("Tie", 0),
        "avg_moves": round(float(avg_moves), 1)
    }
    
    