from mesa import Model
from mesa.space import NetworkGrid
from mesa.datacollection import DataCollector

from agents import Rider, Station, Bike
from schedule import RandomActivationByBreed

import networkx as nx

class BikePath(Model):

    verbose = True  # Print-monitoring

    def __init__(self, height=50, width=50, num_bikes=10, num_riders=100):
        # Set parameters
        self.height = height
        self.width = width
        self.num_bikes = num_bikes
        self.num_riders = num_riders

        self.schedule = RandomActivationByBreed(self)
        self.G = nx.fast_gnp_random_graph(n=20, p=0.2)  # replace with osmnx
        self.grid = NetworkGrid(self.G)
        self.datacollector = DataCollector({
            "Rider": lambda m: m.schedule.get_breed_count(Rider),
            "Missed Rides": lambda m: m.missed_rides
        })

        self.stations = {}
        self.missed_rides = 0

        # Create stations
        self.createStations()

        # Create riders:
        self.createRiders()

        # Create bikes:
        self.createBikes()

        self.running = True
        self.datacollector.collect(self)

    def createStations(self):

        list_of_random_nodes = self.random.sample(self.G.nodes(), 10)

        for n in range(len(list_of_random_nodes)):

            s = Station(n, list_of_random_nodes[n], self, 5, 5)

            self.stations[list_of_random_nodes[n]] = s

            self.grid.place_agent(s, list_of_random_nodes[n])
            # self.schedule.add(s) # Why would stations need to be on the schedule?

    def createRiders(self):
        stations = list(self.stations.values())

        for i in range(self.num_riders):

            # start_station, destination, start_time, end_time, cur_bike

            s = self.random.choice(stations)
            p = s.pos

            d = self.random.choice(stations)

            start = self.random.randrange(24)
            end = self.random.randrange(24)

            r = Rider(i, p, self, s, d, start, end)
            self.grid.place_agent(r, p)
            self.schedule.add(r)

    def createBikes(self):
        for i in range(self.num_bikes):

            # pos, model, cur_station

            s = self.random.choice(list(self.stations.values()))
            p = s.pos

            # start = self.random.randrange(24)
            # end = self.random.randrange(24)

            b = Bike(i, p, self, s)

            s.bikes_here.append(b)

            self.grid.place_agent(b, p)
            self.schedule.add(b)

    def step(self):
        self.schedule.step()
        # collect data
        self.datacollector.collect(self)
        if self.verbose:
            print([self.schedule.time,
                   self.schedule.get_breed_count(Rider)])

    def run_model(self, step_count=200):

        if self.verbose:
            print('Initial number Riders: ',
                  self.schedule.get_breed_count(Rider))

        for i in range(step_count):
            self.step()

        if self.verbose:
            print('')
            print('Final number Riders: ',
                  self.schedule.get_breed_count(Rider))
