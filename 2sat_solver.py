import wizard_parse
import graph_tool.all as gt
import graph_tool.topology as topo
import collections
import time
import random
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


class TwoSAT:
    def __init__(self, party):
        """
        :clauses: A list of each clause which must be satisfied. Clauses are pairs of variables.
        :relationships: A directed graph graph representating the relative age of wizards, where 
        each wizard is a node and an edge UV means that wizard U is younger than wizard V.
        :wizard_map: Mapping between the name of a wizard and the index of it's vertex
        """
        self.party = party
        self.clauses = [Clause.construct_pair(*constraint.split()) for constraint in party.constraints]
        self.g = gt.Graph()
        # for each variable x_i in the 2-SAT instance, xi and ~xi are vertices.
        # xi and ~xi are complements of each other.
        self.g.add_vertex(party.constraint_count * 4)

        # maps the vertex representing a variable to the vertex representing the complement of that variable
        self.vertex_complement = dictionary()

        # clause_mapping takes a clause, and returns a tuple containing the vertices which
        # represent the variables (x_i, ~x_i, x_i+1, ~x_i+1).

        self.clause_mapping = {clause:self.clause_to_vertices(clause) for clause in self.clauses}
        # map each vertex to the variable which it represents. assignments happen in clause_to_verticies.
        self.vertex_to_variable = dictionary()

        # map each vertex to it's assignment, either True or False
        self.vertex_assignment = dictionary()

        # find a satisfying assignment
        self.satisfy()

    def clause_to_vertices(self, clause):
        """
        Returns the two vertices which represent v_i, v_i+1 of a given clause.
        """
        assert clause in self.clauses
        clause.lt.clause = clause
        clause.gt.clause = clause
        index = 4 * (self.clauses.index(clause) + 1)
        v = list(self.g.vertices())
        variables = tuple(v[i] for i in range(index - 4, index))
        self.vertex_complement[variables[0]] = variables[1]
        self.vertex_complement[variables[1]] = variables[0]
        self.vertex_complement[variables[2]] = variables[3]
        self.vertex_complement[variables[3]] = variables[2]
        self.vertex_assignment[variables[0]] = clause.lt
        self.vertex_assignment[variables[2]] = clause.gt
        return variables


    def satisfy(self):
        """
        Solves the 2-SAT instance using an implication graph.
        https://en.wikipedia.org/wiki/Implication_graph
        """
        # for each clause in the form (u OR v),
        # add the edges (~u -> v) and (~v -> u) to G
        # 1 constraint => (x_1 or ~x_2)(~x_1 or x_2)(x_1 or x_2)
        for clause in self.clauses:
            u_t, u_f, v_t, v_f = self.clause_mapping[clause]
            self.g.add_edge(u_f, v_t)
            self.g.add_edge(v_f, u_t)
            self.g.add_edge(u_t, )

        # find the reverse topological order
        reverse_topological_order = topo.topological_sort(self.g)[::-1]

        # find the strongly connected components
        # components[vertex] -> scc id
        components = topo.label_components(self.g)[0]
        
        # each component is marked either TRUE, or FALSE
        marked_components = {} 
        for vertex in reverse_topological_order:
            scc = components[vertex]
            if scc not in marked_components:
                # if a variable and it's complement are members of the same scc, then
                # there is no satisfying assignment
                if components[self.vertex_complement[vertex]] is scc:
                    return False
                # otherwise, mark the current scc as true
                marked_components[scc] = True
                # mark the scc containing the complement of the current variable as false
                marked_components[components[self.vertex_complement[vertex]]] = False

        self.vertex_assignment = {vertex: marked_components[components[vertex]] for vertex in self.g.vertices()}
        return True





# For each SSC, S in reverse topological order
#   if S marked: pass
#   else if S = ~S: (i.e., a variable and its complement belong to the same SCC), the instance is unsatisfiable. 
#   else: mark S := TRUE, ~S := FALSE

# We get a satisfying assignment by assigning to each variable the truth value of the component containing it.

def time_fn(fn, args):
    start = time.time()
    fn(*args)
    t = (time.time() - start)
    print('time taken: %s' % t)
    return int(t) 