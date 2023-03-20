import argparse
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from random import sample
from sklearn.metrics import silhouette_score
import seaborn as sns
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings('ignore')

class KMeans(object):
    max_iter = 1000
    k = 0
    centroids = None

    def __init__(self, k, max_iter=1000):
        self.k = k
        self.max_iter = max_iter
    
    def train(self, data):
        # separate data into X and y
        xFeat = data.iloc[:, :-1]
        y = data.iloc[:,-1]
        # train-test split
        X_train, X_test, y_train, y_test = train_test_split(xFeat, y, test_size=0.4, random_state=42) # increase train/test split because
        # normalize data using standard scaling
        X_train_scaled, X_test_scaled = self.normalize(X_train, X_test)

        return X_train_scaled, X_test_scaled
        
    
    def predict(self, xFeat):
        y_hat = [] # cluster labels
    
        # randomly initialize centroids
        indices = sample(list(xFeat.index.values), self.k) 
        self.centroids = xFeat.loc[indices]
        prev_centroids = None
        
        iterations = 0 # track number of iterations
        while not self.centroids.equals(prev_centroids) and iterations <= self.max_iter:
            assignments = [list() for i in range(len(self.centroids))]

            # assign data to closest centroid
            for i in range(len(xFeat)):
                point = xFeat.iloc[i]
                distances = self.euclidean_distance(point)
                min_index = distances.argmin()
                assignments[min_index].append(pd.to_numeric(point))
            
            # update centroids
            prev_centroids = self.centroids
            self.centroids = [np.mean(cluster, axis=0) for cluster in assignments]
            
            # if a centroid is NaN due to empty clusters, keep previous centroid in same index
            for idx in range(len(self.centroids)):
                centroid = self.centroids[idx]
                if np.isnan(centroid).any():
                    self.centroids[idx] = prev_centroids.to_numpy()[idx]
            
            self.centroids = pd.DataFrame(self.centroids, columns=prev_centroids.columns)
            iterations +=1

        # create result list storing cluster index, data point index and point itself
        info = list()
        for idx, cluster in enumerate(assignments):
            for point in cluster:
                info.append([idx, point.name, point])
                
        # sort by data point index to order records
        info.sort(key = lambda x: x[1])
        
        # return list of integer cluster labels
        for item in info:
            y_hat.append(item[0])
        
        sse = self.SSE(info)
        silhouette = self.silhouette(xFeat, y_hat)

        # add SSE and Silhouette Coef to end of output
        result = [str(label) for label in y_hat]
        result.append("SSE: " + str(round(sse,5)) + " " + "Silhouette Coef: " + str(round(silhouette,5)))

        # return result and evaluation metrics
        # print("Number of Iterations: ", iterations)
        return result, sse, silhouette, y_hat, self.centroids
    

    def euclidean_distance(self, point):
        distances = np.sqrt(np.sum((self.centroids - point)**2, axis=1))
        return distances  

    def normalize(self, X_train, X_test):
        # scale data using sklearn standard scaler (z-score normalization)
        stdScale = StandardScaler()
        X_train_scaled = stdScale.fit_transform(X_train)
        X_test_scaled = stdScale.fit_transform(X_test)

        X_train_scaled = pd.DataFrame(X_train_scaled, columns=X_train.columns)
        X_test_scaled = pd.DataFrame(X_test_scaled, columns=X_test.columns)
        return X_train_scaled, X_test_scaled
    
    def SSE(self, info):
        errors = []
        # iterate over all data points
        for i in range(len(info)):
            point = info[i]
            centroid_idx = point[0]
            centroid = self.centroids.loc[centroid_idx]
            dist = np.sqrt(np.sum((centroid- point[2])**2))
            errors.append(dist**2)
        
        sse = sum(errors)
        return sse
    
    def silhouette(self, xFeat, y_hat):
        score = silhouette_score(xFeat, y_hat)
        return score
    
    def visualize_iris(self, xFeat, y_hat, centroids):
        xFeat['Predicted Cluster'] = y_hat
        x = xFeat['Sepal Length']
        y = xFeat['Petal Length']
        assignments = xFeat['Predicted Cluster']

        centroids_x = centroids.iloc[:,0]
        centroids_y = centroids.iloc[:,2]

        plt.scatter(x, y, c=assignments)
        plt.plot(centroids_x,centroids_y, c='white', marker='.', linewidth='0.01', markerfacecolor='red', markersize=22)
        plt.xlabel('Sepal Length')
        plt.ylabel('Petal Length')
        plt.savefig('Visualize-Iris.png')
        plt.show()
        
    def visualize_wine(self, xFeat, y_hat, centroids):
        xFeat['Predicted Cluster'] = y_hat
        x = xFeat['alcohol']
        y = xFeat['volatile acidity']
        assignments = xFeat['Predicted Cluster']

        centroids_x = centroids.iloc[:,10]
        centroids_y = centroids.iloc[:,1]

        plt.scatter(x, y, c=assignments)
        plt.plot(centroids_x,centroids_y, c='white', marker='.', linewidth='0.01', markerfacecolor='red', markersize=22)
        plt.xlabel('Alcohol')
        plt.ylabel('Volatile Acidity')
        plt.savefig('Visualize-Wine.png')
        plt.show()