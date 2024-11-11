import numpy as np
import matplotlib.pyplot as plt
from SpringSaLaDpy.data_locator import data_file_finder
from .ssalad_ClusterAnalysis import ClusterAnalysis
from .Format import format

def plot(search_directory, times):

    input_file, rounded_times, _ = format(search_directory, times, 'cluster')

    ca = ClusterAnalysis(input_file)
    ca.getMeanTrajectory(SingleTraj=False)
    ca.getSteadyStateDistribution(SS_timePoints=rounded_times)
    
    path = data_file_finder(search_directory, ['pyStat', 'Cluster_stat'], 'SteadyState_distribution.csv')

    with open(path, 'r') as file:
        lines = file.readlines()
    file.close()

    data = [line[:-1].split(',') for line in lines][1:]

    for i, time in enumerate(data):
        data[i] = [float(item) for item in time]

    data_array = np.array(data)

    cs = data_array[:,0]
    f = data_array[:,1]

    average_size_list = []
    for i, cluster_size in enumerate(cs):
        average_size_list.append(cluster_size*f[i])
    average_size = sum(average_size_list)
    
    plt.bar(cs, f)
    plt.axvline(average_size, ls='dashed', lw=1.5, color='k')

    #plt.xlabel('Time (seconds)')
    plt.show()