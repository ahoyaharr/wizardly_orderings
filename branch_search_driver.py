import wizard_parse as wp
import branch_search
from random import shuffle
import re



dirs = ['inputs20', 'inputs35', 'inputs50', 'Staff_Inputs']
#dirs = ['Staff_Inputs']

for dir in dirs:
    files = wp.get_files(dir)
    # Process in ascending numeric order
    files.sort(key=lambda file:int(re.sub("[^0-9]", "", file)))
    for file in files:
        print('===')
        print('searching for solution to', file)
        w, c = wp.parse_partial(dir, file)
        p = branch_search.Party(dir, file)
        cnf = branch_search.CNF(p)
        branch_search.time_fn(cnf.find_assignment, [len(cnf.clauses)])
        order = cnf.create_ordering()
        with open('outputs' + str(p.wizard_count) + wp.separator() + "{}_{}".format(p.wizard_count, files.index(file)), "w") as f:
            f.write(order)
        print(order)