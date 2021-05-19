#Not optimized eclat - still need to optimize by doing prefixes

#import statements
from collections import OrderedDict
import sys
import os

#global variables
# a dictionary to hold the all the frequent itemsets
FinalDataStructure = OrderedDict()
# the minimum support to compare against, as a number of transactions
minsup = int(sys.argv[2])

#a function that converts a horizontal dataset to a vertical, as well as finding the frequent items of k = 1
def setup():
    # A Dictionary to hold the Vertical data set
    VertDataSet = OrderedDict()
    # A Dictionary to hold the frequent items of k = 1
    FrequentItems = OrderedDict()
    # Counter for transactions
    TransactionCount = 0
    # Reading in the dataset of interest
    with open(sys.argv[1], "rt") as file:
        # For each transaction
        for transaction in file:
            # Increment Transaction count
            TransactionCount += 1
            # for each item in the transaction
            x = transaction.split()
            for item in x:
                # if it already exists in the dictionary, add the transaction number to the existing set
                if item in VertDataSet:
                    VertDataSet[item].add(TransactionCount)
                # if it doesn't, make a new set with the current transaction number
                else:
                    VertDataSet[item] = {TransactionCount}
    # for every itemset in the vertical dataset
    for x in VertDataSet:
        # print(x +  " ", DataStructure[x])
        # if the support is greater than the minimum support
        if len(VertDataSet[x]) >= minsup:
            # Add the item to the frequent items dictionary
            FrequentItems[x] = VertDataSet.get(x)
            # add the item to the global frequent items dictionary
            FinalDataStructure[x] = VertDataSet.get(x)
    # print(FrequentItems)
    # return the frequent item dictionary
    return FrequentItems

# Eclat function: finds frequent itemsets of k > 1
def eclat(FrequentItemsPrevious):
    # temporary minimum support
    # avoid duplicates logic counter
    index = 0
    # Dictionary for frequent items at the current level of k
    FrequentItemsCurrent = OrderedDict()
    # for an itemset in the previous level of frequent items
    for x in FrequentItemsPrevious:
        # print("x",x)
        # avoid duplicates logic counter
        count = 0
        # for another itemset in the previous level of frequent items
        for y in FrequentItemsPrevious:
            # looking for the index to target - y>x
            targetIndex = index + 1
            # if we aren't at the right index, continue
            if (count < targetIndex):
                count += 1
                continue
            # finding the union of the two sets
            CandidateSet = FrequentItemsPrevious[x].intersection(FrequentItemsPrevious[y])
            # print(len(CandidateSet))
            # if the support is larger than the min sup
            if (len(CandidateSet) >= minsup):
                # String logic to calculate the new key
                # Creating two empty sets
                a = set()
                b = set()
                # Looping through an itemset string to get each individual item
                for it in x.split(" "):
                    # Adding each individual item to a, making a an itemset (SAME AS X, BUT IN ITEMSET INSTEAD OF STRING)
                    a.add(it)
                for it in y.split(" "):
                    # Adding each individual item to b, making b an itemset (SAME AS Y, BUT IN ITEMSET INSTEAD OF STRING)
                    b.add(it)
                # Combining the two itemsets into one
                c = b.union(a)
                # making a blank list to store the next itemset's string
                nextStr = []
                # for every item in itemset c
                for it2 in c:
                    #add it to the list
                    nextStr.append(it2)
                #Sorting it alphabetically
                nextStr.sort()
                #Creating the next string
                nextStr2 = ""
                # Looping through the list to get each item, add it to string to create itemset
                for it3 in nextStr:
                    nextStr2 += it3
                    nextStr2 += " "
                # It is frequent and we add the itemset (minus the weird space at the end) to the current level's dictionary
                FrequentItemsCurrent[nextStr2[:-1]] = CandidateSet
                # We also add the itemset (minus the weird space at the end) to the global frequent itemset dictionary
                FinalDataStructure[nextStr2[:-1]] = CandidateSet
                # print(CandidateSet)
        # incrementing logic counter
        index += 1
    # if there are still frequent items at this level
    if len(FrequentItemsCurrent) > 0:
        # Recursively call it with the frequent itemsets at the current level
        eclat(FrequentItemsCurrent)


def write_to_file(frequent_itemsets, dataset, minsup):
    input_file = dataset.split('/')[-1]
    output = './output/eclat_' + input_file + '_' + str(minsup) + '.txt'

    # https://stackoverflow.com/questions/12517451/automatically-creating-directories-with-file-output
    if not os.path.exists(os.path.dirname(output)):
        try:
            os.makedirs(os.path.dirname(output))
        except OSError as exc:  # Guard against race condition
            if exc.errno != errno.EEXIST:
                raise

    with open(output, 'w') as f:
        f.truncate()
        for item in frequent_itemsets:
            f.write('[' + item + ']' + ' ' + str(len(FinalDataStructure[item])) + '\n')
    return output


if __name__ == '__main__':
    #Just saying what algo we're running
    print("Eclat")
    # Getting the frequent itemsets of size 1 in a vertical format
    FI = setup()
    # Running Eclat
    eclat(FI)
    output_name = write_to_file(FinalDataStructure,sys.argv[1],minsup)
    print(len(FinalDataStructure["34 36 39 86 90"]))
    # printing the final number of frequent itemsets
    print("Support: " + str(minsup) + ", Frequent Itemsets: " + str(len(FinalDataStructure)) + ", Check " + output_name + " for Itemsets")