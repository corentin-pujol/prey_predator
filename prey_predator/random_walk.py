"""
Generalized behavior for random walking, one grid cell at a time.
"""

from mesa import Agent
#from prey_predator.agents import Sheep, Wolf
import prey_predator.agents

class RandomWalker(Agent):
    """
    Class implementing random walker methods in a generalized manner.

    Not indended to be used on its own, but to inherit its methods to multiple
    other agents.

    """

    grid = None
    x = None
    y = None
    moore = True

    def __init__(self, unique_id, pos, model, moore=True):
        """
        grid: The MultiGrid object in which the agent lives.
        x: The agent's current x coordinate
        y: The agent's current y coordinate
        moore: If True, may move in all 8 directions.
                Otherwise, only up, down, left, right.
        """
        super().__init__(unique_id, model)
        self.pos = pos
        self.moore = moore

    def random_move(self):
        """
        Step one cell in any allowable direction.
        """
        # Pick the next cell from the adjacent cells.
        next_moves = self.model.grid.get_neighborhood(self.pos, self.moore, True)
        next_move = self.random.choice(next_moves)
        # Now move:
        self.model.grid.move_agent(self, next_move)

    def reproduce(self, parent):
        """When an agent reproduces, its energy is halved and it creates a child with similar parameters"""
        parent.energy //= 2
        if type(parent) is prey_predator.agents.Sheep:
            child = prey_predator.agents.Sheep(parent.model.next_id(), parent.pos, parent.model, parent.moore, parent.energy, parent.energy_thresh)
        else:
            child = prey_predator.agents.Wolf(parent.model.next_id(), parent.pos, parent.model, parent.moore, parent.energy, parent.energy_thresh)

        parent.model.schedule.add(child)
        parent.model.grid.place_agent(child, parent.pos)

    def kill(self, entity):
        """Dynamic deletion of the agent"""
        entity.model.grid.remove_agent(entity)
        entity.model.schedule.remove(entity)
