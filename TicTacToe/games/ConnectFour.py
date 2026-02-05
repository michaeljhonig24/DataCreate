from flask import Blueprint, render_template, request, jsonify
from database.db_utils import save_connectfour_game
import random
import copy
import math

connectfour_bp = Blueprint('connectfour', __name__, url_prefix='/connectfour')   

board = [['' for _ in range(7)] for _ in range(6)]
difficulty = 'easy'

@connectfour_bp.route('/')
def game():
    return render_template('ConnectFour.html')

@connectfour_bp.route('/reset', methods=['POST'])
def reset():
    global board
    board = [['' for _ in range(7)] for _ in range(6)]
    print('Board reset')
    return jsonify({'status': 'success', 'board': board}), 200

@connectfour_bp.route('/set_difficulty', methods=['POST'])
def set_difficulty():
    global difficulty
    try:
        data = request.get_json()
        difficulty = data.get('difficulty', 'easy')
        print(f'Difficulty set to {difficulty}')
        return jsonify({'status': 'success', 'difficulty': difficulty}), 200
    except Exception as e:
        print(f'Error setting difficulty: {e}')
        return jsonify({'status': 'error', 'message': str(e)}), 500
    
@connectfour_bp.route('/make_move', methods=['POST'])
def make_move():
    try:
        data = request.get_json()
        column = data['column']
        player = data['player']

        piece = 'R' if player == "Red" else 'Y'

        row = get_lowest_row(column)
        
        if row == -1:
            print(f'Column {column} is full!')
            return jsonify({'status': 'error', 'message': 'Column is full'}), 400
        
        board[row][column] = piece
        print(f'Placed {piece} at row {row}, column {column}')
        print(f'Board state after move:')
        for r in range(6):
            print(f'Row {r}: {board[r]}')

        winner = check_winner(board)
        tie = is_board_full(board) and not winner

        return jsonify({
            'status': 'success',
            'board': board,
            'winner': 'Red' if winner == 'R' else 'Yellow' if winner == 'Y' else None,
            'tie': tie
        }), 200
    
    except Exception as e:
        print(f'Error making move: {e}')
        import traceback
        traceback.print_exc()
        return jsonify({'status': 'error', 'message': str(e)}), 500

@connectfour_bp.route('/save_stats', methods=['POST'])
def save_stats():
    try:
        data = request.get_json()
        save_connectfour_game(
            difficulty=data['difficulty'],
            winner=data['winner'],
            total_moves=data['total_moves'],
            player_color=data['player_color']
        )
        return jsonify({'status': 'success'}), 200
    except Exception as e:
        print(f'Error saving game stats: {e}')
        return jsonify({'status': 'error', 'message': str(e)}), 500
    
@connectfour_bp.route('/bot_move', methods=['POST'])
def bot_move():
    try:
        data = request.get_json()
        difficulty_level = data.get('difficulty', 'easy')
        player = data.get('player')

        piece = "R" if player == "Red" else "Y"

        if difficulty_level == 'easy':
            column = get_random_move(board)
        elif difficulty_level == 'medium':
            column = minimax_move(board, piece, depth=4)
        else:
            column = mcts_move(board, piece, simulations=1000)

        if column is None:
            return jsonify({'status': 'error', 'message': 'No valid moves available'}), 400
        
        row = get_lowest_row(column)
        if row == -1:
            print(f'Column {column} is full!')
            return jsonify({'status': 'error', 'message': 'Column is full'}), 400
        
        board[row][column] = piece

        print(f'Placed {piece} at row {row}, column {column}')
        print(f'Board state after move:')
        for r in range(6):
            print(f'Row {r}: {board[r]}')

        winner = check_winner(board)
        tie = is_board_full(board) and not winner

        print(f'Bot move: column {column}, row {row}')
        return jsonify({
            'status': 'success',
            'board': board,
            'column': column,
            'winner': 'Red' if winner == 'R' else 'Yellow' if winner == 'Y' else None,
            'tie': tie
        }), 200
    
    except Exception as e:
        print(f'Error making bot move: {e}')
        import traceback
        traceback.print_exc()
        return jsonify({'status': 'error', 'message': str(e)}), 500

# HELPER FUNCTIONS 

def get_lowest_row(column):
    """Find lowest available row in a column"""
    for row in range(5, -1, -1):  # Start from bottom (row 5)
        if board[row][column] == '':
            return row
    return -1  # Column is full

def get_valid_columns(board_state):
    """Get list of valid columns"""
    valid = []
    for col in range(7):
        if board_state[0][col] == '':  # Top row empty = column available
            valid.append(col)
    return valid

def is_board_full(board_state):
    """Check if board is completely full"""
    for row in board_state:
        if '' in row:
            return False
    return True

def check_winner(board_state):
    """Check if there's a winner. Returns 'R', 'Y', or None"""
    
    # Check horizontal
    for row in range(6):
        for col in range(4):
            if board_state[row][col] != '':
                if (board_state[row][col] == board_state[row][col+1] ==
                    board_state[row][col+2] == board_state[row][col+3]):
                    return board_state[row][col]
    
    # Check vertical
    for row in range(3):
        for col in range(7):
            if board_state[row][col] != '':
                if (board_state[row][col] == board_state[row+1][col] ==
                    board_state[row+2][col] == board_state[row+3][col]):
                    return board_state[row][col]
    
    # Check diagonal (down-right)
    for row in range(3):
        for col in range(4):
            if board_state[row][col] != '':
                if (board_state[row][col] == board_state[row+1][col+1] ==
                    board_state[row+2][col+2] == board_state[row+3][col+3]):
                    return board_state[row][col]
    
    # Check diagonal (down-left)
    for row in range(3):
        for col in range(3, 7):
            if board_state[row][col] != '':
                if (board_state[row][col] == board_state[row+1][col-1] ==
                    board_state[row+2][col-2] == board_state[row+3][col-3]):
                    return board_state[row][col]
    
    return None

def make_test_move(board_state, column, piece):
    """Make a move on a copy of the board"""
    new_board = copy.deepcopy(board_state)
    
    for row in range(5, -1, -1):
        if new_board[row][column] == '':
            new_board[row][column] = piece
            return new_board
    
    return None  # Column full

#  EASY BOT (RANDOM)

def get_random_move(board_state):
    """Random move selection"""
    valid_columns = get_valid_columns(board_state)
    if not valid_columns:
        return None
    return random.choice(valid_columns)

# MEDIUM BOT (MINIMAX)

def evaluate_board(board_state, piece):
    """Simple board evaluation"""
    opponent = 'Y' if piece == 'R' else 'R'
    score = 0
    
    # Center column preference
    center_array = [board_state[row][3] for row in range(6)]
    center_count = center_array.count(piece)
    score += center_count * 3
    
    # Check for potential wins
    score += count_windows(board_state, piece, 4) * 100
    score += count_windows(board_state, piece, 3) * 5
    score += count_windows(board_state, piece, 2) * 2
    
    # Check opponent threats
    score -= count_windows(board_state, opponent, 4) * 100
    score -= count_windows(board_state, opponent, 3) * 10
    
    return score

def count_windows(board_state, piece, length):
    """Count windows of a certain length"""
    count = 0
    
    # Horizontal
    for row in range(6):
        for col in range(7 - 3):  # 7 - 4 + 1
            window = [board_state[row][col + i] for i in range(4)]
            if window.count(piece) == length and window.count('') == 4 - length:
                count += 1
    
    # Vertical
    for row in range(6 - 3):  # 6 - 4 + 1
        for col in range(7):
            window = [board_state[row + i][col] for i in range(4)]
            if window.count(piece) == length and window.count('') == 4 - length:
                count += 1
    
    # Diagonal (down-right)
    for row in range(6 - 3):
        for col in range(7 - 3):
            window = [board_state[row + i][col + i] for i in range(4)]
            if window.count(piece) == length and window.count('') == 4 - length:
                count += 1
    
    # Diagonal (down-left)
    for row in range(6 - 3):
        for col in range(3, 7):
            window = [board_state[row + i][col - i] for i in range(4)]
            if window.count(piece) == length and window.count('') == 4 - length:
                count += 1
    
    return count

def minimax(board_state, depth, alpha, beta, maximizing_player, piece):
    """Minimax with alpha-beta pruning"""
    valid_cols = get_valid_columns(board_state)
    winner = check_winner(board_state)
    is_terminal = winner is not None or len(valid_cols) == 0
    
    if depth == 0 or is_terminal:
        if is_terminal:
            if winner == piece:
                return (None, 100000)
            elif winner is not None:
                return (None, -100000)
            else:
                return (None, 0)
        else:
            return (None, evaluate_board(board_state, piece))
    
    if maximizing_player:
        value = -math.inf
        best_col = random.choice(valid_cols)
        
        for col in valid_cols:
            temp_board = make_test_move(board_state, col, piece)
            if temp_board:
                new_score = minimax(temp_board, depth - 1, alpha, beta, False, piece)[1]
                if new_score > value:
                    value = new_score
                    best_col = col
                alpha = max(alpha, value)
                if alpha >= beta:
                    break
        
        return best_col, value
    
    else:  # Minimizing player
        value = math.inf
        opponent = 'Y' if piece == 'R' else 'R'
        best_col = random.choice(valid_cols)
        
        for col in valid_cols:
            temp_board = make_test_move(board_state, col, opponent)
            if temp_board:
                new_score = minimax(temp_board, depth - 1, alpha, beta, True, piece)[1]
                if new_score < value:
                    value = new_score
                    best_col = col
                beta = min(beta, value)
                if alpha >= beta:
                    break
        
        return best_col, value

def minimax_move(board_state, piece, depth=4):
    """Get best move using minimax"""
    column, score = minimax(board_state, depth, -math.inf, math.inf, True, piece)
    return column

# HARD BOT (MCTS) 

class MCTSNode:
    def __init__(self, board_state, parent=None, move=None, piece=None):
        self.board = board_state
        self.parent = parent
        self.move = move
        self.piece = piece
        self.children = []
        self.wins = 0
        self.visits = 0
        self.untried_moves = get_valid_columns(board_state)
    
    def is_fully_expanded(self):
        return len(self.untried_moves) == 0
    
    def is_terminal(self):
        return check_winner(self.board) is not None or is_board_full(self.board)
    
    def best_child(self, exploration=1.41):
        """Select best child using UCB1 formula"""
        best_score = -math.inf
        best_children = []
        
        for child in self.children:
            if child.visits == 0:
                return child
            
            exploit = child.wins / child.visits
            explore = exploration * math.sqrt(math.log(self.visits) / child.visits)
            score = exploit + explore
            
            if score > best_score:
                best_score = score
                best_children = [child]
            elif score == best_score:
                best_children.append(child)
        
        return random.choice(best_children) if best_children else None
    
    def expand(self):
        """Expand tree by adding a child node"""
        move = self.untried_moves.pop()
        opponent = 'Y' if self.piece == 'R' else 'R'
        new_board = make_test_move(self.board, move, opponent)
        
        if new_board is None:
            return None
        
        child = MCTSNode(new_board, parent=self, move=move, piece=opponent)
        self.children.append(child)
        return child

def simulate(board_state, piece):
    """Simulate a random game from current state"""
    current_board = copy.deepcopy(board_state)
    current_piece = piece
    
    while True:
        winner = check_winner(current_board)
        if winner is not None:
            return 1 if winner == piece else -1
        
        valid_cols = get_valid_columns(current_board)
        if not valid_cols:
            return 0
        
        col = random.choice(valid_cols)
        current_board = make_test_move(current_board, col, current_piece)
        
        if current_board is None:
            return 0
        
        current_piece = 'Y' if current_piece == 'R' else 'R'

def mcts_move(board_state, piece, simulations=1000):
    """Get best move using Monte Carlo Tree Search"""
    root = MCTSNode(board_state, piece=piece)
    
    for _ in range(simulations):
        node = root
        
        # Selection
        while not node.is_terminal() and node.is_fully_expanded():
            node = node.best_child()
        
        # Expansion
        if not node.is_terminal() and not node.is_fully_expanded():
            node = node.expand()
        
        # Simulation
        if node:
            opponent = 'Y' if piece == 'R' else 'R'
            result = simulate(node.board, opponent)
        else:
            result = 0
        
        # Backpropagation
        while node is not None:
            node.visits += 1
            node.wins += result
            result = -result  # Flip for opponent
            node = node.parent
    
    # Choose best move
    if not root.children:
        valid_cols = get_valid_columns(board_state)
        return random.choice(valid_cols) if valid_cols else None
    
    best_child = max(root.children, key=lambda c: c.visits)
    return best_child.move