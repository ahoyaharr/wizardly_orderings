import wizard_parse
import branch_search
from random import shuffle

#dirs = ['inputs20', 'inputs35', 'inputs50', 'Staff_Inputs']
dirs = ['Staff_Inputs']

for dir in dirs:
    files = wizard_parse.get_files(dir)
    files.sort()
    for file in files:
        print('===')
        print('searching for solution to', file)
        w, c = wizard_parse.parse_partial(dir, file)
        p = branch_search.Party(dir, file)
        cnf = branch_search.CNF(p)
        branch_search.time_fn(cnf.find_assignment, [len(cnf.clauses)])
        order = cnf.create_ordering()
        print(order)