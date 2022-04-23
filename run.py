from src.board import Board
from src.agent import Agent

b = Board()
b.print_world()

a = Agent(b)

a.play(5000)