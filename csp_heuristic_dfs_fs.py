list_node = []
list_constraint = []
f = open("map_aus.txt", "r") # need to use "map_aus.txt" for australia or "map_usa.txt" for usa color mapping
lines = f.readlines()
import random
random.shuffle(lines)
lines = [line.replace('\n', '').replace(' ','').replace('[','').replace(']','') for line in lines]
for line in lines:
    list_elems = line.split(':')
    s = list_elems[0]
    list_d = list_elems[1].split(',')
    if s not in list_node and s != '':
        list_node.append(s)
    for d in list_d:
        if d not in list_node and d != '':
            list_node.append(d)
    for d in list_d:
        if d != s and (s, d) not in list_constraint and (d, s) not in list_constraint and s!='' and d!='':
            list_constraint.append((s,d))
print(list_node, list_constraint)

def check_constraint(n, c):
    ok = True
    for cons in list_constraint:
        if cons[0] == n:
            other_node = cons[1]
            if G.nodes[other_node]['color'] == c:
                ok = False
                return ok
        elif cons[1] == n:
            other_node = cons[0]
            if G.nodes[other_node]['color'] == c:
                ok = False
                return ok
    return ok

def get_removed_domain(n,c):
    result = {}
    for cons in list_constraint:
        if cons[0] == n:
            other_node = cons[1]
            if c in G.nodes[other_node]['domain']:
                G.nodes[other_node]['domain'].remove(c)
                result[other_node] = c
        elif cons[1] == n:
            other_node = cons[0]
            if c in G.nodes[other_node]['domain']:
                G.nodes[other_node]['domain'].remove(c)
                result[other_node] = c
    return result

def get_next_with_heuristic():
    node_not_visited = []
    for n in G.nodes():
        if G.nodes[n]['color'] == '':
            remaining_value = len(G.nodes[n]['domain']) # For MRV
            degree_heuristic =  G.degree(n) # For Degree heuristic
            e = (n, remaining_value, degree_heuristic)
            node_not_visited.append(e)
    node_not_visited.sort(key=lambda x: (x[1],-x[2])) # sorting based on priority of MRV > Degree heuristic
    return node_not_visited[0][0] if len(node_not_visited) > 0 else None

def get_color_with_heuristic(n):
    lease_constraining_value = []
    neighbors = list(G.neighbors(n))
    for c in G.nodes[n]['domain']:
        rules_out = 0
        for node in list(G.neighbors(n)):
            if G.nodes[node]['color'] == '' and c in G.nodes[node]['domain']:
                rules_out+=1
        e = (c, rules_out)
        lease_constraining_value.append(e)
    lease_constraining_value.sort(key=lambda x: x[1])
    return [tup[0] for tup in lease_constraining_value]


def color_map(i,n):
    global no_bt
    if i == len(G.nodes()):
        return True

    # use heuristic LCV
    sorted_color_domain = get_color_with_heuristic(n)
    for c in sorted_color_domain:
        G.nodes[n]['color'] = c
        ok = check_constraint(n, c)
        if ok:
            domain_remove = get_removed_domain(n,c)

            # use heuristic MRV, Degree
            next_n = get_next_with_heuristic()
            success = color_map(i+1, next_n)
            if success:
                return success
            for k,v in domain_remove.items():
                if v not in G.nodes[k]['domain']:
                    G.nodes[k]['domain'].append(v)
            no_bt +=1
        G.nodes[n]['color'] = ''
        no_bt +=1
    return False

def check_map_color(G=None, list_color=[]):
    # list node, # list_constraint, # list_color
    import random
    success = color_map(0, list_node[random.randint(0, len(list_node)-1)])
    return success

if __name__=='__main__':
    import time, copy
    start_time = time.time()
    max_no_color = 10
    success_with_max_no_color = False
    for no_color in range(1, max_no_color + 1):
        list_color = [c for c in range(no_color)]
        import networkx as nx
        import matplotlib.pyplot as plt

        G = nx.Graph()
        G.add_nodes_from(list_node, color='')
        G.add_edges_from(list_constraint)
        for n in G.nodes:
            G.nodes[n]['domain'] = copy.deepcopy(list_color)

        # for n in G.nodes():
        #     print(G.nodes[n]['domain'], G.nodes[n]['color'])
        no_bt = 0
        success = check_map_color(G, list_color)
        if success:
            print("Success with X(G) = ", no_color, " and No of Backtrack = ", no_bt)
            # for n in G.nodes():
            #     print(n, G.nodes[n]['color'])
            success_with_max_no_color = True
            break
        print()
        print()
    if not success_with_max_no_color:
        print('Failed, need more than %s colors !!!' % (max_no_color))
    print("--- %s seconds ---" % (time.time() - start_time))
