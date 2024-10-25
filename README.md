# Moran_Game_Kill
This is a Moran Game that Kills A Few Member of the Population After Certain Generations. This was a project to simulate evolutionary game theory, and how populations interact with each other. 

Some of the code was written by ChatGPT, but modified by me. Here's the code ChatGPT wrote: 

import numpy as np
import random

# Define the game matrix and population size
R = 1.0  # Reward for cooperation
S = 0.0  # Sucker's payoff
T = 1.5  # Temptation to defect
P = 0.5  # Punishment for defecting
pop_size = 100

# Define the initial population and ideal of each individual
pop = np.random.choice([0, 1], size=pop_size)
ideals = np.random.uniform(size=pop_size)

# Define the mutation rate
mu = 0.01

# Define the number of generations to play before killing off a species
num_generations_before_kill = 50

# Define the species to kill off and the fraction of the population to kill
species_to_kill = 0
fraction_to_kill = 0.5

# Define the total number of generations to play
total_num_generations = 100

# Run the Moran process for the specified number of generations
for i in range(total_num_generations):
    # Check if it's time to kill off a species
    if i > 0 and i % num_generations_before_kill == 0:
        # Kill off a fraction of the specified species
        species_indices = np.where(pop == species_to_kill)[0]
        num_to_kill = int(len(species_indices) * fraction_to_kill)
        pop[np.random.choice(species_indices, size=num_to_kill, replace=False)] = 1 - species_to_kill

    # Compute the fitness of each individual
    fitness = np.zeros(pop_size)
    for j in range(pop_size):
        fitness[j] = ideals[j] * (R * pop[j] * (pop == 1).sum() + S * pop[j] * (pop == 0).sum() +
                                  T * (pop == 1).sum() * (pop == 0).sum() + P * (pop == 0).sum() * (pop == 0).sum())
    # Normalize the fitness
    fitness /= fitness.sum()

    # Choose the individual to reproduce and the individual to die
    reproducer = np.random.choice(pop_size, p=fitness)
    dead = np.random.choice(pop_size)

    # Update the population
    if random.random() < mu:
        # Mutate the reproducer
        pop[dead] = 1 - pop[reproducer]
    else:
        # Replace the dead individual with the reproducer
        pop[dead] = pop[reproducer]

    # Update the ideals of each individual
    for j in range(pop_size):
        if random.random() < mu:
            # Mutate the ideal of the j-th individual
            ideals[j] = np.random.uniform()

    # Print the population and ideals every 10 generations
    if i % 10 == 0:
        print("Generation {}: {}".format(i, pop))
        print("Generation {}: {}".format(i, ideals))
