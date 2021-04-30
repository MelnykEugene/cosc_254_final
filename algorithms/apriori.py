import sys
import collections
import math
from item_set import ItemSet
import tracemalloc
import timeit
import os

dataset = sys.argv[1]
dataset='./datasets/'+dataset
minsup = int(sys.argv[2])  # absolute

def wrapper(func, *args, **kwargs):
    def wrapped():
        return func(*args, **kwargs)
    return wrapped

def apriori(verbose=True):
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
    if verbose: print('read transactions into memory')

    frequent_items = [x for x in items_support.keys() if items_support[x] >= minsup]
    if not frequent_items:
        return []
    else:
        frequent_items.sort()
    if verbose: print('obtained ' + str(len(frequent_items)) + ' frequent items')

    # add frequent items to the resulting collection of frequent itemsets
    frequent_itemsets = [(x, items_support[x]) for x in frequent_items]

    # ----------------------------------------------------------------------
    k = 1
    frequentsK = frequent_items
    # generate k+1 itemsets
    while True:
        if k == 1:
            candidates = get_candidates_2(frequentsK)
        else:
            # pruning happens here
            candidates = get_candidates_kp1(frequentsK, k )
        if verbose: print('obtained ' + str(len(candidates)) + ' candidates of length ' + str(k + 1))
        k += 1
        # only keep those who are frequent
        frequentsK = [candidate for candidate in candidates if check_candidate_support(candidate, transactions)]
        if verbose: print('of which ' + str(len(frequentsK)) + ' are frequent')
        if verbose: print()
        # save into the results list
        for itemset in frequentsK:
            frequent_itemsets.append((itemset.itemset, itemset.support))

        if not frequentsK:
            break

    write_to_file(frequent_itemsets,dataset,minsup)
    return frequent_itemsets


# generates candidates of length 2
def get_candidates_2(frequent_items):
    candidates = []
    for i in range(len(frequent_items)):
        for j in range(i + 1, len(frequent_items)):
            # lexicographic order is maintained both in the list of candidates and within any candidate
            candidates.append(ItemSet([frequent_items[i], frequent_items[j]]))
    return candidates


# generates candidates of length k+1
def get_candidates_kp1(frequentsK, k):
    candidates = []
    for i in range(len(frequentsK)):
        itemset1 = frequentsK[i].itemset
        for j in range(i + 1, len(frequentsK)):
            itemset2 = frequentsK[j].itemset

            # if the first k-1 items are the same
            if (itemset1[:-1] == itemset2[:-1]
                    # and the last items respect lexicographic order
                    and itemset1[len(itemset1) - 1] < itemset2[len(itemset2) - 1]):
                # join to make a new k+1 candidate
                candidate = []
                candidate.extend(itemset1)
                candidate.append(itemset2[-1])
                candidate = ItemSet(candidate)
            else:
                # some optimization here by conditionally continuing the OUTER loop?
                continue

            if check_frequency_of_all_immediate_subsets(candidate, frequentsK):
                candidates.append(candidate)
    return candidates


# prunes candidates of length K+1 if they contain a non-frequent subset of length K
def check_frequency_of_all_immediate_subsets(candidate, frequentsK_1):
    # remove ith item to obtain an immediate subset
    for i in range(0, len(candidate.itemset)):
        # cut out ith item
        subset = candidate.itemset[0:i] + candidate.itemset[i + 1::]
        # if any of the resulting subsets is not frequent, disregard the candidate
        if not subset in [set.itemset for set in frequentsK_1]:
            return False

    return True


# check whether out K+1 candidate is frequent by naive counting
def check_candidate_support(candidate, transactions):
    supp = 0
    for transaction in transactions:
        if len(transaction) < len(candidate.itemset):
            continue
        if set(candidate.itemset) <= set(transaction):
            supp += 1
    candidate.support = supp
    if supp >= minsup:
        return True
    else:
        return False

def write_to_file(frequent_itemsets,dataset,minsup):
    input_file = dataset.split('/')[-1]
    output = './output/apriori_' + input_file + '_' + str(minsup) +'.txt'

    #https://stackoverflow.com/questions/12517451/automatically-creating-directories-with-file-output
    if not os.path.exists(os.path.dirname(output)):
        try:
            os.makedirs(os.path.dirname(output))
        except OSError as exc: # Guard against race condition
            if exc.errno != errno.EEXIST:
                raise
        
    with open(output,'w') as f:
        f.truncate()
        for item in frequent_itemsets:
            f.write(str(item[0]) + '   ' + str(item[1])+'\n')



if __name__=='__main__':
    print('Apriori')
    print('found ' + str(len(apriori())) + ' frequent itemsets, check output directory')

# if __name__ == '__main__':
#     print("apriori")
#     tracemalloc.start()
#     wrappedeapriori = wrapper(apriori)
#     time_apriori = timeit.timeit(wrappedeapriori, number=1)*1000
#     print("milliseconds",time_apriori)
#     print("seconds",time_apriori/1000)
#     print("minutes",time_apriori/60000)
#     current, peak = tracemalloc.get_traced_memory()
#     print(f"Current memory usage is {current / 10 ** 6}MB; Peak was {peak / 10 ** 6}MB")
#     tracemalloc.stop()
#     print(len(apriori()))
