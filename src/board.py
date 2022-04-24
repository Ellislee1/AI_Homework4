import numpy as np
from copy import deepcopy

KEY = {
    5: '███',
    # 1: '$$$',
    # -1: '!!!',
    # # 0: '___',
    # 10: ' ■ '
}


class Board:
    def __init__(self, size=4, no_win=1, no_loss=2, max_walls=3, deterministic = True):
        self.initialize_board(size, no_win, no_loss, max_walls)
        self.deterministic = deterministic
        self.probs = [0.3, 0.7, 0.8, 0.9]
    
    def initialize_board(self, size, no_win, no_loss, max_walls):
        self.board = np.zeros((size,size))

        self.win_states = set()
        self.lose_states = set()
        self.walls = set()

        while no_win > 0:
            coords = np.random.randint(0, size, 2)
            if self.board[coords[0],coords[1]] == 0:
                self.board[coords[0],coords[1]] = 10

                self.win_states.add(np.array2string(coords))

                no_win -= 1
        
        print(self.win_states)
        while no_loss > 0:
            coords = np.random.randint(0,size,2)
            if self.board[coords[0],coords[1]] == 0:
                self.board[coords[0],coords[1]] = -10
                self.lose_states.add(np.array2string(coords))
                no_loss -= 1
        
        max_walls = np.random.randint(max(max_walls-2,1),max_walls+1)

        print(self.lose_states)
        while max_walls > 0:
            coords = np.random.randint(0,size,2)
            if self.board[coords[0],coords[1]] == 0:
                self.board[coords[0],coords[1]] = 5
                self.walls.add(np.array2string(coords))
                max_walls -= 1

        print(self.walls)

        self.state = self.start

    @property
    def start(self):
        start = None
        while start is None:
            coords = np.random.randint(0, len(self.board),2)
            s = np.array2string(coords)
            if s not in self.walls and s not in self.win_states and s not in self.lose_states:
                start = coords
        
        return start

    @property
    def is_end(self):
        return (np.array2string(self.state) in self.win_states) or (np.array2string(self.state) in self.lose_states)

    @property
    def reward(self):
        if np.array2string(self.state) in self.win_states:
            return 10
        if np.array2string(self.state) in self.lose_states:
            return -10
        
        return 0
    
    def update_vals(self, vals):
        for i, val in vals.items():
            if i in self.walls or i in self.lose_states or i in self.win_states:
                continue
            i = i.replace('[','').replace(']','')

            pos = np.fromstring(i, dtype=int, sep=' ')
            
            self.board[pos[0],pos[1]] = val

    def move_position(self, action):
        next_state = self.state.copy()

        actions = ["up", "right", "down", "left"]

        index = actions.index(action)

        add = 0
        if not self.deterministic:
            ran = np.random.uniform(0,1)
            
            if 0.95 <= ran < 1:
                add = 3
            elif 0.9 <= ran < 0.9:
                add = 2
            elif 0.7 <= ran < 0.8:
                add = 10
        
        index = (index+add) % len(actions)

        action = actions[index]

        if action == "up":
            next_state = np.array([self.state[0]-1, self.state[1]])
        elif action == "down":
            next_state = np.array([self.state[0]+1, self.state[1]])
        elif action == "left":
            next_state = np.array([self.state[0], self.state[1]-1])
        elif action == "right":
            next_state = np.array([self.state[0], self.state[1]+1])
        
        if next_state[0] < 0 or next_state[0] > len(self.board)-1:
            return self.state.copy()
        elif next_state[1] < 0 or next_state[1] > len(self.board)-1:
            return self.state.copy()
        
        return self.check_walls(next_state)
    
    def check_walls(self, next_state):
        if np.array2string(next_state) in self.walls:
            return self.state.copy()
        return next_state

    def print_world(self):
        for row in self.board:
            row_s = '|'
            for col in row:
                if col not in KEY:
                    row_s += f'{col:.1f}|'
                else:
                    row_s += f'{KEY[col]}|'
            print(row_s)

    def copy(self):
        return deepcopy(self)
