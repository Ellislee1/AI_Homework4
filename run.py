from src.board import Board
from src.agent import Agent
from src.q_learner import QLearner
from src.api import Api
from src.direction import Direction


def make_move_loop(world: int = 0):
    api = Api()
    q_learner = QLearner()
    flagOne = True
    flagTwo = True
    location = api.get_location()

    while flagOne and flagTwo:
        # print('q vals: ', q_learner.q_values)
        # enter a world if not in one
        if not location:
            print("new location")
            api.enter_world(world)
            location = 0, 0
            flagOne = False

        # direction = Direction.SOUTH
        direction = q_learner.pick_direction(location)
        new_location, reward = api.make_move(direction)

        q_learner.update_q_value(location, direction, reward, new_location)
        # hit an exit tile (ex: (19, 0) in world 0)
        if not new_location:
            print("new location")
            api.enter_world(world)
            flagTwo = False

        q_learner.save_values_to_file()
        location = new_location


def run(world: int = 0):
     #b = Board()
     #b.print_world()
     #a = Agent(b)
     #a.play(5000)
    make_move_loop(world)


def api_tests():
    # api = Api()
    # api.enter_world()
    # api.get_location()
    # api.make_move(Direction.NORTH)
    # api.get_location()

    # api.get_score()
    # api.get_runs()
    return


if __name__ == "__main__":
    run()
    # q_learner.save_values_to_file()

    # api_tests()
