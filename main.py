from models.species import Species
from models.simulation import Simulation
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend for environments without display
import matplotlib.pyplot as plt
import os
import numpy as np

# Create plots directory if it doesn't exist
os.makedirs('plots', exist_ok=True)

# Initialize prey population with LOWER birth rate
prey = Species(
    name="Prey",
    birth_rate=0.3,      # Reduced from 0.3
    death_rate=0.05,
    latency_period=3,
    initial_population=100
)

# Extra prey species
prey2 = Species(
    name="Prey2",
    birth_rate=0.2,
    death_rate=0.04,
    latency_period=4,
    initial_population=60
)

# Initialize predator population
predator = Species(
    name="Predator",
    birth_rate=0.1,      # Slightly reduced from 0.1
    death_rate=0.1,      # Reduced from 0.1
    latency_period=5,
    initial_population=20
)

# Create simulation with HIGHER interaction rate
sim = Simulation(
    prey=[prey, prey2],
    predator=predator,
    interaction_rate=0.02,      # Increased from 0.02
    predation_success=0.8        # Slightly reduced from 0.8
)

# Run simulation for specified timesteps
timesteps = 200
print(f"Running simulation for {timesteps} timesteps...")

for t in range(1, timesteps + 1):
    sim.step(t)
    
    # Print progress every 50 steps
    if t % 50 == 0:
        prey_pop, pred_pop = sim.get_populations()
        print(f"Step {t}: Prey = {prey_pop}, Predators = {pred_pop}")
    
    # Safety check for extinction
    if len(prey.ages) == 0 or len(predator.ages) == 0:
        print(f"\nSimulation ended at step {t} due to extinction")
        if len(prey.ages) == 0:
            print("All prey died out!")
        if len(predator.ages) == 0:
            print("All predators died out!")
        break

print("Simulation complete!")

# Plot results
plt.figure(figsize=(12, 6))
plt.plot(sim.time, prey.population, label='Prey', color='blue', linewidth=2)
plt.plot(sim.time, prey2.population, label='Prey2', color='green', linewidth=2)
plt.plot(sim.time, predator.population, label='Predator', color='red', linewidth=2)
plt.xlabel('Time', fontsize=12)
plt.ylabel('Population', fontsize=12)
plt.legend(fontsize=12)
plt.title('Predator–Prey Simulation with Reproductive Latency', fontsize=14)
plt.grid(True, alpha=0.3)
plt.tight_layout()

# Save plot to file
output_file = 'plots/predator_prey_simulation.png'
plt.savefig(output_file, dpi=150, bbox_inches='tight')
print(f"\nPlot saved to: {output_file}")

# Stochastic Visualization Plot

plt.figure(figsize=(14, 7))

# get extinction timestep
predator_extinct_step = None
for i, pop in enumerate(predator.population):
    if pop == 0:
        predator_extinct_step = sim.time[i]
        break

# jitter clouds
prey_j = np.array(prey.population) + np.random.normal(0, 0.015*np.max(prey.population), len(prey.population))
prey2_j = np.array(prey2.population) + np.random.normal(0, 0.015*np.max(prey2.population), len(prey2.population))
pred_j = np.array(predator.population) + np.random.normal(0, 0.1*np.max(predator.population + [1]), len(predator.population))

# smooth lines
plt.plot(sim.time, prey.population, linewidth=2.5, color="#4A90E2", alpha=0.5)
plt.plot(sim.time, prey2.population, linewidth=2.5, color="#7ED321", alpha=0.5)
plt.plot(sim.time, predator.population, linewidth=2.5, color="#D0021B", alpha=0.6)

# variance shading (prettiest part)
plt.fill_between(sim.time,
                 np.array(prey.population)*0.9,
                 np.array(prey.population)*1.1,
                 color="#4A90E2", alpha=0.10)

plt.fill_between(sim.time,
                 np.array(prey2.population)*0.9,
                 np.array(prey2.population)*1.1,
                 color="#7ED321", alpha=0.10)

plt.fill_between(sim.time,
                 np.array(predator.population)*0.85,
                 np.array(predator.population)*1.15,
                 color="#D0021B", alpha=0.15)

# scatter jitter dots
plt.scatter(sim.time, prey_j, s=10, color="#4A90E2", alpha=0.3, label="Prey (stochastic)")
plt.scatter(sim.time, prey2_j, s=10, color="#7ED321", alpha=0.3, label="Prey2 (stochastic)")
plt.scatter(sim.time, pred_j, s=25, color="#D0021B", alpha=0.4, label="Predator (stochastic)")

# extinction marker
if predator_extinct_step is not None:
    plt.axvline(predator_extinct_step, color="black", linestyle="--", alpha=0.6)
    plt.text(predator_extinct_step + 1, max(prey.population)*0.05,
             "Predator Extinction", fontsize=12, color="black")

# formatting
plt.title("Stochastic Predator–Prey Graph", fontsize=18)
plt.xlabel("Time")
plt.ylabel("Population")
plt.legend()
plt.grid(alpha=0.3, linestyle="--")
plt.tight_layout()

# save file
pretty_2 = "plots/Stochastic_Visualization.png"
plt.savefig(pretty_2, dpi=150, bbox_inches="tight")
print(f"Stochastic Plot")


# Print final statistics
print(f"\nFinal Results:")
print(f"Prey: {prey.population[-1]} (started with {prey.population[0]})")
print(f"Predators: {predator.population[-1]} (started with {predator.population[0]})")

# Calculate some statistics
max_prey = max(prey.population)
max_predator = max(predator.population)
print(f"\nPeak Populations:")
print(f"Prey peak: {max_prey}")
print(f"Predator peak: {max_predator}")