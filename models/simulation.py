import numpy as np

class Simulation:
    def __init__(self, prey, predator, interaction_rate, predation_success):
        # allow either a single prey species or a list
        if isinstance(prey, list):
            self.prey_list = prey
        else:
            self.prey_list = [prey]

        self.predator = predator
        self.interaction_rate = interaction_rate
        self.predation_success = predation_success
        self.time = [0]

    def step(self, t):

        total_prey_eaten = 0

        # predator-prey interaction for all prey species
        for prey in self.prey_list:
            interactions = min(len(prey.ages), len(self.predator.ages))

            if interactions > 0:
                events = np.random.rand(interactions) < self.interaction_rate
                eaten = int(np.sum(events) * self.predation_success)
                eaten = min(eaten, len(prey.ages))

                if eaten > 0:
                    indices = np.random.choice(len(prey.ages), size=eaten, replace=False)
                    prey.ages = np.delete(prey.ages, indices)

                total_prey_eaten += eaten

        # predator reproduction
        for _ in range(total_prey_eaten):
            if np.random.rand() < self.predator.birth_rate:
                self.predator.ages = np.concatenate(
                    (self.predator.ages, np.zeros(1, dtype=int))
                )

        # internal dynamics (birth/death)
        for prey in self.prey_list:
            prey.step()

        self.predator.step()

        # time record
        self.time.append(t)

    def get_populations(self):
        total_prey = sum(len(prey.ages) for prey in self.prey_list)
        return total_prey, len(self.predator.ages)
