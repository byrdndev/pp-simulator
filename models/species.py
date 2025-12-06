# Each species will have:
# - population count
# - birth/death rates
# - latency period
# - reproductive age tracker
# Given example:

import numpy as np

class Species:
    def __init__(self, name, birth_rate, death_rate, latency_period, initial_population):
        self.name = name
        self.birth_rate = birth_rate
        self.death_rate = death_rate
        self.latency_period = latency_period
        self.population = [initial_population] # list to track over time
        self.ages = np.random.randint(0, latency_period + 1, size=initial_population)

    def step(self, interactions=0):
        # Age all individuals
        self.ages += 1

        # Apply deaths
        deaths = np.random.rand(len(self.ages)) < self.death_rate
        self.ages = self.ages[~deaths]

        # Apply births only for mature individuals
        mature = self.ages >= self.latency_period
        births = np.sum(np.random.rand(np.sum(mature)) < self.birth_rate)
        new_ages = np.zeros(births, dtype=int) # newborns start at age 0
        self.ages = np.concatenate((self.ages, new_ages))

        self.population.append(len(self.ages))