import requests
from typing import List, Optional, Tuple, Union

API_FILE_PATH = 'src/api.txt'
TEAM_ID = '1314'
MAIN_API = 'https://www.notexponential.com/aip2pgaming/api/rl/gw.php'
INFO_API = 'https://www.notexponential.com/aip2pgaming/api/rl/score.php'
OK = 'OK'


class Api:
    
    def __init__(self):
        # parse api key info
        with open(API_FILE_PATH) as f:
            self.api_key = f.readline().strip()
            self.user_id = f.readline().strip()
        self.moves: List[Tuple[int, int]] = []
        # Added dummy user agent because the default python user-agent was being rejected
        self.headers = {'x-api-key': self.api_key, 'userid': self.user_id, 'Content-Type':
                        'application/x-www-form-urlencoded', 'User-Agent': 'XY'}
        self.world = 0
        self.location = -1, -1
        self.run_id = -1
        return

    def enter_world(self, world_id: int = 0):
        """Create a new game with the specified opponent id."""
        data = {'type': 'enter', 'worldId': str(world_id), 'teamId': TEAM_ID}
        try:
            response = requests.post(MAIN_API, headers=self.headers, data=data)
            json = response.json()
            if json['code'] == OK:
                self.world = json['worldId']
                self.run_id = json['runId']
            else:
                print('There was an error creating the game. ', end='')
                if 'message' in json:
                    print(json['message'], end='')
                print()
        except requests.exceptions.HTTPError as e:
            print('There was an error entering the world: ', e)

    def get_location(self):
        """Get the current location"""
        params = {'type': 'location', 'teamId': TEAM_ID}
        try:
            response = requests.get(MAIN_API, headers=self.headers, params=params)
            json = response.json()
            if json['code'] == OK:
                world = int(json['world'])
                state = json['state']
                print(f'world: {world}, state: {state}')
            else:
                print('Something went wrong getting the current location. ', end='')
                if 'message' in json:
                    print(json['message'], end='')
                print()
        except requests.exceptions.HTTPError as e:
            print('There was an error getting the current location: ', e)

    def make_move(self, direction: str) -> Optional[Tuple[Tuple[int, int], float]]:
        """Make a move in the specified direction.py (N, S, E, W)"""
        data = {'teamId': TEAM_ID, 'type': 'move', 'move': direction, 'worldId': self.world}
        try:
            response = requests.post(MAIN_API, headers=self.headers, data=data)
            json = response.json()
            if json['code'] == OK:
                if response.status_code == 200:
                    x = int(json['newState']['x'])
                    y = int(json['newState']['y'])
                    location = x, y
                    self.location = location
                    print('Location after move: ', self.location)
                    increment = json['scoreIncrement']
                    # todo: update q values based on reward
                    reward = json['reward']
                    return location, reward
                else:
                    print('Something went wrong making a move. Status code: ', response.status_code)
            else:
                print('Something went wrong making a move. ', end='')
                if 'message' in json:
                    print(json['message'], end='')
                print()
        except requests.exceptions.HTTPError as e:
            print('There was an error making the move: ', e)

        return None

    def get_runs(self):
        """Get a list of all the moves from the current game (the newest move is at the start)."""
        params = {'teamId': TEAM_ID, 'type': 'runs', 'count': 20}
        try:
            response = requests.get(INFO_API, headers=self.headers, params=params)
            json = response.json()
            if json['code'] == OK:
                print('runs: ', json['runs'])
                return self.moves
            else:
                print('Something went wrong getting the runs. ', end='')
                if 'message' in json:
                    print(json['message'], end='')
                print()
        except requests.exceptions.HTTPError as e:
            print('There was an error getting the runs: ', e)

    def get_score(self):
        """Gets the current score (only useful after many runs have been completed)."""
        params = {'teamId': TEAM_ID, 'type': 'score'}
        try:
            response = requests.get(INFO_API, headers=self.headers, params=params)
            json = response.json()
            if json['code'] == OK:
                print('score: ', json['score'])
            else:
                print('Something went wrong getting the runs. ', end='')
                if 'message' in json:
                    print(json['message'], end='')
                print()
        except requests.exceptions.HTTPError as e:
            print('There was an error getting the runs: ', e)

