continuous_optimization = """
from numpy.random import randint
from numpy.random import rand


def objective(x):
    return x[0] ** 2.0 + x[1] ** 2.0


def decode(bounds, n_bits, bitstring):
    decoded = list()

    largest = 2 ** n_bits

    for i in range(len(bounds)):
        start, end = i * n_bits, i * n_bits + n_bits 

        substring = bitstring[start: end]

        chars = "".join([str(s) for s in substring])


        integer = int(chars, 2)

        value = bounds[i][0] + (integer / largest) * bounds[i][1] -bounds[i][0]

        decoded.append(value)

    return decoded

def selection(pop, scores, k=3):
    selection_ix = randint(len(pop))

    for ix in randint(0, len(pop), k-1):
        if scores[ix] < scores[selection_ix]:
            selection_ix = ix

    return pop[selection_ix]


def crossover(p1, p2, r_cross):

    c1, c2 = p1.copy(), p2.copy()

    if rand() < r_cross:
        pt = randint(1, len(p1) - 2)

        c1 = p1[:pt] + p2[pt:]
        c2 = p2[:pt] + p1[pt:]

    return [c1, c2]

def mutation(bitstring, r_mut):
    for i in range(len(bitstring)):
        if rand() < r_mut:
            bitstring[i] = 1 - bitstring[i]


def genetic_algorithm(
        objective, bounds, n_bits, n_iter,
        n_pop, r_cross, r_mut):
    pop = [
            randint(0, 2, n_bits*len(bounds)).tolist()
            for _ in range(n_pop)
        ]
    best, best_eval = 0, objective(decode(bounds, n_bits, pop[0]))
    for gen in range(n_iter):
        decoded = [
            decode(bounds, n_bits, p)
            for p in pop
        ]
        scores = [objective(d) for d in decoded]

        for i in range(n_pop):
            if scores[i] < best_eval:

                best, best_eval = pop[i], scores[i]

                print("> iteration %d, new best f(%s) = %f" % (gen, decoded[i], scores[i]))

        selected = [selection(pop, scores) for _ in range(n_pop)]
        children = list()

        for i in range(0, n_pop, 2):
            p1, p2 = selected[i], selected[i+1]
            for c in crossover(p1, p2, r_cross):
                mutation(c, r_mut)      
                children.append(c)

        pop = children

    return [best, best_eval]
bounds = [[-5.0, 5.0], [-5.0, 5.0]]
n_iter = 1000
n_bits = 160
n_pop = 100
r_cross = 0.9
r_mut = 1.0 / (float(n_bits) * len(bounds))


print("Starting genetic algorithm")
best, score = genetic_algorithm(objective, bounds, n_bits, n_iter, n_pop, r_cross, r_mut)
decoded = decode(bounds, n_bits, best)
print("Genetic algorithm complete")
print(f"Best Solution: {decoded}")
print(f"Fitness Score of the best solution: {score:.2f}")
"""