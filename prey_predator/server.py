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
model_params = {"initial_sheep":100,
        "initial_wolves":50,
        "sheep_reproduce":0.04,
        "wolf_reproduce":0.05,
        "wolf_gain_from_food":20,
        "grass":False,
        "grass_regrowth_time":30,
        "sheep_gain_from_food":4,
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
         #model_params,
         {"width":20,
          "height":20,
          "initial_sheep": UserSettableParameter("slider", "Sheep quantity", 10, 1, 20, 1),
          "initial_wolves": UserSettableParameter("slider", "Wolf quantity", 10, 1, 20, 1),
          "sheep_reproduce": UserSettableParameter("slider", "Sheep reproduce rate", 0.04, 0.01, 0.1, 0.01),
          "wolf_reproduce": UserSettableParameter("slider", "Wolf reproduce rate", 0.05, 0.01, 0.1, 0.01),
          "wolf_gain_from_food": UserSettableParameter("slider", "Wolf energy from food", 20, 1, 30, 1),
          "grass_regrowth_time": UserSettableParameter("slider", "Grass regrowth time", 30, 1, 50, 1),
          "sheep_gain_from_food": UserSettableParameter("slider", "Sheep energy from food", 4, 1, 30, 1)}
)
server.port = 8521
