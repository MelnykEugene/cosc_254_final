#wrapper class for our itemset lists. Keeping support information local is invaluable for more complicated algos
class ItemSet:
    itemset = []
    support = 0

    def __init__(self, itemset):
        self.itemset = itemset

    def inc_support(self):
        self.support += 1

    #allows to print this class
    def __str__(self):
        return str((self.itemset, self.support))

    #allows to properly print lists of our custom class
    def __repr__(self):
        return str(self)
