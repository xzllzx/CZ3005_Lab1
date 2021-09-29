import json
import pandas
import networkx as nx
import matplotlib.pyplot as plt
from itertools import combinations
from timeit import default_timer as timer
from math import log

def checkAuthors():
    df = pandas.read_csv('dataset/Faculty_xml.csv', header=0)
    col_a = set(df.Faculty)
    try:
        with open("dataset/article.json", encoding="utf8") as json_file:
            list_of_authors = []
            dict_of_authors = {}
            data = json.load(json_file)
            counter = 0
            zero = 0
            onevsone = 0
            printcount = 0
            for key in data:
                if data[key]['publication_type'] == 'proceedings':
                    author_list = data[key]['editor']
                else:
                    author_list = data[key]['author']
                #scse_author_list = [author for author in author_list if author in col_a]
                #scse_author_list = set(author_list) & col_a
                scse_author_list = (col_a).intersection(author_list)
                #print(data[key]['author'])
                if len(scse_author_list)>2:
                    #print(scse_author_list)
                    #print(list(combinations(scse_author_list, 2)))
                    #print(key)
                    for pair in list(combinations(scse_author_list, 2)):
                        if not pair in dict_of_authors:
                            dict_of_authors[pair] = 1
                        else:
                            dict_of_authors[pair] += 1
                    printcount += 1
                elif len(scse_author_list)>1:
                    #print(scse_author_list)
                    #print(list(combinations(scse_author_list, 2)))
                    temp_author_tuple = tuple(scse_author_list)
                    if not temp_author_tuple in dict_of_authors:
                        dict_of_authors[temp_author_tuple] = 1
                    else:
                        dict_of_authors[temp_author_tuple] += 1
                    onevsone += 1
                else:
                    zero += 1
                counter += 1
            print("zero: ", zero, "\nonevsone: ", onevsone, "\nprintcount: ", printcount)
            print("dict_of_authors: \n")
            #for key in dict_of_authors:
                #print("Authors: ", key, "Count: ", dict_of_authors[key], "\n")
            return dict_of_authors
            '''
            for i in range(0,len(data)-1):
                count = 0
                for j in data[i]['author']:
                    if j in col_a:
                        count += 1
                        if j not in list_of_authors:
                            list_of_authors.append(j)
                if count >= 2:
                    print("Collaboration success!")
                    print(data[i]['title'])
                    for j in data[i]['author']:
                        if j in col_a:
                            print(j)
                    print(data[i]['year'])
                #print(1)
            print(list_of_authors)
            '''
    except ValueError:
        print('Decoding JSON has failed')
        return
        
'''
Wholesale copied from https://networkx.org/documentation/stable//auto_examples/basic/plot_properties.html
'''
def graphProperties(G):
    pathlengths = []

    print("Source vertex {Target:Length, }")
    for v in G.nodes():
        spl = dict(nx.single_source_shortest_path_length(G, v))
        #print(f"{v} {spl} ")
        for p in spl:
            pathlengths.append(spl[p])

    print()
    print(f"Average shortest path length: {sum(pathlengths) / len(pathlengths)}")

    # histogram of path lengths
    dist = {}
    for p in pathlengths:
        if p in dist:
            dist[p] += 1
        else:
            dist[p] = 1

    print()
    print("Length #Paths")
    verts = dist.keys()
    for d in sorted(verts):
        print(f"{d} {dist[d]/2}")

    print(f"\nRadius: {nx.radius(G)}")
    print(f"Diameter: {nx.diameter(G)}")
    print(f"Eccentricity: {nx.eccentricity(G)}")
    print(f"Center: {nx.center(G)}")
    print(f"Periphery: {nx.periphery(G)}")
    print(f"Density: {nx.density(G)}")

def scseQ1Graph(dict):
    G = nx.Graph()
    nestedList = [(k[0], k[1], v) for k,v in dict.items()]
    #print(nestedList)
    #for author_pair in nestedList:
    #    G.add_edge(author_pair[0], author_pair[1], weight = author_pair[2])
    G.add_weighted_edges_from(nestedList)
    #G.edges(data=True)
    edges = G.edges()
    
    colors = [G[u][v]['color'] for u,v in edges]
    weights = [log(G[u][v]['weight'] + 0.5) for u,v in edges]

    '''Method 1'''
    pos = nx.spring_layout(G, seed = 140)
    nx.draw(G, pos, with_labels=True, font_size=6, edge_color=colors, width=weights)
    labels = nx.get_edge_attributes(G,'weight')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=labels, font_size=6)
    
    '''Method 2
    elarge = [(u, v) for (u, v, d) in G.edges(data=True) if d["weight"] > 3]
    esmall = [(u, v) for (u, v, d) in G.edges(data=True) if d["weight"] <= 3]

    #nodes
    nx.draw_networkx_nodes(G, pos, node_size=70)
    # edges
    nx.draw_networkx_edges(G, pos, edgelist=elarge, width=6)
    nx.draw_networkx_edges(G, pos, edgelist=esmall, width=6, alpha=0.5, edge_color="b", style="dashed")
    # labels
    nx.draw_networkx_labels(G, pos, font_size=20, font_family="sans-serif")'''

    #graphProperties(G)
    plt.tight_layout()
    plt.show()

def main():
    collab_dict = checkAuthors()
    G = scseQ1Graph(collab_dict)

    #G = nx.gnm_random_graph(10, 20)
    #graphProperties(G)
    '''start = timer()
    checkAuthors()
    end = timer()
    print("Time taken: " + str(end - start))'''

if __name__ == "__main__":
    main()