import sys
import collections
from item_set import ItemSet
from hash_tree_general import HashTree
import timeit
import tracemalloc

tracemalloc.start()
dataset = 'datasets/mushroom.dat'
print('dataset:' + dataset)
minsup = float(sys.argv[1])  # absolute
print('minsup: ' + str(minsup))
branch_fraction = float(sys.argv[2])
print('branch fraction: ' +str(branch_fraction))

def hash_apriori(branch_fraction,verbose=True):
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
    branch_factor = int(max_item*branch_fraction)

    if verbose: 
        print('branch fraction: ' + str(branch_fraction))
        print('branch factor set to ' + str(branch_factor))

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
            candidates_tree_kp1 = get_candidates_2(frequent_tree_k, branch_factor,verbose=False)
        else:
            candidates_tree_kp1 = get_candidates_kp1(frequent_tree_k, branch_factor,verbose=False)
        
        if candidates_tree_kp1.get_candidate_count() == 0:
            if verbose: print('found no new candidates at k = ' + str(k + 1))
            if verbose: print('finished')
            break

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
    print(len(frequent_itemsets))
    return frequent_itemsets


# generates candidates of length 2 in simple way
def get_candidates_2(frequent_items,branch_factor,verbose=False):
    candidate_tree = HashTree(2, branch_factor)
    for i in range(len(frequent_items)):
        for j in range(i + 1, len(frequent_items)):
            candidate_tree.insert_candidate(ItemSet([frequent_items[i], frequent_items[j]]), verbose)
    return candidate_tree


# generates candidates of length k+1
# using the union of candidates of length k that share first k-1 items (like normal apriori)
# leveraging lexicographic order and the fact that candidates sharing the first k-1 items live in the same leaf
def get_candidates_kp1(hashtree_k,branch_factor,verbose=False):
    k = hashtree_k.itemset_size
    candidate_hashtree_kp1 = HashTree(k + 1, branch_factor)

    node = hashtree_k.last_leaf
    prev_frequents=[]

    while node is not None:
        prev_frequents.extend(node.itemsets)
        node = node.next_leaf
    
    for i in range(len(prev_frequents)):
        itemset1 = prev_frequents[i]
        for j in range(i + 1, len(prev_frequents)):
            itemset2 = prev_frequents[j]
            if itemset1.itemset[:-1]==itemset2.itemset[:-1] and itemset1.itemset[-1] < itemset2.itemset[-1]:
                candidate = []
                candidate.extend(itemset1.itemset)
                candidate.append(itemset2.itemset[-1])
            else:
                continue
                
            if check_frequency_of_all_immediate_subsets(candidate, hashtree_k):
                candidate_hashtree_kp1.insert_candidate(ItemSet(candidate), verbose)

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


#aprioris = apriori()
#hashes=hash_apriori()
def wrapper(func, *args, **kwargs):
    def wrapped():
        return func(*args, **kwargs)
    return wrapped

wrapped = wrapper(hash_apriori,branch_fraction)

#t10i4d100k with minsup = 1000 shows a performance improvement of 90x. takes about 1h to run
print('hashapriori took: '+str(timeit.timeit(wrapped,number=1)))
current, peak = tracemalloc.get_traced_memory()
print(f"Current memory usage is {current / 10 ** 6}MB; Peak was {peak / 10 ** 6}MB")
tracemalloc.stop()
# print(hash_apriori())
print('=========================================================')

#aprioris=apriori()
#hashes=hash_apriori()
#print('difference in output: '+str([x for x in aprioris if x not in hashes] + [x for x in hashes if x not in aprioris]))
