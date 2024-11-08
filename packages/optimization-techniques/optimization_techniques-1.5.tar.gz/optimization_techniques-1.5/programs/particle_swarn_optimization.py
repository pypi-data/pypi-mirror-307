particle_swarn_optimization = """
import numpy as np

class PSO:
    def __init__(self,fitness_function,bounds,n_particle,max_iter,w=0.5,c1=1.0,c2=1.5):
        self.fitness_function = fitness_function
        self.bounds = bounds
        self.n_particle = n_particle
        self.max_iter = max_iter
        self.w = w 
        self.c1 = c1
        self.c2 = c2
        self.particles = []
        self.gbest_postion = None
        self.gbest_value = float('inf')

    class Particle:
        def __init__(self,bounds):
            self.position = np.random.uniform(bounds[:,0],bounds[:,1],len(bounds))
            self.velocity = np.random.uniform(-1,1,len(bounds))
            self.pbest_position = self.position.copy()
            self.pbest_value = float('inf')

        def update_velocity(self,gbest_position,w,c1,c2):
            r1 = np.random.rand(len(self.position))
            r2 = np.random.rand(len(self.position))
            cognitive_velocity = c1 * r1 * (self.pbest_position - self.position)
            social_velocity = c2 * r2 * (gbest_position - self.position)
            self.velocity = w * self.velocity + cognitive_velocity + social_velocity

        def update_position(self,bounds):
            self.position += self.velocity
            self.position = np.clip(self.position,bounds[:,0],bounds[:,1])
    
    def run(self):
        self.particles = [self.Particle(self.bounds) for _ in range(self.n_particle)]
        self.gbest_postion = np.random.uniform(self.bounds[:,0],self.bounds[:,1],len(self.bounds))
        self.gbest_value = float('inf')

        for iteration in range(self.max_iter):
            for particle in self.particles:
                fitness = self.fitness_function(particle.position)

                if fitness < particle.pbest_value:
                    particle.pbest_position = particle.position.copy()
                    particle.pbest_value = fitness
                
                if fitness < self.gbest_value:
                    self.gbest_postion = particle.position.copy()
                    self.gbest_value = fitness

            print(f"Iteration {iteration+1} Best Fitness : {self.gbest_value} Best Position :{self.gbest_postion}")

            for particle in self.particles:
                particle.update_velocity(self.gbest_postion,self.w,self.c1,self.c2)
                particle.update_position(self.bounds)

        return self.gbest_postion,self.gbest_value
    
def objective_function(x):
    return sum(x**2)

bounds = np.array([[-5.12,5.12]] * 3)
pso = PSO(fitness_function=objective_function,bounds=bounds,n_particle=50,max_iter=100)
best_position, best_value = pso.run()
print(f"Best Position : {best_position}")
print(f"Best value : {best_value}")

"""