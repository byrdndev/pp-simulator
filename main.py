from models.species import Species
from models.simulation import Simulation
import matplotlib.pyplot as plt

# Initialize populations
prey = Species("Prey", birth_rate=0.3, death_rate=0.05, latency_period=3,
initial_population=100)
predator = Species("Predator", birth_rate=0.1, death_rate=0.1, latency_period=5,
initial_population=20)

# Create simulation
sim = Simulation(prey, predator, interaction_rate=0.02, predation_success=0.8)

# Run for N steps
timesteps = 200
for t in range(timesteps):
    sim.step(t)

# Plot results
plt.plot(sim.time, prey.population, label='Prey')
plt.plot(sim.time, predator.population, label='Predator')
plt.xlabel('Time')
plt.ylabel('Population')
plt.legend()
plt.title('Predator–Prey Simulation with Reproductive Latency')
plt.show()