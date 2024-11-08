import networkx as nx
import os
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import glob
import pandas as pd
from progress.bar import ChargingBar

def read_db_structures(filename):
    #only reads first structure
    # Open the .db file
    with open(filename, 'r') as file:
        # Read the lines
        lines = file.readlines()

    names = []
    seqs = []
    pairs = []
    for line in lines:
        if line[0] == '>':
            names.append(line[1:])
        elif line[0] in ['A','C','G','U','a','c','g','u']:
            seq = list(line)[:-1]
        elif line[0] in ['.','(',')']:
            seqs.append(seq)
            pairs.append(list(line)[:-1])

    return names,seqs,pairs

def read_ct_structures(file,prefix):

    # Open the .ctfile
    with open(file, 'r') as file:
        # Read the lines
        lines = file.readlines()

    #Make list of structures with each structure being a list of lines split into the CT columns.
    S= []
    Stemp = ['Null']
    names = []
    for line in lines:

        #separate structures based on some notable "prefix" that appears in each structre title ('#' in Seismic)
        if prefix in line:

            S.append(Stemp)
            Stemp = []
            names.append(line.split()[1])

        else:
            Stemp.append(line.split())

    S.append(Stemp)
    file.close()

    S = S[1:]

    return(names,S)

def create_db_graph(seq,pair,colors):
    #generate empty graph
    G = nx.Graph()

    #create node at infinity
    G.add_node(0,base='N',label='O',color = colors[0])

    #add nodes for each base
    for x in range(len(seq)):

        G.add_node(x+1,base=seq[x],color = colors[x+1])

    #create "pending" list to pair appropriately.
    pending=[]

    for x in range(len(pair)):
        G.add_edge(x,x+1,color='#642FDB') #from 0 at infinity to 1, then 1 to 2 etc. up to last base

        #Adds a connection point is open brackett
        if pair[x] == '(':
            pending.append(x+1)

        #Connects node to last open brackett from the pending list. 
        elif pair[x] == ')':
            G.add_edge(pending[-1],x+1,color = '#E9913F')
            pending = pending[:-1]

        #ignores if not a brackett i.e. a dot
        else:
            pass

    #G.add_edge(x+1,0)
        
    return G

def conGraphStep(G,line, ROCAUC, color):

    G.add_node(int(line[0]), base = line[1], label = ROCAUC, color = color)

    G.add_edge(int(line[0]),int(line[2]),color = '#642FDB')

    if int(line[0]) < int(line[4]):

        G.add_edge(int(line[0]),int(line[4]), color = '#E9913F')

    return

def create_ct_graph(struc,AUC,colors):
    #generate empty graph
    G = nx.Graph()

    #create node at infinity
    G.add_node(0,base='N',label = 'O',color = colors[0])


    if isinstance(AUC, np.ndarray):# == False:
        for x in range(len(struc)):

            #Adds new node for each base and relevant connected edges
            conGraphStep(G,struc[x],AUC[x],colors[x+1])


    else:
        for x in range(len(struc)):

            #Adds new node for each base and relevant connected edges
            conGraphStep(G,struc[x],'',colors[x+1])

        
    return G

def plotGraph(G,name,color,node_size,bases,view,edge_color,**kwargs):

    args = dict(kwargs.items())

    plt.rcParams["figure.figsize"] = (15,15)

    try:
        pos = args['pos']
        
    except:
        pos = nx.kamada_kawai_layout(G)

    if edge_color == True:
        edge_colors = [G.edges[n]['color'] for n in G.edges]
    else:
        edge_colors = ['black' for n in G.edges]

    if color == None:
        
        nx.draw(G,pos,with_labels=False,node_size = node_size, edge_color = edge_colors)

    else:
        node_colors = [G.nodes[n]['color'] for n in G.nodes]
        nx.draw(G,pos,with_labels=False,node_size = node_size,node_color=node_colors,cmap=sns.color_palette("viridis", as_cmap=True), edge_color = edge_colors)

    if bases == True:
        #Label nodes with base
        labels = nx.get_node_attributes(G, 'base')
        nx.draw_networkx_labels(G, pos, labels)

    plt.savefig('Structures/'+name+'.svg')
    plt.savefig('Structures/'+name+'.png')

    if view == True:
        plt.show()

    plt.close()

    return(pos)

def plotGraph3D(G,name,view,**kwargs):

    args = dict(kwargs.items())

    try:
        pos = args['pos']
        
    except:
        pos = nx.kamada_kawai_layout(G,dim = 3)

    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    for node, coords in pos.items():
        ax.scatter(coords[0], coords[1], coords[2], label=node,color = 'black')

    for edge in G.edges():
        node1 = edge[0]
        node2 = edge[1]
        x = [pos[node1][0], pos[node2][0]]
        y = [pos[node1][1], pos[node2][1]]
        z = [pos[node1][2], pos[node2][2]]
        ax.plot(x, y, z, color='gray')

    #for node, coords in pos.items():
        #ax.text(coords[0], coords[1], coords[2], node, color='red')

    plt.savefig('Structures/3D_'+name+'.svg')
    plt.savefig('Structures/3D_'+name+'.png')

    if view == True:
        plt.show()

    plt.close()

    return(pos)

    
################################################################################

#Create Graph from file
def graph(filename,**kwargs):

    newpath = r'Structures' 
    if not os.path.exists(newpath):
        os.makedirs(newpath)

    args = dict(kwargs.items())

    try:
        num_strucs = args['num_strucs']
        
    except:
        num_strucs = 1

    try:
        prefix = args['prefix']
        
    except:
        prefix = '#'

    #plot color default:none
    try:
        color = args['color']
        color_type = 'varna'
    except:
        color = None
        color_type = None

    #plot bases default:false
    try:
        bases = args['bases']
    except:
        bases = False

    #node size default:10
    try:
        node_size = args['node_size']
    except:
        node_size = 10

    #view graph default:False
    try:
        view = args['view']
    except:
        view = False

    #view graph default:10
    try:
        edge_color = args['edge_color']
    except:
        edge_color = True

    try:
        dim = args['dim']
        
    except:
        dim = 2



    #read in file if dot-bracket
    if filename[-2:]=='db':
    
        names,seqs,pairs = read_db_structures(filename)

    #read in file if connectivity table
    elif filename[-2:] == 'ct':
        
        names, seqs = read_ct_structures(filename,prefix)

    #read in colors from varna file
    if color_type == 'varna':
        with open(color, 'r') as file:
            # Read the lines
            colors = file.readlines()
        newcolors = [0.25]
        for x in range(len(colors)):
            newcolors.append((float(colors[x][:-2])+1)/2)
        file.close()

    else:
        newcolors = np.zeros(len(seqs[0])+1)


    graphs = []
    
    if filename[-2:]=='db':
        
        if num_strucs == 'all':
            num_strucs = len(pairs)
            
        for x in range(num_strucs):
            try:
                G = create_db_graph(seqs[x],pairs[x],newcolors)
                graphs.append(G)
            except:
                break


    elif filename[-2:] == 'ct':

        if num_strucs == 'all':
            num_strucs = len(seqs)
        
        for x in range(num_strucs):

            try:
                G = create_ct_graph(seqs[x],'',newcolors)
                graphs.append(G)

            except:
                break

    
    positions = []
    for x in range(len(graphs)):

        pos = plotGraph(graphs[x],names[x],color,node_size,bases,view,edge_color)
        
        positions.append(pos)

    return

################################################################################

#Create Graph from file
def graph3D(filename,**kwargs):

    newpath = r'Structures' 
    if not os.path.exists(newpath):
        os.makedirs(newpath)

    args = dict(kwargs.items())

    try:
        num_strucs = args['num_strucs']
        
    except:
        num_strucs = 1

    try:
        prefix = args['prefix']
        
    except:
        prefix = '#'

    #plot color default:none
    try:
        color = args['color']
        color_type = 'varna'
    except:
        color = None
        color_type = None

    #plot bases default:false
    try:
        bases = args['bases']
    except:
        bases = False

    #node size default:10
    try:
        node_size = args['node_size']
    except:
        node_size = 10

    #view graph default:False
    try:
        view = args['view']
    except:
        view = True

    #view graph default:10
    try:
        edge_color = args['edge_color']
    except:
        edge_color = True


    #read in file if dot-bracket
    if filename[-2:]=='db':
    
        names,seqs,pairs = read_db_structures(filename)

    #read in file if connectivity table
    elif filename[-2:] == 'ct':
        
        names, seqs = read_ct_structures(filename,prefix)

    #read in colors from varna file
    if color_type == 'varna':
        with open(color, 'r') as file:
            # Read the lines
            colors = file.readlines()
        newcolors = [0.25]
        for x in range(len(colors)):
            newcolors.append((float(colors[x][:-2])+1)/2)
        file.close()

    else:
        newcolors = np.zeros(len(seqs[0])+1)


    graphs = []
    
    if filename[-2:]=='db':
        
        if num_strucs == 'all':
            num_strucs = len(pairs)
            
        for x in range(num_strucs):
            try:
                G = create_db_graph(seqs[x],pairs[x],newcolors)
                graphs.append(G)
            except:
                break


    elif filename[-2:] == 'ct':

        if num_strucs == 'all':
            num_strucs = len(seqs)
        
        for x in range(num_strucs):

            try:
                G = create_ct_graph(seqs[x],'',newcolors)
                graphs.append(G)

            except:
                break

    
    positions = []
    for x in range(len(graphs)):

        pos = plotGraph3D(graphs[x],names[x],view)
        
        positions.append(pos)

    return

################################################################################
################################################################################
################################################################################
################################################################################
################################################################################
################################################################################
'''
Cloning Calc
'''
def Cloning():
    vol=float(input("Volume to fill: "))

    x=0

    while x==0:
        ins=input("Number of inserts: ")

        try:
            ins=int(ins)
            x=1

        except:
            pass


    C=[]
    M=[]
    C.append(float(input("Concentration of Vector: ")))
    M.append(float(input("Bp of Vector: ")))

    for x in range(0,ins):
        st1="Concentration of Insert "+str(x+1)+": "
        st2="Bp of Insert "+str(x+1)+": "

        C.append(float(input(st1)))
        M.append(float(input(st2)))


    V=[1]

    for x in range(1,ins+1):

        V.append(3*C[0]*M[x]/M[0]/C[x])

    tot=0
    for x in V:
        tot+=x

    rat=vol/tot

    print("\n\n\n\n\n")

    print("Vector: ",rat*V[0])
    for x in range(1,ins+1):
        print("Insert ",x,": ",rat*V[x])


    return()

################################################################################
################################################################################
################################################################################
################################################################################
################################################################################
################################################################################
'''
ddPCR Plotting
'''
def PlotAmp(files,output):

    bar = ChargingBar('Processing', max=len(files)+3, suffix = '%(percent).1f%% - %(eta)ds')

    df = pd.DataFrame(columns = ['Ch1 Amplitude','Ch2 Amplitude','Cluster','Well'])
    for file in files:

        bar.next()

        well = file.split('_')[-2]

        dfTemp = pd.read_csv(file)

        dfTemp['Well'] = well       

        df = pd.concat([df,dfTemp],ignore_index = True)

        sns.scatterplot(data = dfTemp, x = 'Ch1 Amplitude', y = 'Ch2 Amplitude', hue =  'Cluster',edgecolor = None,palette = 'viridis')
        plt.xlim(0,12000)
        plt.ylim(0,10000)
        plt.savefig(output+'/Amplitude/'+well+'_2D_Amp.png')
        plt.savefig(output+'/Amplitude/'+well+'_2D_Amp.svg')
        plt.close()

    bar.next()

    category_positions = {category: i for i, category in enumerate(df['Well'].unique())}

    ax = sns.stripplot(data = df, x = 'Well', y = 'Ch1 Amplitude',hue = 'Cluster',jitter = 0.5,legend = False,palette = 'viridis')
    for category, position in category_positions.items():
        ax.axvline(x=position+0.5, color='red', linestyle='--')
    plt.savefig(output+'/Amplitude/1D_Ch1_Amp.png')
    plt.savefig(output+'/Amplitude/1D_Ch1_Amp.svg')
    plt.close()

    bar.next()

    ax = sns.stripplot(data = df, x = 'Well', y = 'Ch2 Amplitude',hue = 'Cluster',jitter = 0.5,legend = False,palette = 'viridis')
    for category, position in category_positions.items():
        ax.axvline(x=position+0.5, color='red', linestyle='--')
    plt.savefig(output+'/Amplitude/1D_Ch2_Amp.png')
    plt.savefig(output+'/Amplitude/1D_Ch2_Amp.svg')
    plt.close()

    bar.next()
    bar.finish()

    
    
    return


def ddPCR_amp(folder, output):

    output = output+'/Figures'

    if not os.path.exists(output):
        os.makedirs(output)
        os.makedirs(output+'/Amplitude')
        os.makedirs(output+'/Ratios')
        
    files = glob.glob(folder+'/*Amplitude.csv')

    PlotAmp(files,output)
    

    return


###############################################################################
#import human readable plate map and convert into computer readable df
def meta(file):

    df = pd.DataFrame()

    df['Well'] = ['A1','A2','A3','A4','A5','A6','A7','A8','A9','A10','A11','A12',
                  'B1','B2','B3','B4','B5','B6','B7','B8','B9','B10','B11','B12',
                  'C1','C2','C3','C4','C5','C6','C7','C8','C9','C10','C11','C12',
                  'D1','D2','D3','D4','D5','D6','D7','D8','D9','D10','D11','D12',
                  'E1','E2','E3','E4','E5','E6','E7','E8','E9','E10','E11','E12',
                  'F1','F2','F3','F4','F5','F6','F7','F8','F9','F10','F11','F12',
                  'G1','G2','G3','G4','G5','G6','G7','G8','G9','G10','G11','G12',
                  'H1','H2','H3','H4','H5','H6','H7','H8','H9','H10','H11','H12']

    xls = pd.ExcelFile(file)

    sheets = xls.sheet_names

    for sheet in sheets:

        with pd.ExcelFile(file) as xls:
            dfTemp = pd.read_excel(xls,sheet)

            dfTemp = dfTemp.set_index('Unnamed: 0')
            dfTemp = dfTemp.reset_index().melt(id_vars='Unnamed: 0', var_name='Column', value_name=sheet)
            dfTemp['Well'] = dfTemp['Unnamed: 0']+dfTemp['Column'].astype(str)

            dfTemp = dfTemp.drop(columns=['Unnamed: 0','Column'])

            df = pd.merge(df, dfTemp, on='Well')

    return(df)
