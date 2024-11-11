# -*- coding: utf-8 -*-
"""
Created on Tue Mar 16 18:43:43 2021

@author: Ani Chattaraj
"""

from .DataPy import ReadInputFile, InterSiteDistance, ProgressBar, displayExecutionTime
import re, json, pickle
import numpy as np
import networkx as nx
from glob import glob
import matplotlib.pyplot as plt
from csv import writer
from numpy import pi, array
from collections import defaultdict, OrderedDict, namedtuple, Counter
import os
from SpringSaLaDpy.data_locator import data_file_finder
import time

font = {'family' : 'Arial',
        'size'   : 16}

plt.rc('font', **font)


def connected_component_subgraphs(G):
    for c in nx.connected_components(G):
        yield G.subgraph(c)
# pos = center of mass, radius = Radius of gyration, 
#density = sites/volume
Cluster = namedtuple('Cluster', ['pos', 'radius', 'density'])

class ClusterDensity:

    def __init__(self, txtfile, ss_timeSeries):
        self.simObj = ReadInputFile(txtfile)
        tf, dt, dt_data, dt_image = self.simObj.getTimeStats()
        self.box = self.simObj.getBoundingBox()
        self.ss_timeSeries = ss_timeSeries
        inpath = self.simObj.getInpath() + "/data"
        numRuns = self.simObj.getNumRuns()
        self.N_frames = int(tf/dt_image)
        self.inpath = inpath
        if numRuns == 0:
            self.numRuns = 25
        else:    
            self.numRuns = numRuns

    def __repr__(self):
        simfile = self.simObj.txtfile.split('/')[-1]
        info = f"Class : {self.__class__.__name__}\nSystem : {simfile}"
        return info

    @staticmethod
    def getMolIds(molfile, molName):
        molDict = {}
        mIds = []
        with open(molfile, 'r') as tmpfile:
            for line in tmpfile:
                line = line.strip().split(',')
                if line[-1] == molName:
                    mIds.append(line[0])
        molDict[molName] = mIds
        return molDict

    @staticmethod
    def getSiteIds(sitefile, molName):
        siteDict = {}
        sIds = []
        with open(sitefile, 'r') as tmpfile:
            for line in tmpfile:
                line = line.strip().split(',')
                if line[-1].split()[0] == molName:
                    sIds.append(line[0])
        siteDict[molName] = sIds
        return siteDict

    @staticmethod
    def getRevDict(myDict):
        # k,v = key : [val1, val2, ...]
        revDict = {}
        for k,v in myDict.items():
            for val in v:
                revDict[val] = k
        return revDict
    @staticmethod
    def splitArr(arr, n):
        subArrs = []
        if (len(arr)%n == 0):
            f = int(len(arr)/n)
            i = 0
            while (i < len(arr)):
                sub_arr = arr[i : i+f]
                i += f
                subArrs.append(sub_arr)
            return subArrs
        else:
            print(f"Can't split the given array (length = {len(arr)}) into {n} parts")

    def mapSiteToMolecule(self):
        sIDfile = InterSiteDistance.findFile(self.inpath, self.numRuns, "SiteIDs")
        mIDfile = InterSiteDistance.findFile(self.inpath, self.numRuns, "MoleculeIDs")
        molName, molCount = self.simObj.getMolecules()
        molIDs, siteIDs = {}, {}
        for mol in molName:
            molIDs.update(self.getMolIds(mIDfile, mol))
            siteIDs.update(self.getSiteIds(sIDfile, mol))
        spmIDs = {} # sites per molecule
        for mol, count in zip(molName, molCount):
            #molDict = {}
            arr = self.splitArr(siteIDs[mol], count)
            mol_ids = molIDs[mol]
            d = dict(zip(mol_ids, arr))
            spmIDs.update(d)
        rev_spm = self.getRevDict(spmIDs)
        return rev_spm

    @staticmethod
    def getBindingStatus(frame):
        linkList = []
        posDict = {}
        colorDict = {}
        radDict = {}
        for curline in frame:
            if re.search("ID", curline):
                line = curline.split()
                posDict[line[1]] = [float(line[4]),float(line[5]), float(line[6])] # order = x,y,z
                colorDict[line[1]] = line[3]
                radDict[line[1]] = float(line[2])
                #IdList.append(line.split()[1])

            if re.search("Link", curline):
                line = curline.split()
                linkList.append((line[1], line[3]))
        return posDict, linkList, colorDict, radDict

    @staticmethod
    def createGraph(IdList, LinkList):
        G = nx.Graph()
        G.add_nodes_from(IdList)
        G.add_edges_from(LinkList)
        return G
    
    @staticmethod
    def createMultiGraph(LinkList):
        MG = nx.MultiGraph()
        MG.add_edges_from(LinkList)
        return MG

    @staticmethod
    def getFrameIndices(viewerfile):
        frame_indices = []
        tps = []
        with open(viewerfile, 'r') as tmpfile:
            lines = tmpfile.readlines()
            for i, line in enumerate(lines):
                if re.search("SCENE", line):
                    frame_indices.append(i)
                    tp = lines[i+1].split()[-1]
                    tps.append(tp)

            frame_indices.append(len(lines))

        return tps, frame_indices
    
    def getSteadyStateFrameIndices(self, viewerfile, time_course=False):
        frame_indices = []
        ss_indices = [] 
        tps = []
        index_pairs = []
        
        '''
        with open(viewerfile, 'r') as tmpfile:
            lines = tmpfile.readlines()
            for i, line in enumerate(lines):
                if re.search("SCENE", line):
                    frame_indices.append(i)
                    tp = lines[i+1].split()[-1]
                    tps.append(tp)
                    if any([np.isclose(float(tp), t) for t in self.ss_timeSeries]):
                        ss_indices.append(i)
            frame_indices.append(len(lines))
        tmpfile.close()
        '''

        if True:
            count = 0
            scenes = 0
            scene_pattern = re.compile("SCENE")
            with open(viewerfile, 'r') as tmpfile:
                for i, line in enumerate(tmpfile):
                    count = i
                    if scene_pattern.search(line):
                        frame_indices.append(i + scenes)
                        scenes = scenes + 1
                        tp = next(tmpfile).split()[-1]
                        tps.append(tp)
                        if time_course:
                            ss_indices.append(i + scenes - 1)
                        else:
                            if any(np.isclose(float(tp), t) for t in self.ss_timeSeries):
                                ss_indices.append(i + scenes - 1) 
                frame_indices.append(count + scenes + 1)
            tmpfile.close()

        for ii, elem in enumerate(frame_indices):
            if elem in ss_indices:
                index_pairs.append((elem, frame_indices[ii+1]))

        return tps, index_pairs

    @staticmethod
    def calc_RadGy(posList, massList, cubic_com=True):
        if cubic_com:
            massList = massList.reshape(-1, 1)
            weighted_array = posList * massList
            weighted_sum = np.sum(weighted_array, axis=0)
            sum_weights = np.sum(massList)
            center = weighted_sum / sum_weights
        else:
            # posList = N,3 array for N sites
            center = np.mean(posList, axis=0) # center of cluster
        
        Rg2 = np.mean(np.sum((posList - center)**2, axis=1))
        rmax2 = np.max(np.sum((posList - center)**2, axis=1), axis=0)
        return center, np.sqrt(Rg2), np.sqrt(rmax2)
    
    @staticmethod
    def calc_zagreb_indices(MG, node_list):
        # MG: MULTI-GRAPH Object # multiple edges allowed between two nodes 
        d1List = []
        d2List = []
        nodes = list(MG.nodes())
        specific_mol = []
        #links = [(nodes[i], nodes[j]) for i in range(len(nodes)) for j in range(len(nodes)) if i<j]
        for n in nodes:
            d1List.append(MG.degree(n))
        for n1,n2 in set(MG.edges()):
            d2List.append((MG.degree(n1), MG.degree(n2)))
        d1Arr = array(d1List)
        
        specific_nodes = [node for node in nodes if node in node_list]

        for node in specific_nodes:
            specific_mol.append(MG.degree(node))

        # M1, M2: first and second Zagreb indices
        M1 = sum(d1Arr**2)
        M2 = sum([d1*d2 for d1,d2 in d2List])
        
        if node_list == []:
            specific_mol = d1Arr

        return M1, M2, d1Arr, specific_mol
        

    def getClusterDensity(self, viewerfile, cs_thresh=1, molecule_list=[], cubic_com=True, time_course=False):        
        # cluster size,  radius of gyration
        # M1, M2: Zagreb indices
        csList, RgList, rmaxList, M1List, M2List = [], [], [], [], []
        
        mtp_cs, mtp_rg, mtp_rmax = [], [], [] # mtp: multi timepoint stat
        
        # MCL: molecular cross linking (number of bonds per molecule)  
        MCL = []
        msm = self.mapSiteToMolecule()

        tps, index_pairs = self.getSteadyStateFrameIndices(viewerfile, time_course=time_course)

        section1 = time.time()

        run_num = os.path.split(viewerfile)[1].split('_')[-1][3:-4]
        search_directory = os.path.join(os.path.split(os.path.split(viewerfile)[0])[0])
        molecule_name_file = data_file_finder(search_directory=search_directory, path_list=['data', f'Run{run_num}'], search_term='MoleculeIDs.csv')
        name_to_IDs = {}

        with open(molecule_name_file, 'r') as file:
            lines = file.readlines()
            for line in lines:
                name = line.split(',')[1][:-1]
                ID_num = line.split(',')[0]
                if name not in name_to_IDs.keys():
                    name_to_IDs[name] = [ID_num]
                else:
                    name_to_IDs[name].append(ID_num)

        node_list = [] 
        if molecule_list != []:
            for molecule in molecule_list:
                node_list.extend(name_to_IDs[molecule])

        '''
        path = os.path.join(os.path.split(molecule_name_file)[0], 'molecule_links.txt')
        open(path, 'w').close()
        '''

        with open(viewerfile, 'r') as infile:
            lines = infile.readlines()
            for i,j in index_pairs:
                #i,j = index_pairs[-1]
                current_frame = lines[i:j]
                cs_frame, rg_frame, rmax_frame = [], [], [] # clusters in current frame
                posDict, Links, _, radDict = self.getBindingStatus(current_frame)
                Ids = [_ for _ in posDict.keys()]
                #mIds, mLinks = [msm[k] for k in Ids], [(msm[k1], msm[k2]) for k1,k2 in Links]
                sG = self.createGraph(Ids, Links)
                #mG = self.createGraph(mIds, mLinks)
                
                '''
                with open(path, 'a') as outfile:
                    outfile.write(f'\n\n{current_frame[0]}')
                    outfile.write(current_frame[1])
                outfile.close()
                '''

                #G.subgraph(c) for c in connected_components(G)
                count = 0
                for sg in connected_component_subgraphs(sG):
                    mLinks = [(msm[k1], msm[k2]) for k1, k2 in sg.edges()]
                    # connection between two different molecules                    
                    bonds = [(m1,m2) for m1,m2 in mLinks if m1 != m2]
                    
                    '''
                    if len(bonds) > 0:
                            count += 1
                            with open(path, 'a') as outfile:
                                outfile.write(f'\nCluster {count}')
                                for bond in bonds:
                                    outfile.write(f'\nBOND\t{bond[0]}\t:\t{bond[1]}')
                            outfile.close()
                    '''

                    MG = self.createMultiGraph(bonds)

                    # cluster size (number of molecules)
                    cs = len(MG.nodes())

                    if cs > cs_thresh:
                        M1, M2, dArr, specific_mols = self.calc_zagreb_indices(MG, node_list=node_list)
                        MCL.extend(specific_mols)
                       
                        sites = list(sg.nodes)
                        
                        posList = np.array([posDict[s] for s in sites])
                        massList = np.array([float(radDict[s])**3 for s in sites])
                        
                        center, Rg, rmax = self.calc_RadGy(posList, massList, cubic_com=cubic_com)
                        
                        cs_frame.append(cs)
                        rg_frame.append(Rg)
                        rmax_frame.append(rmax)
                        
                        csList.append(cs)
                        RgList.append(Rg)
                        rmaxList.append(rmax)
                        M1List.append(M1)
                        M2List.append(M2)
                
                mtp_cs.append(cs_frame)
                mtp_rg.append(rg_frame)
                mtp_rmax.append(rmax_frame)

        return [csList, RgList, rmaxList, M1List, M2List], MCL, mtp_cs, mtp_rg, mtp_rmax
    
    @staticmethod  
    def plotRg(csList, RgList, time_str):
        fig, ax = plt.subplots(figsize=(5,3))
        ax.scatter(csList, RgList, color='k', s=4)
        ax.set_xlabel('Cluster size (molecules)')
        ax.set_ylabel('Radius of Gyration (nm)')
        ax.xaxis.set_major_locator(plt.MaxNLocator(integer=True, min_n_ticks=1))
        plt.title('Radius of Gyration Scatter Plot' + time_str)
        plt.show() 
    
    @staticmethod
    def plotBondsPerMolecule(countDict, time_str, mol_str):
        fig, ax = plt.subplots(figsize=(5,3))
        bonds, freq = countDict.keys(), countDict.values()
        ax.bar(bonds, freq, width=0.3, color='grey')
        ax.set_xlabel('Bonds per molecule')
        ax.set_ylabel('Frequency')
        ax.xaxis.set_major_locator(plt.MaxNLocator(integer=True, min_n_ticks=1))
        plt.title(f'Bonds per Molecule{mol_str} Histogram{time_str}')
        plt.show()
        
    @displayExecutionTime
    def getCD_stat(self, cs_thresh=1, title_str='', hist=False, indices=[], cubic_com=True):
        # collect statistics at the last timepoint
        sysName = self.inpath.split('/')[-2].replace('_SIM_FOLDER','')
        print('\nSystem: ', sysName)
        print("Calculating Cluster Density ...")
      
        outpath = self.simObj.getOutpath("BF_stat")
        vfiles = glob(self.simObj.getInpath() + "/viewer_files/*.txt")[:]

        N_traj = len(vfiles)

        header = 'Cluster size, Rg (nm), M1, M2'
        MCL_stat = []
        cs_tmp, rg_tmp = [], []

        search_directory = os.path.join(os.path.split(os.path.split(vfiles[0])[0])[0])
        molecule_name_file = data_file_finder(search_directory=search_directory, path_list=['data', f'Run{0}'], search_term='MoleculeIDs.csv')
        names = []
        with open(molecule_name_file, 'r') as file:
            lines = file.readlines()
            for line in lines:
                name = line.split(',')[1][:-1]
                if name not in names:
                    names.append(name)

        molecule_list = []

        for index in indices:
            molecule_list.append(names[index])

        for i, vfile in enumerate(vfiles):
            res, MCL, mtp_cs, mtp_rg, mtp_rmax = self.getClusterDensity(vfile, cs_thresh=cs_thresh, molecule_list=molecule_list, cubic_com=cubic_com)
            #print(array(mtp_rg))
            MCL_stat.extend(MCL)
            cs_tmp.extend(mtp_cs)
            rg_tmp.extend(mtp_rg)
            
            if cs_thresh == 1:
                runNum = vfile.split('_')[-1] # Run0.txt
                #np.savetxt(outpath + '/cs_' + runNum , array(mtp_cs))
                with open(outpath + '/cs_' + runNum, 'w') as of:
                    for item in mtp_cs:
                        of.write(f'{item}')
                        of.write('\n')
                
                with open(outpath + '/rg_' + runNum, 'w') as of:
                    for item in mtp_rg:
                        of.write(f'{item}')
                        of.write('\n')
            
            ProgressBar("Progress", (i+1)/N_traj)

        counts_norm = {k: (MCL_stat.count(k)/len(MCL_stat)) for k in set(MCL_stat)}
        
        if cs_thresh == 1:
            fName = '/Bonds_per_single_molecule.csv'
        else:
            fName = f'/Bonds_per_single_molecule_cs_gt_{cs_thresh}.csv'
            
        with open(outpath + fName, "w", newline='') as of:
            obj = writer(of)
            obj.writerow(['BondCounts','frequency'])
            obj.writerows(zip(counts_norm.keys(), counts_norm.values()))
        
        csList = np.concatenate(cs_tmp).ravel().tolist()
        rgList = np.concatenate(rg_tmp).ravel().tolist()
        if hist:
            print('Molecules:')
            all_indices = []
            for i, name in enumerate(names):
                all_indices.append(i)
                print(f'{i}: {name}')
            print('\nList of Indices:')
            print(all_indices)

            add_str = ''
            for index in indices:
                add_str = add_str + f'{names[index]}, '
            add_str = add_str[:-2]
            if add_str != '':
                mol_str = f' ({add_str})'
            else:
                mol_str = ''

            
            bonds, freq = list(counts_norm.keys()), list(counts_norm.values())
            
            full_path  = outpath + '/histogram.txt'
            with open(full_path,'w') as file:
                file.write(f'Bonds per Molecule\tFrequency\n')
                for i in range(len(bonds)):
                    file.write(f'{bonds[i]}\t{freq[i]}\n')
            file.close()
            print(f'Wrote chart data! Output File: {full_path}')
            self.plotBondsPerMolecule(counts_norm, title_str, mol_str)

        else:
            full_path  = outpath + '/radius_of_gyration.txt'
            with open(full_path,'w') as file:
                file.write(f'Cluster Size\tRaiuds of Gyration\n')
                for i in range(len(csList)):
                    file.write(f'{csList[i]}\t{rgList[i]}\n')
            file.close()
            print(f'Wrote chart data! Output File: {full_path}')
            self.plotRg(csList, rgList, title_str)

       
'''
files = glob('C:/Users/chatt/Desktop/pytest/springsalad/test_dataset/A5_B5_flex_3nm_2nm_count_40_SIM_FOLDER/A5_B5_flex_3nm_2nm_count_40_SIM.txt')        

for txtfile in files[:]:
    cd = ClusterDensity(txtfile, ss_timeSeries=[ 0.02, 0.04])
    cd.getCD_stat(cs_thresh=1)
    
'''





