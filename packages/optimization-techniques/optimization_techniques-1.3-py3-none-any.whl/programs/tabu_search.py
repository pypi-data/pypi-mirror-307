tabu_search = """
import numpy as np

class TabuSearch:
    def __init__(self,fitness_function,initial_solution,tabu_list_size=10,max_iter=100):
        self.fitness_function = fitness_function
        self.initial_solution = initial_solution
        self.tabu_list = []
        self.tabu_list_size = tabu_list_size
        self.max_iter = max_iter
        self.current_solution = initial_solution
        self.best_solution = initial_solution
        self.best_solution_value = self.fitness_function(self.best_solution)

    def generate_neighbour(self,solution):
        return [solution+4,solution-4]

    def apply_tabu_restriction(self,neighbours,tabu_list):
        return [neighbour for neighbour in neighbours if neighbour not in tabu_list]

    def select_neighbour(self,neighbours):
        best_neighbour = None
        best_neighbour_value = float('inf')

        for neighbour in neighbours:
            neighbour_value = self.fitness_function(neighbour)
            if neighbour_value < best_neighbour_value:
                best_neighbour = neighbour
                best_neighbour_value = neighbour_value

        return best_neighbour,best_neighbour_value

    def update_tabu_list(self,tabu_list,move,tabu_list_size):
        tabu_list.append(move)
        if len(tabu_list) > tabu_list_size:
            tabu_list.pop(0)

    def run(self):
        for iter in range(self.max_iter):
            neighbours = self.generate_neighbour(self.current_solution)

            allowed_neighbours = self.apply_tabu_restriction(neighbours,self.tabu_list)

            best_neighbour,best_neighbour_value = self.select_neighbour(allowed_neighbours)

            if best_neighbour_value < self.best_solution_value:
                self.best_solution = best_neighbour
                self.best_solution_value = best_neighbour_value
                print(f"Iteration : {iter+1} New best solution found: x = {self.best_solution}, f(x) = {self.best_solution_value}")
            
            self.update_tabu_list(self.tabu_list,best_neighbour,self.tabu_list_size)

            self.current_solution = best_neighbour

            if best_neighbour_value == 0:
                break

        print(f"List : {self.tabu_list} New best solution found: x = {self.best_solution}, f(x) = {self.best_solution_value}")
        # return 

def objective_function(x):
    return x**2

initial_solution = np.random.randint(-100,100)
ts = TabuSearch(objective_function,initial_solution)
ts.run()

"""