import os
import networkx as nx
from .data import parse_all


def get_output_path():
    dirpath = os.path.dirname(os.path.realpath(__file__))
    return dirpath + '/../output/'


def run():
    output_path = get_output_path()
    graphs = []
    for index, data in enumerate(parse_all()):
        print("Graph {:d}".format(index))
        #print("Graph data: {:s}".format(str(data)))

        graph = nx.DiGraph()
        fill_graph(graph, data)
        graphs.append(graph)

        longest_path, path_length = mark_longest_path(graph)
        print("Longest path: {:s}".format(str(longest_path)))
        print("Path length: {:d}".format(path_length))

        analyze_graph(graph)
        write_labels(graph, index)
        write_graph(graph, index, output_path)
        print("Graph {:d} done.\n\n".format(index))

    print("Processed {:d} graphs".format(len(graphs)))


def write_labels(graph, index):
    path = get_output_path() + str(index)
    outfile = open(path + '-table.csv', 'w')
    outfile.write("zacatek,konec,trvani,zacatek_e,zacatek_l,konec_e,konec_l,rezerva\n")
    for l, r in graph.edges:
        edge = graph[l][r]
        edge['label'] = label_format.format(l, r, edge['trvani'], edge['zacatek_e'], edge['zacatek_l'], edge['konec_e'], edge['konec_l'], edge['rezerva'])
        outfile.write("{:d},{:d},{:d},{:d},{:d},{:d},{:d},{:d}\n".format(l, r, edge['trvani'], edge['zacatek_e'], edge['zacatek_l'], edge['konec_e'], edge['konec_l'], edge['rezerva']))

    outfile.close()


def write_graph(graph, index, output_path):
    agraph = nx.nx_agraph.to_agraph(graph)
    path = output_path + str(index)
    print("Writing {:s}".format(path))
    agraph.write(path + '-graphviz.dot')
    agraph.draw(path + '-graph.png', 'png', 'dot')


def mark_longest_path(graph):
    longest_path = nx.dag_longest_path(graph, 'trvani')
    path_length = 0
    prev = None
    for node in longest_path:
        if prev is None:
            prev = node
            continue

        edge = graph[prev][node]
        edge['color'] = 'red'
        path_length += edge['trvani']
        prev = node
    return longest_path, path_length


def fill_graph(graph, data):
    for rown, row in enumerate(data, 1):
        for coln, cell in enumerate(row, 1):
            # we don't care about cells containing 0
            if cell == 0:
                continue
            graph.add_edge(rown, coln, trvani=cell)


label_format = '''<<TABLE>
<TR><TD COLSPAN="2"><B>{:d} - {:d}</B></TD></TR>
<TR><TD>trvani</TD><TD>{:d}</TD></TR>
<TR><TD>zacatek_e</TD><TD>{:d}</TD></TR>
<TR><TD>zacatek_l</TD><TD>{:d}</TD></TR>
<TR><TD>konec_e</TD><TD>{:d}</TD></TR>
<TR><TD>konec_l</TD><TD>{:d}</TD></TR>
<TR><TD>rezerva</TD><TD>{:d}</TD></TR>
</TABLE>>'''


highest_konec_e = 0


def analyze_graph(source_graph: nx.DiGraph):
    graph = source_graph

    for node in graph.nodes:
        if len(graph.pred[node]) > 0:
            continue
        mark_earliest(graph, node, 0)

    for node in graph.nodes:
        if len(graph.succ[node]) > 0:
            continue
        mark_latest(graph, node, highest_konec_e)


def mark_earliest(graph: nx.DiGraph, parent, konec_e):
    global highest_konec_e
    # first find the lowest of the parents
    for gp in graph.predecessors(parent):
        edge = graph[gp][parent]
        if 'konec_e' in edge and edge['konec_e'] > konec_e:
            konec_e = edge['konec_e']

    # compute, save values and recurse
    for succ in graph.successors(parent):
        edge = graph[parent][succ]

        edge['zacatek_e'] = konec_e
        edge['konec_e'] = konec_e + edge['trvani']
        highest_konec_e = max(highest_konec_e, edge['konec_e'])
        mark_earliest(graph, succ, edge['konec_e'])


def mark_latest(graph: nx.DiGraph, parent, zacatek_l):
    # first find the highest of the children
    for gc in graph.successors(parent):
        edge = graph[parent][gc]
        if 'zacatek_l' in edge and edge['zacatek_l'] < zacatek_l:
            zacatek_l = edge['zacatek_l']

    # compute, save values and recurse
    for pred in graph.predecessors(parent):
        edge = graph[pred][parent]

        edge['konec_l'] = zacatek_l
        edge['zacatek_l'] = zacatek_l - edge['trvani']
        edge['rezerva'] = edge['zacatek_l'] - edge['zacatek_e']

        mark_latest(graph, pred, edge['zacatek_l'])
