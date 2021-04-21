import tracemalloc
from collections import OrderedDict
import timeit
import sys

# give filename in argument
filename = sys.argv[1]
minsup = int(sys.argv[2])
#dict to hold initial tids
tidSets = {}
#dict to hold supp and diffsets
diffSets = {}
trans_set = set()


#function to make the layout vertical
def vertical_layout(filename):
    freq_1_items = []
    trans_num = 0
    with open(filename, "rt") as file:
        for transaction in file:
            trans_num +=1
            #replace part helps when the data has commas in it, likt the TK dataset
            for item in transaction.replace(",", " ").split():
                #if item already exists in our set of tids, add the new transaction to its set,
                # otherwise start its set with this transaction
                if item in tidSets:
                    tidSets[item].add(trans_num)
                else:
                    tidSets[item] = {trans_num}
    
    #creating a set containing all possible tids (will help with calculating diffsets of first 1-length itemsets)                
    for tid in range(1, trans_num +1):
        trans_set.add(tid)
    
    #for every 1-itemset in tidSets, find its supp, and if supp > minsup
    #add its sup plus its diffset to diffSets by finding the difference between its tidset and the overall tidset
    #not sure how optimized this is, could possibly optimize it better but I cannot think of another way of 
    #finding diffsets for the intitial 1-itemsets              
    for key,value in tidSets.items():
        supp = len(value)
        if supp >= minsup:
            freq_1_items.append(key)
            diffSets[key] = [supp, trans_set.difference(value)]
            
    '''print(freq_1_items)  '''
    #will maintain order
    freq_1_items.sort(key=int)    
    #print(freq_1_items)
    return freq_1_items


def dEclat(prev_freq):
    new_freq = []
    #for all possible itemsets in the prev_freq
    for i in range (0,len(prev_freq)):
        # get the item
        item1 = prev_freq[i]
        #make it to a list
        i1_list = item1.split()
        for j in range (i+1,len(prev_freq)):
            #do the same for every item2 starting after our item1
            item2 = prev_freq[j]
            i2_list = item2.split()
            #check whether they share the same prefix (check everything in the two lists except the last element)
            #AND also check that the last elements in both lists are different
            #we don't want to join two same itemsets
            #however, I am not sure if we really need the second condition
            if i1_list[:-1] == i2_list[:-1] and i1_list[-1] != i2_list[-1]:
                #calculate the diffset of the union
                union_diffset = diffSets[item2][1].difference(diffSets[item1][1])
                #calculate the min_supp using the cardinality of the diffset
                union_supp = diffSets[item1][0] - len(union_diffset)
                if union_supp >= minsup:
                    #if supp >= minsup, add it to the diffSet as a key
                    #with two parameters for value: the unions support and the union's diffset
                    diffSets[item1 + " " + i2_list[-1]] =[union_supp,union_diffset]
                    #also add the union to our list of new_freq for the next iteration
                    new_freq.append(item1 + " " + i2_list[-1])

    #if new_freq has itemsets in it, run dEclat again
    if len(new_freq) > 0:
        dEclat(new_freq)

#method to calculate time
def wrapper(func, *args, **kwargs):
    def wrapped():
        return func(*args, **kwargs)
    return wrapped

if __name__ == '__main__':
    print("dEclat")
    tracemalloc.start()
    into = vertical_layout(filename)
    wrappedE = wrapper(dEclat, into)
    time_eclat = timeit.timeit(wrappedE, number=1)*1000
    print("number of freq itemsets: ",len(diffSets))
    print("time in millisecond",time_eclat)
    print("time in second",time_eclat/1000)
    print("time in min",time_eclat/60000)
    current, peak = tracemalloc.get_traced_memory()
    print(f"Current memory usage is {current / 10 ** 6}MB; Peak was {peak / 10 ** 6}MB")
    tracemalloc.stop()