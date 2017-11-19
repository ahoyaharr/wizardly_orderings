import wizard_parse
import greedy_solver
from random import shuffle

dirs = ['inputs20', 'inputs35', 'inputs50']

for dir in dirs:
    for file in wizard_parse.get_files(dir):
        w, c = wizard_parse.parse_partial(dir, file)

        number_to_wizard = {i: w[i] for i in range(len(w))}
        wizard_to_number = {w[i]: i for i in range(len(w))}

        w_m = [wizard_to_number[wizard] for wizard in w]
        c_m = [[wizard_to_number[constraint.split()[0]],
                wizard_to_number[constraint.split()[1]],
                wizard_to_number[constraint.split()[2]]]
               for constraint in c]

        best, errors = '', 999
        while errors != 0:
            shuffle(w_m)
            a, b = greedy_solver.greedy_find(w_m, c_m)
            if b == 0:
                print(print('SOLUTION FOUND @', file, a, ':', b))
                break
            if b < errors:
                best, errors = a, b
        print('finished. best solution @', file, best, ':', errors)
