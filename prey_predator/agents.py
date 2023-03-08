from mesa import Agent
from prey_predator.random_walk import RandomWalker


class Sheep(RandomWalker):
    """
    A sheep that walks around, reproduces (asexually) and gets eaten.

    The init is the same as the RandomWalker.
    """

    def __init__(self, unique_id, pos, model, moore, energy=None):
        super().__init__(unique_id, pos, model, moore=moore)
        self.energy = energy

    def step(self):
        """
        A model step. Move, then eat grass and reproduce.
        """
        #first, we move
        self.random_move()

        #then we eat grass if we can
        if self.model.grass:
            entities_on_cell = self.model.grid.get_cell_list_contents([self.pos])
            grass = [ent for ent in entities_on_cell if type(ent) is GrassPatch][0]
            if grass.is_grown:
                self.eat(grass)
            
            #we loose energy
            self.energy -= 1

        #we die if we have no energy left
        if self.energy < 0 :
            self.kill(self)
            return
        
        #we reproduce
        if self.random.random() < self.model.sheep_reproduce:
            self.reproduce(self)
        
    def eat(self, grass):
        grass.mow()
        self.energy += self.model.sheep_gain_from_food

        

class Wolf(RandomWalker):
    """
    A wolf that walks around, reproduces (asexually) and eats sheep.
    """

    def __init__(self, unique_id, pos, model, moore, energy=None):
        super().__init__(unique_id, pos, model, moore=moore)
        self.energy = energy

    def step(self):
        #first, we move
        self.random_move()

        #then we eat a sheep if we can
        if self.energy < 25:
            entities_on_cell = self.model.grid.get_cell_list_contents([self.pos])
            sheep_on_cell = [ent for ent in entities_on_cell if type(ent) is Sheep]
            if len(sheep_on_cell)>0:
                chosen_sheep = self.random.choice(sheep_on_cell)
                self.eat(chosen_sheep)
        
        #we loose energy
        self.energy -= 1

        #we die if we have no energy left
        if self.energy < 0 :
            self.kill(self)
            return
    
        #we reproduce
        if self.random.random() < self.model.wolf_reproduce:
            self.reproduce(self)
    
    def eat(self, chosen_sheep):
        chosen_sheep.kill(chosen_sheep)
        self.energy += self.model.wolf_gain_from_food


class GrassPatch(Agent):
    """
    A patch of grass that grows at a fixed rate and it is eaten by sheep
    """

    timer = 0

    def __init__(self, unique_id, pos, model, fully_grown, countdown):
        """
        Creates a new patch of grass

        Args:
            grown: (boolean) Whether the patch of grass is fully grown or not
            countdown: Time for the patch of grass to be fully grown again
        """
        super().__init__(unique_id, model)
        self.is_grown = fully_grown
        self.countdown = countdown

    def step(self):
        if self.is_grown:
            return
        
        self.timer -= 1
        if self.timer < 0:
            self.is_grown=True

    def mow(self):
        self.is_grown = False
        self.timer = self.countdown

