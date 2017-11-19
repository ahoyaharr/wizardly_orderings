import os
import sys

WINDOWS_ENCODING = '\\'
UNIX_ENCODING = '/'

SYSTEM_TYPE = 'windows'


def parse_complete(d, s):
    file = open(os.path.dirname(os.path.realpath(sys.argv[0])) + separator() + d + separator() + s)
    total = file.read().splitlines()
    wizards = total[1].split()
    constraints = total[3:]
    return wizards, constraints


def parse_partial(d, s):
    file = open(os.path.dirname(os.path.realpath(sys.argv[0])) + separator() + d + separator() + s)
    total = file.read().splitlines()
    wizards = set()
    wizard_count = int(total[0])
    constraints = total[3:]
    for constraint in constraints:
        for wizard in constraint.split():
            if wizard not in wizards:
                wizards.add(wizard)
            if wizard_count == len(wizards):
                break
    return sorted(list(wizards)), constraints

def get_files(path, absolute=False):
    def get_script_path(p):
        return os.path.dirname(os.path.realpath(sys.argv[0])) + separator() + p

    files = os.listdir(get_script_path(path))
    return [get_script_path(path) + separator() + file for file in files] if absolute else files


def separator():
    return WINDOWS_ENCODING if SYSTEM_TYPE == 'windows' else UNIX_ENCODING


def print_wizards(w, c):
    w_s = ', '.join(w)
    c_s = '\n'.join(c)
    print('Wizard Names:', w_s, '\n Subject To:\n', c_s)
