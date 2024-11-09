from .core.population import Population
from .config.default_parameters import DEFAULT_PARAMS

class GenOptimizer:
    def __init__(self, function, dimension, varbound, params=None):
        self.function = function
        self.dimension = dimension
        self.varbound = varbound
        self.params = params or DEFAULT_PARAMS
        self.population = Population(self.dimension, self.varbound, self.params)

    def run(self):
        for generation in range(self.params['max_num_iteration']):
            self.population.evaluate_population(self.function)
            self.population.evolve()
