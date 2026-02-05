from flask import Blueprint, render_template, request, jsonify
from database.db_utils import save_tictactoe_game
import random
import time
import pickle

ttt_bp = Blueprint('tictactoe', __name__, url_prefix='/tictactoe')

rl_agent = None
board = [['-','-','-'],['-','-','-'],['-','-','-']]
difficulty = 'easy'

@ttt_bp.route('/')
def game():
    return render_template('TicTacToe.html')


@ttt_bp.route('/set_difficulty', methods=['POST'])
def set_difficulty():
    global difficulty
    try:
        data = request.get_json()
        difficulty = data.get('difficulty', 'easy')
        print(f'Difficulty set to: {difficulty}')
        return jsonify({"status": "success", "difficulty": difficulty}), 200
    except Exception as e:
        print(f'Error: {e}')
        return jsonify({"status": "error", "message": str(e)}), 500
    

@ttt_bp.route('/get_index', methods=['POST'])
def get_pos():
    global difficulty
    try:
        data = request.get_json()
        choice = data.get('choice')
        position = int(data.get('position'))
        if (position <= 2 and position >= 0):
            board[0][position] = choice
            move = [0, position]
        elif (position <= 5 and position >= 3):
            board[1][position - 3] = choice
            move = [1, position - 3]
        else:
            board[2][position - 6] = choice
            move = [2, position - 6]
        print(f'Current board: {board}')
        print(f'Move played: {move}')
        winner = check_winner(board)
        
        if winner:
            print(f'Winner Found!')
            return jsonify({"status": "success",
                            "board": board,
                            "winner": winner,
                            "bot_move": None}), 200
        
        if all(cell != '-' for row in board for cell in row):
            return jsonify({"status": "success",
                            "board": board,
                            "winnner": None,
                            "bot_move": None}), 200
        
        time.sleep(1)

        
        if choice == 'X':
            bot_choice = 'O'
        else:
            bot_choice = 'X'

        if difficulty == 'easy':
            bot_position = get_random_move(board)
        elif difficulty == 'medium':
            bot_position = get_rl_move(board)
        elif difficulty == 'hard':
            bot_position = get_best_move(board, bot_choice, choice)
        else:
            bot_position = get_random_move(board)

        if bot_position is not None:
            if (bot_position <= 2 and bot_position >= 0):
                board[0][bot_position] = bot_choice
                bot_move = [0, bot_position]
            elif (bot_position <= 5 and bot_position >= 3):
                board[1][bot_position - 3] = bot_choice
                bot_move = [1, bot_position - 3]
            else:
                board[2][bot_position - 6] = bot_choice
                bot_move = [2, bot_position - 6]
            print(f'Current board after Bot: {board}')

            winner = check_winner(board)

            print(f'Bot Move Played: {bot_move}')
            return jsonify({
                        "status": 'success',
                        "board": board,
                        "winner": winner,
                        "bot_move": bot_position
                }), 200
            
        return jsonify({"status": "success",
                        "board": board, "winner": None,
                        "bot_move": None}), 200
    
    except Exception as e:
        print(f'Error: {e}')
        return jsonify({"status": "error", "message": str(e)}), 500

@ttt_bp.route('/reset', methods=['POST'])
def reset():
    global board 
    board = [['-','-','-'],['-','-','-'],['-','-','-']]
    print(f'Board reset: {board}')
    return jsonify({"status": "success", "board": board}), 200

@ttt_bp.route('/save_stats', methods=['POST'])
def save_stats():
    try:
        data = request.get_json()
        save_tictactoe_game(
            difficulty=data['difficulty'],
            winner = data['winner'],
            total_moves = data['total_moves'],
            player_symbol = data['player_symbol']
        )
        return jsonify({"status": "success"}), 200
    except Exception as e:
        print(f'Error saving stats: {e}')
        return jsonify({"status": "error", "message": str(e)}), 500

@ttt_bp.route('/load_model', methods=["POST"])
def load_model_route():
    # load pre-trained model
    global rl_agent
    rl_agent = QLearningAgent()
    success = rl_agent.load_model('q_table.pkl')
    if success:
        return jsonify({'status': 'success'}), 200
    else:
        return jsonify({'status': 'error', 'message': 'No model found'}), 404
    
def get_random_move(board):
    empty_positions = []
    for row in range(3):
        for col in range(3):
            if board[row][col] == '-':
                position = row * 3 + col
                empty_positions.append(position)
    
    if empty_positions:
        return random.choice(empty_positions)
    return None

def minimax(board, depth, is_maximizing, bot_choice, player_choice, alpha=-float('inf'), beta=float('inf')):
    winner = check_winner(board)
    # Base cases
    if winner == bot_choice:
        # Bot wins Prefer faster wins
        return 10 - depth
    if winner == player_choice:
        # Player wins prefer slower losses
        return depth - 10 
    if all(cell != '-' for row in board for cell in row):
        return 0 # check if board is full
    
    if is_maximizing:
        #bot's turn - maximize score
        best_score = -float('inf')
        for row in range(3):
            for col in range(3):
                if board[row][col] == '-':
                    board[row][col] = bot_choice
                    score = minimax(board, depth + 1, False, bot_choice, player_choice, alpha, beta)
                    board[row][col] = '-'
                    best_score = max(score, best_score)
                    alpha = max(alpha, score)
                    if beta <= alpha:
                        break
            if beta <= alpha:
                break
        return best_score
    else:
        #Player's turn - minimize score
        best_score = float('inf')
        for row in range(3):
            for col in range(3):
                if board[row][col] == '-':
                    board[row][col] = player_choice
                    score = minimax(board, depth + 1, True, bot_choice, player_choice, alpha, beta)
                    board[row][col] = '-'
                    best_score = min(score, best_score)
                    beta = min(beta, score)
                    if beta <= alpha:
                        break
            if beta <= alpha:
                break
        return best_score
    
def get_best_move(board, bot_choice, player_choice):
    best_score = -float('inf')
    best_move = None

    for row in range(3):
        for col in range(3):
            if board[row][col] == '-':
                board[row][col] = bot_choice
                score = minimax(board, 0, False, bot_choice, player_choice)
                board[row][col] = '-'
                if score > best_score:
                    best_score = score
                    best_move = row * 3 + col
    return best_move

def check_winner(board):
    for row in board:
        if row[0] == row[1] == row[2] and row[0] != '-':
            return row[0]
    for col in range(3):
        if board[0][col] == board[1][col] == board[2][col] and board[0][col] != '-':
            return board[0][col]

    if board[0][0] == board[1][1] == board[2][2] and board[0][0] != '-':
        return board[0][0]
    if board[0][2] == board[1][1] == board[2][0] and board[0][2] != '-':
        return board[0][2]
    
    return None


class QLearningAgent:
    def __init__(self, epsilon = 0.05, alpha = 0.6, gamma = 0.95):
        self.q_table = {} # State-action pairs
        self.epsilon = epsilon # Exploration rate
        self.alpha = alpha # Learning Rate
        self.gamma = gamma # Discount Factor for future rewards

    def get_state_key(self, board):
        return ''.join([''.join(row) for row in board])
        # converts board into one hashable string
        # ex board becomes "XOOXOXOOX"
        
    def get_q_value(self, state, action):
        state_key = self.get_state_key(state)
        if state_key not in self.q_table:
            self.q_table[state_key] = {}
        return self.q_table[state_key].get(action, 0.0)
        # Q-value for state-action pair

    def get_available_actions(self, board):
        #get all empty positions
        actions = []

        for row in range(3):
            for col in range(3):
                if board[row][col] == '-':
                    actions.append((row, col))
        return actions
    
    def choose_action(self, board, training=True):
        # greedy selection process for actions
        available_actions = self.get_available_actions(board)

        if not available_actions:
            return None
        
        # random move from avaiable actions
        if training and random.random() < self.epsilon:
            return random.choice(available_actions)
        
        best_action = None
        best_value = -float('inf')
        
        for action in available_actions:
            q_value = self.get_q_value(board, action)
            if q_value > best_value:
                best_value = q_value
                best_action = action

        if best_action is not None:
            return best_action
        else:
            return random.choice(available_actions)
        
    def update_q_value(self, state, action, reward, next_state):
        # state: s, action: a, reward: r, next_state: s'
        state_key = self.get_state_key(state)
        if state_key not in self.q_table:
            self.q_table[state_key] = {}

        #get max Q-value for next state
        next_actions = self.get_available_actions(next_state)
        max_next_q = 0
        if next_actions:
            max_next_q = max([self.get_q_value(next_state, action) for action in next_actions])

        current_q = self.q_table[state_key].get(action, 0.0)
        new_q = current_q + self.alpha * (reward + self.gamma * max_next_q - current_q)
        self.q_table[state_key][action] = new_q
        # Q-learning update formula

    def save_model(self, filename = 'q_table.pkl'):
        # save trained q-table
        with open(filename, 'wb') as f:
            pickle.dump(self.q_table, f)
        print(f'Model saved to {filename}')

    def load_model(self, filename = 'q_table.pkl'):
        try:
            with open(filename, 'rb') as f:
                self.q_table = pickle.load(f)
                print(f'Model loaded from {filename}')
                return True
        except FileNotFoundError:
            print('No saved model found')
            return False
        
def get_rl_move(board):
    # get move from trained RL agent
    global rl_agent
    if rl_agent is None:
        rl_agent = QLearningAgent()
        rl_agent.load_model('q_table_trained.pkl')

    action = rl_agent.choose_action(board, training=False)
    if action:
        row, col = action
        return row * 3 + col
    return None
