list_node = [
    "Western Australia", "Northern Territory", "South Australia",
    "Queensland", "New South Wales", "Victoria",
    "Tasmania"
]
list_constraint = [
    ("Western Australia", "Northern Territory"),
    ("Western Australia", "South Australia"),
    ("South Australia", "Northern Territory"),
    ("Queensland", "Northern Territory"),
    ("Queensland", "South Australia"),
    ("Queensland", "New South Wales"),
    ("New South Wales", "South Australia"),
    ("Victoria", "South Australia"),
    ("Victoria", "New South Wales"),
    # ("Victoria", "Tasmania")
]

if __name__ == '__main__':
    import networkx as nx
    import matplotlib.pyplot as plt
    G = nx.Graph()
    G.add_nodes_from(list_node)
    G.add_edges_from(list_constraint)
    # G.node['Western Australia']['color'] = 'red'
    # print(G.nodes(data=True))
    nx.draw(G)
    plt.savefig("path.png")
