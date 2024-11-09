tabu_search = """
import pandas as pd
import numpy as np
from itertools import combinations

class TS:
    def __init__(self, path, seed, tabu_tenure):
        self.path = path
        self.seed = seed
        self.tabu_tenure = tabu_tenure

        self.instance_dict = self.input_data()
        self.initial_solution = self.get_initial_solution()

        self.tabu_str, self.best_solution, self.best_obj_val = self.tabu_search()

    def input_data(self):
        return pd.read_csv(self.path, names=[
            "job", "weight", "processing_time","due_date"
        ], index_col=0).to_dict("index")

    def get_tabu_structure(self):
        return {
            swap: {
                "tabu_time": 0,
                "move_val": 0
            }

            for swap in combinations(self.instance_dict.keys(), 2)
        }

    def get_initial_solution(self):
        arr = np.array(list(self.instance_dict.keys()))
        np.random.shuffle(arr)
        return arr

    def obj_func(self, solution):
        dict = self.instance_dict
        t = 0

        obj_val = 0

        for job in solution:
            c_i = t + dict[job]["processing_time"]
            d_i = dict[job]["due_date"]
            t_i = max(0, c_i - d_i)
            w_i = dict[job]["weight"]

            obj_val += w_i * t_i
            t = c_i
        return obj_val

    def swap_move(self, solution, i, j):
        new_solution = np.copy(solution)
        i = np.where(new_solution == i)[0][0]
        j = np.where(new_solution == j)[0][0]
        new_solution[[i, j]] = new_solution[[j, i]]
        return new_solution

    def tabu_search(self):
        tenure = self.tabu_tenure

        tabu_str = self.get_tabu_structure()
        best_solution = np.copy(self.initial_solution)
        best_obj_val = self.obj_func(best_solution)

        current_solution = np.copy(self.initial_solution)
        current_obj_val = best_obj_val

        iter = 1
        terminate = 0
        while terminate  < 100:

            if iter < 10:
                print(f"Iteration {iter}: best value: {best_obj_val:.3f}")

            for move in tabu_str:
                candidate_solution = self.swap_move(current_solution, *move)
                candidate_obj_val = self.obj_func(candidate_solution)

                tabu_str[move]["move_val"]  = candidate_obj_val

            while True:
                best_move = min(
                    tabu_str,
                    key = lambda x: tabu_str[x]["move_val"]
                )

                move_val = tabu_str[best_move]["move_val"]
                tabu_time = tabu_str[best_move]["tabu_time"]

                if tabu_time < iter:

                    current_solution = self.swap_move(current_solution, *best_move)
                    current_obj_val = self.obj_func(current_solution)

                    if move_val < best_obj_val:
                        best_solution = np.copy(current_solution)
                        best_obj_val = move_val
                        terminate = 0
                    else :
                        terminate += 1

                    tabu_str[best_move]["tabu_time"] = iter + tenure
                    iter += 1
                    break
                else:
                    if move_val < best_obj_val:
                        current_solution = self.swap_move(current_solution, *best_move)
                        current_obj_val = self.obj_func(current_solution)
                        terminate = 0
                        iter += 1
                        break
                    else:
                        tabu_str[best_move]["move_val"] = np.inf
                        continue

        print("Tabu search terminated")
        print("Performed Iterations:", iter, "Best Solution:", best_solution, "Best Value: ", best_obj_val, sep="\n")
        return tabu_str, best_solution, best_obj_val

print("Tabu search started")

ts = TS("tabu_jobs.csv", 42, 5)
"""