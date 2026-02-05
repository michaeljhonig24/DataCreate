import random
import pickle

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

def minimax(board, depth, is_maximizing, bot_choice, player_choice, alpha=-float('inf'), beta=float('inf')):
    winner = check_winner(board)
    if winner == bot_choice:
        return 10 - depth
    if winner == player_choice:
        return depth - 10
    if all(cell != '-' for row in board for cell in row):
        return 0
    
    if is_maximizing:
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

class QLearningAgent:
    def __init__(self, epsilon=0.05, alpha=0.6, gamma=0.95):
        self.q_table = {}
        self.epsilon = epsilon
        self.alpha = alpha
        self.gamma = gamma

    def get_state_key(self, board):
        return ''.join([''.join(row) for row in board])
        
    def get_q_value(self, state, action):
        state_key = self.get_state_key(state)
        if state_key not in self.q_table:
            self.q_table[state_key] = {}
        return self.q_table[state_key].get(action, 0.0)

    def get_available_actions(self, board):
        actions = []
        for row in range(3):
            for col in range(3):
                if board[row][col] == '-':
                    actions.append((row, col))
        return actions
    
    def choose_action(self, board, training=True):
        available_actions = self.get_available_actions(board)
        if not available_actions:
            return None
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
        state_key = self.get_state_key(state)
        if state_key not in self.q_table:
            self.q_table[state_key] = {}
        next_actions = self.get_available_actions(next_state)
        max_next_q = 0
        if next_actions:
            max_next_q = max([self.get_q_value(next_state, action) for action in next_actions])
        current_q = self.q_table[state_key].get(action, 0.0)
        new_q = current_q + self.alpha * (reward + self.gamma * max_next_q - current_q)
        self.q_table[state_key][action] = new_q

    def save_model(self, filename='q_table.pkl'):
        with open(filename, 'wb') as f:
            pickle.dump(self.q_table, f)
        print(f'Model saved to {filename}')

def train_agent(episodes):
    agent = QLearningAgent()
    initial_epsilon = 0.3
    final_epsilon = 0.001
    initial_alpha = 0.9
    final_alpha = 0.3
    wins = 0
    losses = 0
    draws = 0

    for episode in range(episodes):
        agent.epsilon = initial_epsilon - (initial_epsilon - final_epsilon) * (episode / episodes)
        agent.alpha = initial_alpha - (initial_alpha - final_alpha) * (episode / episodes)
        board = [['-','-','-'],['-','-','-'],['-','-','-']]
        game_history = []
        agent_is_x = (episode % 2 == 0)

        if agent_is_x:
            current_player = 'X'
            agent_symbol = 'X'
            opponent_symbol = 'O'
        else:
            current_player = 'O'
            agent_symbol = 'O'
            opponent_symbol = 'X'

        while True:
            if current_player == agent_symbol:
                state = [row[:] for row in board]
                action = agent.choose_action(board, training=True)
                if action is None:
                    break
                row, col = action
                board[row][col] = agent_symbol
                game_history.append((state, action))
                winner = check_winner(board)
                if winner == agent_symbol:
                    reward = 10
                    for state, action in game_history:
                        agent.update_q_value(state, action, reward, board)
                    wins += 1
                    break
                elif winner == opponent_symbol:
                    reward = -10
                    for state, action in game_history:
                        agent.update_q_value(state, action, reward, board)
                    losses += 1
                    break
                if all(cell != '-' for row in board for cell in row):
                    reward = 0
                    for state, action in game_history:
                        agent.update_q_value(state, action, reward, board)
                    draws += 1
                    break
                current_player = opponent_symbol
            else:
                minimax_prob = 0.85
                if random.random() < minimax_prob:
                    bot_position = get_best_move(board, opponent_symbol, agent_symbol)
                    if bot_position is not None:
                        row = bot_position // 3
                        col = bot_position % 3
                    else:
                        break
                else:
                    available = []
                    for row in range(3):
                        for col in range(3):
                            if board[row][col] == '-':
                                available.append((row, col))
                    if not available:
                        break
                    row, col = random.choice(available)
                board[row][col] = opponent_symbol
                winner = check_winner(board)
                if winner == opponent_symbol:
                    reward = -10
                    for state, action in game_history:
                        agent.update_q_value(state, action, reward, board)
                    losses += 1
                    break
                current_player = agent_symbol

        if (episode + 1) % 10000 == 0:
            print(f'Episode {episode + 1}/{episodes}')
            print(f'Wins: {wins}, Losses: {losses}, Draws: {draws}')
            print(f'win rate: {wins/(wins+losses+draws) * 100:.2f}%')
            wins = losses = draws = 0

    agent.save_model()
    return agent

if __name__ == '__main__':
    print('Starting Q-Learning training')
    agent = train_agent(episodes=150000)
    print('\n Training complete!')
    print('Model saved as q_table.pkl')
    print('You can now use hard difficulty in the game!')