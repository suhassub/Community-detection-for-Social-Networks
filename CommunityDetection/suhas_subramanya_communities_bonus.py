import networkx as nx
import community as cm
import re
import matplotlib.pyplot as plt
from random import random
import sys


def communities_main():
    filename=sys.argv[1]
    fil = open(filename, 'r')
    G=nx.Graph()
    GCopy=nx.Graph()
    modularity_dictionary={}
    modularval_graph={}

    for line in fil:
        splitvalues=line.split(" ")
        G.add_edge(int(splitvalues[0]),int(re.sub('\n','',splitvalues[1])))
        GCopy.add_edge(int(splitvalues[0]),int(re.sub('\n','',splitvalues[1])))

    for eachnode in G.nodes():
        modularity_dictionary[eachnode]=1
    mod_value=calculate_modularity(GCopy,modularity_dictionary)
    for each in modularity_dictionary.iteritems():
        modularval_graph[each[0]]=each[1]


    while(G.number_of_edges()>0):
        Girvannewman(G)
        modularity_dictionary.clear()
        count=1
        for eachconnected in nx.connected_components(G):
            for eachnode in eachconnected:
                modularity_dictionary[eachnode]=count
            count+=1
        mod_values=calculate_modularity(GCopy,modularity_dictionary)
        if mod_values>mod_value:
            mod_value=mod_values
            for each in modularity_dictionary.iteritems():
                modularval_graph[each[0]]=each[1]


    printdictionary={}
    for each in modularval_graph.iteritems():
        if printdictionary.__contains__(each[1]):
            commlist=printdictionary[each[1]]
            commlist.append(each[0])
            printdictionary[each[1]]=commlist
        else:
            commlist=[]
            commlist.append(each[0])
            printdictionary[each[1]]=commlist
    for key,value in sorted(printdictionary.iteritems()):
        print sorted(printdictionary[key])


    val_map={}
    count=1
    for key,value in printdictionary.iteritems():
        rand_value=random()
        for each in value:
            val_map[each]=count
        count+=1


    values = [val_map.get(node, 0.25) for node in GCopy.nodes()]
    nx.draw(GCopy, cmap = plt.get_cmap('jet'), node_color = values)


    plt.savefig(sys.argv[2])



def calculate_modularity(G,modularity_dictionary):
    value=cm.modularity(modularity_dictionary,G)
    return value


def Girvannewman(G):
    initialcomp = nx.number_connected_components(G)
    '''totalnumcomp = initialcomp
    while totalnumcomp <= initialcomp:'''
    bw = edge_betweenness(G)
    '''nx.edge_betweenness_centrality(G)'''
    maximum_value = max(bw.values())
    for key, value in bw.iteritems():
        if float(value) == maximum_value:
            G.remove_edge(key[0],key[1])
    totalnumcomp = nx.number_connected_components(G)



#*********** To Calculate Edge betweenness **************
def edge_betweenness(G):
    betweennessdict={}
    for each in G.nodes():
        directedGraph=ConstructDFS(G,each)
        numbofShortest={}
        for eachnode in directedGraph.nodes():
            numbofShortest[eachnode]=0
        numbofShortestPaths(directedGraph,each,numbofShortest)
        betweenness={}
        contributionofeachnode={}
        for eachnode in directedGraph.nodes():
            contributionofeachnode[eachnode]=1
        contributionofeachnode[each]=0
        CalulateEdgebetweenness(directedGraph,each,numbofShortest,betweenness,contributionofeachnode)
        for eachedge in betweenness:
            if eachedge not in betweennessdict:
                betweennessdict[eachedge]=0
            betweennessdict[eachedge]=betweennessdict[eachedge]+betweenness[eachedge]
    for eachedge in betweennessdict:
        betweennessdict[eachedge]=betweennessdict[eachedge]/2
    return betweennessdict


def CalulateEdgebetweenness(G,source,numbofShortest,betweenness,contributionofeachnode):
    childnodes=G.neighbors(source)
    if(len(childnodes)==0):
        return
    for eachchild in childnodes:
        if tuple(sorted((source,eachchild))) in betweenness:
            continue
        betweenness[tuple(sorted((source,eachchild)))] = 0
        CalulateEdgebetweenness(G,eachchild,numbofShortest,betweenness,contributionofeachnode)
        eachedgebetweenness = float(contributionofeachnode[eachchild])/float(numbofShortest[eachchild])
        edge = tuple(sorted([source,eachchild]))
        betweenness[edge] = betweenness[edge] + eachedgebetweenness
        contributionofeachnode[source] = contributionofeachnode[source] +eachedgebetweenness


def ConstructDFS(G,root):
    currentdictionary={}
    currentdictionarycopy={}
    level={}
    visited=[]
    diG=nx.DiGraph()
    diG.add_node(root)
    currentdictionary[root]=1
    level[root]=1
    count=2

    while len(currentdictionary)>=1:
        for eachnode in currentdictionary.iteritems():
            visited.append(eachnode[0])
            for eachchild in getchildnodes(G,eachnode):
                if (visited.__contains__(eachchild)):
                    diG.add_node(eachchild)
                    continue;
                if (level.has_key(eachchild) and level[eachchild]!=level[eachnode[0]]) or not level.has_key(eachchild):
                    diG.add_edge(eachnode[0],eachchild)
                    currentdictionarycopy[eachchild]=1
                    level[eachchild]=count
        count=count+1
        currentdictionary={}
        currentdictionary=currentdictionarycopy
        currentdictionarycopy={}
    return diG


def getchildnodes(G,eachnode):
    listofchildnodes=[]
    '''flag=0
    for eachedge in G.edges():
        if eachnode[0] == eachedge[0]:
            flag=1
            break
    if(flag==1):'''
    for each in G.neighbors(eachnode[0]):
            listofchildnodes.append(each)
    return  listofchildnodes


def numbofShortestPaths(G,eachnode,numofShortestPath):
    for each in G.edges():
        if(each[1]!=None):
            numofShortestPath[each[1]]=numofShortestPath[each[1]]+1

    return numofShortestPath
#***************** To Calculate Edge betweenness *******************



communities_main()