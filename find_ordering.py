#    def order_clauses(self):
 #       clause_data = [[c.lt.target, c.lt.context1, c.lt.context2] for c in self.clauses]
  #      unpacked_clauses = list(chain.from_iterable(clause_data))
   #     wizards = list(set(unpacked_clauses))
    #    wizard_frequency = {wizard: unpacked_clauses.count(wizard) for wizard in wizards}
     #   wizards.sort(key=lambda wizard: -1 * wizard_frequency[wizard])
     ##   wizard_frequency = {wizards[i]: pow(2, i) for i in range(len(wizards))}
      #  self.clauses.sort(key=lambda c: -1 * \
      #      (wizard_frequency[c.lt.context1] + wizard_frequency[c.lt.context2] + wizard_frequency[c.lt.target]))
      #  return wizards

from itertools import chain

def order_by_frequency(l):
    """
    l: a list of lists in the form [ [w1, w2, w3], ...]
    return: a list in the form [w1, w2, ...], in ascending order of frequency
    """
    # the contents of the internal lists of l unpacked into a larger list
    unpacked = list(chain.from_iterable(l))
    # w is a list of the wizards
    w = list(set(list(unpacked)))
    # count the number of occurrences of each wizard in unpacked and store in a dictionary
    frequency = {wizard: unpacked.count(wizard) for wizard in w}
    # order the list of wizards in ascending order of their frequency
    w.sort(key=lambda wizard: frequency[wizard])
    return w


def score_list(l, c, scores=None):
    """
    l: a list of lists in the form [ [w1, w2, w3], ...]
    c: the maximum power to use
    return: a dictionary containing a score for each wizard.
    if a dictionary containing scores is passed in, then
    scores are updated by addition
    """
    o = order_by_frequency(l)
    s = {o[i]:int(pow(2, c - i)) for i in range(len(o))}
    if not scores:
        return s
    for key in s:
        scores[key] = scores[key] + s[key] if key in scores else s[key]
    return scores

