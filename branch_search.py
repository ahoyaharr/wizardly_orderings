import wizard_parse

dir = 'inputs20'
file = 'input20_0.in'


class Party:
    def __init__(self, dir, file):
        self.wizards, self.constraints = wizard_parse.parse_partial(dir, file)  # Wizards and constraints
        self.wizard_count = len(self.wizards)  # The number of wizards at the party
        self.constraint_count = len(self.constraints)  # The number of constraints


class Variable:
    def __init__(self, context1, context2, target, less_than):
        # Arguments come in the form of a constraint: {w_1, w_2, w_3}.
        assert less_than is True or less_than is False
        self.target = target
        self.context1 = context1
        self.context2 = context2
        self.less_than = less_than  # True => target < context1, target < context2


class Clause:
    def __init__(self, lt, gt):
        self.satisfied = False
        self.lt = lt
        self.gt = gt

    @staticmethod
    def construct_pair(c1, c2, c3):
        """
        For any given constraint, c3 is not in the range of c1 and c2. This is equivalently represented
        as either c3 is greater than c1 and c2, or it is less than c1 and c2.
        :return: The clause of x_i := c3 is below the range and x_{i+1} := c3 is above the range.
        """
        return Clause(Variable(c1, c2, c3, True), Variable(c1, c2, c3, False))


class CNF:
    def __init__(self, party):
        self.clauses = [Clause.construct_pair(*constraint.split()) for constraint in party.constraints]
        self.relationships = {wizard: set() for wizard in party.wizards}

    def validate_relationships(self):
        """
        If i is a member of the set associated with k, and k is a member of the list associated with i,
        then there is a contradiction and there must have been a mistake.
        :return: True if there is no contradiction, otherwise False.
        """
        for wizard in self.relationships:
            associations = self.relationships[wizard]
            for associate in associations:
                if wizard in self.relationships[associate]:
                    return False
        return True

    def find_assignment(self):
        """
        Performs an exhausive, branching search to find a valid assignment by populating relationship data.
        :return: True if a valid assignment is found, otherwise False.
        """
        if not self.validate_relationships():
            return False

        return False

    def create_ordering(self):
        """
        Constructs a valid ordering using relationship data from a valid assignment.
        :return: A valid ordering, or False if a valid ordering does not exist.
        """
        if not self.find_assignment():
            return False
        ordering = list()
        return ordering


p = Party(dir, file)
c = CNF(p)
