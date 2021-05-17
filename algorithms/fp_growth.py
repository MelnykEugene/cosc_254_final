from csv import reader
import sys

class fp_node:
    '''
    Create a Node class to act as a node in the FP-tree
    takes in an item, holds a count for the itemset that is made
    by the path from the root to itself
    '''

    #node created with item value, support count and parent node
    # a node keeps track of the next node with same item in the tree in another path and its children
    def __init__(self, item : str, support : int, parent):
        self.item = item
        self.support = support
        self.parent = parent
        self.children = {}
        self.next = None
    # increase the count
    def increase_count (self, count):
        self.support += count




def fp_growth(similar_holder : dict, minimum_support : int, suffix : set, freq_items : list): #doesn't return anything, adds to freq_items

    #takes item from previous fp-tree
    items_on_path = []
    for item in similar_holder.keys():
        items_on_path.append(item)
    # for each item on an fp tree
    for item in items_on_path:
        frequent = set()
        frequent.add(item)
        # create a set of current item and the suffix made from previous recursive run
        frequent = frequent.union(suffix)
        item_node = similar_holder[item]
        #count in an fp tree represents the frequency of that path from the root which corresponds to an itemset
        count = item_node.support
        #append to the list taken in as a parameter the itemset and its support
        freq_items.append((frequent, count))

        prefix_paths = []
        frequency = []
        #go through each occurence of item i and find the paths to the root
        while item_node != None:
            path = []
            #find path to root
            ascend_tree(item_node, path)
            if len(path) > 0:
                #appends that path except the item its self to list which will be the basis to create conditional fp_trees
                prefix_paths.append(path[1:])
                frequency.append(item_node.support)
            item_node = item_node.next
        #using frequency and paths as a list create conditional fp_tree
        ith_tree, new_holder = make_conditional_prefix_tree(prefix_paths, frequency, minimum_support)
        #while fp tree is able to be generated meaning there is at least a node in the holder for head pointers
        if new_holder != None:
            fp_growth(new_holder, minimum_support, frequent, freq_items)

#method to go up path to the root
def ascend_tree(node, path):
    if node.parent != None:
        path.append(node.item)
        ascend_tree(node.parent, path)



def make_conditional_prefix_tree(transactions : list, freq_array : list, minimum_support : int):  #return fp_node, dict
    '''
    Create conditional FpTree from previous paths:
        Args:
            transactions : list
            freq_array : list
            minimum_support: int
        Returns:
            Fp tree
            dictionary of items with head node for each item
    '''

    temp_holder = {}
    freq_index = 0
    for transaction in transactions:
        for item in transaction:

            if item in temp_holder:
                temp_holder[item] += freq_array[freq_index]
            else:
                temp_holder[item] = freq_array[freq_index]
        freq_index += 1

    #infrequent items should be removed from the dictionary
    #holder = {k: v for k, v in temp_holder.items() if v >= minimum_support}
    holder = dict((item, sup) for item, sup in temp_holder.items() if sup >= minimum_support)

    if len(holder) > 0:
        # similar item holder whose value are initialized as none
        similar_holder = {}
        # now ready to create the FP tree
        fp_tree = fp_node('Root', 1, None)
        freq_index = 0
        for transaction in transactions:
            #need to sort each transaction based on frequency and remove items which are not frequent, anti-monotonicyty lets us do that
            transaction = [item for item in transaction if item in holder]
            transaction.sort(key=lambda x: holder[x], reverse=True)
            current = fp_tree
            #start at the root
            for x in transaction:
                #if the item is already on the path we are in
                if x in current.children:
                    current.children[x].increase_count(freq_array[freq_index])
                else: #if new occurence create a new node
                    new_node = fp_node(x, freq_array[freq_index], current)
                    current.children[x] = new_node
                    #make a link in the similar items holder
                    if x in similar_holder:
                        temp_node = similar_holder[x]
                        while temp_node.next != None:
                            temp_node = temp_node.next
                        temp_node.next = new_node
                    else:
                        similar_holder[x] = new_node
                #change current node to the node that was changed or added and loop continues for each item
                current = current.children[x]
            freq_index += 1
        return fp_tree, similar_holder

    else:
        return None, None

def make_fp_tree(file_path : str, minimum_support: int):
    '''
    Create FpTree from transactions:
        Args:
            file_path: str
            minimum_support: int
        Returns:
            Fp tree
            dictionary of items with head node for each item
    '''
    transactions = []

    data = open(file_path, 'r')
    data_reader = reader(data)
    for line in data_reader:
        # break down each transaction into a list of the item
        for item in line:
            line = item.split()
        transactions.append(line)

    # now creating a dictionary to calculate the support of each item
    temp_holder = {}
    for transaction in transactions:
        #print(transaction)
        for item in transaction:
            #   print(item)
            if item in temp_holder:
                temp_holder[item] += 1
            else:
                temp_holder[item] = 1

    # infrequent items should be removed from the dictionary
    holder = dict((item, sup) for item, sup in temp_holder.items() if sup >= minimum_support)

    if len(holder) > 0:
        # similar item holder whose value are initialized as none

        similar_holder = {}

        #Now ready to create the FP tree
        fp_tree = fp_node('Root', 1, None)
        for transaction in transactions:
            #need to sort each transaction based on frequency and remove items which are not frequent, anti-monotonicyty lets us do that
            transaction = [item for item in transaction if item in holder]
            transaction.sort(key=lambda x: holder[x], reverse=True)
            current = fp_tree
            #start at the root
            for x in transaction:
                #if the item is already on the path we are in
                if x in current.children:
                    current.children[x].increase_count(1)
                else: #if new occurence create a new node
                    new_node = fp_node(x, 1 ,current)
                    current.children[x] = new_node
                    #make a link in the similar items holder
                    if x in similar_holder:
                        temp_node = similar_holder[x]
                        while temp_node.next != None:
                            temp_node = temp_node.next
                        temp_node.next = new_node
                    else:
                        similar_holder[x] = new_node
                #change current node to the node that was changed or added and loop continues for each item
                current = current.children[x]
        return fp_tree, similar_holder

    else:
        return None, None

if __name__ == '__main__':
    file = 'newacc.txt'
    min_sup = 1500
    fp_tree, holder = make_fp_tree(file, min_sup)
    frequent_items = []

    fp_growth(holder, min_sup, set(), frequent_items)
    print(len(frequent_items))
