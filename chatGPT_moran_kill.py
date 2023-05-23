import numpy as np
import random

time_to_vax = 0
total_pop = 0
times_run = 0
percentTotal = 0
#Written by ChatGPT and Ethan Child


# Define the game matrix and population size
while times_run < 10:
    Agreement = 1.0  # Agreement for cooperation
    Vaccine = 0.1 # Payoff for Getting Vaccine
    Pain = 0.05 # Pain of getting vax
    pop_size = 100
    percent_update = 0.1
    want_vax = 0.5
    full_vax = False

    # Define the initial population and ideal of each individual
    population = np.random.choice([0, 1], size=pop_size, p=[1 - want_vax, want_vax])
    # how to correlate conviction with 1 or 0?
    conviction = np.random.uniform(size=pop_size)

    pop_coop = 0

    # Define the mutation rate stemming from the news
    news_rate = 0.01

    # Define the number of generations to play before killing off a species
    # This is the number of generations before anti-vaxxers start dying
    num_generations_before_kill = 250

    # Define the species to kill off and the fraction of the population to kill
    species_to_kill = 0
    chance_of_death = 0.01

    # Define the total number of generations to play
    total_num_generations = 1000

    # Run the Moran process for the specified number of generations
    for i in range(total_num_generations + 1):
        pop_coop = 0
        q = 0
        while q < pop_size:
            if population[q] == 1:
                pop_coop+= 1
            q += 1
        # Check if it's time to kill off a species
        if i > 0 and i > num_generations_before_kill and i % 10 == 0:
            # Kill off a fraction of the specified species

            species_indices = np.where(population == species_to_kill)[0]
            num_to_kill = int(len(species_indices))
            killed = 0
            for l in species_indices:
                randfloat = np.random.random(size=None)
                if randfloat < chance_of_death:
                    population = np.delete(population, l - killed)
                    pop_size -= 1
                    killed += 1


        # Compute the fitness of each individual
        fitness = np.zeros(pop_size)
        for j in range(pop_size):
            fitness[j] = conviction[j] * ((Agreement + Vaccine - Pain) * population[j] * (population == 1).sum() + (Vaccine - Pain - chance_of_death) * population[j] * (population == 0).sum() +
                                          (Vaccine) * (population == 1).sum() * (population == 0).sum() + (Agreement - chance_of_death) * (population == 0).sum() * (population == 0).sum())
        # Normalize the fitness
        fitness /= fitness.sum()



        # update a good number of them
        for y in range(int(pop_size * percent_update)):
            # Choose the individual to reproduce and the individual to die
            reproducer = np.random.choice(pop_size, p=fitness)
            dead = np.random.choice(pop_size)
            # Update the population
            if np.random.random() < news_rate:
                # Mutate the reproducer
                population[dead] = 1 - population[reproducer]
            # Replace the dead individual with the reproducer
            population[dead] = population[reproducer]

        # Update the conviction of each individual
        for j in range(pop_size):
            if random.random() < news_rate:
                # Mutate the ideal of the j-th individual
                conviction[j] = np.random.uniform()
        # record vaccination percentage
        vax_percent = pop_coop / pop_size
        if (vax_percent == 1 and full_vax == False):
            full_vax = True
            print("Full vaccination achieved in generation " + str(i) + " at population level of " + str(pop_size))

            times_run += 1
            time_to_vax += i
            percentTotal += 1
            total_pop += pop_size
            break
        # Print the population and conviction every 10 generations
        #if i % 100 == 0:

        #print("number of pro-vaxxers in generation " + str(i) + ": " + str(pop_coop))
        #print("percent of population willing to vaccinate: " + str(vax_percent))
        #print("population size: " + str(pop_size))
        if i == 1000:
            print("Final vaccination level was " + str(vax_percent) + " with a population size of " + str(pop_size))
            percentTotal += vax_percent
            time_to_vax += i
            times_run += 1
            total_pop += pop_size

average_time = time_to_vax / times_run
average_percent = percentTotal / times_run
average_pop = total_pop / times_run
print("Average vaccination percentage was: " + str(average_percent) + " with an average population level of " + str(average_pop) + " players after an average of " + str(average_time) + " generations")
