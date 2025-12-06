# this file will manage interactions between predator and prey.

from .species import Species
import numpy as np

class Simulation:
    def __init__(self, prey, predator, interaction_rate, predation_success):
        self.prey = prey
        self.predator = predator
        self.interaction_rate = interaction_rate
        self.predation_success = predation_success
        self.time = [0]

    def step(self, t):
        # Predator-prey interactions
        interactions = min(len(self.prey.ages), len(self.predator.ages))
        events = np.random.rand(interactions) < self.interaction_rate
        prey_eaten = np.sum(events) * self.predation_success
        prey_eaten = int(min(prey_eaten, len(self.prey.ages)))

        # Remove eaten prey
        if prey_eaten > 0:
            self.prey.ages = self.prey.ages[:-prey_eaten]
        # Predator birth boost from feeding
        for _ in range(prey_eaten):
            if np.random.rand() < self.predator.birth_rate:
                self.predator.ages = np.concatenate((self.predator.ages, np.zeros(1, dtype=int)))
        
        # Apply internal birth/death dynamics
        self.prey.step()
        self.predator.step()
        self.time.append(t)