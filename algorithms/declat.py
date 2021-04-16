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


if __name__ == '__main__':
    print("declat")
from collections import OrderedDict
import sys
#A Dictionary to hold the
DataStructure = OrderedDict()
DataStructureLoop = OrderedDict()
TransactionCount = 0;
minsup = 2
with open("datasets/input.dat", "rt") as file:
    for transaction in file:
        TransactionCount += 1;
        x = transaction.split()
        x.pop()
        for item in x:
            if item in DataStructure:
                DataStructure[item].add(TransactionCount)
            else:
                DataStructure[item] = {TransactionCount}
print(DataStructure)
index = 0;
for x in DataStructure:
    count = 0
    for y in DataStructure:
        targetIndex = index+1
        if(count<targetIndex):
            count+=1
            continue
        tempSet = DataStructure[x].union(DataStructure[y])
        if(len(tempSet)>minsup):
            DataStructureLoop[x + " " + y] = tempSet
    index += 1
print(DataStructureLoop)
