from mesa import Agent
import networkx as nx
from datetime import datetime


class Rider(Agent):
    def __init__(self, unique_id, node, model, start_station, destination, start_time, end_time, speed=20, bike=None, birthyear=0, gender=0):
        super().__init__(unique_id, model)
        self.node = node
        self.start_station = start_station
        self.destination = destination
        self.wait_count = 0
        self.speed = speed  # set speed here based on duration?
        self.birthyear = birthyear
        self.gender = gender

        try:
            self.path = nx.shortest_path(model.G, start_station.node, destination.node)
            # print(start_station.node, destination.node, self.path)
        except nx.exception.NetworkXNoPath:
            self.path = []
            print("No path")

        self.start_time = datetime(start_time)
        self.end_time = datetime(end_time)
        self.bike = bike

    def move(self):

        # Keep track of speed based on start/end

        if len(self.path) < 1:
            return

        self.model.grid.move_agent(self, self.path[0])
        self.model.grid.move_agent(self.bike, self.path[0])

        self.path = self.path[1:]

    def step(self):

        # if there's a bike here, grab the bike and move to the next station

        # if at a station
        # TODO: I can easily ALSO model dockless bikes by just removing the at a station check

        # print(self, self.pos, self.destination.pos, self.bike)

        if self.bike:

            # keep track of *speed*

            if self.pos == self.destination.pos:

                self.destination.bikes_here.append(self.bike)
                self.bike.has_rider = False
                self.bike.rider = None

                self.model.grid._remove_agent(self, self.pos)
                self.model.schedule.remove(self)

            else:
                self.move()

        elif self.pos == self.start_station.pos:
            s = self.model.stations[self.pos]
            if s.bikes_here:
                b = s.bikes_here.pop()
                b.rider = self
                b.has_rider = True
                b.destination = self.destination
                self.bike = b
                self.wait_count = 0
            else:
                if self.wait_count >= 10:
                    self.model.missed_rides += 1
                    self.model.grid._remove_agent(self, self.pos)
                    self.model.schedule.remove(self)

                else:
                    self.wait_count += 1


class Bike(Agent):
    def __init__(self, unique_id, node, model, cur_station, destination=None, dockless=False):
        super().__init__(unique_id, model)
        self.node = node
        self.cur_station = cur_station
        self.destination = destination
        self.has_rider = False
        self.rider = None
        self.dockless = dockless

    def rebalance(self):
        pass
        # Rebalance by going to another station

    def step(self):
        self.rebalance()


class Station(Agent):
    def __init__(self, unique_id, node, model, capacity, num_bikes):
        super().__init__(unique_id, model)
        self.node = node
        self.capacity = capacity
        self.num_bikes = num_bikes
        self.outage = False
        self.bikes_here = []

    def step(self):
        pass
