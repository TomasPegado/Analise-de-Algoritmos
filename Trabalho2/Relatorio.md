# Relatório: Trabalho 2 - Grafo de Estados
- Bruno Wolf (2212576)
- Tomás Lenzi (2220711)

## Representação do Tabuleiro e Estruturas de Dados

Representamos o tabuleiro por uma tupla de 9 inteiros, onde cada inteiro corresponde a uma posição do tabuleiro 3x3. Os números de 1 a 8 representam as peças e o número 0 representa a casa vazia. Por exemplo, a configuração (1, 2, 3, 4, 5, 6, 7, 8, 0) representa o tabuleiro com a casa vazia no canto inferior direito.

Para montar o grafo de estados, são utilizadas as seguintes estruturas de dados:

- **Dicionário de configuração para número do nó**: mapeia cada configuração (tupla) para um índice único do nó.
- **Dicionário de número do nó para configuração**: permite recuperar a configuração original a partir do índice do nó.
- **Dicionário de adjacência**: armazena, para cada nó, a lista de nós vizinhos (configurações que podem ser alcançadas com um único movimento).

Essas estruturas permitem a construção eficiente do grafo, a busca de vizinhos e a navegação entre configurações.

## Criação do Grafo de Espaço de Estados

1) **Número de nós e arestas**

O grafo de espaço de estados do possui:

- **362880 nós** (todas as permutações possíveis das 9 posições, incluindo as não solúveis)
- **483840 arestas** (cada movimento possível entre configurações)

2) **Exemplo de dois nós conectados por uma aresta**

- Configuração 1: (1, 2, 3, 4, 5, 6, 7, 8, 0)
- Configuração 2: (1, 2, 3, 4, 5, 6, 7, 0, 8)
Essas duas configurações estão conectadas por uma aresta, pois é possível mover a peça 8 para a posição vazia em um único movimento.

3) **Exemplo de dois nós não conectados por uma aresta**

- Configuração 1: (1, 2, 3, 4, 5, 6, 7, 8, 0)
- Configuração 2: (1, 2, 3, 4, 5, 6, 0, 7, 8)
Essas duas configurações **não** estão conectadas diretamente por uma aresta, pois não é possível chegar de uma à outra em um único movimento.

---

## BFS para Contagem de Componentes Conexos

1) **Código principal da BFS**
```python
def bfs_componentes_conexos(self):
    visitado = set()
    componentes = 0
    for no in range(len(self.hash_no_para_cfg)):
        if no not in visitado:
            componentes += 1
            fila = [no]
            visitado.add(no)
            while fila:
                atual = fila.pop(0)
                for vizinho in self.adjacencia[atual]:
                    if vizinho not in visitado:
                        visitado.add(vizinho)
                        fila.append(vizinho)
    return componentes
```

2) **Número de componentes conexos**
- O grafo possui **2 componentes conexos**.

---

## Caminho Mais Curto

1) **Configuração inicial viável que necessita o maior número de movimentos para chegar à configuração final**
- Configuração: **(8, 6, 7, 2, 5, 4, 3, 0, 1)**

2) **Número de movimentos necessários para ir dessa configuração à configuração final**
- **31 movimentos**

---

*Todos os resultados acima foram obtidos a partir da execução do código em `GrafoDeEstados.py`.*
