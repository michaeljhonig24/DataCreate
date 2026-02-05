from flask import Blueprint, request, jsonify, render_template
from database.db_utils import save_checkers_game
import torch
import torch.nn as nn
import torch.optim as optim
import numpy as np
from collections import deque
import random
import copy

checkers_bp = Blueprint('checkers', __name__, url_prefix='/checkers')

board = [['-' for _ in range(8)] for _ in range(8)]
difficulty = 'easy'

@checkers_bp.route('/')
def game():
    return render_template('Checkers.html')

@checkers_bp.route('/reset', methods=["POST"])
def reset():
    global board
    board = [['-' for _ in range(8)] for _ in range(8)]

    for row in range(3):
        for col in range(8):
            if (row + col) % 2 == 1:
                board[row][col] = '⚫️'

    for row in range(5, 8):
        for col in range(8):
            if (row + col) % 2 == 1:
                board[row][col] = '⚪️'
    
    print(f'Board reset: {board}')
    return jsonify({'status': 'success', 'board': board}), 200


@checkers_bp.route('/set_difficulty', methods=['POST'])
def set_difficulty():
    global difficulty
    try:
        data = request.get_json()
        difficulty = data.get('difficulty', 'easy')
        print(f'Difficulty set to: {difficulty}')
        return jsonify({'status': "success", "difficulty": difficulty}), 200
    except Exception as e:
        print(f'Error: {e}')
        return jsonify({"status": "error", "message": str(e)}), 500
    
@checkers_bp.route('/get_valid_moves', methods=['POST'])
def get_valid_moves():
    try:
        data = request.get_json()
        position = data['position']
        player = data['player']

        row = position // 8
        col = position % 8

        valid_moves = calculate_valid_moves(row, col, player)

        return jsonify({'status': 'success', 'valid_moves': valid_moves}), 200
    except Exception as e:
        print(f'Error getting valid moves: {e}')
        return jsonify({'status': 'error', 'message': str(e)}), 500
    
@checkers_bp.route('save_stats', methods=['POST'])
def save_stats():
    try:
        data = request.get_json()
        save_checkers_game(
            difficulty=data['difficulty'],
            winner=data['winner'],
            total_moves=data['total_moves'],
            player_captures=data['player_captures'],
            bot_captures=data['bot_captures'],
            player_king_captures=data['player_king_captures'],
            bot_king_captures=data['bot_king_captures']
        )
        return jsonify({'status': 'success'}), 200
    except Exception as e:
        print(f'Error saving game stats: {e}')
        return jsonify({'status': 'error', 'message': str(e)}), 500


@checkers_bp.route('/make_move', methods=['POST'])
def make_move():
    try:
        data = request.get_json()
        from_pos = data['from']
        to_pos = data['to']
        player = data['player']

        if isinstance(from_pos, list):
            from_pos = from_pos[0]
        if isinstance(to_pos, list):
            to_pos = to_pos[0]

        from_row = from_pos // 8
        from_col = from_pos % 8
        to_row = to_pos // 8
        to_col = to_pos % 8

        board[to_row][to_col] = player
        board[from_row][from_col] = '-'

        captured = None
        if abs(to_row - from_row) == 2:
            mid_row = (from_row + to_row) // 2
            mid_col = (from_col + to_col) // 2
            board[mid_row][mid_col] = '-'
            captured = mid_row * 8 + mid_col

        if (player == '⚪️' and to_row == 0) or (player == '⚫️' and to_row == 7):
            board[to_row][to_col] = '♕' if player == '⚪️' else '♛'
        elif (player == '⚫️' and to_row == 0) or (player == '⚪️' and to_row == 7):
            board[to_row][to_col] = '♛' if player == '⚫️' else '♕'
        
        winner = check_winner()
        tie = False
        if not winner:
            opponent = '⚫️' if player in ['⚪️','♕'] else '⚪️'
            if not has_valid_moves(opponent):
                tie = True
        print(f'Current board: {board}')
        return jsonify({'status': 'success', 'board': board, 'captured': captured, 'winner': winner, 'tie': tie}), 200

    except Exception as e:
        print(f'Error making move: {e}')
        return jsonify({'status': "error", 'message': str(e)}), 500
    
def calculate_valid_moves(row, col, player):
    valid_moves = []
    piece = board[row][col]

    if player == '⚪️' or player == '♕':
        if piece not in ['⚪️','♕']:
            return []
        opponent = '⚫️'
        if piece == '♕':
            directions = [(1, -1), (1, 1), (-1, -1), (-1, 1)]
        else:
            directions = [(-1, -1), (-1, 1)]
            
    elif player == '⚫️' or player == '♛':
        if piece not in ['⚫️', '♛']:
            return []
        opponent = '⚪️'
        if piece == '♛':
            directions = [(1, -1), (1, 1), (-1, -1), (-1, 1)]
        else:
            directions = [(1, -1), (1, 1)]
    else:
        return []

    for dr, dc in directions:
        new_row = row + dr
        new_col = col + dc

        if 0 <= new_row < 8 and 0 <= new_col < 8:
            if board[new_row][new_col] == '-':
                valid_moves.append(new_row * 8 + new_col)

    for dr, dc in directions:
        jump_row = row + 2 * dr
        jump_col = col + 2 * dc
        mid_row = row + dr
        mid_col = col + dc

        if 0 <= jump_row < 8 and 0 <= jump_col < 8:
            mid_piece = board[mid_row][mid_col]
            if player == '⚪️' or player == '♕':
                can_capture = mid_piece in ['⚫️', '♛']
            else:
                can_capture = mid_piece in ['⚪️', '♕']
            if can_capture and board[jump_row][jump_col] == '-':
                valid_moves.append(jump_row * 8 + jump_col)

    return valid_moves

def has_valid_moves(player):
    for row in range(8):
        for col in range(8):
            piece = board[row][col]
            position = row * 8 + col
            if player == '⚪️' and piece in ['⚪️', '♕']:
                valid_moves = calculate_valid_moves(row, col, player)
                if valid_moves:
                    return True
            elif player == '⚫️' and piece in ['⚫️', '♛']:
                valid_moves = calculate_valid_moves(row, col, player)
                if valid_moves:
                    return True

    return False

def check_winner():

    white_pieces = 0
    black_pieces = 0

    for row in board:
        for cell in row:
            if cell in ['⚪️','♕']:
                white_pieces += 1
            elif cell in ['⚫️', '♛']:
                black_pieces += 1
    
    if white_pieces == 0:
        return '⚫️'
    elif black_pieces == 0:
        return '⚪️'
    
    return None

def get_all_valid_moves_for_player(board, player):
    moves = []

    for row in range(8):
        for col in range(8):
            piece = board[row][col]

            if player == '⚪️' and piece in ['⚪️', '♕']:
                valid_moves = calculate_valid_moves(row, col, piece)
                for move in valid_moves:
                    moves.append({'from': row * 8 + col,
                                  'to': move,
                                  'piece': piece
                                  })
            elif player == '⚫️' and piece in ['⚫️', '♛']:
                valid_moves = calculate_valid_moves(row, col, piece)
                for move in valid_moves:
                    moves.append({
                        'from': row * 8 + col,
                        'to': move,
                        'piece': piece
                    })

    return moves

def evaluate_board(board, player):
    ''' 
    Evaluate board position where:
    Positive = good for player
    Negative = good for opponent
    '''

    score = 0

    opponent = '⚫️' if player == '⚪️' else '⚪️'
    player_king = '♕' if player == '⚪️' else '♛'
    opponent_king = '♛' if player == '⚪️' else '♕'

    for row in range(8):
        for col in range(8):
            piece = board[row][col]

            if piece == player:
                score += 10
            elif piece == player_king:
                score += 15
            elif piece == opponent:
                score -= 10
            elif piece == opponent_king:
                score -= 15

    return score

def make_test_move(board, move):
    new_board = copy.deepcopy(board)

    from_pos = move['from']
    to_pos = move['to']
    from_row = from_pos // 8
    from_col = from_pos % 8
    to_row = to_pos // 8
    to_col = to_pos % 8

    # move piece
    piece = new_board[from_row][from_col]
    new_board[to_row][to_col] = piece
    new_board[from_row][from_col] = '-'

    # capture piece
    if abs(to_row - from_row) == 2:
        mid_row = (from_row + to_row) // 2
        mid_col = (from_col + to_col) // 2
        new_board[mid_row][mid_col] = '-'

    # king promotion

    if (piece == '⚪️' and to_row == 0) or (piece == '⚫️' and to_row == 7):
        new_board[to_row][to_col] = '♕' if piece == '⚪️' else '♛'
    
    return new_board

def minimax(board, depth, player, is_maximizing):

    if depth == 0:
        return evaluate_board(board, player)
    
    opponent = '⚫️' if player == '⚪️' else '⚪️'

    if is_maximizing:
        max_score = float('-inf')
        moves = get_all_valid_moves_for_player(board, player)

        if not moves:
            return -1000
        
        for move in moves:
            new_board = make_test_move(board, move)
            score = minimax(new_board, depth - 1, player, False)

            if score is not None:
                max_score = max(max_score, score)
        
        if max_score == float('-inf'):
            return evaluate_board(board, player)
        
        return max_score
    
    else:
        min_score = float('inf')
        moves = get_all_valid_moves_for_player(board, opponent)

        if not moves:
            return 1000
        
        for move in moves: 
            new_board = make_test_move(board, move)
            score = minimax(new_board, depth - 1, player, True)

            if score is not None:
                min_score = min(min_score, score)
        
        if min_score == float('inf'):
            return evaluate_board(board, player)
        
        return min_score
    
def get_best_move(board, player, depth):
    moves = get_all_valid_moves_for_player(board, player)

    if not moves:
        return None
    
    best_move = None
    best_score = float('-inf')

    for move in moves:
        new_board = make_test_move(board, move)
        score = minimax(new_board, depth - 1, player, False)

        if score is not None and score > best_score: 
            best_score = score
            best_move = move

    if best_move is None:
        return random.choice(moves)
    
    return best_move

def easy_bot_move(board, player):
    moves = get_all_valid_moves_for_player(board, player)

    if not moves:
        return None
    
    if random.random() < 0.3:
        return random.choice(moves)
    
    return get_best_move(board, player, depth = 1)

def hard_bot_move(board, player):
    moves = get_all_valid_moves_for_player(board, player)

    if not moves:
        return None

    return get_best_move(board, player, depth=5)

@checkers_bp.route('/bot_move', methods=["POST"])
def bot_move():
    try:
        data = request.get_json()
        difficulty = data.get('difficulty', 'easy')
        opponent = data.get('opponent')

        if difficulty == 'easy':
            move = easy_bot_move(board, opponent)
        elif difficulty == 'medium':
            move = medium_bot_move(board, opponent)
        else:
            move = hard_bot_move(board, opponent)

        if not move:
            return jsonify({'status': 'error', 'message': 'No valid moves'}), 400
        
        from_pos = move['from']
        to_pos = move['to']

        from_row = from_pos // 8
        from_col = from_pos % 8
        to_row = to_pos // 8
        to_col = to_pos % 8
        
        piece = board[from_row][from_col]
        board[to_row][to_col] = piece
        board[from_row][from_col] = '-'
        
        captured = None
        if abs(to_row - from_row) == 2:
            mid_row = (from_row + to_row) // 2
            mid_col = (from_col + to_col) // 2
            board[mid_row][mid_col] = '-'
            captured = mid_row * 8 + mid_col

        if (piece == '⚪️' and to_row == 0) or (piece == '⚫️' and to_row == 7):
            board[to_row][to_col] = '♕' if piece == '⚪️' else '♛'

        winner = check_winner()
        tie = False
        if not winner:
            opponent_player = '⚪️' if opponent in ['⚫️','♛'] else '⚫️'
            if not has_valid_moves(opponent_player):
                tie = True
        
        return jsonify({
            'status': 'success',
            'move': move,
            'board': board,
            'captured': captured,
            'winner': winner,
            'tie': tie
        }), 200
    
    except Exception as e:
        print(f'Error in bot_move: {e}')
        return jsonify({'status': 'error', 'message': str(e)}), 500
    
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

class CheckersDQN(nn.Module):
    def __init__(self):
        super(CheckersDQN, self).__init__()
        
        self.network = nn.Sequential(
            nn.Linear(320, 256),
            nn.ReLU(),
            nn.Dropout(0.2),
            nn.Linear(256, 128),
            nn.ReLU(),
            nn.Dropout(0.2),
            nn.Linear(128, 64),
            nn.ReLU(),
            nn.Linear(64, 1)
        )

    def forward(self, x):
        return self.network(x)
    
def board_to_state(board):
    state = []
    for row in board:
        for cell in row:
            if cell == '-':
                state.extend([1, 0, 0, 0, 0])
            elif cell == '⚪️':
                state.extend([0, 1, 0, 0, 0])
            elif cell == '⚫️':
                state.extend([0, 0, 1, 0, 0])
            elif cell == '♕':
                state.extend([0, 0, 0, 1, 0])
            elif cell == '♛':
                state.extend([0, 0, 0, 0, 1])
    return torch.FloatTensor(state)

dqn_model = None

def load_dqn_model():
    global dqn_model
    try:
        dqn_model = CheckersDQN().to(device)
        checkpoint = torch.load('checkers_dqn.pth', map_location=device)
        dqn_model.load_state_dict(checkpoint['model_state_dict'])
        dqn_model.eval()
        print("DQN model loaded successfully")
        return True
    except FileNotFoundError:
        print("DQN model file not found.")
        return False
    except Exception as e:
        print(f"Error loading DQN model: {e}")
        return False
load_dqn_model()

def medium_bot_move(board, player):
    moves = get_all_valid_moves_for_player(board, player)

    if not moves:
        print("[MEDIUM BOT] No valid moves available")
        return None
    
    if dqn_model is None:
        print('DQN model not available')
        return get_best_move(board, player, depth=5)
    
    best_move = None
    best_score = float('-inf')

    for move in moves:
        test_board = make_test_move(board, move)
        state = board_to_state(test_board).to(device)

        with torch.no_grad():
            q_value = dqn_model(state).item()

        if q_value > best_score:
            best_score = q_value
            best_move = move

    print(f'[MEDIUM BOT] Best move: {best_move}, Q-value: {best_score:.4f}')
    return best_move if best_move else random.choice(moves)


    