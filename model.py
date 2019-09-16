from mesa import Model
from mesa.space import MultiGrid
from mesa.datacollection import DataCollector

from agents import Rider, Station, Bike
from schedule import RandomActivationByBreed


class BikePath(Model):

    verbose = True  # Print-monitoring

    def __init__(self, height=50, width=50, num_bikes=100, num_riders=10):
        # Set parameters
        self.height = height
        self.width = width
        self.num_bikes = num_bikes
        self.num_riders = num_riders

        self.schedule = RandomActivationByBreed(self)
        self.grid = MultiGrid(self.height, self.width, torus=False) #should this be a network grid or a continuousspace?
        self.datacollector = DataCollector({"Rider": lambda m: m.schedule.get_breed_count(Rider), })

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
        for i in range(10):

            x = self.random.randrange(self.width)
            y = self.random.randrange(self.height)

            while not self.grid.is_cell_empty((x, y)):

                x = self.random.randrange(self.width)
                y = self.random.randrange(self.height)

            s = Station((x, y), self, 5, 5, i)

            self.stations[(x,y)] = s

            self.grid.place_agent(s, (x, y))
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

            r = Rider(p, self, s, d, start, end)
            self.grid.place_agent(r, p)
            self.schedule.add(r)

    def createBikes(self):
        for i in range(self.num_bikes):

            # pos, model, cur_station

            s = self.random.choice(list(self.stations.values()))
            p = s.pos

            start = self.random.randrange(24)
            end = self.random.randrange(24)

            b = Bike(p, self, s)

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
