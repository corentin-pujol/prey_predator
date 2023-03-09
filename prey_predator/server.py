from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.modules import CanvasGrid, ChartModule
from mesa.visualization.UserParam import UserSettableParameter

from prey_predator.agents import Wolf, Sheep, GrassPatch
from prey_predator.model import WolfSheep


def wolf_sheep_portrayal(agent):
    if agent is None:
        return

    portrayal = {}

    if type(agent) is Sheep:
        portrayal["Shape"] = "circle"
        portrayal["Filled"] = "true"
        portrayal["r"] = .5
        portrayal["Color"] = "#666666"
        portrayal["Layer"] = 1

    elif type(agent) is Wolf:
        portrayal["Shape"] = "circle"
        portrayal["Filled"] = "true"
        portrayal["r"] = .3
        portrayal["Color"] = "#AA0000"
        portrayal["Layer"] = 2
        if agent.model.show_energy:
            portrayal["text"] = agent.energy
            portrayal["text_color"] = "white"

    elif type(agent) is GrassPatch:
        portrayal["Shape"] = "rect"
        portrayal["w"] = 1
        portrayal["h"] = 1
        portrayal["Filled"] = "true"
        if agent.is_grown:
            portrayal["Color"] = "green"
        else:
            portrayal["Color"] = "brown"
        portrayal["Layer"] = 0

    return portrayal

#sliders
model_params = {
        "width":20,
        "height":20,
        "grass": UserSettableParameter('checkbox', 'Grass activated', value=True),
        "show_energy": UserSettableParameter('checkbox', 'Show wolves energy', value=False),
        "initial_sheep": UserSettableParameter("slider", "Sheep quantity", 10, 1, 100, 1),
        "initial_wolves": UserSettableParameter("slider", "Wolf quantity", 10, 1, 100, 1),
        "sheep_reproduce": UserSettableParameter("slider", "Sheep reproduce rate", 0.04, 0.01, 0.1, 0.01),
        "wolf_reproduce": UserSettableParameter("slider", "Wolf reproduce rate", 0.05, 0.01, 0.1, 0.01),
        "wolf_gain_from_food": UserSettableParameter("slider", "Wolf energy from food", 20, 1, 30, 1),
        "sheep_gain_from_food": UserSettableParameter("slider", "Sheep energy from food", 4, 1, 30, 1),
        "grass_regrowth_time": UserSettableParameter("slider", "Grass regrowth time", 30, 1, 50, 1),
        "sheep_initial_energy": UserSettableParameter("slider", "Sheep maximal initial energy", 40, 25, 75, 1),
        "wolf_initial_energy": UserSettableParameter("slider", "Wolves maximal initial energy", 40, 25, 75, 1),
}


canvas_element = CanvasGrid(wolf_sheep_portrayal, 20, 20, 500, 500)
chart = [{"Label": "Wolves", "Color": "#AA0000"}, {"Label": "Sheep", "Color": "#666666"}]
if model_params["grass"]:
    chart.append({"Label": "Grass", "Color": "green"})
chart_element = ChartModule(chart)



server = ModularServer(
            WolfSheep, 
            [canvas_element, chart_element], 
            "Prey Predator Model", 
            model_params,
)
server.port = 8521