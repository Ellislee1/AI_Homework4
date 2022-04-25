from src.board import Board
from src.agent import Agent
from src.q_learner import QLearner
from src.api import Api


def run():
    b = Board()
    b.print_world()

    a = Agent(b)

    a.play(5000)


def api_tests():
    api = Api()
    # api.enter_world()
    # api.get_score()
    api.get_location()
    api.make_move('N')
    # api.get_location()
    # api.get_runs()


if __name__ == "__main__":
    # run()
    q_learner = QLearner()
    q_learner.read_q_values()
    print('q vals: ', q_learner.q_values)
    # q_learner.save_values_to_file()

    # api_tests()
