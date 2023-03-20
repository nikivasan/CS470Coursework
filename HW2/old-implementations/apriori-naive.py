import argparse
from itertools import combinations
import time

def apriori(data, min_sup, output):
    """
    Apriori main function

    Parameters
    ----------
    data: numpy array
        Transaction dataset
    min_sup: int
        Minimum support.
    output : txt
        Output file containing patterns found.
    """

    global_freq_itemsets = list() # final list frequent itemsets
    global_support = dict() # dictionary to store support mapping; key: itemset, value: support

    # generate L1 itemsets and make transcations into lists
    transactions = set()
    itemsets = set()
    for row in data:
        transactions.add(frozenset(row))
        for itemset in row:
            itemsets.add(frozenset([itemset]))
    
    k=1
    while(len(itemsets) != 0):
        start1 = time.time()
        freq_k_sets = list() # local frequent pattern list 
        support_counts = support_mapping(itemsets, transactions, global_support) # get support of k-itemsets 
        for itemset, count in support_counts.items():
            if count >= min_sup:
                freq_k_sets.append(itemset) # keep itemsets that meet minimum support
        global_freq_itemsets.extend(freq_k_sets) # add those itemsets to global list
        itemsets = get_candidates(freq_k_sets, k+1, global_freq_itemsets) # get k+1-candidates 
        print("Iteration ", k, "Num Patterns Found: ", len(freq_k_sets), "Runtime (sec): ", round(time.time()-start1,3))
        k+=1
    
    write_output(output, global_freq_itemsets, global_support)

    return global_freq_itemsets

def get_candidates(itemsets, k, global_freq_itemsets):
    """
    Generate candidate itemsets of length k. 
    """
    candidates = set()
    for i1 in itemsets:
        for i2 in itemsets:
            joined_item = i1.union(i2) # self join itemsets 
            if len(joined_item) == k:
                subsets = list(combinations(joined_item, k-1)) # find all subsets of joined itemset
                if all(len(subset) == k-1 for subset in subsets): 
                    candidates.add(joined_item) # only add candidate itemsets whos subsets are of length k-1  
    return candidates


def support_mapping(candidates, transactions, global_support):
    """
    Get support of each itemset and store in global dictionary. 
    """
    support_count = {}
    for transcation in transactions: # iterate through all transcations
        for itemset in candidates: # iterate through all itemsets 
            if itemset.issubset(transcation): # update support 
                support_count[itemset] = support_count.get(itemset, 0) + 1 
                global_support[itemset] = global_support.get(itemset, 0) + 1
    
    support_count = dict(sorted(support_count.items(), key=lambda x:x[1], reverse=True)) # sort support dictionary
    
    return support_count 


def write_output(output, freq_itemsets, global_support):
    """
    Write output to text file. 
    """
    with open(output, 'w') as f:
        for itemset in freq_itemsets:
            support = global_support[itemset]
            itemset = list(itemset)
            str_item = ' '.join(map(str,itemset))
            pattern = str_item + " (" + str(support) + ")"
            f.write(pattern)
            f.write('\n')


def main():
    """
    Main file to run from the command line.
    """
    # set up the program to take in arguments from the command line
    parser = argparse.ArgumentParser()
    parser.add_argument("--data",
                    default="T10I4D100K.txt",
                    # default="sample_data.txt",
                    help="filename of provided test dataset")
    args = parser.parse_args()

    # read transcation text file as integers
    with open(args.data) as f:
        data = []
        for line in f: 
            data.append([int(x) for x in line.split()])
    
    # call apriori function
    output = 'my-output.txt'
    min_sup = 500
    start_time = time.time() # measure runtime 
    result = apriori(data, min_sup, output)
    end_time = time.time() - start_time

    print("Program Runtime (sec): " , round(end_time,5))


if __name__ == "__main__":
    main()