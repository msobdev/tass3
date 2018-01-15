import networkx as nx
import matplotlib.pyplot as plt
import polon.getting_data as polon

csvFilePath = "../polon/"

def drawGraph(G):
    pos = nx.spring_layout(G)
    edge_labels = nx.get_edge_attributes(G, 'weight')
    nx.draw(G, pos=pos, with_labels=True, label_pos=0.5)
    nx.draw_networkx_edge_labels(G, pos=pos, edge_labels = edge_labels)
    plt.show()

def addAuthors(G, nodes):
    for node in nodes:
        name = node.split("/")
        weight = G.get_edge_data(name[0], name[1], default=0.0)
        if weight != 0.0:
            G.add_edge(name[0], name[1], weight=weight['weight'] + 1.0)
        else:
            G.add_edge(name[0], name[1], weight=1.0)

def addPublicists(G, nodes):
    for node in nodes:
        name = node.split("/")
        name2 = name[1].split("-")
        weight = G.get_edge_data(name[0], name2[0], default=0.0)
        if weight == 0.0:
            G.add_edge(name[0], name2[0], weight=float("0."+name2[1]))

def addNodes(G, authors, publicists):
    addPublicists(G, publicists)
    addAuthors(G, authors)

def getPublicistsFromCsv(csvFile):
    patents = polon.getPatentsList(csvFile, polon.myFieldnames2)
    publicists = []
    for patent in patents:
        publicists.extend(patent.get('publicists').split(";"))
    return publicists

def generatePairsFromList(nodes):
    result = []
    for p1 in range(len(nodes)):
        for p2 in range(p1 + 1, len(nodes)):
            result.extend([nodes[p1]+"/"+nodes[p2]])
    return result

def getPatentsAuthors(csvFile):
    patents = polon.getPatentsList(csvFile, polon.myFieldnames2)
    patentsAuthors = []
    for patent in patents:
        temp = []
        for author in patent.get('publicists').split(";"):
            temp.append(author.split('/')[0])
        temp = list(set(temp))
        for authors in temp:
            if len(temp) == 1:
                patentsAuthors.append(authors+"/"+authors)
        patentsAuthors.extend(generatePairsFromList(temp))
    return patentsAuthors

def createGraph(csvFile):
    G = nx.Graph()
    publicists = getPublicistsFromCsv(csvFile)
    patentsAuthors = getPatentsAuthors(csvFile)
    addNodes(G, patentsAuthors, publicists)
    drawGraph(G)


createGraph(csvFilePath + "test2.csv")