from kmeans import KMeans
import argparse
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

def plot_sse(data):
    k_values = []
    sse_tests = []
    for k in range(2,21):
        k_values.append(k)
        km = KMeans(k)
        _, X_test = km.train(data)
        _,sse_test,_,_,_= km.predict(X_test)
        sse_tests.append(sse_test)
    plt.plot(k_values, sse_tests, marker='+', color='b')
    plt.xticks(np.arange(2,21,step=1))
    plt.title("SSE vs K Values")
    plt.xlabel("K Values")
    plt.ylabel("SSE")
    plt.savefig('SSE-plot-wine.png')
    plt.show()

def plot_silhouette(data):
    k_values = []
    s_tests = []
    for k in range(2,21):
        k_values.append(k)
        km = KMeans(k)
        _, X_test = km.train(data)
        _,_,silhouette_test,_,_ = km.predict(X_test)
        s_tests.append(silhouette_test)
    plt.plot(k_values, s_tests, marker='+', color='b')
    plt.xticks(np.arange(2,21,step=1))
    plt.title("Silhouette Coefficient vs K Values")
    plt.xlabel("K Values")
    plt.ylabel("Silhouette Coefficient")
    plt.savefig('Silhouette-plot-wine.png')
    plt.show()

def write_output(result, output):
    with open(output, 'w') as f:
        for item in result:
            f.write(item)
            f.write('\n')

def main():
    """
    Main file to run from the command line.
    """
    ### CHANGE THIS ###
    no_plot = True
    
    if no_plot:
        parser = argparse.ArgumentParser()
        parser.add_argument("k",
                            default=3,
                            type=int,
                            help="the number of neighbors")
        parser.add_argument("--data",
                            default="winequality-red.csv",
                            help="filename of provided test dataset")
        args = parser.parse_args()
        
        # read in data
        df = pd.read_csv('winequality-red.csv', sep=';')
        df.drop(columns=['quality'])
    
        # run k-means function
        output = 'output-wine.txt'
        km = KMeans(args.k)
        xTrain, xTest = km.train(df)
        # result_train,_,_,y_hat_train,centroids_train = km.predict(xTrain) # predict training data + SSE/Silhouette
        result_test,_,_,y_hat_test,centroids_test = km.predict(xTest) # predict testing data + SSE/Silhouette

        # visualize clusters 
        km.visualize_wine(xTest,y_hat_test,centroids_test)

        # write output
        write_output(result_test, output)
    else:
        parser = argparse.ArgumentParser()
        parser.add_argument("--data",
                            default="winequality-red.csv",
                            help="filename of provided test dataset")
        args = parser.parse_args()
        # read in data
        df = pd.read_csv('winequality-red.csv', sep=';')
        df.drop(columns=['quality'])
    
        plot_sse(df)
        plot_silhouette(df)

if __name__ == "__main__":
    main()