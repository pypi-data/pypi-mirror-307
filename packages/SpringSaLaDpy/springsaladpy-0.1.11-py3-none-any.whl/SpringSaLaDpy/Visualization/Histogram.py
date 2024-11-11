from .ssalad_ClusterAnalysis import *
from .Molclustpy_visualization_funcitons import *
from .Format import format

def plot(search_directory, times, bins=[], mode='foTM'):
    
    input_file, rounded_times, title_str = format(search_directory, times, 'cluster')

    ca = ClusterAnalysis(input_file)
    ca.getSteadyStateDistribution(SS_timePoints=rounded_times)

    plotClusterDistCopy(search_directory, rounded_times, bins, title_str, mode=mode)