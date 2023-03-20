This program is self-contained within the `apriori.py` file. The following packages are required: 
- argparse
- itertools 
- time
- re

The requirements.txt file has all modules installed in my venv for this project. 

Ensure that the data is in the same directory as the script. Either pass the dataset as a parameter (e.g. python apriori.py <dataset>) 
or use/adapt the default parser parameter, which is currently the T10I4D100K.txt file that was provided with the homework. You may also
update the support count in the main method of the file. The result will write to a file called 'my-output.txt' in the same directory. The 
`test_equality.py` file may be used to compare the output of my program on the T10I4D100K dataset with the provided example output.  