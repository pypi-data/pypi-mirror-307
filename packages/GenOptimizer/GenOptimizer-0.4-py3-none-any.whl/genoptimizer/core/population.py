import random
from ..operators.selection import roulette_selection
from ..operators.crossover import one_point_crossover
from ..operators.mutation import mutate
from ..operators.fitness import evaluate

class Individual:
    def __init__(self, genes, fitness=0):
        self.genes = genes
        self.fitness = fitness

def evaluate_genes(genes, function):
    return function(genes)

class Population:
    def __init__(self, dimension, varbound, params):
        self.dimension = dimension
        self.varbound = varbound
        self.params = params
        self.individuals = [self.create_individual() for _ in range(params['population_size'])]
        

    def create_individual(self):
        genes = [random.uniform(self.varbound[i][0], self.varbound[i][1]) for i in range(self.dimension)]
        return Individual(genes)

    def evaluate_population(self, function):
        # Utiliza evaluate_genes para calcular el fitness de cada individuo
        for ind in self.individuals:
            ind.fitness = evaluate(ind.genes, function)  # Usando la función evaluate de fitness.py
            
    def evolve(self):
        new_population = []
        while len(new_population) < len(self.individuals):
            parent1 = roulette_selection(self.individuals)
            parent2 = roulette_selection(self.individuals)
            child1_genes, child2_genes = one_point_crossover(parent1.genes, parent2.genes)
            mutate(child1_genes, self.varbound)
            mutate(child2_genes, self.varbound)
            new_population.append(Individual(child1_genes))
            new_population.append(Individual(child2_genes))
        self.individuals = new_population
