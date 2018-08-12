# -*- coding: utf-8 -*-
import networkx

from . import utils


def convert(problem, special=None):
    if problem['TYPE'] == 'TOUR':
        raise Exception('Cannot convert TOUR to networkx.Graph')

    G = networkx.Graph() if utils.is_symmetric(problem) else networkx.DiGraph()
    G.graph['name'] = problem.get('NAME')
    G.graph['comment'] = problem.get('COMMENT')
    G.graph['type'] = problem.get('TYPE')
    G.graph['dimension'] = problem.get('DIMENSION')
    G.graph['capacity'] = problem.get('CAPACITY')
    G.graph['depots'] = problem.get('DEPOT_SECTION', [])
    G.graph['demands'] = problem.get('DEMAND_SECTION', {})

    wfunc = utils.create_weight_function(problem, special=special)

    if not utils.is_explicit(problem):
        for i, coord in problem['NODE_COORD_SECTION'].items():
            G.add_node(i, coord=coord)

    for i, j in utils.get_edges(problem):
        G.add_edge(i, j, weight=wfunc(i, j))

    for i in G.nodes:
        G.nodes[i]['display'] = utils.get_display(problem, i)

    return G
