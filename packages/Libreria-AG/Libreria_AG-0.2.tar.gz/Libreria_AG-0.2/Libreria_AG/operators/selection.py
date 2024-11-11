import random

def roulette_selection(population):
    total_fitness = sum(ind.fitness for ind in population)
    pick = random.uniform(0, total_fitness)
    current = 0
    for individual in population:
        current += individual.fitness
        if current > pick:
            return individual
