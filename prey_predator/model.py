"""
Prey-Predator Model
================================

Replication of the model found in NetLogo:
    Wilensky, U. (1997). NetLogo Wolf Sheep Predation model.
    http://ccl.northwestern.edu/netlogo/models/WolfSheepPredation.
    Center for Connected Learning and Computer-Based Modeling,
    Northwestern University, Evanston, IL.
"""

from mesa import Model
from mesa.space import MultiGrid
from mesa.datacollection import DataCollector

from prey_predator.agents import Sheep, Wolf, GrassPatch
from prey_predator.schedule import RandomActivationByBreed


class WolfSheep(Model):
    """
    Wolf-Sheep Predation Model
    """

    description = (
        "A model for simulating wolf and sheep (predator-prey) ecosystem modelling."
    )

    moore = True
    sheep_initial_energy = 50
    wolf_initial_energy = 50

    def __init__(
        self,
        height=20,
        width=20,
        initial_sheep=100,
        initial_wolves=50,
        sheep_reproduce=0.04,
        wolf_reproduce=0.05,
        wolf_gain_from_food=20,
        grass=False,
        grass_regrowth_time=30,
        sheep_gain_from_food=4,
    ):
        """
        Create a new Wolf-Sheep model with the given parameters.

        Args:
            initial_sheep: Number of sheep to start with
            initial_wolves: Number of wolves to start with
            sheep_reproduce: Probability of each sheep reproducing each step
            wolf_reproduce: Probability of each wolf reproducing each step
            wolf_gain_from_food: Energy a wolf gains from eating a sheep
            grass: Whether to have the sheep eat grass for energy
            grass_regrowth_time: How long it takes for a grass patch to regrow
                                 once it is eaten
            sheep_gain_from_food: Energy sheep gain from grass, if enabled.
        """
        super().__init__()
        # Set parameters
        self.height = height
        self.width = width
        self.initial_sheep = initial_sheep
        self.initial_wolves = initial_wolves
        self.sheep_reproduce = sheep_reproduce
        self.wolf_reproduce = wolf_reproduce
        self.wolf_gain_from_food = wolf_gain_from_food
        self.grass = grass
        self.grass_regrowth_time = grass_regrowth_time
        self.sheep_gain_from_food = sheep_gain_from_food

        self.schedule = RandomActivationByBreed(self)
        self.grid = MultiGrid(self.height, self.width, torus=True)
        data = {"Wolves": lambda m: m.schedule.get_breed_count(Wolf), "Sheep": lambda m: m.schedule.get_breed_count(Sheep)}
        if self.grass:
            data["Grass"] = lambda m: len([grass for grass in m.schedule.agents_by_breed[GrassPatch].values() if grass.is_grown])
        self.datacollector = DataCollector(data)

        # Create sheep:
        for _ in range(self.initial_sheep):
            pos = (self.random.randrange(self.width), self.random.randrange(self.height))
            sheep = Sheep(self.next_id(), pos, self, self.moore, self.random.randrange(self.sheep_initial_energy))
            self.schedule.add(sheep)
            self.grid.place_agent(sheep, pos)

        # Create wolves:
        for _ in range(self.initial_wolves):
            pos = (self.random.randrange(self.width), self.random.randrange(self.height))
            wolf = Wolf(self.next_id(), pos, self, self.moore, self.random.randrange(self.wolf_initial_energy))
            self.schedule.add(wolf)
            self.grid.place_agent(wolf, pos)

        # Create grass patches
        for x in range(width):
            for y in range(height):
                pos = (x, y)
                grass = GrassPatch(self.next_id(), pos, self, True, self.grass_regrowth_time)
                self.schedule.add(grass)
                self.grid.place_agent(grass, pos)

    def step(self):
        self.schedule.step()
        # Collect data
        self.datacollector.collect(self)

    def run_model(self, step_count=200):
        for _ in range(step_count):
            self.step()
            

