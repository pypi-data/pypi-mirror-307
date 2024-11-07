shortest_edge_initialization = """
import random

class GeneticOperations:
    @staticmethod
    def partially_matched_crossover(parent1, parent2):
        start, end = sorted(random.sample(range(len(parent1)), 2))
        child = [-1] * len(parent1)
        child[start:end] = parent1[start:end]

        for i in range(start, end):
            if parent2[i] not in child:
                swap_value = parent2[i]
                index = i
                while child[index] != -1:
                    index = parent2.index(parent1[index])
                child[index] = swap_value

        for i in range(len(parent1)):
            if child[i] == -1:
                child[i] = parent2[i]

        return child

    @staticmethod
    def order_crossover(parent1, parent2):
        start, end = sorted(random.sample(range(len(parent1)), 2))
        child = [-1] * len(parent1)
        child[start:end] = parent1[start:end]

        pointer = end
        for city in parent2:
            if city not in child:
                if pointer == len(parent1):
                    pointer = 0
                child[pointer] = city
                pointer += 1

        return child

    @staticmethod
    def mutation_inversion(path):
        start, end = sorted(random.sample(range(len(path)), 2))
        path[start:end] = path[start:end][::-1]
        return path

    @staticmethod
    def mutation_insertion(path):
        city_index = random.randint(0, len(path) - 1)
        city = path.pop(city_index)
        insert_position = random.randint(0, len(path) - 1)
        path.insert(insert_position, city)
        return path

cities = ['A', 'B', 'C', 'D', 'E']
distance_matrix = {
    'A': {'B': 10, 'C': 15, 'D': 20, 'E': 25},
    'B': {'A': 10, 'C': 35, 'D': 25, 'E': 30},
    'C': {'A': 15, 'B': 35, 'D': 30, 'E': 20},
    'D': {'A': 20, 'B': 25, 'C': 30, 'E': 15},
    'E': {'A': 25, 'B': 30, 'C': 20, 'D': 15},
}

class ShortestEdgeInitialization:
    def __init__(self, cities, population_size):
        self.cities = cities  
        self.population_size = population_size  

    def initialize_population(self):
        population = []
        for _ in range(self.population_size):
            path = self.cities[:]
            random.shuffle(path)  
            population.append(path)
        return population

    def partially_matched_crossover(self, parent1, parent2):
        return GeneticOperations.partially_matched_crossover(parent1, parent2)

    def order_crossover(self, parent1, parent2):
        return GeneticOperations.order_crossover(parent1, parent2)

    def mutation_inversion(self, path):
        return GeneticOperations.mutation_inversion(path)

    def mutation_insertion(self, path):
        return GeneticOperations.mutation_insertion(path)

shortest_edge_initializer = ShortestEdgeInitialization(cities, 5)
population1 = shortest_edge_initializer.initialize_population()

parent1, parent2 = population1[0], population1[1]
child_pmx = shortest_edge_initializer.partially_matched_crossover(parent1, parent2)
child_ox = shortest_edge_initializer.order_crossover(parent1, parent2)
mutated_path_inversion = shortest_edge_initializer.mutation_inversion(parent1[:])
mutated_path_insertion = shortest_edge_initializer.mutation_insertion(parent1[:])

print("Shortest Edge Initialization Population:", population1)
print("PMX Crossover Result:", child_pmx)
print("OX Crossover Result:", child_ox)
print("Inversion Mutation Result:", mutated_path_inversion)
print("Insertion Mutation Result:", mutated_path_insertion)

"""

nearest_neighbour_initialization = """
import random

class GeneticOperations:
    @staticmethod
    def partially_matched_crossover(parent1, parent2):
        start, end = sorted(random.sample(range(len(parent1)), 2))
        child = [-1] * len(parent1)
        child[start:end] = parent1[start:end]

        for i in range(start, end):
            if parent2[i] not in child:
                swap_value = parent2[i]
                index = i
                while child[index] != -1:
                    index = parent2.index(parent1[index])
                child[index] = swap_value

        for i in range(len(parent1)):
            if child[i] == -1:
                child[i] = parent2[i]

        return child

    @staticmethod
    def order_crossover(parent1, parent2):
        start, end = sorted(random.sample(range(len(parent1)), 2))
        child = [-1] * len(parent1)
        child[start:end] = parent1[start:end]

        pointer = end
        for city in parent2:
            if city not in child:
                if pointer == len(parent1):
                    pointer = 0
                child[pointer] = city
                pointer += 1

        return child

    @staticmethod
    def mutation_inversion(path):
        start, end = sorted(random.sample(range(len(path)), 2))
        path[start:end] = path[start:end][::-1]
        return path

    @staticmethod
    def mutation_insertion(path):
        city_index = random.randint(0, len(path) - 1)
        city = path.pop(city_index)
        insert_position = random.randint(0, len(path) - 1)
        path.insert(insert_position, city)
        return path

cities = ['A', 'B', 'C', 'D', 'E']
distance_matrix = {
    'A': {'B': 10, 'C': 15, 'D': 20, 'E': 25},
    'B': {'A': 10, 'C': 35, 'D': 25, 'E': 30},
    'C': {'A': 15, 'B': 35, 'D': 30, 'E': 20},
    'D': {'A': 20, 'B': 25, 'C': 30, 'E': 15},
    'E': {'A': 25, 'B': 30, 'C': 20, 'D': 15},
}

class NearestNeighborInitialization:
    def __init__(self, cities, distance_matrix, population_size):
        self.cities = cities  
        self.distance_matrix = distance_matrix 
        self.population_size = population_size 

    def find_nearest_neighbor(self, current_city, visited):
        min_distance = float('inf')
        nearest_city = None
        for city in self.cities:
            if city not in visited:
                distance = self.distance_matrix[current_city][city]
                if distance < min_distance:
                    min_distance = distance
                    nearest_city = city
        return nearest_city

    def initialize_population(self):
        population = []
        for _ in range(self.population_size):
            path = []
            visited = set()
            current_city = random.choice(self.cities)  
            while len(visited) < len(self.cities):
                path.append(current_city)
                visited.add(current_city)
                next_city = self.find_nearest_neighbor(current_city, visited)
                current_city = next_city
            population.append(path)
        return population

    def partially_matched_crossover(self, parent1, parent2):
        return GeneticOperations.partially_matched_crossover(parent1, parent2)

    def order_crossover(self, parent1, parent2):
        return GeneticOperations.order_crossover(parent1, parent2)

    def mutation_inversion(self, path):
        return GeneticOperations.mutation_inversion(path)

    def mutation_insertion(self, path):
        return GeneticOperations.mutation_insertion(path)

nearest_neighbor_initializer = NearestNeighborInitialization(cities, distance_matrix, 5)
population2 = nearest_neighbor_initializer.initialize_population()

parent1, parent2 = population2[0], population2[1]
child_pmx = nearest_neighbor_initializer.partially_matched_crossover(parent1, parent2)
child_ox = nearest_neighbor_initializer.order_crossover(parent1, parent2)
mutated_path_inversion = nearest_neighbor_initializer.mutation_inversion(parent1[:])
mutated_path_insertion = nearest_neighbor_initializer.mutation_insertion(parent1[:])

print("Nearest Neighbor Initialization Population:", population2)
print("PMX Crossover Result:", child_pmx)
print("OX Crossover Result:", child_ox)
print("Inversion Mutation Result:", mutated_path_inversion)
print("Insertion Mutation Result:", mutated_path_insertion)

"""