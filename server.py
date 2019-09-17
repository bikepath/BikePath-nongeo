from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.modules import NetworkModule, ChartModule
from FoliumVisualization.FoliumModule import FoliumModule

from agents import Rider, Station, Bike
from model import BikePath


def portrayal(G):
    # if agent is None:
    #     return

    portrayal = {}

    portrayal = dict()

    print("apple")

    portrayal['nodes'] = [{'id': node_id,
                           'size': 3 if agents else 1,
                           'color': '#CC0000' if not agents or agents[0].wealth == 0 else '#007959',
                           'label': "node",
                           }
                          for (node_id, agents) in G.nodes.data('agent')]

    print("piano")

    portrayal['edges'] = [{'id': edge_id,
                           'source': source,
                           'target': target,
                           'color': '#000000',
                           }
                          for edge_id, (source, target, _) in enumerate(G.edges)]

    print("banana")

    # if type(agent) is Rider:
    #     portrayal["Shape"] = "resources/person.svg"
    #     portrayal["Color"] = "red"
    #     portrayal["scale"] = 0.9
    #     portrayal["Layer"] = 1

    # if type(agent) is Bike:
    #     portrayal["Shape"] = "resources/bike.svg"
    #     portrayal["Color"] = "green"
    #     portrayal["scale"] = 0.95
    #     portrayal["Layer"] = 0

    # elif type(agent) is Station:
    #     if agent.outage:
    #         portrayal["Color"] = "gray"
    #     else:
    #         portrayal["Color"] = "blue"

    #     portrayal["Shape"] = "rect"
    #     portrayal["Filled"] = "true"
    #     portrayal["Layer"] = 2
    #     portrayal["w"] = 1
    #     portrayal["h"] = 1

    return portrayal


# network_element = NetworkModule(portrayal, 500, 500, library='sigma')
folium_element = FoliumModule()

chart_element = ChartModule([{"Label": "Rider", "Color": "#AA0000"}])

server = ModularServer(BikePath, [folium_element, chart_element], "BikePath")
