from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.modules import ChartModule
from NetworkVisualization.NetworkExtendedVisualization import NetworkExtendedModule

from agents import Rider, Station, Bike
from model import BikePath
from collections import defaultdict


def get_breed(a):
    if type(a) is Rider:
        return "Rider"
    elif type(a) is Station:
        return "Station"
    elif type(a) is Bike:
        return "Bike"
    else:
        return None

def get_tooltip(agents):
    count = defaultdict(int)

    for i in agents:
        count[get_breed(i)] += 1

    tooltip = ''

    for k in count.keys():
        tooltip += str(count[k]) + ' ' + k + ', '

    return tooltip[:-2]


def portrayal(G):
    portrayal = dict()

    portrayal['nodes'] = [{'id': node_id,
                           'size': 3 if agents else 1,
                           'color': '#CC0000' if not agents else '#007959',
                           'tooltip': None if not agents else get_tooltip(agents),  # fix this
                           'agents': [get_breed(a) for a in agents]
                           }
                          for (node_id, agents) in G.nodes.data('agent')]

    portrayal['edges'] = [{'id': edge_id,
                           'source': source,
                           'target': target,
                           'color': '#000000',
                           }
                          for edge_id, (source, target) in enumerate(G.edges)]

    # if agent is None:
    #     return

    # portrayal = {}

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


network_element = NetworkExtendedModule(portrayal, 500, 500)
chart_element = ChartModule([{"Label": "Rider", "Color": "#AA0000"}])

server = ModularServer(BikePath, [network_element, chart_element], "BikePath")
