import sys
import collections
from item_set import ItemSet
from single_hash_tree import HashTree
import timeit
import tracemalloc

tracemalloc.start()
dataset = 'datasets/T40I10D100K.dat'
output = '/output/apriori/' + sys.argv[1]
minsup = float(sys.argv[2])  # absolute
print('minsup: ' + str(minsup))
data_size = int(sys.argv[3])
branch_factor = None

def setup():
    transactions = []
    items_support = collections.defaultdict(int)

    max_item = 0
    with open(dataset, 'r') as f:
        for line in f:
            transaction = [int(x) for x in str.split(line)]
            transactions.append(transaction)
            for item in transaction:
                if item > max_item: max_item = item
                items_support[item] += 1


    frequent_items = [x for x in items_support.keys() if items_support[x] >= minsup]
    if not frequent_items:
        return []
    else:
        frequent_items.sort()

    frequent_itemsets = [(x, items_support[x]) for x in frequent_items]
    return transactions, frequent_itemsets, frequent_items, max_item

def hash_apriori():
    transactions,frequent_itemsets, frequent_items, branch_factor = setup()
    print()
    print(dataset)
    print("transactions: " +str(len(transactions)))
    print('support threshold: '+str(minsup))
    print('frequent items: '+str(len(frequent_items)))
    print('branching factor: ' + str(branch_factor))
    print()

    frequent_pairs = get_candidates_2(frequent_items,branch_factor)#
    print("Calculating pair supports")
    for transaction in transactions:
        frequent_pairs.update_supports(transaction)
    

    frequents = filter(frequent_pairs)
    frequent_itemsets.extend(frequents)
    if len(frequents)==0:
            print('No frequent pairs found, aborting...')
           
            return frequent_itemsets
    frequent_tree_k=frequent_pairs
    k=2

    while True:
        new_candidates_count = frequent_tree_k.next_tree()

        if new_candidates_count == 0:
            print('no new candidates')
            break

        for transaction in transactions:
            if len(transaction) >= k + 1:
                frequent_tree_k.update_supports(transaction)

        frequents = filter(frequent_tree_k)
        frequent_itemsets.extend(frequents)

        if len(frequents)==0:
            print('no frequents')
            break
        k += 1

    return frequent_itemsets


def get_candidates_2(frequent_items,branch_factor):
    candidates=[]
    for i in range(len(frequent_items)):
        for j in range(i + 1, len(frequent_items)):
            candidates.append(ItemSet([frequent_items[i], frequent_items[j]]))
    candidate_tree = HashTree(branch_factor,candidates)
    return candidate_tree

def filter(tree):
    node = tree.last_leaf
    frequents=[]
    while node is not None:
        itemsets_to_iterate = node.itemsets.copy()
        for itemset in itemsets_to_iterate:
            if itemset.support >= minsup:
                frequents.append((itemset.itemset, itemset.support))
            else:
                node.itemsets.remove(itemset)
        node = node.next_leaf
    return frequents

print(timeit.timeit(hash_apriori,number=1))
#print(len(hash_apriori()))