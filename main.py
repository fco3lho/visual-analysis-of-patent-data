import networkx as nx
import matplotlib.pyplot as plt

# Cria grafo vazio
G = nx.Graph()

peopleArray = ["pessoa1", "pessoa2", "pessoa3"]
patentsArray = ["patent1", "patent2", "patent3"]

# Adiciona vértices
for i in peopleArray:
  G.add_node(i)
for i in patentsArray:
  G.add_node(i)

# Adiciona arestas
G.add_edge('pessoa1', 'patent1')
G.add_edge('pessoa2', 'patent1')
G.add_edge('pessoa3', 'patent2')
G.add_edge('pessoa1', 'patent2')
G.add_edge('pessoa1', 'patent3')
G.add_edge('pessoa3', 'patent3')

# Lista os vértices
print('Lista de vértices')
print(G.nodes())
input()

# Percorre o conjunto de vértices
print('Percorrendo os vértices')
for v in G.nodes():
  print(v)
input()

# Lista os arestas
print('Lista de arestas')
print(G.edges())
input()

# Percorre o conjunto de arestas
print('Percorrendo os arestas')
for e in G.edges():
  print(e)
input()

# Mostra a lista de graus
print('Lista de graus de G')
print(G.degree())
input()

# Acessa o grau do vértice v2
print("O grau do vértice pessoa2 é %d" %G.degree()['pessoa2'])

# Grafo como lista de adjacências
print("Grafo como lista de adjacências")
print(G['pessoa1'])
print(G['pessoa2'])
print(G['pessoa3'])
print(G['patent1'])
print(G['patent2'])
print(G['patent3'])
input()

# Obtém a matriz de adjacências do grafo G
print("Matriz de adjacências de G")
A = nx.adjacency_matrix(G) # Retorna uma matriz esparsa para economizar memória
print(A.todense()) # Converte para matriz densa (padrão)

# Adiciona um campo peso em cada aresta do grafo
G['pessoa1']['patent1']['peso'] = 5
G['pessoa2']['patent1']['peso'] = 10
G['pessoa3']['patent2']['peso'] = 2
G['pessoa1']['patent2']['peso'] = 7
G['pessoa1']['patent3']['peso'] = 4
G['pessoa3']['patent3']['peso'] = 8

# Lista de cada aresta e seus respectivos pesos
print("Adicionando pesos nas arestas")
for edge in G.edges():
  u = edge[0]
  v = edge[1]
  print("O peso da aresta", edge, 'vale ', G[u][v]['peso'])
input()
print()

# Plotando o grafo como imagem
print("Plotando o grafo como imagem...")
plt.figure(1)
nx.draw_networkx(G, pos=nx.spring_layout(G), with_labels=True)
plt.show()
