class ItemSet:
    itemset = []
    support = 0

    def __init__(self, itemset):
        self.itemset = itemset

    def inc_support(self):
        self.support += 1

    def __str__(self):
        return str(self.itemset)