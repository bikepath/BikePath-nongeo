from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.modules import ChartModule
from mesa.visualization.UserParam import UserSettableParameter

from LeafletVisualization.LeafletModule import LeafletModule

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
                           'size': 3 if data['agent'] else 1,
                           'tooltip': get_tooltip(data['agent']),  # fix this
                           'agents': [get_breed(a) for a in data['agent']],
                           'lat': data['y'],
                           'long': data['x']
                           }
                          for (node_id, data) in G.nodes(data=True) if len(data['agent']) > 0]

    # print("port", len(portrayal['nodes']))

    return portrayal


leaflet_element = LeafletModule(portrayal, view=[42.36, -71.05])

chart_element = ChartModule([{"Label": "Rider", "Color": "#AA0000"}])
chart_element_rides = ChartModule([{"Label": "Missed Rides", "Color": "#AA0000"}])

model_params = {
    "place": "Boston, MA",
    "num_bikes": UserSettableParameter("slider", "Number of Bikes", 500, 100, 2000, 1),
    "num_riders": UserSettableParameter("slider", "Number of Riders", 500, 100, 2000, 1),
    "place_name": UserSettableParameter("static_text", value="Boston, MA"),
}

server = ModularServer(BikePath, [leaflet_element, chart_element, chart_element_rides], "BikePath", model_params)
