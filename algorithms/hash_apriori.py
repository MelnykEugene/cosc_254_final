import sys
import collections
from item_set import ItemSet
from hash_tree import HashTree
import timeit

dataset = '/Users/yevhenmelnyk/Desktop/data_mining/mining_final/datasets/T10I4D100k.dat'
print('dataset: ' + dataset)
output = './output/apriori/' + sys.argv[1]
minsup = float(sys.argv[2])  # absolute
print('minsup: ' + str(minsup))
data_size = int(sys.argv[3])
branch_factor = None


def hash_apriori(verbose=False):
    # in-memory transaction storage
    transactions = []

    # this can be made into an array indexed by int(item) to save memory
    items_support = collections.defaultdict(int)

    max_item = 0
    with open(dataset, 'r') as f:
        for line in f:
            transaction = [int(x) for x in str.split(line)]
            transactions.append(transaction)
            for item in transaction:
                if item > max_item: max_item = item
                items_support[item] += 1

    if verbose: print('read transactions into memory')
    global branch_factor
    branch_factor=max_item
    if verbose: print('branch factor set to ' + str(branch_factor))

    print()
    frequent_items = [x for x in items_support.keys() if items_support[x] >= minsup]
    if not frequent_items:
        return []
    else:
        frequent_items.sort()
    if verbose: print('obtained ' + str(len(frequent_items)) + ' frequent items')

    frequent_itemsets = [(x, items_support[x]) for x in frequent_items]

    k = 1
    frequent_tree_k = frequent_items
    # generate candidates of length k+1
    while True:
        if verbose: print('mining candidate tree for k = ' + str(k + 1))
        if k == 1:
            candidates_tree_kp1 = get_candidates_2(frequent_tree_k, verbose=False)
        else:
            candidates_tree_kp1 = get_candidates_kp1(frequent_tree_k, verbose=False)

        if candidates_tree_kp1.get_candidate_count() == 0:
            if verbose: print('found no new candidates at k = ' + str(k + 1))
            if verbose: print('finished')
            break

        # print leaves debug
        # node = candidates_tree_kp1.last_leaf
        # while node is not None:
        #     print('leaf has itemsets '+str([(itemset.itemset,itemset.support) for itemset in node.itemsets]))
        #     node=node.next_leaf

        # print first level interior debug
        # node = candidates_tree_kp1.root
        # for i in range(len(node.childs)):
        #     next=node.childs[i]
        #     if next is not None:
        #         print(next)

        if verbose: print('obtained ' + str(
            candidates_tree_kp1.get_candidate_count()) + ' candidates in candidate hashtree for k = ' + str(k + 1))

        if verbose: print('calculating supports...')
        # calculate supports for the new candidate tree
        for transaction in transactions:
            if len(transaction) >= k + 1:
                candidates_tree_kp1.update_supports(transaction)

        if verbose: print('filtering candidate hashtree...')

        # validate support, save frequents, remove infrequents
        node = candidates_tree_kp1.last_leaf
        while node is not None:
            # we are going to go through a list and remove items from it
            # to avoid problems with iteration of a mutating list, we instead iterate through a copy
            itemsets_to_iterate = node.itemsets.copy()
            for itemset in itemsets_to_iterate:
                if itemset.support >= minsup:
                    frequent_itemsets.append((itemset.itemset, itemset.support))
                else:
                    node.itemsets.remove(itemset)
                    candidates_tree_kp1.population -= 1
            node = node.next_leaf

        if verbose: print(str(candidates_tree_kp1.get_candidate_count()) + ' candidates are frequent')
        if verbose: print()
        # move to the next iteration using current successful candidates to generate k+2
        k += 1
        frequent_tree_k = candidates_tree_kp1

        if frequent_tree_k.get_candidate_count() == 0:
            if verbose: print('finished')
            break

    return frequent_itemsets


# generates candidates of length 2
def get_candidates_2(frequent_items, verbose=False):
    candidate_tree = HashTree(2, branch_factor)
    for i in range(len(frequent_items)):
        for j in range(i + 1, len(frequent_items)):
            candidate_tree.insert_candidate(ItemSet([frequent_items[i], frequent_items[j]]), verbose)
    return candidate_tree


# generates candidates of length k+1
# using the union of candidates of length k that share first k-1 items (like normal apriori)
# leveraging lexicographic order and the fact that candidates sharing the first k-1 items live in the same leaf
def get_candidates_kp1(hashtree_k, verbose=False):
    k = hashtree_k.itemset_size
    candidate_hashtree_kp1 = HashTree(k + 1, branch_factor)

    node = hashtree_k.last_leaf
    while node is not None:
        for i in range(len(node.itemsets)):
            itemset1 = node.itemsets[i]
            for j in range(i + 1, len(node.itemsets)):
                itemset2 = node.itemsets[j]
                # don't forget to remove this line in prod
                # assert (itemset1.itemset[:-1] == itemset2.itemset[:-1])
                # assert len(itemset1.itemset) == k
                # if we have the right order, join to get new candidate
                if itemset1.itemset[-1] < itemset2.itemset[-1]:
                    candidate = []
                    candidate.extend(itemset1.itemset)
                    candidate.append(itemset2.itemset[-1])
                else:
                    continue
                if check_frequency_of_all_immediate_subsets(candidate, hashtree_k):
                    candidate_hashtree_kp1.insert_candidate(ItemSet(candidate), verbose)

        node = node.next_leaf
    return candidate_hashtree_kp1


# prunes candidates of length K+1 if they contain a non-frequent subset of length K
# we do so by looking up subsets in the previous-iteration frequent tree
#  this treats 'candidate' as an int array as opposed to ItemSet for convenience.
def check_frequency_of_all_immediate_subsets(candidate_kp1, hash_tree_k):
    # remove ith item to obtain an immediate k-subset
    for i in range(0, len(candidate_kp1)):
        # cut out ith item
        subset = candidate_kp1[0:i] + candidate_kp1[i + 1::]
        # if any of the resulting subsets is not in the frequent tree for length k, disregard the candidate
        if not hash_tree_k.lookup(subset):
            return False
    return True


from apriori import apriori
#aprioris = apriori()
#hashes=hash_apriori()
print('hashapriori took: '+str(timeit.timeit(hash_apriori,number=1)))
print(hash_apriori())
print('=========================================================')
print('apriori took: ' + str(timeit.timeit(apriori,number=1)))

#aprioris=apriori()
#hashes=hash_apriori()
#print('difference in output: '+str([x for x in aprioris if x not in hashes] + [x for x in hashes if x not in aprioris]))