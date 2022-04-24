from src.board import Board
from src.agent import Agent
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
    api_tests()
