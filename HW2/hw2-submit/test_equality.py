import argparse


def main():
    """
    Test whether my output and example output are equal.
    """
    # set up the program to take in arguments from the command line
    parser = argparse.ArgumentParser()
    parser.add_argument("--my_output",
                    default="result500-mw.txt",
                    help="filename of my output")
    parser.add_argument("--example_output",
                default="example-output.txt",
                help="filename of provided output")
    args = parser.parse_args()

    # read my output text file 
    with open(args.my_output) as f:
        my_output = []
        for line in f: 
            my_output.append(line.strip())
    
    # read example output text file 
    with open(args.example_output) as f:
        ex_output = []
        for line in f: 
            ex_output.append(line.strip())
    
    # sort and write my output file for visual comparison
    my_output = sorted(my_output)
    with open('sorted-my-output.txt', 'w') as f:
        for tuple in my_output:
            f.write(tuple)
            f.write('\n')
    
    # # sort and write example output file for visual comparison
    # ex_output = sorted(ex_output)
    # with open('sorted-ex-output.txt', 'w') as f:
    #     for tuple in ex_output:
    #         f.write(tuple)
    #         f.write('\n')


    count = 0
    for i1 in my_output:
        for i2 in ex_output:
            if i1 == i2:
                count+=1
    
    print("Correct Number of Patterns?" , len(my_output) == len(ex_output))
    print("Correct Patterns?" , set(my_output) == set(ex_output))
    print("Overall Accuracy: ", round(count/len(my_output) * 100, 3), "%")

if __name__ == "__main__":
    main()