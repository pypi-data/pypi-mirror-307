binary_optimization = """
import numpy as np

class GeneticAlgorithmBO:
    def __init__(self, fitness_function,num_bits,pop_size=50, generation = 50, crossover_rate=0.8,mutation_rate=0.1) -> None:
        self.fitness_function = fitness_function
        self.num_bits = num_bits
        self.pop_size = pop_size
        self.generation = generation
        self.crossover_rate = crossover_rate
        self.mutation_rate = mutation_rate
        self.population = self.initialize_population()

    def initialize_population(self):
        return np.random.randint(2,size=(self.pop_size,self.num_bits))
    
    def find_fitness(self,population):
        return np.array([self.fitness_function(individual) for individual in population])
    
    def selection(self,fitness):
        probability = fitness / fitness.sum()
        return np.random.choice(self.pop_size,2,replace=False,p=probability)
    
    def crossover(self,parent1,parent2):
        if np.random.rand() < self.crossover_rate:
            crossover_point = np.random.randint(1,self.num_bits)
            offspring_1 = np.concatenate((parent1[:crossover_point],parent2[crossover_point:]))
            offspring_2 = np.concatenate((parent2[:crossover_point],parent1[crossover_point:]))
            return offspring_1,offspring_2
        return parent1,parent2
    
    def mutation(self,individual):
        for i in range(self.num_bits):
            if np.random.rand() < self.mutation_rate:
                individual[i] = 1 - individual[i]
        return individual
    
    def run(self):
        for generation in range(self.generation):
            fitness = self.find_fitness(self.population)
            new_population = []

            print(f"Generation:{generation + 1} -> Best Fitness : {np.max(fitness)}")

            while len(new_population) < self.pop_size:
                parent1_idx, parent2_idx = self.selection(fitness)
                parent1, parent2 = self.population[parent1_idx], self.population[parent2_idx]
                offspring_1, offspring_2 = self.crossover(parent1,parent2)
                offspring_1, offspring_2 = self.mutation(offspring_1), self.mutation(offspring_2)
                new_population.extend([offspring_1,offspring_2])
        
            self.population = np.array(new_population[:self.pop_size])
        
        final_fitness = self.find_fitness(self.population)
        best_idx = np.argmax(final_fitness)
        best_solution = self.population[best_idx]
        best_fitness = final_fitness[best_idx]
        return best_solution, best_fitness
        
def objective_function(x):
    return sum(x)

ga = GeneticAlgorithmBO(fitness_function=objective_function,num_bits=20)
print(ga.run())
"""

continuous_optimization = """
import numpy as np

class GeneticAlgorithmCO:
    def __init__(self,fitness_function,bounds,pop_size,generation=50,crossover_rate = 0.8,mutation_rate = 0.1) -> None:
        self.fitness_function = fitness_function
        self.bounds = bounds
        self.dimensions = len(self.bounds)
        self.pop_size = pop_size
        self.generation = generation
        self.crossover_rate = crossover_rate
        self.mutation_rate = mutation_rate
        self.population = self.initialize_population()

    def initialize_population(self):
        return np.array(
            [[ np.random.uniform(high,low) for high, low in self.bounds]   
               for _ in range(self.pop_size)
            ]
        )
    
    def find_fitness(self, population):
        return np.array([self.fitness_function(individual) for individual in population])
    
    def selection(self,fitness):
        indices = np.random.choice(self.pop_size,4,replace=False)
        selected = np.argsort(fitness[indices])[:2]
        return indices[selected[0]],indices[selected[1]]

    def crossover(self,parent1,parent2):
        if np.random.rand() < self.crossover_rate:
            alpha = np.random.rand(self.dimensions)
            offspring_1 = alpha * parent1 + (1-alpha) * parent2
            offspring_2 = alpha * parent2 + (1-alpha) * parent1
            return offspring_1,offspring_2
        return parent1,parent2
    
    def mutation(self,individual):
        for i in range(self.dimensions):
            if np.random.rand() < self.mutation_rate:
                mutation_value = np.random.normal(0,1)
                individual[i] += mutation_value
                individual[i] = np.clip(individual[i],self.bounds[i][0],self.bounds[i][1])
        return individual
        

    def run(self):
        for generation in range(self.generation):
            fitness = self.find_fitness(self.population)
            new_population = []

            print(f"Iteration{generation+1} -> Best Fitness : {np.min(fitness)}")

            while len(new_population) < self.pop_size:
                parent1_idx, parent2_idx = self.selection(fitness)
                parent1, parent2 = self.population[parent1_idx], self.population[parent2_idx]

                offspring1, offspring2 = self.crossover(parent1,parent2)
                offspring1, offspring2 = self.mutation(offspring1),self.mutation(offspring2)
                new_population.extend([offspring1,offspring2])

            self.population = np.array(new_population[:self.pop_size])
        
        final_fitness = self.find_fitness(self.population)
        best_idx = np.argmin(final_fitness)
        best_solution = self.population[best_idx]
        best_fitness = final_fitness[best_idx]
        return best_solution,best_fitness
    
def objective_function(x):
    return sum(x**2)

bounds = [(-10,10)] * 5

ga = GeneticAlgorithmCO(fitness_function=objective_function,bounds=bounds,pop_size=50)
best_solution,best_fitness = ga.run()
print(f"Best Solution: {best_solution}, Best Fitness: {best_fitness}")

"""