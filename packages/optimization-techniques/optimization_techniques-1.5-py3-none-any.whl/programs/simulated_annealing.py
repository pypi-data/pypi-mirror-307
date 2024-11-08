simulated_annealing = """
import numpy as np

class SimulatedAnnealing:
    def __init__(self,fitness_function,initial_solution,current_temp=100,min_temp=0,max_iter=1000,alpha=0.9) -> None:
        self.fitness_function = fitness_function
        self.current_solution = np.array(initial_solution)
        self.current_fitness = self.fitness_function(self.current_solution)
        self.current_temp = current_temp
        self.min_temp = min_temp
        self.max_iter = max_iter
        self.alpha = alpha
        self.best_solution = self.current_solution
        self.best_fitness = self.fitness_function(self.best_solution)

    def neighbour(self,solution):
        return solution + np.random.uniform(-1,1,size=solution.shape)
    
    def acceptance_probability(self,current_fitness,new_fitness):
        if new_fitness < current_fitness:
            return 1.0
        else:
            return np.exp((current_fitness - new_fitness) / self.current_temp)
        
    def run(self):
        for iter in range(self.max_iter):
            new_solution = self.neighbour(self.current_solution)
            new_fitness = self.fitness_function(new_solution)
            if np.random.rand() < self.acceptance_probability(self.current_fitness,new_fitness):
                self.current_solution = new_solution
                self.current_fitness = new_fitness

            if self.current_fitness < self.best_fitness:
                self.best_solution = self.current_solution
                self.best_fitness = self.current_fitness

            print(f"Iteration:{iter+1} -> Best Fitness:{self.best_fitness}")

            self.current_temp *= self.alpha

            if self.current_temp <= self.min_temp:
                break

        print(self.current_temp)
        return self.best_solution,self.best_fitness

def objective_function(x):
    return np.sum(x**2)

initial_solution = np.array([5,5])

sa = SimulatedAnnealing(fitness_function=objective_function,initial_solution=initial_solution)
best_solution,best_fitness = sa.run()
print(f"Best Solution:{best_solution}, Best Fitness:{best_fitness}")

"""