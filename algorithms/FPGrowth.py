import os
import sys

def process_file(file):
    transactions_list = []
    with open(file, 'r') as f:
        for line in f:
            transaction = line.split()
            transactions_list.append(transaction)
    return transactions_list


class node:
    def __init__(self, item, item_count=0, parent=None, link=None):
        self.item = item
        self.item_count = item_count
        self.parent = parent
        self.link = link
        self.children = {}


# FPTREE class and method
class fptree:
    def __init__(self, data, minsup=400):
        self.data = data
        self.minsup = minsup

        self.root = node(item="Null", item_count=1)

        # each line of transaction with new order from the most frequent items to less
        self.transsort = []
        # node table containing linkedList of paths of the same item
        self.nodetable = []

        # dictionary containing item and the support count
        self.itemdic = {}
        self.sorteditemdic = {}

        # when the fptree class is created, this function is called to create an FP tree of the dataset
        self.constructTree(data)

        # this is the function that builds the fpree

    def constructTree(self, data):
        # get support counts
        for transaction in data:
            for item in transaction:
                if item in self.itemdic.keys():
                    self.itemdic[item] += 1
                else:
                    self.itemdic[item] = 1
        itemlist = list(self.itemdic.keys())

        # filter items with support below minsup
        for item in itemlist:
            if (self.itemdic[item] < self.minsup):
                del self.itemdic[item]

        # sort the remaing items in descending order.
        self.wordsortdic = sorted(self.itemdic.items(), key=lambda x: (-x[1], x[0]))

        # making a nodetable(headertable) that has the items, their counts, and linked list of paths
        t = 0
        for i in self.wordsortdic:
            item = i[0]
            itemc = i[1]
            self.sorteditemdic[item] = t
            t += 1
            iteminfo = {'itemn': item, 'itemcc': itemc, 'linknode': None}
            self.nodetable.append(iteminfo)

        for line in data:
            sup = []
            for col in line:
                # only keep items with support count higher than minsupport
                if col in self.itemdic.keys():
                    sup.append(col)

            if len(sup) > 0:
                sortsup = sorted(sup, key=lambda k: self.sorteditemdic[k])
                self.transsort.append(sortsup)
                R = self.root
                for i in sortsup:
                    if i in R.children.keys():
                        R.children[i].item_count += 1
                        R = R.children[i]
                    else:

                        R.children[i] = node(i, 1, parent=R, link=None)
                        R = R.children[i]

                        # link this node to  the nodetable
                        for iteminfo in self.nodetable:
                            if iteminfo["itemn"] == R.item:

                                # find the last node of the  node linkedlist
                                if iteminfo["linknode"] is None:
                                    iteminfo["linknode"] = R
                                else:
                                    iter_node = iteminfo["linknode"]
                                    while (iter_node.link is not None):
                                        iter_node = iter_node.link
                                    iter_node.link = R

    # create transactions for the conditional tree
    def condtreetran(self, N):
        if N.parent is None:
            return None

        condtreeline = []
        # starting from the leaf node reverse add word till hit root
        while N is not None:
            line = []
            PN = N.parent
            while PN.parent is not None:
                line.append(PN.item)
                PN = PN.parent
            # reverse order the transaction
            line = line[::-1]
            for i in range(N.item_count):
                condtreeline.append(line)
            N = N.link
        return condtreeline

    # Finding frequent itemsets list.
    def findfreqitemsets(self, parentnode=None):
        if len(list(self.root.children.keys())) == 0:
            return []
        result = []
        sup = self.minsup
        # starting from the end of nodetable
        revtable = self.nodetable[::-1]
        for n in revtable:
            fqset = [set(), 0]
            if (parentnode == None):
                fqset[0] = {n['itemn'], }
            else:
                fqset[0] = {n['itemn']}.union(parentnode[0])
            fqset[1] = n['itemcc']
            result.append(fqset)
            condtran = self.condtreetran(n['linknode'])
            # recursively build the conditinal fp tree
            if (len(condtran) > 0):
                contree = fptree(condtran, sup)
                conwords = contree.findfreqitemsets(fqset)
                if conwords is not None:
                    for words in conwords:
                        result.append(words)
        return result


def write_to_file(frequent_itemsets, dataset, minsup):
    input_file = dataset.split('/')[-1]
    output = './output/FPGrowth_' + input_file + '_' + str(minsup) + '.txt'

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
            finalString = ""
            for x in item[0]:
                finalString += x
                finalString += ", "

            f.write('[' + finalString[:-2] + ']' + '   ' + str(item[1])+'\n')

    return output

if __name__ == '__main__':
    print("FPGrowth")
    minsup = int(sys.argv[2])
    transactions_list = process_file("./datasets/" + sys.argv[1])

    fp_tree = fptree(transactions_list, minsup)

    frequentitemset = fp_tree.findfreqitemsets()
    output_name = write_to_file(frequentitemset,sys.argv[1],minsup)
    print("Support: " + str(minsup) + ", Frequent Itemsets: " + str(len(frequentitemset)) + ", Check " + output_name + " for Itemsets")




