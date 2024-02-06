import networkx as nx
import matplotlib.pyplot as plt

G = nx.Graph()

autors = ["Felipe", "Thiago", "Gabriel", "Mateus", "Giovanna", "Leila", "Tadeu"]
patents = ["Computação", "Dengue", "COVID", "Variola", "Carnaval", "Álcool", "Direito"]

# Insere os nós no grafo
for i in autors:
  G.add_node(i)
for i in patents:
  G.add_node(i)

# Liga os nós
G.add_edge("Felipe", "Computação")
G.add_edge("Felipe", "Dengue")
G.add_edge("Thiago", "Dengue")
G.add_edge("Thiago", "COVID")
G.add_edge("Thiago", "Variola")
G.add_edge("Gabriel", "Álcool")
G.add_edge("Gabriel", "Carnaval")
G.add_edge("Mateus", "Direito")
G.add_edge("Mateus", "Computação")
G.add_edge("Giovanna", "Carnaval")
G.add_edge("Giovanna", "COVID")
G.add_edge("Leila", "Dengue")
G.add_edge("Tadeu", "Direito")

# Dicionário para adicionar cores aos nós
colors = {node: 'red' for node in autors}
colors.update({node: 'blue' for node in patents})

# Plota grafo
nx.draw(G, nx.spring_layout(G), with_labels=True, node_color=[colors[node] for node in G.nodes()], cmap=plt.cm.rainbow)
plt.show()

# Seleciona subgrafo com base em algum nó para plotar suas principais ligações
selectNode = "Dengue"
subgraph = nx.Graph(G.subgraph([selectNode] + list(G.neighbors(selectNode))))
nx.draw(subgraph, nx.spring_layout(G), with_labels=True, node_color=['red' if node == selectNode else 'gray' for node in subgraph.nodes()])
plt.show()