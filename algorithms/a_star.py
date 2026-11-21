import heapq
from typing import Callable, Optional
from puzzle.base_search import BaseSearch
from puzzle.state import State, GOAL_STATE
from puzzle.result import SearchResult

# Posição (linha, coluna) de cada peça no estado objetivo.
GOAL_POSITIONS = {tile: divmod(index, 3) for index, tile in enumerate(GOAL_STATE)}


class AStar(BaseSearch):
    """Busca A* com f(n) = g(n) + h(n).

    Heurística padrão: distância de Manhattan (admissível e consistente).
    Aceita heurística opcional: AStar(heuristic=fn).
    Empates em f são resolvidos pelo menor h.
    """

    def __init__(self, heuristic: Optional[Callable[[State], int]] = None):
        self._heuristic = heuristic

    def heuristic(self, state: State) -> int:
        """Distância de Manhattan: soma das distâncias de cada peça (exceto o vazio)
        até sua posição no objetivo."""
        distance = 0
        for index, tile in enumerate(state.tiles):
            if tile == 0:
                continue
            row, col = divmod(index, 3)
            goal_row, goal_col = GOAL_POSITIONS[tile]
            distance += abs(row - goal_row) + abs(col - goal_col)
        return distance

    def search(self, initial: State) -> SearchResult:
        h_fn = self._heuristic if self._heuristic is not None else self.heuristic

        counter = 0
        h0 = h_fn(initial)
        frontier = [(h0, h0, counter, initial)]   # (f, h, desempate, estado)
        best_g = {initial: 0}                      # menor g conhecido de cada estado
        closed = set()                             # estados já expandidos
        nodes_expanded = 0
        nodes_generated = 1
        max_frontier_size = 1

        while frontier:
            _, _, _, current = heapq.heappop(frontier)

            if current in closed:
                continue  # entrada antiga, o estado já foi expandido por um caminho melhor

            if current.is_goal:
                return SearchResult(
                    solution=current,
                    nodes_expanded=nodes_expanded,
                    nodes_generated=nodes_generated,
                    max_frontier_size=max_frontier_size,
                    depth=current.cost,
                )

            closed.add(current)
            nodes_expanded += 1
            children = current.neighbors()
            nodes_generated += len(children)

            for child in children:
                if child in closed:
                    continue
                if child.cost < best_g.get(child, float("inf")):
                    best_g[child] = child.cost
                    h = h_fn(child)
                    counter += 1
                    heapq.heappush(frontier, (child.cost + h, h, counter, child))

            # Estados abertos = descobertos e ainda não expandidos.
            max_frontier_size = max(max_frontier_size, len(best_g) - len(closed))

        return SearchResult(
            solution=None,
            nodes_expanded=nodes_expanded,
            nodes_generated=nodes_generated,
            max_frontier_size=max_frontier_size,
        )
