import numpy as np
import matplotlib.pyplot as plt
from SpringSaLaDpy.data_locator import data_file_finder
from .ssalad_ClusterAnalysis import ClusterAnalysis
from .Format import format

def plot(search_directory, mode='ACO', fill=False):

    input_file, _, _ = format(search_directory, [0], 'cluster')

    ca = ClusterAnalysis(input_file)
    ca.getMeanTrajectory(SingleTraj=False)
    
    path = data_file_finder(search_directory, ['pyStat', 'Cluster_stat'], 'Clustering_dynamics.csv')

    with open(path, 'r') as file:
        lines = file.readlines()
    file.close()

    data = [line[:-1].split(',') for line in lines][1:]

    for i, time in enumerate(data):
        data[i] = [float(item) for item in time]

    data_array = np.array(data)

    x = data_array[:,0]/1e3
    
    if mode=='ACO':
        y = data_array[:,2]
        plt.plot(x,y)
        plt.ylabel('ACO')
        if fill:
            yerr = data_array[:,3]
            plt.fill_between(x, y-yerr, y+yerr, alpha=0.2)
            plt.title('Average Cluster Occupancy (bounds of 1 SD)')
        else:
            plt.title('Average Cluster Occupancy')
    elif mode=='ACS':
        y = data_array[:,1]
        plt.plot(x,y)
        plt.ylabel('ACS')
        plt.title('Average Cluster Size')
        if fill:
            print('Warning, no standard deviation data available for ACS')
    else:
        print('Error: Please enter either \'ACO\' or \'ACS\' as the mode')

    plt.xlabel('Time (seconds)')
    plt.show()