# -*- coding: utf-8 -*-
import networkx

from . import utils


def convert(problem, special=None):
    G = networkx.Graph() if utils.is_symmetric(problem) else networkx.DiGraph()
    G.graph['name'] = problem.get('NAME')
    G.graph['comment'] = problem.get('COMMENT')
    G.graph['type'] = problem.get('TYPE')
    G.graph['dimension'] = problem.get('DIMENSION')
    G.graph['capacity'] = problem.get('CAPACITY')
    G.graph['depots'] = problem.get('DEPOT_SECTION', [])
    G.graph['demands'] = problem.get('DEMAND_SECTION', {})
    # G.graph['fixed_edges'] = problem.get('FIXED_EDGES_SECTION', set())

    if utils.is_explicit(problem):
        add_explicit_edges(G, problem)
    else:
        add_calculated_edges(G, problem, wfunc=special)

    for i in G.nodes:
        G.nodes[i]['display'] = utils.get_display(problem, i)

    return G


# def add_edge(G, i, j, weight):
#     is_fixed = (i, j) in G.graph['fixed_edges']
#     G.add_edge(i, j, weight=weight, is_fixed=is_fixed)


def add_explicit_edges(G, problem):
    matrix = utils.create_explicit_matrix(problem)
    ebunches = [(i, j, matrix[i, j]) for i, j in utils.get_edges(problem)]
    G.add_weighted_edges_from(ebunches)
    # for i, j in utils.get_edges(problem):
    #     ebunches.append()
    #     weight = matrix[i, j]
    #     add_edge(G, i, j, weight)


def add_calculated_edges(G, problem, wfunc=None):
    for i, coord in problem['NODE_COORD_SECTION'].items():
        G.add_node(i, coord=coord)

    wfunc = utils.create_weight_function(problem, wfunc)
    ebunches = [(i, j, wfunc(i, j)) for i, j in utils.get_edges(problem)]
    G.add_weighted_edges_from(ebunches)
    # for i, j in utils.get_edges(problem):
    #     weight = wfunc(i, j)
    #     add_edge(G, i, j, weight)
