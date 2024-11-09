particle_swarn_optimization  = """
import random
import sys
import numpy as np
from scipy.spatial import distance

target = np.random.uniform(-10, 10, 3)
print("Generated Target Position: ", target)

def fitness_sphere(position):
    return distance.euclidean(position, target)


class Particle:
    def __init__(self, fitness, dim, minx, maxx, seed):
        self.position = np.random.uniform(minx, maxx, dim)
        self.velocity = np.random.uniform(minx, maxx, dim)

        self.fitness = fitness(self.position)
        self.best_part_pos = np.copy(self.position)
        self.best_part_val = self.fitness

def pso(fitness, max_iter, n, dim, minx, maxx):

    w = 0.729
    c1 = 1.49445
    c2 = 1.49445

    swarm = [Particle(fitness, dim, minx, maxx, i) for i in range(n)]

    best_swarm_particle = max(
        swarm,
        key = lambda x: x.fitness
    )

    best_swarm_pos = best_swarm_particle.position
    best_swarm_val = best_swarm_particle.fitness

    for t in range(max_iter):

        if t % 10 == 0:
            print(f"Iteration {t}: best value: {best_swarm_val:.3f}", end=" ")
            print(f"Best position: {np.around(best_swarm_pos, 3)}")

        for p in swarm:
            p.velocity = w * p.velocity + \
                c1 * np.random.rand(dim) * (p.best_part_pos - p.position) + \
                c2 * np.random.rand(dim) * (best_swarm_pos - p.position)

            p.velocity = np.clip(p.velocity, minx, maxx)
            p.position = p.position + p.velocity

            p.fitness = fitness(p.position)

            if p.fitness < p.best_part_val:
                p.best_part_pos = np.copy(p.position)
                p.best_part_val = p.fitness

            if p.fitness < best_swarm_val:
                best_swarm_pos = p.position
                best_swarm_val = p.fitness
    return best_swarm_pos, best_swarm_val

dim = target.shape[0]
num_particles = 50
max_iter = 100

print("Starting PSO")
best_pos, best_val = pso(fitness_sphere, max_iter, num_particles, dim, -10., 10.)

print("Completed PSO")
print(f"Best position: {np.around(best_pos, 3)}")
print(f"Best value: {best_val:.3f}")
"""