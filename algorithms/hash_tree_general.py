#leaf nodes of the tree store the itemsets
#we also keep them in a linked list for easy access
class LeafNode:
    itemsets = None
    next_leaf = None

    def __init__(self):
        self.itemsets = []

#interior nodes of the tree serve as hashtables that route the traversal of the tree based on the hash of the current item
class InteriorNode:
    childs = None

    def __init__(self, h):
        self.childs = [None] * h


class HashTree:
    # branching factor
    h = None

    #the tree has to know the itemset size, which determines its depth
    itemset_size = 0
    population = 0
    root = None
    #counting leaf nodes for debug
    leaf_nodes = 0

    # for convenience, we chain all of the leaf nodes in a reverse linked list. this is a reference to the last link
    last_leaf = None

    def __init__(self, itemset_size, h):
        self.itemset_size = itemset_size
        # print('created tree with notional itemset size '+str(itemset_size))
        self.h = h
        self.root = InteriorNode(h)

    # entry-point method for populating the hashtree
    def insert_candidate(self, candidate, verbose=False):
        self.insert(self.root, candidate, 0, verbose)
        self.population += 1

    # recursive search for the right place to insert
    # k = current level in three
    # current_node = the starting node for a given branch of recursion
    def insert(self, current_node, itemset, k, verbose):

        #if leaf node has been reached, we insert the itemset here
        if isinstance(current_node, LeafNode):
            if verbose: print('inserting ' + str(itemset) + ' into leaf with ' + str(current_node.itemsets))
            current_node.itemsets.append(itemset)
        
        #else we need to search further
        else:
            #the "hash function" is the identity
            direction = itemset.itemset[k] % self.h
            next_node = current_node.childs[direction]
            # if next node doesn't exist, we either make it interior or leaf depending on current depth k
            if next_node is None: 
                if k == (len(itemset.itemset) - 2):  # if this is true then the next node must be a leaf
                    next_node = LeafNode()
                    self.leaf_nodes += 1

                    if verbose: print('created leaf node expecting to insert' + str(itemset))
                    # set the new node to the head of linked of leaf nodes and point to the previous last added node
                    next_node.next_leaf = self.last_leaf
                    self.last_leaf = next_node
                else:
                    if verbose: print('inserted interior node at level ' + str(k + 1))
                    next_node = InteriorNode(self.h)
                # make the current node properly point to the new node
                current_node.childs[direction] = next_node

            # if the next node does exist (or was just created), simply advance the recursion
            self.insert(next_node, itemset, k + 1, verbose)

    #tells whether the candidate is in the hashtree. 
    def lookup(self, candidate):
        k = 0
        current_node = self.root
        # for the itemset to be in the tree, there must be a path of length exactly len(itemset)
        # that ends in a leaf node containing the itemset
        while k < len(candidate) - 1:
            direction = candidate[k] % self.h
            next_node = current_node.childs[direction]
            if next_node is None:
                return False
            current_node = next_node
            k += 1

        # assert isinstance(current_node,LeafNode)
        # all of the items in a leaf share all the items except for the last.
        # therefore we can search for our candidate based on the last item only and leverage binary search
        leaf_itemsets_last_items = [x.itemset[-1] for x in current_node.itemsets]
        return candidate[-1] in leaf_itemsets_last_items

    # given a transaction, increases the support of all itemsets in the tree contained in the transcation
    # entry-point for recursion
    def update_supports(self, transaction):
        self.update(self.root, transaction, 0, list())

    # recursive call
    # http://www.cs.uoi.gr/~tsap/teaching/2012f-cs059/material/datamining-lect3.pdf
    # the link kinda explains what is going on (slides 43-44).
    # the fixed variable stores the prefix of the transaction that we've "fixed" so far
    def update(self, node, transaction, first_position, fixed):
        last_possible_path = len(transaction) - self.itemset_size + len(fixed)
        for i in range(first_position, last_possible_path + 1):
            direction = transaction[i] % self.h
            next_node = node.childs[direction]

            new_fixed = fixed.copy()
            new_fixed.append(transaction[i])

            if next_node is None:
                continue

            if isinstance(next_node, InteriorNode):
                self.update(next_node, transaction, i + 1, new_fixed)

            else:
                # assert isinstance(next_node,LeafNode)
                # print('update() arrived at leaf node with candidates' + str(next_node.itemsets))
                # print('meanwhile fixed is '+str(new_fixed))
                for j in range(i + 1, len(transaction)):
                    new_new_fixed=new_fixed.copy()
                    new_new_fixed.append(transaction[j])
                    for itemset in next_node.itemsets:
                        if new_new_fixed==itemset.itemset:
                            itemset.inc_support()


    def get_candidate_count(self):
        return self.population
