from mesa import Model
from mesa.space import NetworkGrid
from mesa.datacollection import DataCollector

from agents import Rider, Station, Bike
from schedule import TimedActivation

import csv
import json
import osmnx as ox
import networkx as nx


class BikePath(Model):

    verbose = False  # Print-monitoring

    def __init__(self, height=50, width=50, num_bikes=10, num_riders=100, place='Boston, Massachusetts, USA'):
        # Set parameters
        self.height = height
        self.width = width
        self.num_bikes = num_bikes
        self.num_riders = num_riders
        self.place = place

        self.schedule = TimedActivation(self)

        if 'Quincy' in place:
            self.G = ox.graph_from_file('data/quincy.osm')
        elif 'Boston' in place:
            self.G = ox.graph_from_file('data/boston.osm')
        else:
            self.G = ox.graph_from_place(place, network_type='bike')

        # self.G = self.G.to_directed()

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

        if 'Boston' in self.place:
            stations = []

            with open('data/station_information.json') as json_file:
                data = json.load(json_file)['data']['stations']
                for s in data:
                    node, dist = ox.utils.get_nearest_node(self.G, (s['lat'], s['lon']), return_dist=True)
                    if dist < 500:
                        station = Station(int(s['station_id']), node, self, s['capacity'], 0)
                        self.grid.place_agent(station, node)
                        self.stations[node] = station

        else:
            stations = self.random.sample(self.G.nodes(), 100)
            for n in range(len(stations)):

                s = Station(n, stations[n], self, 5, 5)

                self.stations[stations[n]] = s

                self.grid.place_agent(s, stations[n])

    def createRiders(self):
        # tripduration,starttime,stoptime,start station id,start station name,start station latitude,start station longitude,end station id,end station name,end station latitude,end station longitude,bikeid,usertype,birth year,gender

        stations = list(self.stations.values())

        if 'Boston' in self.place:

            i = 0

            with open('data/201909-bluebikes-tripdata-SMALL.csv') as csvfile:

                spamreader = csv.reader(csvfile)

                next(spamreader)

                for row in csvfile:

                    row = row.strip().split(',')

                    start = next((x for x in stations if x.unique_id == int(row[3])), None)
                    end = next((x for x in stations if x.unique_id == int(row[7])), None)

                    if start is None or end is None:
                        print("Station not found", i)
                        continue

                    starttime = row[1]
                    endtime = row[2]

                    try:
                        speed = float(nx.shortest_path_length(self.G, source=start.node, target=end.node, weight='cost')) / float(row[0])
                    except nx.exception.NetworkXNoPath as _:
                        print("Station not in scope")
                        speed = 5

                    r = Rider(i, start.node, self, start, end, starttime, endtime, speed=speed, birthyear=int(row[13]), gender=int(row[14]))
                    self.grid.place_agent(r, start.node)
                    self.schedule.add(r)

                    i += 1

        else:
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
            s.num_bikes += 1

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
