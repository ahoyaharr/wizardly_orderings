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
        """
        A clause has two variables.
        :param lt: w_3
        :param gt:
        """
        self.satisfied = False
        self.lt = lt
        self.gt = gt

    def is_satisfied(self):
        return bool(self.satisfied)

    def satisfy_clause(self, lt, relationship):
        """
        Satisfies a clause by satisfying one variable in a clause. A clause which has already been
        satisfied may not be satisfied (doing so would cause a contradiction).
        :param lt: True the clause is satisfied by assigning TRUE to the lt variable, and False otherwise.
        :param relationship: the relationship dictionary to update.
        :return: updated relationship data.
        """
        assert self.is_satisfied() is False
        v = self.lt if lt else self.gt
        if v.less_than:
            relationship[v.target].update([v.context1, v.context2])
        else: # greater_than case
            relationship[v.context1].add(v.target)
            relationship[v.context2].add(v.target)
        self.satisfied = 'less_than' if v.less_than is True else 'greater_than'
        return relationship

    def dissatisfy_clause(self, relationship):
        """
        dissatisfy a clause, and reverts changes to the relationship data.
        :param relationship: the relationship data
        :return: the reverted relationship data
        """
        assert self.is_satisfied() is True
        if self.satisfied is 'less_than':
            relationship[self.lt.target].remove(self.lt.context1)
            relationship[self.lt.target].remove(self.lt.context2)
        else: # 'greater_than' case
            relationship[self.gt.context1].remove(self.gt.target)
            relationship[self.gt.context2].remove(self.gt.target)
        self.satisfied = False
        return relationship

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

    def next_unsatisfied_clause(self):
        for clause in self.clauses:
            if not clause.is_satisfied():
                return clause
        return 'finished'

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
        next_clause = self.next_unsatisfied_clause()
        if next_clause is 'finished' and self.validate_relationships():
            return True

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
