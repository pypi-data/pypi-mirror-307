import random

def mutate(individual, varbound):
    gene = random.randint(0, len(individual) - 1)
    individual[gene] = random.uniform(varbound[gene][0], varbound[gene][1])
