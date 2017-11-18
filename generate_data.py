import random
import os


def generate_data(w_count, c_count):
    def is_duplicate(c):
        alternate = [c[1], c[0], c[2]]
        return c in constraint or alternate in constraint

    constraint = []
    wizards = [i for i in range(w_count)]
    while len(constraint) < c_count:
        i = [wizards.index(r) for r in random.sample(set(wizards), 3)]
        i.sort()
        c = random.choice([[i[0], i[1], i[2]], [i[1], i[2], i[0]]])

        if not is_duplicate(c):
            constraint += [c]

    return wizards, constraint

def make_files(file_count, wizard_count):
    d = generate_data(wizard_count, 500)
    lines = write_file(d[0], d[1])
    for i in range(file_count):
        with open(str(wizard_count) + '\\' + "{}_{}".format(wizard_count, i), "w") as f:
            f.write(lines[0])
            f.write('\n')
            f.write(lines[1])
            f.write('\n')
            f.write(lines[2])
            f.write('\n')
            for s in lines[3]:
                f.write(s)
                f.write('\n')


def write_file(wizards, constraints):
    line1 = str(len(wizards))
    line2 = ' '.join([str(name) for name in wizards])
    line3 = str(len(constraints))
    rest = [' '.join([str(c) for c in lst]) for lst in constraints]
    return line1, line2, line3, rest


make_files(5000, 20)