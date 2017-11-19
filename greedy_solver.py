from sys import maxsize


def greedy_find(wizards, constraints):
    def evaluate_ordering(ordering):
        error_count = 0
        for c in constraints:
            c_1 = ordering.index(c[0]) if c[0] in ordering else -maxsize // 2
            c_2 = ordering.index(c[1]) if c[1] in ordering else maxsize // 2
            c_3 = ordering.index(c[2]) if c[2] in ordering else abs(c_1) + abs(c_2)
            if c_1 < c_3 < c_2 or c_1 > c_3 > c_2:
                error_count += 1
        return error_count

    def add_wizard(w):
        permutations = [order[:k] + [w] + order[k:] for k in range(len(order) + 1)]
        rankings = [evaluate_ordering(o) for o in permutations]
        return permutations[rankings.index(min(rankings))]

    order = [wizards[0]]
    for wizard in wizards[1:]:
        order = add_wizard(wizard)
    #if evaluate_ordering(order) == 2:
    #    print(order)
    return order, evaluate_ordering(order)
