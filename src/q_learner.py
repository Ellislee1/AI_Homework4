from typing import List, Tuple
from pathlib import Path

Q_VALUE = List[float]
BASE_Q_PATH = 'src/world'
WORLD_SIZE = 1600


class QLearner:

    def __init__(self, world: int = 0):
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
