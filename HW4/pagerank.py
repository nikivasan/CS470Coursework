import argparse 
from collections import defaultdict
import numpy as np
import csv

def page_rank(data, beta, output):
    graph, node_list = create_graph(data) # create graph
    numeric_graph = map_graph(graph, node_list) # transform alphabetical graph to numeric
    
    n = len(node_list) # number of nodes 
    M_transpose = init_M(n, numeric_graph) # initialize transition probability matrix

    # Formula: Beta * M * v + (1-Beta)e / n
    
    M = M_transpose.T # transpose M
    M_beta = M * beta # multiply by beta
    v_0 = np.array([1/n for i in range(n)], dtype=float) # v_0 is vector of initial probs with n components
    one_vec = np.ones(n)
    e = np.array( ((1-beta)* one_vec) / n) # add teleportation factor

    curr_rank = v_0
    prev_rank  = None

    iterations = 0
    convergence_value = 0.00001 # threshold for element-wise uniqueness among page rank vectors
    while not np.array_equal(curr_rank, prev_rank): # iterate until two vectors are equal to each other
        iterations +=1
        prev_rank = curr_rank
        curr_rank = np.matmul(M_beta, curr_rank) + e # update page rank
        
        # handles edge case of minor digit differences in vector components that prevent convergence
        diffs = np.array([abs(curr_rank[i] - prev_rank[i]) for i in range(len(curr_rank))], dtype=float) 
        if iterations > 1:
            if np.all([True if i < convergence_value else False for i in diffs ]):
                break
    
    print("Algorithm converged in ", iterations, " iterations")
    print("Page Rank Vector: ", np.round(curr_rank,3))
    
    page_rank = np.round(curr_rank,3)
    result = list(zip(node_list, page_rank)) # attach node to pagerank
    result = sorted(result, key = lambda x: (-x[1], x[0]))

    print(result)
    write_output(result, output)

    return result

def create_graph(data):
    graph = defaultdict(list) # store original graph
    node_list = list() # store list of unique nodes

    for pair in data:
        node = pair[0] # add data to graph 
        outlink = pair[1]
        graph[node].append(outlink) 

        for element in pair:    # add unique nodes to list
            if element not in node_list:
                node_list.append(element)
    return graph, node_list

def map_graph(graph, node_list):
    node_map = dict() # store each node with a unique index
    for idx, node in enumerate(node_list):
        if node not in node_map.keys():
            node_map[node] = idx

    numeric_graph = dict() # convert graph to numerics (e.g. A, B, C -> 0, 1, 2)
    for node, edges in graph.items():
        new_node = node_map[node]
        new_edges = [node_map[edge] for edge in edges]
        numeric_graph[new_node] = new_edges
    
    return numeric_graph

def init_M(n, graph):
     # populate M_tranpose with correct probabilities 
    M_transpose = np.array([[0]*n for _ in range(n)], dtype=float) # initialize transition probability matrix M 

    for row_idx in range(n): 
        node = row_idx
        if node in graph:
            outgoing_edges = graph[node]
        else:
            outgoing_edges = [-999] # signifies node is a deadend (not stored as a parent in the graph, no outgoing edges)
        init_prob = round(1/len(outgoing_edges),2)
        for col_idx in range(n):
            if outgoing_edges[0] != -999: # for a non-dead end node
                if col_idx in outgoing_edges: # if col represents an outgoing edge, assign probability
                    M_transpose[row_idx][col_idx] = init_prob
                else:                     # else, assign 0
                    M_transpose[row_idx][col_idx] = 0
            else:                         # dead end node is all 0s 
                M_transpose[row_idx][row_idx] = 0
    
    return M_transpose

def read_DOT(input_file):
    edges = []
    with open(input_file) as f:
        for line in f.readlines():
            if line.startswith('digraph') or line.startswith('rankdir') or line.startswith('}'):
                continue
            line = line.replace(' ', '')
            line = line.replace('\n', '')
            edge = line.split('->')
            edges.append(tuple(edge))
    return edges

def write_output(result, output):
    header = ['vertex', 'pagerank']
    with open(output, 'w') as f:
        writer = csv.writer(f)
        writer.writerow(header)
        for item in result:
            writer.writerow(item)

def main():
    """
    Main file to run from the command line.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("graph",
                default="graph1.dot",
                help="filename of graph")
    args = parser.parse_args()
    
    # read in data, add column names
    data = read_DOT(args.graph)
    
    # run algorithm
    beta = 0.8
    output = 'pagerank5.csv' ## CHANGE THIS DEPENDING ON GRAPH 
    result = page_rank(data, beta, output)

if __name__ == "__main__":
    main()