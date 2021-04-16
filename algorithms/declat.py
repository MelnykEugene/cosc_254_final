# Change from a horiz to a vertical
#
#
# dEclat(a set of class members for a subtree rooted at P)
# For loop for an itemset i in P
# Nested For loop for another itemset j (with j > i)in P
# Set R is equal to the union of both itemsets
# Compute the diffset of R by subtracting the diffset of j from the diffset of i
# If the support of R is greater than or equal to the min support threshold
# 	Transaction dataset of i is equal to the union of the transaction dataset (initially
# empty) and R
# For every transaction dataset of i that isn’t empty, do dEclat(transaction dataset of i)

from collections import OrderedDict

FinalDataStructure = OrderedDict()

def setup():
    # A Dictionary to hold the Vertical data set
    DataStructure = OrderedDict()
    FrequentItems = OrderedDict()
    # Counter for transactions
    TransactionCount = 0;
    minsup = 7000
    with open("datasets/mushroom.dat", "rt") as file:
        # For each transaction
        for transaction in file:
            # Increment Transaction count
            TransactionCount += 1;
            # for each item in the transaction
            x = transaction.split()
            for item in x:
                # if it already exists in the dictionary, add the transaction number to the existing set
                if item in DataStructure:
                    DataStructure[item].add(TransactionCount)
                # if it doesn't, make a new set with the current transaction number
                else:
                    DataStructure[item] = {TransactionCount}
    # printing the vertical dataset
    for x in DataStructure:
        # print(x +  " ", DataStructure[x])
        if len(DataStructure[x]) >= minsup:
            FrequentItems[x] = DataStructure.get(x)
            FinalDataStructure[x] = DataStructure.get(x)
    # print(FrequentItems)
    return FrequentItems
def eclat(DataStructure):
    # temporary minimum support
    minsup = 7000
    # avoid duplicates logic counter
    index = 0;

    DataStructureLoop = OrderedDict()
    # for the an item in the dataset
    # print(DataStructure)
    for x in DataStructure:
        # print("x",x)
        # avoid duplicates logic counter
        count = 0
        # for another item in the dataset
        for y in DataStructure:
            # print("y" ,y)
            # looking for the index to target - y>x
            targetIndex = index + 1
            # if we aren't at the right index, continue
            if (count < targetIndex):
                count += 1
                continue
            # finding the union of the two sets
            tempSet = DataStructure[x].intersection(DataStructure[y])
            # print(tempSet)
            # if the support is larger than the min sup
            if (len(tempSet) >= minsup):
                # it is frequent and we add to the frequent dictionary
                a = set()
                b = set()
                for it in x.split(" "):
                    a.add(it)
                for it in y.split(" "):
                    b.add(it)
                c = b.union(a)
                nextStr = []
                for it2 in c:
                    nextStr += it2
                nextStr.sort()
                nextStr2 = ""
                for it3 in nextStr:
                    nextStr2 += it3
                    nextStr2 += " "
                DataStructureLoop[nextStr2[:-1]] = tempSet
                FinalDataStructure[nextStr2[:-1]] = tempSet
        # incrementing logic counter
        index += 1
    # print(DataStructureLoop)
    if len(DataStructureLoop) > 0:
        eclat(DataStructureLoop)
if __name__ == '__main__':
    print("declat")
    eclat(setup())
    print(FinalDataStructure.keys())
