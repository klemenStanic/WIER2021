import networkx as nx
from app.models import *
import matplotlib.pyplot as plt

session = Session(engine)

graph = nx.DiGraph()

sites = session.query(Site).all()
links = session.query(Link).all()#[:1000]

for site in sites:
    graph.add_node(site.domain)

c = 0
n = len(links)

for link in links:
    print(f'{c}/{n}\r', end='')
    from_page = session.query(Page).filter(Page.id==link.from_page).first()
    from_site = [i for i in sites if i.id == from_page.site_id][0].domain
    to_page = session.query(Page).filter(Page.id==link.to_page).first()
    to_site = [i for i in sites if i.id == to_page.site_id][0].domain

    if not graph.has_edge(from_site, to_site):
        graph.add_edge(from_site, to_site, weight=1)
    else:
        data = graph.get_edge_data(from_site, to_site)
        graph.add_edge(from_site, to_site, weight=data['weight']+1)
    c += 1


# -------------------------------------------------------------------------------
pos = nx.spring_layout(graph)
all_weights = []
for (node1, node2, data) in graph.edges(data=True):
    all_weights.append(data['weight'])  # we'll use this when determining edge thickness

# 4 b. Get unique weights
unique_weights = list(set(all_weights))
all_edges = [(node1, node2, edge_attr['weight']) for (node1, node2, edge_attr) in graph.edges(data=True)]

print("calculating edge sizes")
# 4 c. Plot the edges - one by one!
for weight in unique_weights:
    # 4 d. Form a filtered list with just the weight you want to draw
    weighted_edges = []
    print(f'{len(all_edges)}\r')
    i = 0
    while i < len(all_edges):
        if all_edges[i][2] == weight:
            weighted_edges.append((all_edges[i][0], all_edges[i][1]))
            all_edges.pop(i)
        i += 1

    #weighted_edges = [(node1, node2) for (node1, node2, edge_attr) in graph.edges(data=True) if edge_attr['weight'] == weight]
    # 4 e. I think multiplying by [num_nodes/sum(all_weights)] makes the graphs edges look cleaner
    width = weight * graph.number_of_nodes() * 5.0 / sum(all_weights)
    nx.draw_networkx_edges(graph, pos, edgelist=weighted_edges, width=width)



# nodes
nx.draw_networkx_nodes(graph, pos, node_size=100)
nx.draw_networkx_nodes(graph, pos, nodelist=['www.gov.si', 'evem.gov.si', 'e-uprava.gov.si','e-prostor.gov.si'], node_size=100, node_color='red')


# labels
nx.draw_networkx_labels(graph, pos, font_size=10, font_family="sans-serif")

sites = None
pages = None
links = None

ax = plt.gca()
plt.axis("off")
plt.tight_layout()
#plt.savefig('images/network_graph.png')
plt.show()
