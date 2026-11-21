from puzzle.base_search import BaseSearch
from puzzle.state import State
from puzzle.result import SearchResult

DEFAULT_DEPTH_LIMIT = 50


class DFS(BaseSearch):
    """Busca em Profundidade com limite de profundidade.

    Para ser completa dentro do limite, a DFS guarda a MENOR profundidade em que
    cada estado foi alcançado e o reabre quando encontra um caminho mais raso.
    (Um conjunto global de visitados descartaria esse caminho mais curto e
    poderia perder soluções com profundidade <= depth_limit.)

    Métricas seguem a mesma convenção da BFS/A* (ver bfs.py).
    """

    def __init__(self, depth_limit: int = DEFAULT_DEPTH_LIMIT):
        self.depth_limit = depth_limit

    def search(self, initial: State) -> SearchResult:
        if initial.is_goal:
            return SearchResult(solution=initial, nodes_generated=1, max_frontier_size=1)

        stack = [initial]
        best_depth = {initial: 0}
        nodes_expanded = 0
        nodes_generated = 1
        max_frontier_size = 1

        while stack:
            current = stack.pop()

            # Entrada obsoleta: o estado já foi alcançado depois por um caminho mais raso.
            if current.cost > best_depth[current]:
                continue

            if current.cost >= self.depth_limit:
                continue  # atingiu o limite: não expande (e não conta como expandido)

            nodes_expanded += 1
            children = current.neighbors()
            nodes_generated += len(children)

            # Teste de objetivo na geração (early goal test).
            for child in children:
                if child.is_goal:
                    return SearchResult(
                        solution=child,
                        nodes_expanded=nodes_expanded,
                        nodes_generated=nodes_generated,
                        max_frontier_size=max_frontier_size,
                        depth=child.cost,
                    )

            # Empilha em ordem reversa para explorar primeiro o primeiro filho gerado.
            for child in reversed(children):
                if child.cost < best_depth.get(child, float("inf")):
                    best_depth[child] = child.cost
                    stack.append(child)

            max_frontier_size = max(max_frontier_size, len(stack))

        return SearchResult(
            solution=None,
            nodes_expanded=nodes_expanded,
            nodes_generated=nodes_generated,
            max_frontier_size=max_frontier_size,
        )
