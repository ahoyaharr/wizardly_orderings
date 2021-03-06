import wizard_parse
import graph_tool.all as gt
import graph_tool.topology as topo
import time
from itertools import chain

class Party:
    def __init__(self, dir, file):
        self.wizards, self.constraints = wizard_parse.parse_partial(dir, file)  # Wizards and constraints
        self.wizard_count = len(self.wizards)  # The number of wizards at the party
        self.constraint_count = len(self.constraints)  # The number of constraints


class Variable:
    def __init__(self, context1, context2, target, less_than, clause=None):
        # Arguments come in the form of a constraint: {w_1, w_2, w_3}.
        assert less_than is True or less_than is False
        self.target = target
        self.context1 = context1
        self.context2 = context2
        self.less_than = less_than  # True => target < context1, target < context2
        self.clause = clause


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
        self.lt.clause = self  # Each variable gets a reference to the clause of
        self.gt.clause = self  # which it is a member

    def __repr__(self):
        return str(self.satisfied) + ', ' + str(self.lt.context1) + ', ' + str(self.lt.context2) + ', ' + str(self.lt.target)

    def is_satisfied(self):
        return bool(self.satisfied)

    def get_vars(self):
        return (self.lt, self.gt)

    def satisfy_clause(self, lt, relationship, mapping):
        """
        Satisfies a clause by satisfying one variable in a clause. A clause which has already been
        satisfied may not be satisfied (doing so would cause a contradiction).
        :param lt: True the clause is satisfied by assigning TRUE to the lt variable, and False otherwise.
        :param relationship: the relationship dictionary to update.
        :return: updated relationship data.
        """
        assert self.is_satisfied() is False
        #if self.is_satisfied():
        #    self.dissatisfy_clause(relationship, mapping)

        v = self.lt if lt else self.gt
        if v.less_than:
            relationship.add_edge(mapping[v.target], mapping[v.context1])
            relationship.add_edge(mapping[v.target], mapping[v.context2])
        else: # greater_than case
            relationship.add_edge(mapping[v.context1], mapping[v.target])
            relationship.add_edge(mapping[v.context2], mapping[v.target])
        self.satisfied = 'less_than' if v.less_than is True else 'greater_than'
        return self.satisfied

    def dissatisfy_clause(self, relationship, mapping):
        """
        dissatisfy a clause, and reverts changes to the relationship data.
        :param relationship: the relationship data
        :return: the reverted relationship data
        """
        assert self.is_satisfied() is True
        if self.satisfied is 'less_than':
            relationship.remove_edge(relationship.edge(mapping[self.lt.target], mapping[self.lt.context1]))
            relationship.remove_edge(relationship.edge(mapping[self.lt.target], mapping[self.lt.context2]))
        else: # greater_than case
            relationship.remove_edge(relationship.edge(mapping[self.gt.context1], mapping[self.gt.target]))
            relationship.remove_edge(relationship.edge(mapping[self.gt.context2], mapping[self.gt.target]))
        self.satisfied = False
        return self.satisfied

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
        """
        :clauses: A list of each clause which must be satisfied. Clauses are pairs of variables.
        :relationships: A directed graph graph representating the relative age of wizards, where 
        each wizard is a node and an edge UV means that wizard U is younger than wizard V.
        :wizard_map: Mapping between the name of a wizard and the index of it's vertex
        """
        self.clauses = [Clause.construct_pair(*constraint.split()) for constraint in party.constraints]
        self.order_clauses()
        self.relationships = gt.Graph()
        self.relationships.add_vertex(party.wizard_count) # Each wizard is a vertex
        self.wizard_map = {party.wizards[i]: i for i in range(party.wizard_count)}
        self.vertex_name = self.relationships.new_vertex_property('string')
        for i in range(party.wizard_count):
            self.vertex_name[i] = party.wizards[i]


    def order_clauses(self):
        clause_data = [[c.lt.target, c.lt.context1, c.lt.context2] for c in self.clauses]
        unpacked_clauses = list(chain.from_iterable(clause_data))
        wizards = list(set(unpacked_clauses))
        wizard_frequency = {wizard: unpacked_clauses.count(wizard) for wizard in wizards}
        wizards.sort(key=lambda wizard: -1 * wizard_frequency[wizard])
        wizard_frequency = {wizards[i]: pow(2, i) for i in range(len(wizards))}
        self.clauses.sort(key=lambda c: -1 * \
            (wizard_frequency[c.lt.context1] + wizard_frequency[c.lt.context2] + wizard_frequency[c.lt.target]))
        return wizards
    

    def next_unsatisfied_clause(self):
        """
        return: the next unsatisfied clause
        """
        for clause in self.clauses:
            if not clause.is_satisfied():
                return clause
        return 'satisfied'

    def is_valid_relationship(self):
        """
        If there is a cycle in relationships, then there is a contradiction. 
        """
        return topo.is_DAG(self.relationships)


    def find_assignment(self, clause):
        if clause == 0 and self.is_valid_relationship():
            return True
        if not self.is_valid_relationship():
            # Revert the changes to the graph caused by the previous find_assignment
            return False

        # Get the current clause
        c = self.clauses[clause - 1]

        # Try satisfying the LT variable
        c.satisfy_clause(True, self.relationships, self.wizard_map)
        if self.find_assignment(clause - 1):
            return True
        # LT must have failed; revert changes to graph
        c.dissatisfy_clause(self.relationships, self.wizard_map)
        # Try satisfying the GT variable
        c.satisfy_clause(False, self.relationships, self.wizard_map)
        r = self.find_assignment(clause - 1)
        if not r:
            # Revert changes if GT failed
            c.dissatisfy_clause(self.relationships, self.wizard_map)
        # Propagate result   
        return r                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              


    def create_ordering(self):
        """
        Constructs a valid ordering using relationship data from a valid assignment.
        :return: A valid ordering, or False if a valid ordering does not exist.
        """
        return ' '.join([self.vertex_name[vertex] for vertex in topo.topological_sort(self.relationships)])


def time_fn(fn, args):
    start = time.time()
    fn(*args)
    t = (time.time() - start)
    print('time taken: %s' % t)
    return int(t) 