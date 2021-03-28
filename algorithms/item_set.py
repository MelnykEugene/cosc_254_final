class ItemSet:
    itemset = []
    support = 0

    def __init__(self, itemset):
        self.itemset = itemset

    def inc_support(self):
        self.support += 1

    def __str__(self):
        return str(self.itemset)

class HashTree:
    h=40
    itemset_size=0
    population=0
    InternalNode root

    def __init__(self,itemset_size,h):
        self.itemset_size=itemset_size
        self.h=h
        root = InternalNode()



class LeafNode:

class InternalNode:
