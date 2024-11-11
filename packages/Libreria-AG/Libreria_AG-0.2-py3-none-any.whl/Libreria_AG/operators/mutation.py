import random

#def mutate(individual, varbound):
 #   gene = random.randint(0, len(individual) - 1)
  #  individual[gene] = random.uniform(varbound[gene][0], varbound[gene][1])

def mutate(individual, varbound):
    gene = random.randint(0, len(individual) - 1)
    new_value = random.uniform(varbound[gene][0], varbound[gene][1])
    individual[gene] = new_value  # Esto es más explícito
