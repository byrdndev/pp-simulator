# this file will manage interactions between predator and prey.

from .species import Species
import numpy as np

class Simulation:
    def __init__(self, prey, predator, interaction_rate, predation_success):
        """
        Initialize the predator-prey simulation.
        
        Parameters:
        - prey: Species object for prey
        - predator: Species object for predators
        - interaction_rate: Probability of encounter per predator-prey pair
        - predation_success: Probability that an encounter results in successful predation
        """
        self.prey = prey
        self.predator = predator
        self.interaction_rate = interaction_rate
        self.predation_success = predation_success
        self.time = [0]
    
    def step(self, t):
        """
        Advance simulation by one timestep.
        
        Parameters:
        - t: Current timestep number
        """
        # FIRST: Handle predator-prey interactions BEFORE internal dynamics
        # Calculate predator-prey interactions
        # Number of potential encounters based on smaller population
        interactions = min(len(self.prey.ages), len(self.predator.ages))
        
        # Determine which encounters happen
        events = np.random.rand(interactions) < self.interaction_rate
        
        # Calculate successful predations
        prey_eaten = int(np.sum(events) * self.predation_success)
        prey_eaten = min(prey_eaten, len(self.prey.ages))
        
        # Remove eaten prey randomly (not just from the end)
        if prey_eaten > 0 and len(self.prey.ages) > 0:
            indices_to_remove = np.random.choice(len(self.prey.ages), size=prey_eaten, replace=False)
            self.prey.ages = np.delete(self.prey.ages, indices_to_remove)
        
        # Predators gain reproductive boost from feeding
        # Each successful kill gives a chance for predator birth
        for _ in range(prey_eaten):
            if np.random.rand() < self.predator.birth_rate:
                # Add a newborn predator (age 0)
                self.predator.ages = np.concatenate((self.predator.ages, np.zeros(1, dtype=int)))
        
        # SECOND: Apply internal birth/death dynamics for both species
        self.prey.step()
        self.predator.step()
        
        # Record timestep
        self.time.append(t)
    
    def get_populations(self):
        """Return current populations of prey and predators."""
        return len(self.prey.ages), len(self.predator.ages)