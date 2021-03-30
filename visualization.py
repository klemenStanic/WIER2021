import networkx as nx
from app.models import *
import matplotlib.pyplot as plt

session = Session(engine)

graph = nx.DiGraph()

sites = session.query(Site).all()
pages = session.query(Page).all()
links = session.query(Link).all()[:1000]

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


e_1 = [(u, v) for (u, v, d) in graph.edges(data=True) if 1 < d["weight"] <= 50]
e_2 = [(u, v) for (u, v, d) in graph.edges(data=True) if 50 < d["weight"] <= 100]
e_3 = [(u, v) for (u, v, d) in graph.edges(data=True) if 100 < d["weight"]]


pos = nx.spring_layout(graph, seed=7)  # positions for all nodes - seed for reproducibility

# nodes
nx.draw_networkx_nodes(graph, pos, node_size=700)

# edges
nx.draw_networkx_edges(graph, pos, edgelist=e_1, width=4)
nx.draw_networkx_edges(graph, pos, edgelist=e_1, width=8)
nx.draw_networkx_edges(graph, pos, edgelist=e_1, width=16)


# labels
nx.draw_networkx_labels(graph, pos, font_size=20, font_family="sans-serif")

ax = plt.gca()
plt.axis("off")
plt.tight_layout()
plt.show()



"""
pos = nx.spring_layout(graph) #there are other layouts that you might want to try.
nx.draw_networkx_nodes(graph, pos, node_color='blue')
plt.show()
"""

