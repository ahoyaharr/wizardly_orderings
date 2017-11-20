import wizard_parse
import greedy_solver
from random import shuffle

dirs = ['inputs20', 'inputs35', 'inputs50']

def fname(s):
    return 'input20_' + s + '.in'

f = [fname('3'), fname('5'), fname('7'), fname('9'), fname('4')]

for dir in dirs:
    #for file in f:
    for file in wizard_parse.get_files(dir):
        w, c = wizard_parse.parse_partial(dir, file)

        number_to_wizard = {i: w[i] for i in range(len(w))}
        wizard_to_number = {w[i]: i for i in range(len(w))}

        w_m = [wizard_to_number[wizard] for wizard in w]
        c_m = [[wizard_to_number[constraint.split()[0]],
                wizard_to_number[constraint.split()[1]],
                wizard_to_number[constraint.split()[2]]]
               for constraint in c]

        constraint_flexibility = 0.1 * len(c)
        c = 0
        best, errors = '', 999
        print('searching for solution to', file)
        while errors >= constraint_flexibility:
            c += 1
            shuffle(w_m)
            a, b = greedy_solver.greedy_find(w_m, c_m)
            if b < errors:
                best, errors = a, b
                print('run', c, '@', file, best, ':', errors)
            if b == 0:
                print(print('SOLUTION FOUND @', file, a, ':', b))
                break

        print('finished. best solution @', file, best, ':', errors)
