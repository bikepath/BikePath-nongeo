import math

from mesa import Agent


class Rider(Agent):
    def __init__(self, unique_id, node, model, start_station, destination, start_time, end_time, bike=None):
        super().__init__(unique_id, model)
        self.node = node
        self.start_station = start_station
        self.destination = destination
        # self.path = self.calc_path()
        self.start_time = start_time
        self.end_time = end_time
        self.bike = bike

    def move(self):

        self.model.grid.move_agent(self, self.path[0])
        self.model.grid.move_agent(self.bike, self.path[0])

        self.path = self.path[1:]

    def calc_path(self):

        def chebyshev(pos_1, pos_2):

            D = 1
            D2 = 1
            dx = abs(pos_1[0] - pos_2[0])
            dy = abs(pos_1[1] - pos_2[1])

            return D * (dx + dy) + (D2 - 2 * D) * min(dx, dy)

        def get_distance(pos_1, pos_2):
            """ Get the distance between two point

            Args:
                pos_1, pos_2: Coordinate tuples for both points.

            """
            x1, y1 = pos_1
            x2, y2 = pos_2
            dx = x1 - x2
            dy = y1 - y2
            return math.sqrt(dx ** 2 + dy ** 2)

        def reconstruct_path(cameFrom, current):

            total_path = [current]
            while current in cameFrom.keys():
                current = cameFrom[current]
                total_path.append(current)

            total_path.reverse()

            return total_path

        def get_neighbors(pos):

            neighbors = []

            if pos[0] - 1 >= 0:
                neighbors.append((pos[0]-1, pos[1]))

            if pos[0] + 1 < self.model.grid.width:
                neighbors.append((pos[0]+1, pos[1]))

            if pos[1] - 1 >= 0:
                neighbors.append((pos[0], pos[1]-1))

            if pos[1] + 1 < self.model.grid.height:
                neighbors.append((pos[0], pos[1]+1))

            if pos[1] - 1 >= 0 and pos[0] - 1 >= 0:
                neighbors.append((pos[0]-1, pos[1]-1))

            if pos[1] + 1 < self.model.grid.height and pos[0] - 1 >= 0:
                neighbors.append((pos[0]-1, pos[1]+1))

            if pos[0] + 1 < self.model.grid.width and pos[1] - 1 >= 0:
                neighbors.append((pos[0]+1, pos[1]-1))

            if pos[0] + 1 < self.model.grid.width and pos[1] + 1 < self.model.grid.height:
                neighbors.append((pos[0]+1, pos[1] + 1))

            return neighbors

        def A_Star(start, goal): #best for grid, Dijkstra better for network

            closedSet = set()
            openSet = set([start])

            cameFrom = dict()

            gScore = dict()
            fScore = dict()

            gScore[start] = 0
            fScore[start] = get_distance(start, goal)

            while len(openSet) > 0:

                curr = None
                curr_f = None

                for pos in openSet:
                    if curr is None or fScore[start] < curr_f:
                        curr_f = fScore[start]
                        curr = pos

                if curr ==  goal:
                    return reconstruct_path(cameFrom, curr)

                openSet.remove(curr)
                closedSet.add(curr)

                for neighbor in get_neighbors(curr):
                    if neighbor in closedSet:
                        continue

                    candG = gScore[curr] + 1 #(1 is for the cost of moving to a neighbor which for now is just 1)

                    if neighbor not in openSet:
                        openSet.add(neighbor)

                    elif candG > gScore[neighbor]:
                        continue

                    cameFrom[neighbor] = curr
                    gScore[neighbor] = candG
                    H = chebyshev(neighbor, goal)
                    fScore[neighbor] = gScore[neighbor] + H

            return []

        return A_Star(self.start_station.pos, self.destination.pos)

    def step(self):

        # if there's a bike here, grab the bike and move to the next station

        # if at a station
        # TODO: I can easily ALSO model dockless bikes by just removing the at a station check

        print(self, self.pos, self.destination.pos, self.bike)

        if self.bike:

            # TODO: Also keep track of start/stop times

            if self.pos == self.destination.pos:

                self.destination.bikes_here.append(self.bike)
                self.bike.has_rider = False
                self.bike.rider = None

                self.model.grid._remove_agent(self.pos, self)
                self.model.schedule.remove(self)

            else:
                self.move()

        elif self.pos == self.start_station.pos:
            s = self.model.stations[self.pos]
            if s.bikes_here:
                b = s.bikes_here.pop(0)
                b.rider = self
                b.has_rider = True
                b.destination = self.destination
                self.bike = b
                self.wait_count = 0
            
            else:
                if self.wait_count >= 10:
                    self.model.grid._remove_agent(self.pos, self)
                    self.model.schedule.remove(self)
                    self.model.missed_rides += 1

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

    def move(self):

        if self.rider:
            pass  # the rider will move the bike
            # self.model.grid.move_agent(self, self.rider.path[0])

    def step(self):
        self.move()


class Station(Agent):
    def __init__(self, unique_id, node, model, capacity, num_bikes):
        super().__init__(unique_id, model)
        self.capacity = capacity
        self.num_bikes = num_bikes
        self.id = id
        self.outage = False
        self.bikes_here = []

    def step(self):
        pass
