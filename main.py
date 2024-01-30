import networkx as nx
import matplotlib.pyplot as plt

# Cria grafo vazio
G = nx.Graph()

# Adiciona vértices
G.add_node('v1')
G.add_node('v2')
G.add_node('v3')
G.add_node('v4')
G.add_node('v5')

# Adiciona arestas
G.add_edge('v1', 'v2')
G.add_edge('v2', 'v3')
G.add_edge('v3', 'v4')
G.add_edge('v4', 'v5')
G.add_edge('v5', 'v1')
G.add_edge('v2', 'v4')

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
print("O grau do vértice v2 é %d" %G.degree()['v2'])

# Grafo como lista de adjacências
print("Grafo como lista de adjacências")
print(G['v1'])
print(G['v2'])
print(G['v3'])
print(G['v4'])
print(G['v5'])
input()

# OBtém a matriz de adjacências do grafo G
print("Matriz de adjacências de G")
A = nx.adjacency_matrix(G) # Retorna uma matriz esparsa para economizar memória
print(A.todense()) # Converte para matriz densa (padrão)

# Adiciona um campo peso em cada aresta do grafo
G['v1']['v2']['peso'] = 5
G['v2']['v3']['peso'] = 10
G['v3']['v4']['peso'] = 2
G['v4']['v5']['peso'] = 7
G['v5']['v1']['peso'] = 4
G['v2']['v4']['peso'] = 8

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
