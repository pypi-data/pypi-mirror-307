from SpringSaLaDpy.data_locator import data_file_finder
import ast

def plot(search_directory):
    
    cluster_file = data_file_finder(search_directory=search_directory, path_list=['pyStat', 'BF_stat'], search_term='cs_Run')
    with open(cluster_file, 'r') as file:
        lines = file.readlines()
    file.close()
    for line in lines:
        print(ast.literal_eval(line[:-1]))


plot('GUI_results\Final_version_test_SIM_FOLDER')