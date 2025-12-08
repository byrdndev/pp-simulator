class Simulation:
    def __init__(self, prey, predator, interaction_rate, predation_success):
        """
        Initialize the predator-prey simulation.
        """
        # allow lists of prey species
        if isinstance(prey, list):
            self.prey_list = prey
        else:
            self.prey_list = [prey]

        self.predator = predator
        self.interaction_rate = interaction_rate
        self.predation_success = predation_success
        self.time = [0]
