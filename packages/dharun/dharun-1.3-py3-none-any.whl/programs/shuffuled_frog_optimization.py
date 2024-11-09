shuffuled_frog_optimization = """
import numpy as np

def opt_func(x):
    return np.sqrt(np.sum(np.square(x)))

def gen_frogs(frogs, dim, sigma, mu):
    return np.random.normal(mu, sigma, (frogs, dim))

def sort_frog(frogs, mplx_no, opt_func):
    fitness = np.array([opt_func(frog) for frog in frogs])

    sorted_idx = np.argsort(fitness)

    memeplexes = np.array_split(sorted_idx, mplx_no)

    return np.array(memeplexes)

def local_search(frogs, memeplex, opt_func, sigma, mu):

    frog_g = frogs[0]

    best_frog = frogs[int(memeplex[0])]
    worst_frog = frogs[int(memeplex[-1])]

    new_worst_frog = worst_frog + (best_frog - worst_frog) * np.random.rand()

    if opt_func(new_worst_frog) > opt_func(worst_frog):

        new_worst_frog = worst_frog + (frog_g - worst_frog) * np.random.rand()

    if opt_func(new_worst_frog) > opt_func(worst_frog):

        new_worst_frog = gen_frogs(1, len(frog_g), sigma, mu)[0]

    frogs[int(memeplex[-1])] = new_worst_frog

    return frogs

def shuffled_leaping_frog(
    opt_func,
    frogs = 30,
    dim = 3,
    sigma = 1,
    mu = 0,
    mplx_no = 3,
    max_iter = 100,
    solution_iter = 1000
    ):

    frogs = gen_frogs(frogs, dim, sigma, mu)

    memeplexes = sort_frog(frogs, mplx_no, opt_func)

    best_solution = frogs[int(memeplexes[0, 0])]

    for i in range(solution_iter):

        if i % 10 == 0:
            print(f"Iteration {i}: best value: {opt_func(best_solution):.3f}", end=" ")
            print(f"Best position: {np.around(best_solution, 3)}")


        # Shuffle memeplexes
        np.random.shuffle(memeplexes)

        for memeplex_idx,  memeplex in enumerate(memeplexes):
            for j in range(max_iter):
                frogs = local_search(frogs, memeplex, opt_func, sigma, mu)

            memeplexes = sort_frog(frogs, mplx_no, opt_func)

            if opt_func(frogs[int(memeplexes[0, 0])]) < opt_func(best_solution):
                best_solution = frogs[int(memeplexes[0, 0])]


    return best_solution, opt_func(best_solution)

print("Starting shuffled leaping frog algorithm")

best_pos, best_val = shuffled_leaping_frog(
    opt_func,
    100,
    3,
    1,
    0,
    5,
    250,
    500
)

print("Completed shuffled leaping frog algorithm")

print(f"Best position: {np.around(best_pos, 3)}")
print(f"Best value: {best_val:.3f}")
"""