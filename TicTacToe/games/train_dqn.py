import copy
import torch
import torch.nn as nn
import torch.optim as optim
from collections import deque
import random


device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print(f'Using device: {device}')


def create_board():
    board = [['-' for _ in range(8)] for _ in range(8)]

    for row in range(3):
        for col in range(8):
            if (row + col) % 2 == 1:
                board[row][col] = '⚫️'

    for row in range(5, 8):
        for col in range(8):
            if (row + col) % 2 == 1:
                board[row][col] = '⚪️'
    return board

def calculate_valid_moves(board, row, col, player):
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
            if(mid_piece == opponent or mid_piece in ['♛', '♕']) and board[jump_row][jump_col] == '-':
                valid_moves.append(jump_row * 8 + jump_col)

    return valid_moves

def get_all_valid_moves_for_player(board, player):
    moves = []

    for row in range(8):
        for col in range(8):
            piece = board[row][col]

            if player == '⚪️' and piece in ['⚪️', '♕']:
                valid_moves = calculate_valid_moves(board, row, col, piece)
                for move in valid_moves:
                    moves.append({'from': row * 8 + col,
                                  'to': move,
                                  'piece': piece
                                  })
            elif player == '⚫️' and piece in ['⚫️', '♛']:
                valid_moves = calculate_valid_moves(board, row, col, piece)
                for move in valid_moves:
                    moves.append({
                        'from': row * 8 + col,
                        'to': move,
                        'piece': piece
                    })

    return moves

def make_move_on_board(board, move):
    new_board = copy.deepcopy(board)
    from_pos = move['from']
    to_pos = move['to']
    from_row = from_pos // 8
    from_col = from_pos % 8
    to_row = to_pos // 8
    to_col = to_pos % 8

    piece = new_board[from_row][from_col]
    new_board[to_row][to_col] = piece
    new_board[from_row][from_col] = '-'

    if abs(to_row - from_row) == 2:
        mid_row = (from_row + to_row) // 2
        mid_col = (from_col + to_col) // 2
        new_board[mid_row][mid_col] = '-'

    if (piece == '⚪️' and to_row == 0) or (piece == '⚫️' and to_row == 7):
        new_board[to_row][to_col] = '♕' if piece == '⚪️' else '♛'

    return new_board

def check_winner(board):

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

def minimax(board, player, depth=2):
    moves = get_all_valid_moves_for_player(board, player)
    if not moves:
        return None
    best_move= None
    best_score = float('-inf')

    for move in moves:
        new_Board = make_move_on_board(board, move)
        score = evaluate_board(new_Board, player)

        if score > best_score:
            best_score = score
            best_move = move
    
    return best_move

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

def easy_bot_move(board, player):
    moves = get_all_valid_moves_for_player(board, player)

    if not moves:
        return None
    
    if random.random() < 0.7:
        return random.choice(moves)
    
    best_move = None
    best_score = float('-inf')
    
    for move in moves:
        new_board = make_move_on_board(board, move)
        score = evaluate_board(new_board, player)
        
        if score > best_score:
            best_score = score
            best_move = move
    
    return best_move if best_move else random.choice(moves)

def medium_bot_move(board, player):
    moves = get_all_valid_moves_for_player(board, player)

    if not moves:
        return None
    
    best_move = None
    best_score = float('-inf')

    for move in moves:
        new_board = make_move_on_board(board, move)
        score = evaluate_board(new_board, player)

        if score > best_score: 
            best_score = score
            best_move = move

    if best_move is None:
        return random.choice(moves)

    return best_move

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
    
class ReplayMemory:
    def __init__(self, capacity = 10000):
        self.memory = deque(maxlen=capacity)

    def push(self, state, reward, next_state, done):
        self.memory.append((state, reward, next_state, done))

    def sample(self, batch_size):
        return random.sample(self.memory, batch_size)

    def __len__(self):
        return len(self.memory)
            
class DQNAgent:
    def __init__(self, learning_rate=0.001, gamma = 0.95):
        self.device = device

        self.model = CheckersDQN().to(device)
        self.target_model = CheckersDQN().to(device)
        self.target_model.load_state_dict(self.model.state_dict())

        self.optimizer = optim.Adam(self.model.parameters(), lr=learning_rate)
        self.loss_fn = nn.MSELoss()
        self.memory = ReplayMemory()

        self.gamma = gamma
        self.epsilon = 1.0
        self.epsilon_decay = 0.9995
        self.epsilon_min = 0.1

        self.batch_size = 64
        self.update_target_every = 100
        self.episodes_trained = 0

    def select_action(self, board, valid_moves, player):
        if random.random() < self.epsilon:
            return random.choice(valid_moves)
        else:
            best_move = None
            best_q = float('-inf')

            for move in valid_moves:

                test_board = make_move_on_board(board, move)
                state = board_to_state(test_board).to(self.device)

                with torch.no_grad():
                    q_value = self.model(state).item()

                if q_value > best_q:
                    best_q = q_value
                    best_move = move
            
            return best_move if best_move else random.choice(valid_moves)
    
    def calculate_reward(self, old_board, new_board, player, done, winner):
        if done:
            if winner == player:
                return 100
            elif winner is None:
                return 0
            else:
                return -100
            
        old_score = self.count_pieces(old_board, player)
        new_score = self.count_pieces(new_board, player)

        reward = (new_score - old_score) * 20
        return reward
    
    def count_pieces(self, board, player):
        score = 0
        player_king = '♕' if player == '⚪️' else '♛'
        for row in board:
            for cell in row:
                if cell == player:
                    score += 1
                elif cell == player_king:
                    score += 2
        return score
    
    def train_step(self):
        if len(self.memory) < self.batch_size:
            return
        
        for _ in range(3):
            batch = self.memory.sample(self.batch_size)
            
            for state, reward, next_state, done in batch:

                state = state.to(self.device)
                next_state = next_state.to(self.device)
                current_q = self.model(state)

                with torch.no_grad():
                    next_q = self.target_model(next_state)
                    if done:
                        target_q = reward
                    else:
                        target_q = reward + self.gamma * next_q.item()

                target_q_tensor = torch.FloatTensor([target_q]).detach().to(self.device)

                loss = self.loss_fn(current_q, target_q_tensor)

                self.optimizer.zero_grad()
                loss.backward()
                self.optimizer.step()

    def update_target_model(self):
        self.target_model.load_state_dict(self.model.state_dict())
    def decay_epsilon(self):
        self.epsilon = max(self.epsilon_min, self.epsilon * self.epsilon_decay)

    def save_model(self, path='checkers_dqn.pth'):
        torch.save({'model_state_dict': self.model.state_dict(), 
                   'optimizer_state_dict': self.optimizer.state_dict(),
                   'epsilon': self.epsilon,
                   'episodes_trained': self.episodes_trained}, path)
        self.model.to(self.device)
        print(f'Model saved to {path}')

    def load_model(self, path='checkers_dqn.pth'):
        checkpoint = torch.load(path, map_location=self.device)
        self.model.load_state_dict(checkpoint['model_state_dict'])
        self.target_model.load_state_dict(checkpoint['model_state_dict'])
        self.optimizer.load_state_dict(checkpoint['optimizer_state_dict'])
        self.epsilon = checkpoint['epsilon']
        self.episodes_trained = checkpoint['episodes_trained']
        print(f'Model loaded from {path}')

def train_dqn(episodes=2000, save_every=500):
    agent = DQNAgent()

    try:
        agent.load_model()
        print("continuing training from saved model")
    except:
        print('starting fresh training')

    wins = 0
    losses = 0
    draws = 0

    for episode in range(episodes):
        board = create_board()
        
        player = '⚪️'
        opponent = '⚫️'
        done = False
        move_count = 0
        max_moves = 200

        while not done and move_count < max_moves:
            valid_moves = get_all_valid_moves_for_player(board, player)
            if not valid_moves:
                done = True
                winner = opponent
                break

            old_board = copy.deepcopy(board)
            move = agent.select_action(board, valid_moves, player)
            board = make_move_on_board(board, move)

            winner = check_winner(board)
            if winner:
                done = True
            
            reward = agent.calculate_reward(old_board, board, player, done, winner)

            state = board_to_state(old_board)
            next_state = board_to_state(board)
            agent.memory.push(state, reward, next_state, done)

            if done:
                break
        
            opponent_moves = get_all_valid_moves_for_player(board, opponent)
            if not opponent_moves:
                done = True
                winner = player
                break
        
            opp_moves = easy_bot_move(board, opponent)
            if opp_moves:
                board = make_move_on_board(board, opp_moves)

            winner = check_winner(board)
            if winner:
                done = True
            
            move_count += 1

        if move_count >= max_moves:
            winner = None
        
        agent.train_step()

        if episode % agent.update_target_every == 0:
            agent.update_target_model()
        
        agent.decay_epsilon()
        agent.episodes_trained += 1

        if winner == player:
            wins += 1
        elif winner == opponent:
            losses += 1
        else:
            draws += 1
        
        if episode % 100 == 0:
            total = wins + losses + draws
            win_rate = wins / total * 100 if total > 0 else 0
            print (f"Episode {episode}/{episodes} | "
                   f"W: {wins} L: {losses} D: {draws} | "
                   f"Win Rate: {win_rate: .1f}% | "
                   f"Epsilon: {agent.epsilon: .3f}")
            wins = 0
            losses = 0
            draws = 0
            
        if episode % save_every == 0 and episode > 0:
            agent.save_model()
            wins = 0
            losses = 0
            draws = 0


    agent.save_model()
    print("training complete")

if __name__ == "__main__":
    # train for 1500 more episodes.
    train_dqn(1500, save_every=500)

        