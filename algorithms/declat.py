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


