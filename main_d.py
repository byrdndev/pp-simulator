from models.species import Species
from models.simulation import Simulation
import matplotlib.pyplot as plt

print("Starting simulation...")

# Initialize prey population
prey = Species(
    name="Prey",
    birth_rate=0.3,
    death_rate=0.05,
    latency_period=3,
    initial_population=100
)
print(f"Prey initialized: {len(prey.ages)} individuals")

# Initialize predator population
predator = Species(
    name="Predator",
    birth_rate=0.1,
    death_rate=0.1,
    latency_period=5,
    initial_population=20
)
print(f"Predator initialized: {len(predator.ages)} individuals")

# Create simulation
sim = Simulation(
    prey=prey,
    predator=predator,
    interaction_rate=0.02,
    predation_success=0.8
)
print("Simulation object created")

# Run simulation for fewer timesteps to test
timesteps = 50
print(f"\nRunning simulation for {timesteps} timesteps...")

for t in range(1, timesteps + 1):
    sim.step(t)
    
    # Print every 10 steps
    if t % 10 == 0:
        prey_pop = len(prey.ages)
        pred_pop = len(predator.ages)
        print(f"Step {t}: Prey = {prey_pop}, Predators = {pred_pop}")
        
        # Check for extinction
        if prey_pop == 0:
            print("WARNING: All prey died!")
            break
        if pred_pop == 0:
            print("WARNING: All predators died!")

print("\nSimulation complete!")
print(f"Final Prey: {len(prey.ages)}")
print(f"Final Predators: {len(predator.ages)}")

# Check if we have data to plot
print(f"\nData collected:")
print(f"Time points: {len(sim.time)}")
print(f"Prey population history length: {len(prey.population)}")
print(f"Predator population history length: {len(predator.population)}")

# Plot results
print("\nCreating plot...")
plt.figure(figsize=(10, 6))
plt.plot(sim.time, prey.population, label='Prey', color='blue', linewidth=2)
plt.plot(sim.time, predator.population, label='Predator', color='red', linewidth=2)
plt.xlabel('Time', fontsize=12)
plt.ylabel('Population', fontsize=12)
plt.legend(fontsize=12)
plt.title('Predator–Prey Simulation with Reproductive Latency', fontsize=14)
plt.grid(True, alpha=0.3)
plt.tight_layout()
print("Displaying plot...")
plt.show()
print("Done!")