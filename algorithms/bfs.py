from collections import deque
from puzzle.base_search import BaseSearch
from puzzle.state import State
from puzzle.result import SearchResult


class BFS(BaseSearch):
    """Busca em Largura (completa e ótima para custo unitário).

    Convenções de métricas (iguais em BFS, DFS e A*):
      - nodes_generated = raiz + todo filho produzido por neighbors() (inclui duplicatas);
      - nodes_expanded  = nós cujos filhos foram efetivamente gerados.
    Teste de objetivo: BFS e DFS testam ao GERAR o nó (early goal test); o A*
    precisa testar ao RETIRAR da fila de prioridade para garantir a otimalidade.
    """

    def search(self, initial: State) -> SearchResult:
        if initial.is_goal:
            return SearchResult(solution=initial, nodes_generated=1, max_frontier_size=1)

        frontier: deque = deque([initial])
        reached = {initial}
        nodes_expanded = 0
        nodes_generated = 1
        max_frontier_size = 1

        while frontier:
            current = frontier.popleft()
            nodes_expanded += 1

            for child in current.neighbors():
                nodes_generated += 1
                # Teste de objetivo na geração: continua ótimo em custo unitário,
                # pois todos os nós de profundidade d são gerados antes dos de d+1.
                if child.is_goal:
                    return SearchResult(
                        solution=child,
                        nodes_expanded=nodes_expanded,
                        nodes_generated=nodes_generated,
                        max_frontier_size=max_frontier_size,
                        depth=child.cost,
                    )
                if child not in reached:
                    reached.add(child)
                    frontier.append(child)

            max_frontier_size = max(max_frontier_size, len(frontier))

        return SearchResult(
            solution=None,
            nodes_expanded=nodes_expanded,
            nodes_generated=nodes_generated,
            max_frontier_size=max_frontier_size,
        )
