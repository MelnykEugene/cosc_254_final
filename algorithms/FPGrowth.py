from collections import *

class Tree:
    def __init__(self, data):
        self.children = []
        self.data = data


if __name__ == '__main__':
    TransactionCount = 0
    Transactions = OrderedDict()
    Counts = {}
    with open("datasets/mushroom.dat", "rt") as file:
        # For each transaction
        for transaction in file:
            # Increment Transaction count
            TransactionCount += 1
            # for each item in the transaction
            x = transaction.split()
            for item in x:
                if TransactionCount in Transactions:
                    Transactions[TransactionCount].add(item)
                # if it doesn't, make a new set with the current transaction number
                else:
                    Transactions[TransactionCount] = {item}
                # if it already exists in the dictionary, add the transaction number to the existing set
                if item in Counts:
                    Counts[item] += 1
                # if it doesn't, make a new set with the current transaction number
                else:
                    Counts[item] = 1
            TransactionCount += 1
    sortedKeys = sorted(Counts, key=lambda x: (-Counts[x], x))
    # print(Counts)
    # print(Transactions)



