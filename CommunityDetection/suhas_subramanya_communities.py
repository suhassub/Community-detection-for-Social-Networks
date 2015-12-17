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
    for key,value in printdictionary.iteritems():
        print sorted(printdictionary[key])


    val_map={}
    count=1
    for key,value in sorted(printdictionary.iteritems()):
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
    bw = nx.edge_betweenness_centrality(G)
    maximum_value = max(bw.values())
    for key, value in bw.iteritems():
        if float(value) == maximum_value:
            G.remove_edge(key[0],key[1])
    totalnumcomp = nx.number_connected_components(G)


communities_main()