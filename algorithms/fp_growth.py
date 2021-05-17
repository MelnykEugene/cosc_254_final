from collections import OrderedDict
import csv


"""Defining the structure of the FP-Tree Node and a method to print it in a
nested list format."""
class fpTreeNode:
    def __init__(self, name, freq, parent):
        self.name = name # contains the name of the item
        self.freq = freq # contains frequency of the item in the dataset
        self.parent = parent # contains the parent node
        self.child = OrderedDict() # contains all the children node information
        self.link = None # for linking to nodes with same name
       

"""The most recent node is linked to the previous node with same name."""
def similar_item_table_update(similar_item, present_node):
    # Traversing 
    while (similar_item.link != None):
        similar_item = similar_item.link
    similar_item.link = present_node


"""This function takes the input dataset and scans it once to create the
frequent item dictionary. Once that is created, it deletes any value in the
dictionary which is below the threshold."""
def fp_tree_preprocess(doc_name, threshold):
    support_count = {}
    transactions_list = []
    with open(doc_name, 'r') as f:
        for line in f:
            transaction = line.split()
            transactions_list.append(transaction)
            for item in transaction:
                if item not in support_count:  
                    support_count[item]= 1
                else:
                    support_count[item]+=1
                    
    # Removing items whcih are below the given support value
    item_freq = {k:v for k,v in support_count.items() if v >= threshold}
    return transactions_list, item_freq


"""This function scans the database for the second time.
After deleting items with low threshold value, it orders the items in a given 
transaction.
The ordered transaction is then sent to the FP-Tree creating function."""
def fp_tree_reorder(data, item_freq):
    root = fpTreeNode('Root',1,None)
    #Sort the frequent item dictionary based on the frequency of the items
    #If two items have the same frequency, the keys are arranged alphabetically
    sorted_item_freq = sorted(item_freq.items(), key=lambda x: (-x[1],x[0]))
    # The similar item table is also created with all the frequent items.
    sorted_keys = []
    similar_item_dict = {}
    for key in sorted_item_freq:
        similar_item_dict[key[0]] = None # Initially all the values are 'None'
        sorted_keys.append(key[0]) # A list of the sorted item structure
    # 2nd scan of the database.
    for row in data:
        # Deletes any item whose frequency is not above the minimum support
        trans = []
        for col in row:
            if col in item_freq:
                trans.append(col)
        # Orders the items in a transaction based on its frequency.
        ordered_trans = []
        for item in sorted_keys:
            if item in trans:
                ordered_trans.append(item)
        # Once ordered, the transaction is sent to be updated in the FP-Tree
        if len(ordered_trans)!= 0:
            fp_tree_create_and_update(root, ordered_trans, similar_item_dict)
    return root, similar_item_dict


"""This function recursively creates the FP-Tree for each transaction."""
def fp_tree_create_and_update(init_node, trans, similar_item_dict):
    # If the child is already present, increment its count
    if trans[0] in init_node.child:
        init_node.child[trans[0]].freq += 1
    # Else, create a new node for the child and link it to its parent
    else:
        init_node.child[trans[0]] = fpTreeNode(trans[0], 1, init_node)
        # For every newly created node, the Similar-Item table is updated
        if similar_item_dict[trans[0]] == None:
            # For the 1st node, replace the 'None' value with the node
            similar_item_dict[trans[0]] = init_node.child[trans[0]]
        else:
            # Traverse till the last similar node, and update the new node
            similar_item_table_update(similar_item_dict[trans[0]],\
                                      init_node.child[trans[0]])
    # The function is recursively called for every item in a transaction
    if len(trans) > 1:
        fp_tree_create_and_update(init_node.child[trans[0]], trans[1::],\
                                  similar_item_dict)


"""Function to create the conditional FP-Tree for every frequent occuring item
in the main FP-Tree.
The function works exactly similar to the fp_tree_create_and_update() function,
except here the similar-item table is not updated"""
def conditional_fptree(name,init_node,data):
    if data[0][0] == name:
        # Skip the conditional tree if no extra frequent items are occuring
        if len(data)>1:
            conditional_fptree(name,init_node,data[1::])
    if data[0][0] != name:
        # If the item is present as a child, increment its count
        if data[0][0] in init_node.child:
            init_node.child[data[0][0]].freq += data[0][1]
        # Else, create a new child node and update its frequency
        else:
            init_node.child[data[0][0]] = fpTreeNode(data[0][0],data[0][1],\
                           init_node)
        # Continue to recursively create the conditional FP-Tree for each item
        if len(data) >1:
            conditional_fptree(name,init_node.child[data[0][0]],data[1::])

"""Function to create the conditional FP-Tree for every time present in the
Similar-Item Table.
Each freqently occuring itemset above the threshold is also considered frequent
"""
def FPGrowth(similar_item_dict, threshold):
    final_cond_base = []
    # Go through every key-value pair present in the Similar-Item Table
    for key,value in similar_item_dict.items():
        final_cond_base_key = []
        condition_base = []
        leaf_item_freq = OrderedDict()
        # Within each key, traverse through every linked node value till end
        while value != None:
            path = []
            leaf_node = value
            leaf_freq = value.freq
            #Within each node, traverse till the parent node and append details
            while leaf_node.parent != None:
                leaf_details = [leaf_node.name, leaf_freq]
                path.append(leaf_details) # append the name and value
                leaf_node = leaf_node.parent # Go to the parent of that node
            # Insert the whole path to condition_base
            condition_base.insert(0,path)
            # Once the  particular node is finished, increment to value.link
            # Then you can traverse for the next same-name node
            value = value.link
        # A frequent item-set dictionary is created for every leaf node
        for row in condition_base:
            for col in row:
                if col[0] not in leaf_item_freq:
                    leaf_item_freq[col[0]] = col[1]
                else:
                    leaf_item_freq[col[0]] += col[1]
        #Items below threshold are removed before creating the conditional base
        leaf_item_freq = {k:v for k,v in leaf_item_freq.items() \
                          if v >= threshold}
        # For every transaction in the condition_base, the items are stored
        for row in condition_base:
            temp = []
            temp_tree = []
            for col in row:
                if col[0] in leaf_item_freq:
                    temp.append(col[0]) # stores only the name of the item
                    temp_tree.append(col) # stores both name and frequency
            #Contains all the frequent items for a particular conditional leaf
            final_cond_base.append(temp)
            final_cond_base_key.append(temp_tree)
        cond_leaf = key
        cond_root = fpTreeNode('Null Set',1,None)
        # Creates the conditional tree from the above conditonal pattern base
        for row in final_cond_base_key:
            conditional_fptree(cond_leaf,cond_root,row)


# Required User Inputs
support = 2000
file_name = 'newacc.txt'

# Function calling in the main program to implement FP Growth algorithm
dataset, freq_items = fp_tree_preprocess(file_name, support)
fptree_root, header_table = fp_tree_reorder(dataset, freq_items)
FPGrowth(header_table,support)
