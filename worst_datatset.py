import statistics as s
import greedy_solver as g
import wizard_parse as p
from random import shuffle


def randomize_test(k, wizards, constraints):
    v = []
    for _ in range(k):
        shuffle(wizards)
        v += [g.greedy_find(wizards, constraints)[1]]
    return s.mean(v)


def find_worst(path):
    files = p.get_files(path)
    worst_sample = files[0]
    most_errors = 0
    for file in files:
        v = p.parse(file)
        result = randomize_test(5, v[0], v[1])
        if result > most_errors:
            most_errors = result
            worst_sample = file
        print(worst_sample, most_errors)
    return worst_sample, most_errors
