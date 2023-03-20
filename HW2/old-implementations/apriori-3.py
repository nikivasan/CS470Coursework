# APRIORI DICTIONARY IMPLEMENTATION 


import argparse
from collections import defaultdict
import itertools
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
    freqSetLength = dict() # key: itemset length, value: itemset
    globalSupport = defaultdict(int) # key: item, value: support
    
    C1itemset, transcations = get_itemset(data) # get C1 itemset and transcation list 
    L1itemset = above_min_sup(C1itemset, transcations, min_sup, globalSupport) # keep candidate above min support 
    
    currLkSet = L1itemset
    
    k=2
    while(len(currLkSet) != 0):
        start1 = time.time()
        freqSetLength[k-1] = currLkSet
        Ckitemset = self_join(currLkSet, k) 
        Ckitemset = prune(Ckitemset, freqSetLength[k-1], k)
        currLkSet = above_min_sup(Ckitemset, transcations, min_sup, globalSupport)
        print("Iteration ", k, "Num Patterns Found: ", len(currLkSet), "Runtime (sec): ", round(time.time()-start1,3))
        k+=1
    
    write_output_dict(output, freqSetLength, globalSupport)
    
    return freqSetLength


def get_itemset(data):
    """
    Generate itemset and list of transcations from data.
    """
    itemset = set()
    transcations = []
    
    for row in data:
        transcations.append(frozenset(row))
        for item in row:
            itemset.add(frozenset([item])) 
    
    return itemset,transcations

def above_min_sup(c_set, t_list, min_sup, globalSupport):
    """
    Remove all items whose subsets are infrequent.
    """
    freqSet = set()
    localSupport = defaultdict(int)

    for item in c_set:
        for transcation in t_list:
            if item.issubset(transcation):
                localSupport[item] += 1
                globalSupport[item] += 1

    localSupport = dict(sorted(localSupport.items(), key=lambda x:x[1], reverse=True))

    for key, value in localSupport.items():
        if value >= min_sup:
            freqSet.add(key)
    
    return freqSet

def self_join(c_set, k):
    """
    Self join itemset Ck to create Lk.
    """
    candidates = set()
    for i1 in c_set:
        for i2 in c_set:
            joined_item = i1.union(i2)
            if len(joined_item) == k:
                candidates.add(joined_item)

    return candidates

def prune(c_set, prev_set, k):
    """
    Remove all items whose subsets are infrequent.
    """
    freqSet = set()
    for item in c_set:
        subsets = list(itertools.combinations(item, k-1))
        for tuple in subsets:            
            if frozenset(tuple) not in prev_set:
                break
        freqSet.add(item)

    return freqSet

def write_output_dict(output, freqSet, supportSet):
    with open(output, 'w') as f:
        for _, value in freqSet.items():
            for itemset in value: 
                support = supportSet[itemset]
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
    
    # run apriori function
    output = 'my-output.txt'
    min_sup = 4

    start_time = time.time() # measure runtime 
    result = apriori(data, min_sup, output)
    end_time = time.time() - start_time

    print("Program Runtime (sec): " , round(end_time,5))

if __name__ == "__main__":
    main()