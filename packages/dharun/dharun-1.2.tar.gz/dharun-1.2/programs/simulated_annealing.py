simulated_annealing = """
from numpy import asarray, exp
from numpy.random import randn, rand, seed
import numpy as np

def objective(x):
    return x[0]**2.0

def simulate_annealing(
        objective,
        bounds,
        n_iterations,
        step_size,
        temp
        ):

    best = np.random.uniform(bounds[:, 0], bounds[:, 1])

    best_eval = objective(best)

    curr, curr_eval = best, best_eval


    for i in range(n_iterations):
        candidate = curr + rand(len(bounds)) * step_size

        candidate_eval = objective(candidate)

        if candidate_eval < best_eval:
            best, best_eval = candidate, candidate_eval
            print("> Iteration %d: f(%s) = %.5f" % (i, best, best_eval))

        diff = candidate_eval - curr_eval
        t = temp / float(i + 1)
        metropolis = exp(-diff/ t)
        if diff < 0 or rand() < metropolis:
            curr, curr_eval = candidate, candidate_eval


    return [best, best_eval]

seed(1)
bounds = asarray([[-5.0, 5.0]])
n_iterations = 1000

step_size = 0.1
temp = 10

print("Started Simulated Annealing Algorithm")
best, score = simulate_annealing(

        objective,
        bounds,
        n_iterations,
        step_size,
        temp
    )
print("\n Simulated Annealing Completed \n")
print(f"")
"""