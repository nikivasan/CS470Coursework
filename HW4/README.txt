** This file contains the instructions to run my code. **

The main file contained in this folder is `pagerank.py`. To run this file, type `python pagerank.py --<graph_DOT_file>` into 
your command line (under the appropriate directory). This will automatically run the code using the provided input file. 
Ensure to change the name of the output csv file produced to be in accordance with the chosen input graph to prevent 
overwriting. This parameter can be found in the main method. The parameter beta may also be adjusted here 
as well (default = 0.8). 

Python libraries needed for this implementation of the pagerank algorithm are: argparse, defaultdict (from collections), 
numpy and csv. I downloaded graphviz both locally on my machine and into my conda environment in order to visualize the 
DOT graph files. 