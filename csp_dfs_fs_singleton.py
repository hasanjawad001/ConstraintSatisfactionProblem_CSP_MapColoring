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

def check_constraint(i, c):
    ok = True
    for cons in list_constraint:
        if cons[0] == list_node[i]:
            other_node = cons[1]
            if G.nodes[other_node]['color'] == c:
                ok = False
                return ok
        elif cons[1] == list_node[i]:
            other_node = cons[0]
            if G.nodes[other_node]['color'] == c:
                ok = False
                return ok
    return ok

def get_removed_domain(i,c):
    result = {}
    for cons in list_constraint:
        if cons[0] == list_node[i]:
            other_node = cons[1]
            if c in G.nodes[other_node]['domain']:
                G.nodes[other_node]['domain'].remove(c)
                if other_node not in result.keys():
                    result[other_node] = [c]
                else:
                    result[other_node].append(c)
                if len(G.nodes[other_node]['domain']) == 1:
                    temp_c = G.nodes[other_node]['domain'][0]
                    temp_i = list_node.index(other_node)
                    temp_result = get_removed_domain(temp_i, temp_c)
                    for k,v in temp_result.items():
                        if k not in result.keys():
                            result[k] = v
                        else:
                            result[k] = list(set(result[k]+v))
        elif cons[1] == list_node[i]:
            other_node = cons[0]
            if c in G.nodes[other_node]['domain']:
                G.nodes[other_node]['domain'].remove(c)
                if other_node not in result.keys():
                    result[other_node] = [c]
                else:
                    result[other_node].append(c)
                if len(G.nodes[other_node]['domain']) == 1:
                    temp_c = G.nodes[other_node]['domain'][0]
                    temp_i = list_node.index(other_node)
                    temp_result = get_removed_domain(temp_i, temp_c)
                    for k,v in temp_result.items():
                        if k not in result.keys():
                            result[k] = v
                        else:
                            result[k] = list(set(result[k]+v))
    return result

def color_map(i):
    global no_bt
    if i == len(G.nodes()):
        return True
    for c in G.nodes[list_node[i]]['domain']:
        G.nodes[list_node[i]]['color'] = c
        ok = check_constraint(i, c)
        if ok:
            domain_remove = get_removed_domain(i,c)
            success = color_map(i+1)
            if success:
                return success
            for k,l in domain_remove.items():
                for v in l:
                    if v not in G.nodes[k]['domain']:
                        G.nodes[k]['domain'].append(v)
            no_bt +=1
        no_bt +=1
    return False

def check_map_color(G=None, list_color=[]):
    # list node, # list_constraint, # list_color
    success = color_map(0)
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
