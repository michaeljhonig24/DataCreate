from database.db_utils import get_tictactoe_stats, get_checkers_stats, get_connectfour_stats    
import json

def view_all_stats():
    print("\n" + "="*50)
    print("Tic-Tac-Toe Stats")
    print("="*50)
    ttt_stats = get_tictactoe_stats()
    print(json.dumps(ttt_stats, indent=2))

    print("\n" + "="*50)
    print("Checkers Stats")
    print("="*50)
    checkers_stats = get_checkers_stats()
    print(json.dumps(checkers_stats, indent=2))

    print("\n" + "="*50)
    print("Connect Four Stats")
    print("="*50)
    connectfour_stats = get_connectfour_stats()
    print(json.dumps(connectfour_stats, indent=2))

if __name__ == "__main__":
    view_all_stats()