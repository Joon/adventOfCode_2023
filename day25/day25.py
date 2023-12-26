import itertools
import sys



lines = [l.strip() for l in open('inputs/day25.txt', 'r').readlines()]

# jqt: rhn xhk nvd
def parse(line):
    bits = line.split(': ')
    key = bits[0]
    connections = bits[1].split(' ')
    return key, connections

connections = {}

for key, connection_list in [parse(l) for l in lines]:
    if key in connections:
        connections[key].extend(connection_list)
    else:
        connections[key] = connection_list
    for c in connection_list:
        if c in connections:
            connections[c].append(key)
        else:
            connections[c] = [key]

print(connections)

def count_connections(connections, key, visited):
    visited.add(key)
    for c in connections[key]:
        if c not in visited:
            count_connections(connections, c, visited)
    return len(visited)

def snip_connection(connections, a, b):
    if b in connections[a]:
        connections[a].remove(b)
        connections[b].remove(a)

sys.setrecursionlimit(10000)

def brute_solve(connections):

    for a, b, c, d, e, f in itertools.permutations(connections.keys(), 6):
        temp_connections = {k: connections[k].copy() for k in connections }
        snip_connection(temp_connections, a, b)
        snip_connection(temp_connections, c, d)
        snip_connection(temp_connections, e, f)
        set_1_nodes = set()
        set_2_nodes = set()
        set_1 = count_connections(temp_connections, a, set_1_nodes)
        set_2 = count_connections(temp_connections, b, set_2_nodes)
        # We have overlap in the sets - they are not seperate. Move on
        if set_1_nodes.intersection(set_2_nodes):
            continue
        # Some nodes got dropped off - move on
        if len(set_1_nodes) + len(set_2_nodes) != len(temp_connections):
            if  len(set_1_nodes) + len(set_2_nodes) > len(temp_connections) - 10:
                print("Some nodes got dropped off", len(set_1_nodes) + len(set_2_nodes), len(temp_connections))
            continue

        print(f"Disconnected {a}/{b}  {c}/{d}  {e}/{f}")
        print("lhs: ", set_1_nodes)
        print("rhs: ", set_2_nodes)
        print("Part 1:", set_1 * set_2)

        break

import networkx as nx
import matplotlib.pyplot as plt

# This static graph is not very useful - the set of nodes is too large so you can't figute out where the lines go so labelling them didn't help
def layout_graph(connections):
    G = nx.Graph()
    for k in connections:
        for c in connections[k]:
            G.add_edge(k, c)
    agraph = nx.nx_agraph.to_agraph(G)
    agraph.draw("nodes.png", format = 'png', prog = 'dot')        

from pyvis.network import Network

# This dynamic graph works better - the nodes squirm around in the browser window so you can see the labels on the connecting edges
def interactive_graph(connections):
    net = Network()
    for k in connections:
        net.add_node(k, label = k)

    for k in connections:
        for c in connections[k]:
            net.add_edge(k, c, label = f'{k} -> {c}')
    net.show('nodes.html', notebook=False)


# Change this to the values found by inspecting nodes.html
a, b, c, d, e, f = ('', '', '', '' ,'' ,'')

if a == '':
    print('Inspect nodes.html to find the three pairs of nodes to disconnect, then update the vars a - f above')
    interactive_graph(connections)
else:
    temp_connections = {k: connections[k].copy() for k in connections }
    snip_connection(temp_connections, a, b)
    snip_connection(temp_connections, c, d)
    snip_connection(temp_connections, e, f)
    set_1_nodes = set()
    set_2_nodes = set()
    set_1 = count_connections(temp_connections, a, set_1_nodes)
    set_2 = count_connections(temp_connections, b, set_2_nodes)
    print("Part 1:", set_1 * set_2)