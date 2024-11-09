gray_wolf_optimization = """
import random
import numpy as np

from scipy.spatial import distance


target = np.random.uniform(-100, 100, 3)
print("Generated Target Position: ", target)

def fitness_sphere(position):
    return distance.euclidean(position, target)

class Wolf:
    def __init__(self, fitness, dim, minx, maxx, seed=0):

        np.random.seed(seed)
        self.position = np.random.uniform(minx, maxx, dim)

        self.fitness = fitness(self.position)

def gwo(fitness, max_iter, n, dim, minx, maxx):

    population = [
        Wolf(fitness, dim, minx, maxx, i) for i in range(n)
    ]

    population = sorted(population, key=lambda x: x.fitness)

    alpha, beta, gamma = population[:3].copy()

    for t in range(max_iter):

        wolf_pos = np.array([wolf.position for wolf in population[:3]])

        if t % 10 == 0:
            print(f"Iteration {t}: best value: {alpha.fitness:.3f}", end=" ")
            print(f"Best position: {np.around(alpha.position, 3)}")

        a = 2 * (1 - t / max_iter)

        for i, wolf in enumerate(population):
            A = a * np.random.uniform(-1, 1, (3, 1))

            C = 2 * np.random.uniform(0, 1, (3, 1))

            X = wolf_pos - A * np.abs(C * wolf_pos - wolf.position)

            Xnew = X.mean(axis=0)

            if fitness(Xnew) < wolf.fitness:
                wolf.position = Xnew
                wolf.fitness = fitness(Xnew)

        population = sorted(population, key=lambda x: x.fitness)
        alpha, beta, gamma = population[:3].copy()

    return alpha.position, alpha.fitness


dim = target.shape[0]
n = 100
max_iter = 100

print("Starting GWO")

best_pos, best_val = gwo(fitness_sphere, max_iter, n, dim, -100., 100.)

print("Completed GWO")

print(f"Best position: {np.around(best_pos, 3)}")

print(f"Best value: {best_val:.3f}")
"""