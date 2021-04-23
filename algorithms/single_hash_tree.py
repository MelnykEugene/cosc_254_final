from item_set import ItemSet

class Node:
    itemsets = None
    next_leaf = None
    childs = None

    def __init__(self, h):
        self.itemsets = []
        self.childs = [None] * h


class HashTree:
    h = None
    last_leaf = None
    height=None
    population=0
    nleaf_nodes=0

    def __init__(self, h,pairs):
        self.h = h
        self.root = Node(h)
        self.height=1
        for itemset in pairs:
            node1 = self.root.childs[itemset.itemset[0]]
            if node1 is None: 
                node1=Node(self.h)
                node1.next_leaf=self.last_leaf
                self.last_leaf=node1
                self.root.childs[itemset.itemset[0]]=node1
            node1.itemsets.append(itemset)
        print('initialalized tree of frequent pairs')
                
    def next_tree(self):
        print('extending tree to height '+str(self.height+1))

        self.population=0
        node = self.last_leaf
        new_last_leaf=None

        while node is not None:
            for i in range(len(node.itemsets)):
                itemset1 = node.itemsets[i]
                for j in range(i + 1, len(node.itemsets)):
                    itemset2 = node.itemsets[j]
                    if itemset1.itemset[-1] < itemset2.itemset[-1]:
                        candidate = []
                        candidate.extend(itemset1.itemset)
                        candidate.append(itemset2.itemset[-1])
                    else:
                        continue
                    if self.check_frequency_of_all_immediate_subsets(candidate):
                        direction = itemset1.itemset[-1] % self.h
                        if node.childs[direction] is None:
                            new_node = Node(self.h)
                            new_node.next_leaf=new_last_leaf
                            new_last_leaf=new_node
                        new_node.itemsets.append(ItemSet(candidate))
                        node.childs[direction]=new_node
                        self.population+=1
                        
            node = node.next_leaf
        self.last_leaf=new_last_leaf
        self.height+=1
        return self.population

    def lookup(self, candidate):
        k = 0
        current_node = self.root
        while k < len(candidate) - 1:
            direction = candidate[k] % self.h
            next_node = current_node.childs[direction]
            if next_node is None:
                return False
            current_node = next_node
            k += 1

        leaf_itemsets_last_items = [x.itemset[-1]
                                    for x in current_node.itemsets]
        return candidate[-1] in leaf_itemsets_last_items

    def check_frequency_of_all_immediate_subsets(self,candidate_kp1):
        for i in range(0, len(candidate_kp1)):
            subset = candidate_kp1[0:i] + candidate_kp1[i + 1::]
            if not self.lookup(subset):
                return False
        return True

    def update_supports(self, transaction):
        self.update(self.root, transaction, 0, list())

    def update(self, node, transaction, first_position, fixed):
        last_possible_path = len(transaction) - (self.height+1) + len(fixed)
        for i in range(first_position, last_possible_path + 1):
            direction = transaction[i] % self.h
            next_node = node.childs[direction]

            new_fixed = fixed.copy()
            new_fixed.append(transaction[i])

            if next_node is None:
                continue

            if len(new_fixed)<self.height:
                self.update(next_node, transaction, i + 1, new_fixed)
            else:
                for j in range(i + 1, len(transaction)):
                    new_new_fixed = new_fixed.copy()
                    new_new_fixed.append(transaction[j])
                    for itemset in next_node.itemsets:
                        if new_new_fixed == itemset.itemset:
                            itemset.inc_support()
