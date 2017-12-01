import wizard_parse as wp
import branch_search
from random import shuffle
import re
import graph_tool.all as gt


#dirs = ['inputs20', 'inputs35', 'inputs50', 'Staff_Inputs']
dirs = ['inputs50']
#f = ['input50_0.in', 'input50_1.in', 'input50_2.in', 'input50_3.in', 'input50_4.in', 'input50_9.in', 'input50_7.in']
#dirs = ['Staff_Inputs']
#f = ['staff_60.in']

t = 0
for dir in dirs:
    files = wp.get_files(dir)
    # Process in ascending numeric order
    files.sort(key=lambda file:int(re.sub("[^0-9]", "", file)))
    for file in files:
    #for file in f:
        print('===')
        print('searching for solution to', file)
        w, c = wp.parse_partial(dir, file)
        p = branch_search.Party(dir, file)
        cnf = branch_search.CNF(p)
        t += branch_search.time_fn(cnf.find_assignment, [len(cnf.clauses)])
        order = cnf.create_ordering()

        #g = cnf.relationships
        #pos = gt.arf_layout(g, max_iter=0)
        #gt.graph_draw(g, pos=pos, output="visualisation" + wp.separator() + "{}_{}".format(t, file) + '.pdf')
        #with open('outputs' + str(p.wizard_count) + wp.separator() + "{}_{}".format(p.wizard_count, files.index(file)), "w") as f:
        #    f.write(order)
        print(order)

print('average time taken:', t // len(f), 'seconds')