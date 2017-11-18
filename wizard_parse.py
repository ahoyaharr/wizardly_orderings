import os
import sys


def parse(s):
    file = open(s)
    total = file.read().splitlines()
    wizards = total[1].split()
    constraints = total[3:]
    return wizards, constraints


def get_files(path):
    def get_script_path(p):
        return os.path.dirname(os.path.realpath(sys.argv[0])) + '\\' + p

    files = os.listdir(get_script_path(path))
    return [get_script_path(path) + '\\' + file for file in files]
