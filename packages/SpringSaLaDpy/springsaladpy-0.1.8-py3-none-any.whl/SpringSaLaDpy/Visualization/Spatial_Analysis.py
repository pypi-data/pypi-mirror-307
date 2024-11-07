from SpringSaLaDpy.input_file_extraction import *
import os
import matplotlib.pyplot as plt
from .ClusTopology_ss import ClusterDensity
from .DataPy import *
from .times_2_title import * 
from .Format import format

def read_viewer(path):
    if path[-7:] == '_FOLDER':
        last_item = ''
    else:
        last_item = os.path.split(path)[1][:-12] + '_FOLDER'
    specific_path  = os.path.join(path, last_item)

    _,split_file = read_input_file(specific_path)
    total_time = float(split_file[0][1].split(' ')[2])
    dt_image = float(split_file[0][5].split(' ')[1])
    count = int(total_time/dt_image)

    input_file = find_txt_file(specific_path)
    return count, dt_image, input_file

def scatter_plot(search_directory, times=[], size_threshold=1, cubic_com=True):
    
    input_file, rounded_times, title_str = format(search_directory, times, file_type='viewer')

    cd = ClusterDensity(input_file, ss_timeSeries=rounded_times)
    cd.getCD_stat(cs_thresh=size_threshold, title_str=title_str, cubic_com=cubic_com)

def histogram(search_directory, times=[], size_threshold=1, indices=[], cubic_com=True):
    
    input_file, rounded_times, title_str = format(search_directory, times, file_type='viewer')

    cd = ClusterDensity(input_file, ss_timeSeries=rounded_times)
    cd.getCD_stat(cs_thresh=size_threshold, title_str=title_str, hist=True, indices=indices, cubic_com=cubic_com)

def time_course(path, indices = [], size_threshold=1, legend_right=True, cubic_com=True, reference_shapes=False):
    count, dt_image, input_file = read_viewer(path)

    times = [0]
    for i in range(int(count) + 1):
        times.append(i*dt_image)
    times.pop(0)

    cd = ClusterDensity(input_file, ss_timeSeries=times)
    vfiles = glob(cd.simObj.getInpath() + "/viewer_files/*.txt")[:]    
    cs_full, rg_full, rmax_full = [[] for _ in range(len(times))], [[] for _ in range(len(times))], [[] for _ in range(len(times))]
    for i, vfile in enumerate(vfiles):
        ProgressBar("Progress", (i+1)/float(len(vfiles)), 40)
        res, MCL, mtp_cs, mtp_rg, mtp_rmax = cd.getClusterDensity(vfile, size_threshold, cubic_com=cubic_com, time_course=True)

        for i in range(len(times)):
            cs_full[i].extend(mtp_cs[i])
            rg_full[i].extend(mtp_rg[i])
            rmax_full[i].extend(mtp_rmax[i])

    outputs = []
    for i in range(4):
        outputs.append([[],[],[]])

    for i, time in enumerate(times):
        #cs_tmp, rg_tmp, rmax_tmp = [], [], []
        
        #ProgressBar("Progress", i/len(times), 40)

        '''
        cd = ClusterDensity(input_file, ss_timeSeries=[time])
        for vfile in vfiles:
            #this line takes up the majority of the computation time
            res, MCL, mtp_cs, mtp_rg, mtp_rmax = cd.getClusterDensity(vfile, size_threshold, cubic_com=cubic_com, time_course=True)

            cs_tmp.extend(mtp_cs)
            rg_tmp.extend(mtp_rg)
            rmax_tmp.extend(mtp_rmax)
        '''
        cs_now = cs_full[i]
        rg_now = rg_full[i]
        rmax_now = rmax_full[i]

        #csList = np.concatenate(cs_now).ravel().tolist()
        #rgList = np.concatenate(rg_now).ravel().tolist()
        #rmaxList = np.concatenate(rmax_now).ravel().tolist()
        distribution = [(rg/rmax) for rg, rmax in zip(rg_now, rmax_now)]
        
        plotting_lists = [rg_now, cs_now, rmax_now, distribution]

        for i, plotting_list in enumerate(plotting_lists):
            if cs_now == []:
                for j in range(3):
                    outputs[i][j].append(None)
            else:
                outputs[i][0].append(min(plotting_list))
                outputs[i][1].append(sum(plotting_list)/len(plotting_list))
                outputs[i][2].append(max(plotting_list))

    plot_dict = {
        0: 'Minimum',
        1: 'Average',
        2: 'Maximum'
    }

    label_dict = {
        0: ['Radius of Gyration', 'Radius of Gyration (nm)'],
        1: ['Cluster Size', 'Molecules per Cluster'],
        2: ['Cluster Radius', 'Radius (nm)'],
        3: ['Mass Distribution Coefficient', 'Radius of Gyration / Radius']
    }

    file_name_dict = {
        0: 'Radius_of_Gyration.txt',
        1: 'Cluster_Size.txt',
        2: 'Cluster_Radius.txt',
        3: 'Mass_Distribution.txt'
    }

    if indices == []:
        indices = [0,1,2]

    legend_list = []
    for i, output in enumerate(outputs):
        plt.figure()
        lines = []
        for index in indices:
            legend_list.append(plot_dict[index])
            line, = plt.plot(times,output[index])
            lines.append(line)
            plt.title(label_dict[i][0])
            plt.ylabel(label_dict[i][1])
        plt.xlabel('Time (seconds)')
        
        full_path = path + '/pyStat/3D_stat/' + file_name_dict[i]
        with open(full_path,'w') as file:
            file.write(f'Time\tMinimum\tAverage\tMaximum\n')
            for i in range(len(times)):
                file.write(f'{times[i]}\t{output[0][i]}\t{output[1][i]}\t{output[2][i]}\n')
        file.close()
        print(f'Wrote chart data! Output File: {full_path}')


        if legend_right:
            top_legend = plt.legend(lines, legend_list, bbox_to_anchor=(1.02, 1), loc='upper left')
        else:
            top_legend = plt.legend(lines, legend_list)      

        if i == 3 and reference_shapes:
            plt.gca().add_artist(top_legend)
            shell = plt.axhline(1, ls='-', lw=1.5, color='k', label='Thin Spherical Shell = 1')
            sphere = plt.axhline(np.sqrt(3/5), ls='dashed', lw=1.5, color='k', label=r'Uniform Solid Sphere = $\sqrt{\frac{3}{5}}$')
            if legend_right:
                plt.legend(handles=[shell, sphere], bbox_to_anchor=(1.02, 0), loc='lower left')
            else:
                plt.legend(handles=[shell, sphere], loc='lower right')
        plt.show()

def scatter_3d(path, run=0, times=[], view=[], site_scale=10, link_thickness=0.75, depth_fade=True):  
    count, dt_image, input_file = read_viewer(path)
    if times == []:
        times.append(-1)

    for time in times:
        if time == -1:
            time_input = []
        else:
            time_input = [time]
        _, rounded_times, title_str = format(path, time_input, 'cluster')
        cd = ClusterDensity(input_file, ss_timeSeries=[rounded_times[0]])
        vfiles = glob(cd.simObj.getInpath() + "/viewer_files/*.txt")[:]

        viewerfile = vfiles[run]

        with open(viewerfile, 'r') as infile:
            tps, index_pairs = cd.getSteadyStateFrameIndices(viewerfile)
            lines = infile.readlines()
            for i,j in index_pairs:
                #i,j = index_pairs[-1]
                current_frame = lines[i:j]
                posDict, linkList, colorDict, radDict = cd.getBindingStatus(current_frame)
        
        fig = plt.figure(figsize=(7,7))
        ax = fig.add_subplot(111, projection='3d')

        x_cords=[]
        y_cords=[]
        z_cords=[]
        colors=[]
        radii = []
        for site in posDict.keys():
            x_cords.append(posDict[site][0])
            y_cords.append(posDict[site][1])
            z_cords.append(posDict[site][2])
            colors.append(colorDict[site])
            radii.append(site_scale*radDict[site])

        connection_list = []
        for link in linkList:
            x_pair = [posDict[link[0]][0], posDict[link[1]][0]]
            y_pair = [posDict[link[0]][1], posDict[link[1]][1]]
            z_pair = [posDict[link[0]][2], posDict[link[1]][2]]
            connection_list.append([x_pair, y_pair, z_pair])

        if depth_fade:
            alpha = None
        else:
            alpha = 1
        ax.scatter(x_cords, y_cords, z_cords, c=colors, s=radii, alpha=alpha)
        for connection in connection_list:
            ax.plot(connection[0], connection[1], connection[2], color='black', linewidth=link_thickness)
        
        if view==[]:
            pass
        else:
            ax.view_init(view[0], view[1], view[2])

        #ax.set_aspect('equal')
        ax.set_xlabel('X (nm)')
        ax.set_ylabel('Y (nm)')
        ax.set_zlabel('Z (nm)')
        ax.set_xlim(cd.box[0][0], cd.box[0][1])
        ax.set_ylim(cd.box[1][0], cd.box[1][1])
        ax.set_zlim(cd.box[2][0], cd.box[2][1])

        ax.set_title(f'3D View of Sites and Links{title_str}')

        plt.show()
    


        
        

        
        
    

    
    