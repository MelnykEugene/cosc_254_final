import sys
import collections
import math

dataset = './datasets/' + sys.argv[0]
minsup = sys.argv[1]  # relative minimum support
data_size = sys.argv[2]


def apriori():
    k = 0
    frequent_itemsets = []

    # in-memory transaction storage
    transactions = []

    # this can be made into an array indexed by int(item) to save memory
    items_support = collections.defaultdict(int)

    with open(dataset, 'r') as f:
        for line in f:
            transaction = [int(x) for x in str.split(line)]
            transactions.append(transaction)
            for item in transaction:
                items_support[item] += 1

    # absolute minimum support
    mincount = math.ceil(minsup * len(transactions))

    frequent_items = [x for x in items_support.keys() if items_support[x] >= mincount]
    if not frequent_items:
        return []
    else:
        frequent_items.sort()


    do:

    while True:


        if

# generates frequent pairs
def get_candidates_2(frequent_items):
    candidates = []
    for i in range(len(frequent_items)):
        for j in range(i + 1, len(frequent_items)):
            candidates.append([i, j])
    return candidates
