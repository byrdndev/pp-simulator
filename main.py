from models.species import Species
from models.simulation import Simulation
import matplotlib.pyplot as plt
import os
import csv

# Create plots and data directories if they don't exist
os.makedirs('plots', exist_ok=True)
os.makedirs('data', exist_ok=True)

# Initialize prey populations
prey = Species(
    name="Prey",
    birth_rate=0.3,      
    death_rate=0.05,
    latency_period=3,
    initial_population=100
)



# ----------------------------------------------------
# Not So Optional Extensions - Add multiple prey variants
# ----------------------------------------------------

# Second prey species
prey2 = Species(
    name="Prey2",
    birth_rate=0.2,
    death_rate=0.04,
    latency_period=4,
    initial_population=60
)

# Third prey species
prey3 = Species(
    name="Prey3",
    birth_rate=0.25,
    death_rate=0.06,
    latency_period=3,
    initial_population=80
)
# ----------------------------------------------------



# Initialize predator population
predator = Species(
    name="Predator",
    birth_rate=0.1,      
    death_rate=0.1,      
    latency_period=5,
    initial_population=20
)

# Create simulation
sim = Simulation(
    prey=[prey, prey2, prey3],
    predator=predator,
    interaction_rate=0.02,      
    predation_success=0.8        
)

# Run simulation for specified timesteps
timesteps = 200
print(f"Running simulation for {timesteps} timesteps...")

for t in range(1, timesteps + 1):
    sim.step(t)
    
    # IMPORTANT: Without the extinction safety check, prey populations can grow uncontrollably, producing massive arrays that exhaust system memory and cause the simulation to crash.
    # So we are highly dependent upon the predotors to go extinct for the safety of the program.
    # Really it's just the first prey species given to us that causes this problem.
    # I think... the most steps I've gotten is 95 before predator goes extinct

    # Safety check for extinction
    all_prey_extinct = all(len(p.ages) == 0 for p in [prey, prey2, prey3])
    if all_prey_extinct or len(predator.ages) == 0:
        print(f"\nSimulation ended at step {t} due to extinction")
        if all_prey_extinct:
            print("All prey species died out!")
        if len(predator.ages) == 0:
            print("All predators died out!")
        break

print("Simulation complete!")

# ----------------------------------------------------
# Not So Optional Extensions - Export results to CSV in /data/
# ----------------------------------------------------

csv_filename = "data/simulation_results.csv"
print(f"\nExporting results to {csv_filename}...")

# Determine the actual length of the simulation, avoid index errors with early extinction
actual_length = len(sim.time)

# Write data to CSV
with open(csv_filename, 'w', newline='') as csvfile:
    fieldnames = ['Time', 'Prey1_Population', 'Prey2_Population', 'Prey3_Population', 
                  'Predator_Population', 'Total_Prey_Population']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    
    writer.writeheader()

    # Write data for each step
    for i in range(actual_length):
        writer.writerow({
            'Time': sim.time[i],
            'Prey1_Population': prey.population[i],
            'Prey2_Population': prey2.population[i],
            'Prey3_Population': prey3.population[i],
            'Predator_Population': predator.population[i],
            'Total_Prey_Population': prey.population[i] + prey2.population[i] + prey3.population[i]
        })

print("Complete...")
# ----------------------------------------------------



# Plot results (default plot type given by instructions)
plt.figure(figsize=(12, 6))
plt.plot(sim.time, prey.population, label='Prey1', color='blue', linewidth=2)
plt.plot(sim.time, prey2.population, label='Prey2', color='green', linewidth=2)
plt.plot(sim.time, prey3.population, label='Prey3', color='cyan', linewidth=2)
plt.plot(sim.time, predator.population, label='Predator', color='red', linewidth=2)
plt.xlabel('Time', fontsize=12)
plt.ylabel('Population', fontsize=12)
plt.legend(fontsize=12)
plt.title('Predator–Prey Simulation with Reproductive Latency', fontsize=14)
plt.grid(True, alpha=0.3)
plt.tight_layout()

plt.savefig("plots/default_plot.png", dpi=150)
print(f"\nDefault plot created and saved to 'plots/default_plot.png'...")



# ----------------------------------------------------
# Include a stochastic visualization (20 pts) (using seaborn or bokeh or matplotlib)
# ----------------------------------------------------

# Calculate data length, helps avoid errors with early extinction
actual_length = min(len(prey.population), len(prey2.population), len(prey3.population), len(predator.population))

# Sum of prey populations
total_prey = [prey.population[i] + prey2.population[i] + prey3.population[i] 
              for i in range(actual_length)]

plt.figure(figsize=(8,6))
plt.scatter(total_prey, predator.population[:actual_length], s=18, alpha=0.5, color="purple")
plt.xlabel("Total Prey Population")
plt.ylabel("Predator Population")
plt.title("Phase-Space Predator vs Prey (Stochastic)")
plt.grid(alpha=0.3)
plt.tight_layout()

plt.savefig("plots/stochastic_plot.png", dpi=150)
print(f"Stochastic plot created and saved to 'plots/stochastic_plot.png'...")
# ----------------------------------------------------
