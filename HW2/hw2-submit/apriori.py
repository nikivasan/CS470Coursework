import argparse
from itertools import combinations
import time
import re

def get_L1itemsets(data, min_sup):
    """
    Find L1 itemsets above minimum support and store transaction indices. 
    """
    L1_itemset = {}
    result = {}

    for tID, transaction in enumerate(data):
        for item in transaction:
            if (item,) not in L1_itemset: # store itemset as tuple, IDs as set
                L1_itemset[(item,)] = set() 
                L1_itemset[(item,)].add(tID)
            else:
                L1_itemset[(item,)].add(tID)
    
    for itemset, tIDs in L1_itemset.items():
        if len(tIDs) >= min_sup: # only keep itemsets above min support 
            result[(itemset,)] = tIDs
    
    return result

def get_candidates(prev_set_dict, k):
    """
    Generate candidate itemsets of length k. 
    """
    Ck_itemset = {}
    for is1, tID1 in prev_set_dict.items(): # iterate through previous set Lk-1 of itemsets
        for is2, tID2 in prev_set_dict.items():
            if is1[:-1] == is2[:-1]: # if the two itemsets have the same key [0:k-1]
                i1_set = set(is1)
                i2_set = set(is2)
                joined_item = i1_set.union(i2_set) # find set union
                if len(joined_item) == k:
                    subsets = list(combinations(joined_item, k-1)) # prune infrequent subsets
                    for subset in subsets:            
                        if subset not in prev_set_dict.keys():
                            break
                        Ck_itemset[tuple(joined_item)] = tID1.intersection(tID2) # if subsets are frequent
                                                                                 # add new candidate to dictionary 
                                                                                 # with intersection of tIDs as value
    return Ck_itemset


def run_apriori(data, min_sup, output):
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
    #  global dictionary to store association rules 
    L_itemsets = {}
    # generate L1 itemsets
    L_itemsets[1] = get_L1itemsets(data, min_sup)

    k=2
    while(len(L_itemsets[k-1]) > 0):
        start1 = time.time()
        # generate candidates
        Ck_itemsets = get_candidates(L_itemsets[k-1], k)
        # generate list Lk 
        Lk_itemsets = {}
        for candidate, tIDs in Ck_itemsets.items():
            if len(tIDs) >= min_sup:
                Lk_itemsets[candidate] = Ck_itemsets[candidate]
        # store k-frequent-patterns in global dictionary
        L_itemsets[k] = Lk_itemsets
        print("Iteration ", k, "Num Patterns Found: ", len(Lk_itemsets.values()), "Runtime (sec): ", round(time.time()-start1,3))
        k+=1
    
    write_output_dict(output, L_itemsets)

    return L_itemsets 

def write_output_dict(output, global_dict): 
    with open(output, 'w') as f:
        for _, rules in global_dict.items():
            for itemset, tIDs in rules.items():
                itemset = list(itemset)
                support = len(tIDs)
                strip_item = [re.sub(r'(,)', '', str(i)) for i in itemset]
                str_item = ' '.join(map(str, strip_item))
                items = re.sub(r'[()]', '', str(str_item))
                pattern = items + " (" + str(support) + ")"
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
    result = run_apriori(data, min_sup, output)
    end_time = time.time() - start_time
    
    print("Program Runtime (sec): " , round(end_time,5))


if __name__ == "__main__":
    main()
