import numpy as np
from typing import List, Tuple
from pathlib import Path
from src.direction import Direction

Q_VALUE = List[float]
BASE_Q_PATH = 'src/world'
GRID_WIDTH = 40
WORLD_SIZE = GRID_WIDTH ** 2
DECAY_FACTOR = 0.95


class QLearner:

    def __init__(self, lr: float = 0.2, gamma: float = 0.02, world: int = 0, epsilon: float = 0.3):
        self.lr = lr
        self.gamma = gamma
        self.epsilon = epsilon
        self.world_run = 0
        self.world = world
        self.q_values: List[Q_VALUE] = []
        self.read_q_values()

    def read_q_values(self):
        # sourcery skip: for-append-to-extend, for-index-underscore
        path = BASE_Q_PATH + str(self.world) + '.txt'
        q_values: List[Q_VALUE] = []
        # if existing q values are already present for this world
        if Path(path).exists():
            # open the file if it exists, otherwise create it
            with open(path, 'r+') as f:
                # q values are saved in the form: N, S, E, W
                for i, line in enumerate(f):
                    if i == 0:
                        header = line.strip().split(',')
                        self.world_run = int(header[0])+1
                        self.epsilon = float(header[1])
                        continue

                    line = line.strip()

                    if line == '':
                        continue
                    # convert values to float
                    values = list(map(float, line.split(',')))
                    q_values.append(values)
        else:
            # otherwise create new q values
            for i in range(WORLD_SIZE):
                q_values.append([0, 0, 0, 0])

        self.q_values = q_values

    def save_values_to_file(self):
        path = BASE_Q_PATH + str(self.world) + '.txt'
        # print('PATH: ', path)
        with open(path, 'w+') as f:
            joined = f'{self.world_run},{self.epsilon}\n'
            # write each q value as separate line
            for values in self.q_values:
                # create comma separated list
                joined += ','.join(str(x) for x in values)
                joined += '\n'
            f.write(joined + '\n')

    def update_q_value(self, location: Tuple[int, int], direction: Direction, reward, new_location: Tuple[int, int]):
        """ Updates the q values based on the location and the move direction.

        API grid world is organized as follows:
         -----------------
        | 0,2 | 1,2 | 2,2 |
        | --------------- |
        | 0,1 | 1,1 | 2,1 |
        | --------------- |
        | 0,0 | 1,0 | 2,0 |
         -----------------
         (i.e. starts from the bottom left corner). Need to map this to the 1-d array of q-values
        """
        x, y = location
        # get the index of the previous q value at this location
        previous_q_values = self.q_values[x + y*GRID_WIDTH]

        # get the corresponding direction
        if direction.value == Direction.NORTH.value:
            _direction = 0
        elif direction.value == Direction.SOUTH.value:
            _direction = 1
        elif direction.value == Direction.EAST.value:
            _direction = 2
        else:
            _direction = 3

        # get the previous value from the saved q values
        previous_value: float = previous_q_values[_direction]

        # if an exit square was hit, just use the reward (new location is None)
        if not new_location:
            new_reward = reward
        else:
            # get the q values for the new location
            new_x, new_y = new_location
            new_q_values = self.q_values[new_x + new_y*GRID_WIDTH]
            # Apply an exponential moving average
            new_reward: float = (1-self.lr) * previous_value + self.lr * (reward + self.gamma * np.max(new_q_values))

        # Update existing q value
        self.q_values[x + y*GRID_WIDTH][_direction] = round(new_reward, 5)

    def pick_direction(self, location: Tuple[int, int]):
        # Get current values for a position.
        # If all zeros pick a random action from possible actions
        # If not use decaying epsilon greedy value to pick next move.

        x, y = location

        current_values = np.array(self.q_values[x + y*GRID_WIDTH])

        if np.random.normal() < self.epsilon or np.all(current_values == 0):
            # Select random action if we are less than our epsilon or if we have no information about the space
            action = np.random.randint(0,4)
        else:
            # Select the best action
            action = np.argmax(current_values)

        if action == 0:
            return Direction.NORTH
        elif action == 1:
            return Direction.SOUTH
        elif action == 2:
            return Direction.EAST
        else:
            return Direction.WEST

    def increment_world_run(self):
        self.world_run += 1

    def decay_epsilon(self):
        self.epsilon *= DECAY_FACTOR




