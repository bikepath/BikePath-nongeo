from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.modules import CanvasGrid, ChartModule

from agents import Rider, Station, Bike
from model import BikePath

def portrayal(agent):
    if agent is None:
        return

    portrayal = {}

    if type(agent) is Rider:
        portrayal["Shape"] = "resources/person.svg"
        portrayal["Color"] = "red"
        portrayal["scale"] = 0.9
        portrayal["Layer"] = 1

    if type(agent) is Bike:
        portrayal["Shape"] = "resources/bike.svg"
        portrayal["Color"] = "green"
        portrayal["scale"] = 0.95
        portrayal["Layer"] = 0

    elif type(agent) is Station:
        if agent.outage:
            portrayal["Color"] = "gray"
        else:
            portrayal["Color"] = "blue"

        portrayal["Shape"] = "rect"
        portrayal["Filled"] = "true"
        portrayal["Layer"] = 2
        portrayal["w"] = 1
        portrayal["h"] = 1

    return portrayal


canvas_element = CanvasGrid(portrayal, 50, 50, 500, 500)
chart_element = ChartModule([{"Label": "Rider", "Color": "#AA0000"}])

server = ModularServer(BikePath, [canvas_element, chart_element], "BikePath")
