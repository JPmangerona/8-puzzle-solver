# 8-Puzzle — Busca em Espaço de Estados

## O que implementar

### `puzzle/state.py`
- `neighbors()` — gera os estados filhos a partir do espaço vazio
- `path()` — reconstrói a sequência de estados do inicial até este
- `actions()` — retorna a sequência de ações usando `path()`

### `algorithms/bfs.py`
- `BFS.search(initial)` — Busca em Largura

### `algorithms/dfs.py`
- `DFS.search(initial)` — Busca em Profundidade

### `algorithms/a_star.py`
- `AStar.heuristic(state)` — função heurística admissível
- `AStar.search(initial)` — Busca A*

## Estrutura

```
├── puzzle/
│   ├── state.py        # State — IMPLEMENTAR neighbors, path, actions
│   ├── result.py       # SearchResult — não alterar
│   └── base_search.py  # Interface BaseSearch — não alterar
├── algorithms/
│   ├── bfs.py          ← IMPLEMENTAR
│   ├── dfs.py          ← IMPLEMENTAR
│   └── a_star.py       ← IMPLEMENTAR
└── main.py
```

## Notas de implementação

- **Ações:** o nome indica para onde o **espaço vazio** se move (`"UP"` = o vazio sobe).
- **Solubilidade:** `State.is_solvable` compara a paridade de inversões com a de `GOAL_STATE`; entradas insolúveis retornam `found=False` sem busca.
- **Métricas:** `nodes_generated` = raiz + todos os filhos de `neighbors()` (inclui duplicatas); `nodes_expanded` = nós que tiveram filhos gerados.
- **Teste de objetivo:** BFS/DFS testam na geração; A* testa ao retirar da fila (necessário para otimalidade).
- **DFS:** guarda a menor profundidade de cada estado e o reabre por um caminho mais raso, para ser completa dentro de `depth_limit`.
- **A\*:** Manhattan derivada de `GOAL_STATE`; reabre estados se achar `g` menor; desempate por `(f, h)`.
- **Testes:** `pytest` (arquivo `tests/test_puzzle.py`).

