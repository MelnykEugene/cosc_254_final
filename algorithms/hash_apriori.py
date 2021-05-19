import sys
import collections
from item_set import ItemSet
from hash_tree import HashTree
import os

dataset = sys.argv[1]
dataset = './datasets/'+dataset
print('dataset:' + dataset)
minsup = int(sys.argv[2])  # absolute
print('minsup: ' + str(minsup))

#determines the out-degree of internal nodes in our tree. the degree will be |itemset_alphabet|*branch_fraction
#so that branch_fraction=1 corresponds precisely to full trie on our itemset alphabet
branch_fraction = float(sys.argv[3])


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

    #flag as to wether we have a max-width tree (i.e trie) or not
    full_tree=False
    branch_factor=int(max_item*branch_fraction)
    if branch_fraction==1:
        full_tree=True

    if verbose: 
        print('branch factor set to ' + str(branch_factor))
        if full_tree:
            print('branch fraction = 1, using optimized candidate generation...')
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
            candidates_tree_kp1 = get_candidates_2(frequent_tree_k,branch_factor)
        else:
            candidates_tree_kp1 = get_candidates_kp1_router(frequent_tree_k, branch_factor, full_tree)
        
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

    write_to_file(frequent_itemsets,dataset,minsup,branch_fraction)
    return frequent_itemsets


# generates candidates of length 2 in simple way
def get_candidates_2(frequent_items,branch_factor):
    candidate_tree = HashTree(2, branch_factor)
    for i in range(len(frequent_items)):
        for j in range(i + 1, len(frequent_items)):
            candidate_tree.insert_candidate(ItemSet([frequent_items[i], frequent_items[j]]))
    return candidate_tree

# router function to decide which mode of generation to use
def get_candidates_kp1_router(hashtree_k,branch_factor,full_tree):
    if full_tree: return get_candidates_kp1_full_tree(hashtree_k,branch_factor)
    else: return get_candidates_kp1(hashtree_k,branch_factor)

# generates candidates of length k+1
# using the union of candidates of length k that share first k-1 items (like normal apriori)
# leveraging lexicographic order and the fact that candidates sharing the first k-1 items live in the same leaf
def get_candidates_kp1_full_tree(hashtree_k,branch_factor):
    k = hashtree_k.itemset_size
    candidate_hashtree_kp1 = HashTree(k + 1, branch_factor)

    #follow the leaf nodes and join itemsets within the same leaf
    node = hashtree_k.last_leaf
    while node is not None:
        for i in range(len(node.itemsets)):
            itemset1 = node.itemsets[i]
            for j in range(i + 1, len(node.itemsets)):
                itemset2 = node.itemsets[j]

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
                    candidate_hashtree_kp1.insert_candidate(ItemSet(candidate))

        node = node.next_leaf

    return candidate_hashtree_kp1

def get_candidates_kp1(hashtree_k,branch_factor):
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
                candidate_hashtree_kp1.insert_candidate(ItemSet(candidate))

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

def write_to_file(frequent_itemsets,dataset,minsup,branch_fraction):
    input_file = dataset.split('/')[-1]
    output = './output/hash_apriori_' + input_file + '_' + str(minsup) + '_' + 'br:'+ str(branch_fraction)+'.txt'

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
    


#aprioris = apriori()
#hashes=hash_apriori()
# print(hash_apriori())
if __name__=='__main__':
    print('Hash-Tree-Apriori')
    print('found ' + str(len(hash_apriori(branch_fraction))) + ' frequent itemsets, check output directory')

#aprioris=apriori()
#hashes=hash_apriori()
#print('difference in output: '+str([x for x in aprioris if x not in hashes] + [x for x in hashes if x not in aprioris]))

