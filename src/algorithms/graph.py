import functools
import operator
from typing import Iterable

import networkx as nx


type Edge = tuple[int, int]
type Weight = int | tuple[int, ...]
type NxWeight = tuple[int, ...]


class Graph:
    def __init__(self):
        self._graph = nx.Graph()
        self._weights: dict[Edge, Weight] = {}

    def add_node(self, name: int | str):
        self._graph.add_node(name)

    def add_nodes(self, names: Iterable[int | str]):
        for name in names:
            self.add_node(name)

    def add_edge(self, edge: Edge, weight: Weight):
        self._weights[edge] = weight

        nx_weight = self.__convert_weight_to_nx(weight)
        assert all(value >= 0 for value in nx_weight), 'Weight cannot be negative'

        self._graph.add_edge(*edge, weight=nx_weight)

    def add_edges(self, edges_with_weights: Iterable[tuple[Edge, Weight]]):
        for edge, weight in edges_with_weights:
            self.add_edge(edge, weight)

    @staticmethod
    def __convert_weight_to_nx(weight: Weight) -> NxWeight:
        if isinstance(weight, tuple):
            return weight

        return (weight,)

    def __get_int_graph(self) -> nx.Graph:
        int_graph = self._graph.copy()

        all_weights: Iterable[tuple[Edge, NxWeight]] = (
            (edge, int_graph.edges[edge]['weight']) for edge in int_graph.edges
        )
        max_length = max(len(weight) for weight in all_weights)

        weights_normalized = ((edge, (0,) * (max_length - len(weight)) + weight) for edge, weight in all_weights)
        max_sums: list[int] = [sum(max(weight[i], 0) for _, weight in weights_normalized) for i in range(max_length)]

        for edge, normalized_weight in weights_normalized:
            int_graph.edges[edge]['weight'] = self.__parse_nx_weight_to_int(normalized_weight, max_sums)

        return int_graph

    @classmethod
    def __parse_nx_weight_to_int(cls, weight: NxWeight, max_sums: list[int]) -> int:
        assert len(weight) == len(max_sums), 'Weight is not normalized'

        return sum(
            value * functools.reduce(operator.mul, max_sums[i + 1:], 1)
            for i, value in enumerate(weight)
        )

    def max_weight_matching(self) -> set[Edge]:
        int_graph = self.__get_int_graph()
        return set(nx.max_weight_matching(int_graph))
