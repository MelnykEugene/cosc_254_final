# cosc_254_final

Usage format:

    cd cs_254_final
    python3 algorithms/apriori.py (str)dataset_filename (int)minsup
    python3 algorithms/hash_apriori.py dataset_filename (int)minsup (float 0<x<=1) branch_fraction
    python3 algorithms/eclat.py dataset_filename minsup
    python3 algorithms/dEclat.py dataset_filename minsup

ToDo's:

Minsup thresholds that don't result in no frequent itemsets of lenth >=3 are not meaningful. Edit our graphs accordingly?

edit ux and add usage examples for eclat/declat
