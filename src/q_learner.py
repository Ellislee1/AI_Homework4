import numpy as np
from typing import List, Tuple
from pathlib import Path
from direction import Direction

Q_VALUE = List[float]
BASE_Q_PATH = 'src/world'
GRID_WIDTH = 40
WORLD_SIZE = GRID_WIDTH * GRID_WIDTH


class QLearner:

    def __init__(self, lr: float = 0.2, gamma: float = 0.02, world: int = 0):
        self.lr = lr
        self.gamma = gamma
        self.world = world
        self.q_values: List[Q_VALUE] = []

    def read_q_values(self):
        path = BASE_Q_PATH + str(self.world) + '.txt'
        q_values: List[Q_VALUE] = []
        # if existing q values are already present for this world
        if Path(path).exists():
            # open the file if it exists, otherwise create it
            with open(path, 'r+') as f:
                # q values are saved in the form: N, S, E, W
                for line in f:
                    line = line.strip()
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
        with open(path, 'w+') as f:
            # write each q value as separate line
            for values in self.q_values:
                # create comma separated list
                joined = ','.join(str(x) for x in values)
                f.write(joined + '\n')
        return

    def update_q_value(self, location: Tuple[int, int], direction: str, reward, new_location: Tuple[int, int]):
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
        direction: int
        if direction == Direction.NORTH:
            direction = 0
        elif direction == Direction.SOUTH:
            direction = 1
        elif direction == Direction.EAST:
            direction = 2
        else:
            direction = 3

        # get the previous value from the saved q values
        previous_value: float = previous_q_values[direction]

        # get the q values for the new location
        new_x, new_y = new_location
        new_q_values = self.q_values[new_x + new_y*GRID_WIDTH]
        # Apply an exponential moving average
        new_reward: float = (1-self.lr) * previous_value + self.lr * (reward + self.gamma * np.max(new_q_values))

        # Update existing q value
        self.q_values[x + y*GRID_WIDTH][direction] = new_reward
