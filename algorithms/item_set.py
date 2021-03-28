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
    root=None

    def __init__(self,itemset_size,h):
        self.itemset_size=itemset_size
        self.h=h
        root = InternalNode
        last_inserted = None

    def update_supports(self,transaction):



class LeafNode:
    candidates=None
    def __init__(self):
        candidates=[]

class InteriorNode:
    childs=None
    def __init__(self):
        childs=[]