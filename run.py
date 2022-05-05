import argparse
from src.q_learner import QLearner
from src.api import Api
from src.direction import Direction


def make_move_loop(world: int = 0):
    api = Api()
    q_learner = QLearner(world=world)
    explorations = 0
    location = api.get_location()
    print('location: ', location)
    if not location:
        print('You are not currently in a world. Entering world ', world)
        api.enter_world(world)
        location = 0, 0

    while explorations < 2:
        direction = q_learner.pick_direction(location)
        new_location, reward = api.make_move(direction)

        q_learner.update_q_value(location, direction, reward, new_location)
        # hit an exit tile (ex: (19, 0) in world 0)
        if not new_location:
            print('new exploration: ', explorations)
            print(f'Reward: {reward}')
            # increase the number of explorations when we exit a world
            explorations += 1
            new_location = 0, 0
            # Decay the epsilon for the next iteration
            q_learner.decay_epsilon()
            q_learner.increment_world_run()
            api.enter_world(world)

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


def get_runs():
    api = Api()
    api.get_runs()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Process inputs for world exploration')
    parser.set_defaults(world=0)
    parser.add_argument('-world', '--world', type=int, dest='world', default=0)

    args = parser.parse_args()
    run(world=args.world)
    # get_runs()
    # q_learner.save_values_to_file()

    # api_tests()
