import numpy as np
np.random.seed(118)

class Agent:
    def __init__(self, board, lr=0.2, epsilon=0.02):
        self.states = []
        self.actions = ["up", "down", "left", "right"]
        self.state = board
        self.lr = lr
        self.epsilon = epsilon

        self.state_values = {}
        for y, y_pos in enumerate(board.board):
            for x, val in enumerate(y_pos):
                self.state_values[np.array2string(np.array([y,x]))] = val
    
    def chooseAction(self):
        mx_next_rwrd = float('-inf')
        action = np.random.choice(self.actions)

        if np.random.uniform(0,1) <= self.epsilon:
            return np.random.choice(self.actions)
        
        for a in self.actions:
            next_rwrd = self.state_values[np.array2string(self.state.movePosition(a))]

            if next_rwrd > mx_next_rwrd:
                action = a
                mx_next_rwrd = next_rwrd
        
        return action

    def act(self, action):
        position = self.state.movePosition(action)
        b = self.state.copy()
        b.state = position
        return b
    
    def reset(self):
        self.states = []
        self.state.state = self.state.start

    def play(self, epochs = 10):
        i = 0
        while i < epochs:
            if self.state.is_end:
                reward = self.state.reward

                self.state_values[np.array2string(self.state.state)] = reward
                print(f'Epoch {i} Game Over!\t{reward}')

                for s in reversed(self.states[:-1]):
                    key = np.array2string(s)
                    reward = self.state_values[key] + self.lr * (reward - self.state_values[key])
                    self.state_values[key] = round(reward, 3)
                
                self.state.update_vals(self.state_values)
                self.state.print_world()
                self.reset()
                i += 1
                self.epsilon = max((1-(i/epochs))/2, 0.03)
                print(self.epsilon)
            else:
                action = self.chooseAction()

                self.states.append(self.state.movePosition(action))

                self.state = self.act(action)
            

