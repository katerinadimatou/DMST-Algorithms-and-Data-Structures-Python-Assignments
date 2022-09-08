import pprint
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("n", type= int, help= "size of polyomino")
parser.add_argument("-p", action="store_true", help="print graph")

args = parser.parse_args()

n = args.n

def FindKeys(n):
    keys = set()
    for y in range (0,n):
        for x in range (-(n-1-y),(n-y)):
            if (y == 0):
                if (x >= 0):
                    keys.add((x,y))
            else:
                 keys.add((x,y))
    return keys

graphKeys= FindKeys(n)

def GraphRepresentation(n, graphKeys):
    graph = dict.fromkeys(graphKeys)
    for (x,y) in graphKeys:
        m = (x, y-1)
        f = (x, y+1)
        k = (x-1, y)
        l = (x+1, y)
        list = []
        if (l in graphKeys):
           list.append(l)
        if (f in graphKeys):
            list.append(f)
        if (k in graphKeys):
            list.append(k)
        if (m in graphKeys):
            list.append(m)
        graph[(x,y)] = list
    return graph

G = GraphRepresentation(n, graphKeys)

untried = {(0,0)}
this_polyomino = []

def Neighbors(G, pol, u, v):
    test = False
    for node in pol:
        if (node == u):
            continue
        elif (v in G[node]):
            test = True
    return test

counter = 0
    
def CountFixedPolyominoes(G, untried, n, this_polyomino):
    global counter
    while len(untried) != 0:
        u = untried.pop()
        this_polyomino.append(u)
        if (len(this_polyomino) == n):
            counter += 1 
        else:
            new_neighbors = set()
            for v in G[u]:
                if (v not in untried and v not in this_polyomino and not Neighbors(G, this_polyomino, u, v)):
                    new_neighbors.add(v)
            new_untried = untried.union(new_neighbors)
            CountFixedPolyominoes(G, new_untried, n, this_polyomino)
        this_polyomino.remove(u) 
    return counter

if args.p:
    pprint.pprint(G)

numberOfPolyominoes = CountFixedPolyominoes(G, untried, n, this_polyomino)
print(numberOfPolyominoes)


            

