# cosc_254_final

Usage format:

	cd cs_254_final
	python3 algorithms/apriori.py (str)dataset_filename (int)minsup
	python3 algorithms/\_hashapriori.py dataset_filename (int)minsup (float 0<x<=1) branch_fraction
	python3 algorithms/\eclat.py dataset_filename (int)minsup 
	python3 algorithms/\dEclat.py dataset_filename (int)minsup 
	
ToDo's:
update hashapriori description, mention the fact that leafs are linked into a list.
evaluating runtime of hashapriori as a function of branhcing factor

Minsup thresholds that don't result in no frequent itemsets of lenth >=3 are not meaningful. Edit our graphs accordingly?

edit ux and add usage examples for eclat/declat

Note\*
All algorithms have an argument for minsup, that is prrovided by the user when they are run. dEclat has an argument for dataset pathname and minsu, in that order.
