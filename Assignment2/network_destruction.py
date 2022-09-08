import pprint
from collections import deque
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-c", action= "store_true", help= "destruction1")
parser.add_argument("-r", action="store_true", help="destruction 2- radius size")
parser.add_argument('args', nargs=argparse.REMAINDER)
args = parser.parse_args()
if args.c:
    remove = int(args.args[0])
    file = args.args[1]
    print(remove,file)
if args.r:
    r = int(args.args[0])
    remove = int(args.args[1])
    file = args.args[2]
    print(r,remove,file)
    
connections_file = open(file, 'r')

a = []
graph = {}

with open(file) as connections_file:
    for line in connections_file:
        a = line.split()
        a = [int(i) for i in a]
        if (graph.get(a[0]) != None):
            graph[a[0]].append(a[1])
        else:
            graph[a[0]] = [a[1]]
        if (graph.get(a[1]) != None):
            graph[a[1]].append(a[0])
        else:
            graph[a[1]]= [a[0]]

connections_file.close()

g = graph.copy()

num = 0
for key in graph:
    num += 1

def findMax(graph, max, comp, node):
    for key in graph.keys():
            count = len(graph[key])
            if (count > max):
                max = count
                node = key
                comp = key
    for key in graph.keys():
        count = len(graph[key])
        if (count == max):
            if (key < comp):
                node = key
                comp = key
    print(node, max)
    return node           


def destruction1(graph, num, remove):
    max = -1
    comp = num + 2
    node = -1
    i = 0
    while (i < remove):
        max = -1
        comp = num + 2
        todel = findMax(graph, max, comp, node)
        del graph[todel]
        for v in graph:
            if(todel in graph[v]):
                graph[v].remove(todel)
        i = i + 1
    
if args.c:
    destruction1(graph, num, remove)

def bfs (g, startNode):
    q = deque()
    
    visited = [ False ] * (len(g) + 1)
    inqueue = [ False ] * (len(g) + 1)
    dist = [-1] * (len(g) + 1)

    dist[startNode] = 0
    i = 1
    q.appendleft(startNode)
    inqueue[startNode] = True
    
    while not (len(q) == 0):
        c = q.pop()
        inqueue[c] = False
        visited[c] = True
        for v in g[c]:
            if not visited[v] and not inqueue[v]:
                dist[v] = dist[c] + 1
                q.appendleft(v)
                inqueue[v] = True
        i = i + 1

    return dist


def FindDistances(g):
    distances = dict.fromkeys(g)
    for v in distances:
        shortestPaths = bfs(g, v)
        distances[v] = shortestPaths
    return distances


d = FindDistances(g)

def Ball(i, r):
    setOfNodes = []
    c = -1
    for dist in d[i]:
        c += 1
        if (dist <= r and dist > 0):
            setOfNodes.append(c)
    return setOfNodes

def tBall(i, r):
    setOfNodes = []
    c = -1
    for dist in d[i]:
        c += 1
        if (dist == r):
            setOfNodes.append(c)
    return setOfNodes


def findNeighbours(node, g):
    neighbours = 0
    for v in g[node]:
        neighbours = neighbours + 1 
    return neighbours - 1


def findCI(node, g, r):
    neighbours = findNeighbours(node, g)  
    setOfNodes = tBall(node, r)
    sum = 0
    for v in setOfNodes:
        sum += findNeighbours(v,g)
    ci = neighbours * sum
    return ci


def findAllCI(g, r):
    ci = [0]
    for v in range(1,len(g)+1): 
        w = findCI(v, g, r)
        ci.append(w)
    return ci


def destruction2(g, remove):
    ci = findAllCI(g,r)
    i = 0
    while (i < remove):
        max = -1
        node = -1
        for z in range (1, len(ci)):
            if (ci[z] > max) :
                max = ci[z]
                node = z
            elif (ci[z] == max):
                if (z < node):
                    max = ci[z] 
                    node = z
        print(node, max)
        nodes = Ball(node, r+1)
        list = g[node]
        g[node]=[]
        for v in list:
            g[v].remove(node)
        for v in nodes:
            dst = bfs(g,v)
            d[v] = dst
            ci[v] = findCI(v, g, r)
        ci[node]=-100
        i = i + 1

    

if args.r:
    destruction2(g, remove)
