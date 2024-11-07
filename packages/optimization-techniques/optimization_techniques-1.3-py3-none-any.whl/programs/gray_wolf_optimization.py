gray_wolf_optimization = """
import numpy as np

class GrayWolf:
    def __init__(self,fitness_function,num_wolves,a=2,dim=2,max_iter=100,lower_bound=-10,upper_bound=10):
        self.fitness_function = fitness_function
        self.num_wolves = num_wolves
        self.a = a
        self.dim = dim
        self.max_iter = max_iter
        self.lower_bound = lower_bound
        self.upper_bound = upper_bound
        self.wolves_position = self.initial_position()

    def initial_position(self):
        return self.lower_bound + (self.upper_bound - self.lower_bound) * np.random.rand(self.num_wolves,self.dim)
    
    def update_position(self,wolves_position,leader_pos,a,dim):
        r1, r2 = np.random.rand(dim),np.random.rand(dim)
        A, C = a*2*r1-a, 2*r2
        d_leader = abs(C*leader_pos - wolves_position)
        return (leader_pos - A * d_leader)
    
    def run(self):
        for t in range(self.max_iter):
            self.a = 2 - t * (2 / self.max_iter)

            fitness = np.apply_along_axis(self.fitness_function,1,self.wolves_position)
            index = np.argsort(fitness)
            alpha_pos = self.wolves_position[index[0]]
            beta_pos = self.wolves_position[index[1]]
            delta_pos = self.wolves_position[index[2]]

            for i in range(self.num_wolves):
                new_alpha_pos = self.update_position(self.wolves_position[i],alpha_pos,self.a,self.dim)
                new_beta_pos = self.update_position(self.wolves_position[i],beta_pos,self.a,self.dim)
                new_delta_pos = self.update_position(self.wolves_position[i],delta_pos,self.a,self.dim)

                self.wolves_position[i] = (new_alpha_pos + new_beta_pos + new_delta_pos) /3

            if t%10 == 0:
                print(f"Iteration:{t}: Best Fitness : {self.fitness_function(alpha_pos)}")

        return alpha_pos
    

def objective_function(x):
    return sum(x**2)

gwo = GrayWolf(objective_function,5)
alpha = gwo.run()
print(f"Best Solution : {alpha},Best Fitness : {objective_function(alpha)}")

"""