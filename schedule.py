from collections import defaultdict
from datetime import datetime, timedelta
from mesa.time import BaseScheduler, RandomActivation
from agents import Rider, Bike


class TimedActivation(BaseScheduler):

    def __init__(self,
                 model,
                 start_time,
                 end_time,
                 timestep=timedelta(minutes=5)):
        super().__init__(model)
        self.start_time = datetime.strptime(start_time)
        self.end_time = datetime.strptime(end_time)
        self.timestep = timestep

    def step(self):
        # Schedule for bikes - redistribution
        # Schedule for riders - moving them around
        for agent in self._agents:
            if type(agent) == Bike:
                pass  # redistribution

            elif type(agent) == Rider:
                # the only thing this should do is trigger bikes if they should start I think
                if agent.start_time >= self.start_time:  # only trigger if time has passed
                    agent.step()

class RandomActivationByBreed(RandomActivation):
    '''
    A scheduler which activates each type of agent once per step, in random
    order, with the order reshuffled every step.

    This is equivalent to the NetLogo 'ask breed...' and is generally the
    default behavior for an ABM.

    Assumes that all agents have a step() method.
    '''

    def __init__(self, model):
        super().__init__(model)
        self.agents_by_breed = defaultdict(dict)

    def add(self, agent):
        '''
        Add an Agent object to the schedule

        Args:
            agent: An Agent to be added to the schedule.
        '''

        self._agents[agent.unique_id] = agent
        agent_class = type(agent)
        self.agents_by_breed[agent_class][agent.unique_id] = agent

    def remove(self, agent):
        '''
        Remove all instances of a given agent from the schedule.
        '''

        del self._agents[agent.unique_id]

        agent_class = type(agent)
        del self.agents_by_breed[agent_class][agent.unique_id]

    def step(self, by_breed=True):
        '''
        Executes the step of each agent breed, one at a time, in random order.

        Args:
            by_breed: If True, run all agents of a single breed before running
                      the next one.
        '''
        if by_breed:
            for agent_class in self.agents_by_breed:
                self.step_breed(agent_class)
            self.steps += 1
            self.time += 1
        else:
            super().step()

    def step_breed(self, breed):
        '''
        Shuffle order and run all agents of a given breed.

        Args:
            breed: Class object of the breed to run.
        '''
        agent_keys = list(self.agents_by_breed[breed].keys())
        self.model.random.shuffle(agent_keys)
        for agent_key in agent_keys:
            self.agents_by_breed[breed][agent_key].step()

    def get_breed_count(self, breed_class):
        '''
        Returns the current number of agents of certain breed in the queue.
        '''
        return len(self.agents_by_breed[breed_class].values())
