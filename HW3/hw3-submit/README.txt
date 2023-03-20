** This file contains the instructions on how to run this program. **

There are three main files in this folder: kmeans.py, run-wine.py and run-iris.py. All code for the algorithm is self-contained 
in the kmeans.py file. To run the algorithm, pick either of the run files, which correspond to a dataset available in the UCI
Machine Learning Repository. The run-wine.py file runs the winequality-red.csv dataset, and the run-iris runs the iris.data testing
data provided to us in the homework. 

In both of the run files, there is a flag `no_plot` that can be changed. If `no_plot` is set to True, please specify a value
for k when running from the terminal, and the algorithm will run with that value and automatically visualize the clusters
in 2D based on pre-selected attributes (which vary depending on the dataset). To visualize the SSE and Silhouette Coefficient 
with respect to different k values (Question 2), set `no_plot` to False. 

The `output-<dataset>.txt` file presents the output of the algorithm with the specified dataset (`no_plot` = True) in the required formatting.