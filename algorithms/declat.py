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
#A Dictionary to hold the Vertical data set
DataStructure = OrderedDict()
#A dictionary to hold the unions that are frequent
DataStructureLoop = OrderedDict()
#Counter for transactions
TransactionCount = 0;
#temporary minimum support
minsup = 2
#converting a horizontal dataset to a vertical
with open("datasets/input.dat", "rt") as file:
    #For each transaction
    for transaction in file:
        #Increment Transaction count
        TransactionCount += 1;
        #for each item in the transaction
        x = transaction.split()
        x.pop()
        for item in x:
            #if it already exists in the dictionary, add the transaction number to the existing set
            if item in DataStructure:
                DataStructure[item].add(TransactionCount)
            #if it doesn't, make a new set with the current transaction number
            else:
                DataStructure[item] = {TransactionCount}
#printing the vertical dataset
print(DataStructure)
#avoid duplicates logic counter
index = 0;
#for the an item in the dataset
for x in DataStructure:
    #avoid duplicates logic counter
    count = 0
    #for another item in the dataset
    for y in DataStructure:
        #looking for the index to target - y>x
        targetIndex = index+1
        #if we aren't at the right index, continue
        if(count<targetIndex):
            count+=1
            continue
        #finding the union of the two sets
        tempSet = DataStructure[x].intersection(DataStructure[y])
        #if the support is larger than the min sup
        if(len(tempSet)>=minsup):
            #it is frequent and we add to the frequent dictionary
            DataStructureLoop[x + " " + y] = tempSet
    #incrementing logic counter
    index += 1
#printing frequent items of k = 2
print(DataStructureLoop)
