import wizard_parse
import branch_search
from random import shuffle

dirs = ['inputs20', 'inputs35', 'inputs50', 'Staff_Inputs']

for dir in dirs:
    for file in wizard_parse.get_files(dir):
        print('searching for solution to', file)
        w, c = wizard_parse.parse_partial(dir, file)
        p = branch_search.Party(dir, file)
        cnf = branch_search.CNF(p)
        branch_search.time_fn(cnf.find_assignment, [len(cnf.clauses)])
        order = cnf.create_ordering()
        print(order)