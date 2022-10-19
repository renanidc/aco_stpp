import math
import random
import numpy
import networkx as nx 
import generate_graphs

G = generate_graphs.create_instance()

num_ants = 6
taxa_evaporação = 3
max_iteracoes = 100
iteracao = 0
source = 'a'
target = 'w'
solutions = []

feromonios = nx.get_edge_attributes(G,'feromonio')
pesos = nx.get_edge_attributes(G,'weight')
visitados = []
colors_visited = []

def atualiza_trilha_feromonio():
    print('atualiza feromonio...')

def atualiza_solucoes():
    ant = {'caminho':[], custo: 0, cores:['blue', 'blue', 'red', 'green']}

def escolhe_proximo_no(vizinhos, start_node, colors):
    
    no_escolhido_peso = 999
    no_escolhido_feromonio = -1
    
    # faz busca aleatória
    try:
        vizinhos = dict(vizinhos)
        vizinho_aleatorio = list(vizinhos.keys())
        #print(f'esses são os vizinhos: {list(vizinhos.keys())}')
        # remover nos visitados da lista e seleciona um vizinho aleatorio  
        vizinho_aleatorio = list(set(vizinho_aleatorio) - set(visitados))
        vizinho_aleatorio = random.choice(vizinho_aleatorio)
        visitados.append(vizinho_aleatorio)

        #print(f'visitados: {visitados}')
        return vizinho_aleatorio, colors[vizinho_aleatorio], int(vizinhos[vizinho_aleatorio]['weight']), 'valid'
    except:
        #print('entrou em um circuito! solução inválida')
        return 'w', colors['w'], 999, 'invalid'

# a formiga parte da colônia e vai até o destino (voltando pelo mesmo caminho e atualizando a trilha de feromônios)  
def busca_caminho():
    #print('busca caminho...')
    
    caminho = []
    custo = 0
    cores_visitadas = []
    
    #nodes = list(G.nodes())
    start_node = 'a'
    final_node = 'w'
    #print(f'start_node: {start_node}')
    
    # encontrar vizinhos do nó inicial
    vizinhos = G[start_node]
    #print(vizinhos)
    
    # encontrar cores de todos os nós
    colors = nx.get_node_attributes(G, "color")
    #print(colors)
    
    # inicializar variaveis com os valores do ponto inicial (colonia)
    no_escolhido = start_node
    caminho.append(start_node)
    visitados.append(start_node)
    #colors_visited.append(colors[start_node])
    cores_visitadas.append(colors[start_node])
    
    while(no_escolhido != final_node):
        
        no_escolhido, cor, peso, status = escolhe_proximo_no(vizinhos, start_node, colors)
        
        cores_visitadas.append(cor)
        custo = custo + peso
        
        #print(f'no_escolhido: {no_escolhido}')
        vizinhos = G[no_escolhido]
        caminho.append(no_escolhido)
        #print(f'caminho: {caminho}')
    
    #adicionar solução no conjunto
    solution = {} 
    solution['caminho'] = caminho
    solution['custo'] = custo
    solution['cores'] = cores_visitadas
    solution['status'] = status 
    #print(f'solução: {solution}\n')
    
    # limpar trilha de visitados
    del visitados[:]
    visitados.append(start_node)
    
    return solution

for i in range(0,10000):
    solution = busca_caminho()
    solutions.append(solution)

#print(solutions)

# find best_solution
def find_best_solution():
    min_custo = 9999
    max_cores = -1
    best_ant = None

    for ant in solutions:
        if(ant['custo'] <= min_custo and len(set(ant['cores']))>= max_cores and ant['status'] == 'valid'):
            best_ant = ant
            min_custo = ant['custo']
            max_cores = len(set(ant['cores']))

    return best_ant

best_ant = find_best_solution()
print(best_ant)


# exibir grafo com a melhor solução encontrada

# Importa uma biblioteca para gerar figuras e gráficos
import matplotlib.pyplot as plt

plt.figure(figsize=(8,12))

# Guarda os pesos de cada aresta em um dicionário
pesos = nx.get_edge_attributes(G,'weight')

# Guarda as cores de cada nó do grafo
g_colors = nx.get_node_attributes(G,'color')

colors = []
for node in g_colors:
    colors.append(g_colors[node])

# Separa as arestas que fazem parte do menor caminho e guarda em arestas_vermelhas
best_path = best_ant['caminho']
arestas_vermelhas = list(zip(best_path,best_path[1:]))

# Marca os vértices que estão no CCM para serem pintados de azul e os outros de branco
#cor_vertices = ['yellow' if not node in best_path else 'green' for node in G.nodes()]

# Marca as arestas que estão no CCM para serem pintados de vermelho e as outras de preto
cor_arestas = ['black' if not edge in arestas_vermelhas and not tuple(reversed(edge)) in arestas_vermelhas else 'red' for edge in G.edges()]

# Calcula automaticamente a posição de cada vértice 
# Note que as posições mudam de uma execução para a outra, dá para fazer diferente
# e fixar cada posição

pos=nx.spring_layout(G) 

# Prepara os vértices para serem desenhados usando as cores pré-determinadas e o tamanho 800
nx.draw_networkx(G, pos,node_color= colors,edge_color= cor_arestas, node_size=800)

# Preparar para mostrar os pesos de cada aresta (sem isso mostra apenas as linhas)
nx.draw_networkx_edge_labels(G, pos, edge_labels=pesos)

# Mostra o grafo
plt.show()

