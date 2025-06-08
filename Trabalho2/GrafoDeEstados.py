"""
    Implementação do grafo de estados do jogo
"""

import itertools
from collections import defaultdict

class GrafoDeEstados8Puzzle:
    def __init__(self):
        self.n = 9  # 8 peças + 1 vazio
        self.tamanho = 3  # tabuleiro 3x3
        self.hash_cfg_para_no = dict()
        self.hash_no_para_cfg = dict()
        self.adjacencia = defaultdict(list)
        self._construir_grafo()

    def _construir_grafo(self):
        # Gerar todas as permutações possíveis das peças (0 = vazio)
        todas_cfgs = list(itertools.permutations(range(self.n)))
        for idx, cfg in enumerate(todas_cfgs):
            self.hash_cfg_para_no[cfg] = idx
            self.hash_no_para_cfg[idx] = cfg
        # Gerar arestas
        for cfg in todas_cfgs:
            idx = self.hash_cfg_para_no[cfg]
            for vizinha in self._gerar_vizinhas(cfg):
                idx_vizinha = self.hash_cfg_para_no[vizinha]
                self.adjacencia[idx].append(idx_vizinha)

    def _gerar_vizinhas(self, cfg):
        # Retorna todas as configurações vizinhas (um movimento)
        vizinhas = []
        zero_idx = cfg.index(0)
        x, y = divmod(zero_idx, self.tamanho)
        movimentos = [(-1,0), (1,0), (0,-1), (0,1)]  # cima, baixo, esquerda, direita
        for dx, dy in movimentos:
            nx, ny = x + dx, y + dy
            if 0 <= nx < self.tamanho and 0 <= ny < self.tamanho:
                novo_idx = nx * self.tamanho + ny
                nova_cfg = list(cfg)
                # Troca o zero com a peça vizinha
                nova_cfg[zero_idx], nova_cfg[novo_idx] = nova_cfg[novo_idx], nova_cfg[zero_idx]
                vizinhas.append(tuple(nova_cfg))
        return vizinhas

    def contar_nos_e_arestas(self):
        num_nos = len(self.hash_cfg_para_no)
        num_arestas = sum(len(v) for v in self.adjacencia.values()) // 2  # cada aresta contada 2x
        return num_nos, num_arestas

    def verificar_conexao(self, cfg1, cfg2):
        # cfg1 e cfg2 são tuplas de 9 elementos
        idx1 = self.hash_cfg_para_no.get(cfg1)
        idx2 = self.hash_cfg_para_no.get(cfg2)
        if idx1 is None or idx2 is None:
            return False
        return idx2 in self.adjacencia[idx1]

    def verificar_nao_conexao(self, cfg1, cfg2):
        return not self.verificar_conexao(cfg1, cfg2)

    def numero_do_no(self, cfg):
        return self.hash_cfg_para_no.get(cfg)

    def configuracao_do_no(self, idx):
        return self.hash_no_para_cfg.get(idx)

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

    def encontrar_configuracao_mais_distante_de_cfg_final(self, cfg_final=(1,2,3,4,5,6,7,8,0)):
        idx_final = self.hash_cfg_para_no[cfg_final]
        visitado = set()
        dist = dict()
        fila = [(idx_final, 0)]
        visitado.add(idx_final)
        dist[idx_final] = 0
        while fila:
            atual, d = fila.pop(0)
            for vizinho in self.adjacencia[atual]:
                if vizinho not in visitado:
                    visitado.add(vizinho)
                    dist[vizinho] = d + 1
                    fila.append((vizinho, d + 1))
        # Encontrar o nó mais distante
        idx_mais_distante = max(dist, key=dist.get)
        distancia_maxima = dist[idx_mais_distante]
        cfg_mais_distante = self.hash_no_para_cfg[idx_mais_distante]
        return cfg_mais_distante, distancia_maxima

# Exemplo de uso:
if __name__ == "__main__":
    grafo = GrafoDeEstados8Puzzle()
    nos, arestas = grafo.contar_nos_e_arestas()
    print(f"Número de nós: {nos}")
    print(f"Número de arestas: {arestas}")
    # Exemplo de consulta
    cfg1 = (1,2,3,4,5,6,7,8,0)
    cfg2 = (1,2,3,4,5,6,7,0,8)
    print(f"Conectados? {grafo.verificar_conexao(cfg1, cfg2)}")
    print(f"Não conectados? {grafo.verificar_nao_conexao(cfg1, (1,2,3,4,5,6,0,7,8))}")
    # Contar componentes conexos
    componentes = grafo.bfs_componentes_conexos()
    print(f"Número de componentes conexos: {componentes}")
    # Encontrar configuração mais distante de cfg*
    cfg_mais_distante, distancia_maxima = grafo.encontrar_configuracao_mais_distante_de_cfg_final()
    print(f"Configuração viável mais distante de cfg*: {cfg_mais_distante}")
    print(f"Número de movimentos necessários: {distancia_maxima}")

