import math
from collections import deque
import random
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-i",action="store", dest="ITEMS", type=int, help="number of circles")
parser.add_argument("-r", action="store", dest="RADIUS", type=int, help="same circles- radius size")
parser.add_argument("--min_radius",action="store", dest="MIN_RADIUS", type=int, help="minimum radius")
parser.add_argument("--max_radius", action="store", dest="MAX_RADIUS", type=int, help="maximum radius")
parser.add_argument("-b",action="store", dest="BOUNDARY_FILE", type=int, help="boundaries")
parser.add_argument("--seed", action="store", dest="SEED", type=int, help="seed for random numbers")
parser.add_argument('args', nargs=argparse.REMAINDER)
args = parser.parse_args()


#cm = (x,y,r)


def findDistance(c0, cm):
    d = math.sqrt((cm[0] - c0[0]) ** 2 + (cm[1] - c0[1]) ** 2)
    distance = round(d, 2)
    return distance

#cm = (x, y, r)
def findTangentialCircle(cm, cn, r):
    dx = cn[0] - cm[0]
    dy = cn[1] - cm[1]
    d = math.sqrt(dx ** 2 + dy ** 2)
    r1 = cm[2] + r 
    r2 = cn[2] + r
    λ = (r1 ** 2 - r2 ** 2 + d ** 2) / (2 * d ** 2) 
    ε = math.sqrt(r1 ** 2 / d ** 2 - λ ** 2)
    kx = cm[0] + λ * dx - ε * dy
    ky = cm[1] + λ * dy + ε * dx 
    kx = round(kx, 2)
    ky = round(ky, 2) 
    return (kx, ky, r)

#line = (ux, uy, vx, vy)

def DistancefromLineSegment(line, cm):
    l2 = (line[0] - line[2]) ** 2 + (line[1] - line[3]) ** 2 
    if (l2 == 0):
        d = math.sqrt((line[0] - cm[0]) ** 2 + (line[1] - cm[1]) ** 2)
    else:
        t = ((cm[0] - line[0]) * (line[2] - line[0]) + (cm[1] - line[1]) * (line[3] - line[1]))/ l2
        px = line[0] + t(line[2] - line[0])
        py = line[1] + t(line[3] - line[1])
        d = math.sqrt((px - cm[0]) ** 2 + (py - cm[1]) ** 2) 
        distance = round(d,2)
    return distance


def findNearestCircle(q, start):
    min = 10 ** 9
    cmin = q[-1]
    for c in (q[-1], q[1]):
        d = findDistance(start, c)
        if (d < min):
            min = d
            cmin = c
            index = q.index(c)
    for c in range(len(q)-1, 1, -1):
        d = findDistance(start, q[c])
        if (d == min):
            cmin = q[c]
            index = c
            break
    return cmin, index 

def socialdistancingSameCircles(r, items, file):
    exportFile = open(file, "w")
    c1 = (0.00, 0.00, r)
    start = c1
    #print(c1)
    exportFile.write('%.2f %.2f %d\n' % c1)
    c2 = (round(2*r,2), 0.00, r)
    #print(c2)
    exportFile.write('%.2f %.2f %d\n' % c2)
    q = deque()
    q.appendleft(c1)
    q.appendleft(c2)
    circles = 2
    while (circles < items):     
        if (findTangentialCircle(c1, c2, r) in q):
            q.remove(c1)
            if(len(q)>=2):
                c1, index_1 = findNearestCircle(q, start)
            #print(q[-1])
            #q.pop()
                print(index_1)
                if(index_1==len(q)-1):
                    c1 = q[-1]
                    c2 = q[0]
                else:
                    c2 = q[index_1-1]
            print(c1," ",c2)
            #print("second center", c1)
            #c2 = added
            #cm = findTangentialCircle(c1, c2, r)
            #added = cm
            #q.appendleft(cm)
            #circles += 1
        c2 = findTangentialCircle(c1, c2, r)
        q.appendleft(c2)
        circles += 1
        #print(c2)
        exportFile.write('%.2f %.2f %d\n' % c2)



if args.RADIUS:
    items = args.ITEMS
    #print(items)
    radius = args.RADIUS
    #print(radius)
    file = args.args[0]
    #print(file, "lala")
    socialdistancingSameCircles(radius, items, file)

def intersectingCircles(c1, c2):
    centersdistance = findDistance(c1, c2)
    sumOfRadiuses = c1[2] + c2[2]
    if (centersdistance < sumOfRadiuses):
        return True
    else:
        return False



def socialdistancingDifferentCircles(items, minr, maxr, seed, file):
    exportFile = open(file, "w")
    random.seed(seed)
    rm = random.randint(minr, maxr)
    cm = (0.00, 0.00, rm)
    start = cm
    print(cm)
    exportFile.write('%.2f %.2f %d\n' % cm)
    rn = random.randint(minr, maxr)
    cn = (rm + rn, 0.00, rn)
    print(cn)
    exportFile.write('%.2f %.2f %d\n' % cn)
    q = deque()
    q.appendleft(cm)
    q.appendleft(cn)
    circles = 2
    while (circles < items):
        print(circles)
        cm, index_m = findNearestCircle(q, start)
        startingIndex = index_m
        ri = random.randint(minr, maxr)
        ci = findTangentialCircle(cm, cn, ri)
        #print(q.index(cn))
        index_n = 0
        Intersecting = True
        while (Intersecting):
            print(index_m)
            print(index_n)
            while (index_n < index_m):
                Intersecting = False
                if (intersectingCircles(ci, q[index_n + 1])):
                    Intersecting = True
                    cn = q[index_n + 1]
                    for c in range (0, index_n):
                        del q[c]
                    break
                index_n += 1  
                if (intersectingCircles(ci, q[index_m - 1])):
                    Intersecting = True
                    cm = q[index_m - 1]
                    for c in range (index_m, startingIndex):
                        del q[c]
                    break
                index_m = index_m - 1  
            ci = findTangentialCircle(cm, cn, ri)    
        q.appendleft(ci)
        print(ci)
        exportFile.write('%.2f %.2f %d\n' % ci)
        circles += 1
          
    
if args.MIN_RADIUS:
    items = args.ITEMS
    #print(items)
    minr = args.MIN_RADIUS
    #print(minr)
    maxr = args.MAX_RADIUS
    #print(maxr)
    seed = args.SEED
    #print(seed)
    file = args.args[0]
    #print(file, "lala")
    socialdistancingDifferentCircles(items, minr, maxr, seed, file)



b = []
i = 0
    
def fitsBoundaries(b, ci):
    if (DistancefromLineSegment(b[0], ci) < ci[2]):
        return False
    elif (DistancefromLineSegment(b[1], ci) < ci[2]):
        return False
    elif (DistancefromLineSegment(b[2], ci) < ci[2]):
        return False
    elif (DistancefromLineSegment(b[3], ci) < ci[2]):
        return False
    else:
        return True
    


def socialdistancingSameCirclesBounded(r, items, boundaries_file, file):
    exportFile = open(file, "w")
    c1 = (0.00, 0.00, r)
    start = c1
    exportFile.write('%.2f %.2f %d\n' % c1)
    c2 = (round(2*r,2), 0.00, r)
    exportFile.write('%.2f %.2f %d\n' % c2)
    q = deque()
    q.appendleft(c1)
    q.appendleft(c2)
    circles = 2
    live=q
    while (circles < items and len(live) > 0):     
        if (findTangentialCircle(c1, c2, r) in q):
            q.remove(c1)
            live.remove(c1)
            if(len(q)>=2):
                c1, index_1 = findNearestCircle(q, start)
                print(index_1)
                if(index_1==len(q)-1):
                    c1 = q[-1]
                    c2 = q[0]
                else:
                    c2 = q[index_1-1]
        c2 = findTangentialCircle(c1, c2, r)
        if (fitsBoundaries(b, c2)):
            q.appendleft(c2)
            circles += 1
            exportFile.write('%.2f %.2f %d\n' % c2)
        else:
            live.remove(c1)
    print(circles)


if args.BOUNDARY_FILE and args.RADIUS:
    items = args.ITEMS
    radius = args.RADIUS
    boundaries_file = args.BOUNDARY_FILE
    with open(boundaries_file) as boundaries:
        for line in boundaries:
            a = line.split()
            a = [int(i) for i in a]
            b[i] = (a[0], a[1], a[2], a[3])
            i += 1
    file = args.args[0]
    socialdistancingSameCirclesBounded(radius, items,boundaries_file, file)


def socialdistancingDifferentCirclesBounded(minr, maxr, seed, boundaries_file, file):
    exportFile = open(file, "w")
    random.seed(seed)
    rm = random.randint(minr, maxr)
    cm = (0.00, 0.00, rm)
    start = cm
    #print(cm)
    exportFile.write('%.2f %.2f %d\n' % cm)
    rn = random.randint(minr, maxr)
    cn = (rm + rn, 0.00, rn)
    #print(cn)
    exportFile.write('%.2f %.2f %d\n' % cn)
    live=[]
    q = deque()
    q.appendleft(cm)
    q.appendleft(cn)
    circles = 2
    live.append(cm)
    live.append(cn)
    while (len(live) > 0):
        #print(circles)
        cm, index_m = findNearestCircle(q, start)
        startingIndex = index_m
        ri = random.randint(minr, maxr)
        ci = findTangentialCircle(cm, cn, ri)
        #print(q.index(cn))
        index_n = 0
        Intersecting = True
        while (Intersecting):
            #print(index_m)
            #print(index_n)
            while (index_n < index_m):
                copyq=q
                copylive=live
                Intersecting = False
                if (intersectingCircles(ci, q[index_n + 1])):
                    Intersecting = True
                    cn = q[index_n + 1]
                    for c in range (0, index_n):
                        del q[c]
                        live.remove(q[c])
                    break
                index_n += 1  
                if (intersectingCircles(ci, q[index_m - 1])):
                    Intersecting = True
                    cm = q[index_m - 1]
                    for c in range (index_m, startingIndex):
                        del q[c]
                        live.remove(q[c])
                    break
                index_m = index_m - 1  
            ci = findTangentialCircle(cm, cn, ri)
            if(not fitsBoundaries(b, ci)):
                live.remove(cm)
                q=copyq
                live=copylive
            else:
                break
        q.appendleft(ci)
        live.append(ci)
        live=q
        #print(ci)
        exportFile.write('%.2f %.2f %d\n' % ci)
        circles += 1
    print(circles)

if args.BOUNDARY_FILE and args.MIN_RADIUS:
    minr = args.MIN_RADIUS
    maxr = args.MAX_RADIUS
    seed = args.SEED
    boundaries_file = args.BOUNDARY_FILE
    with open(boundaries_file) as boundaries:
        for line in boundaries:
            a = line.split()
            a = [int(i) for i in a]
            b[i] = (a[0], a[1], a[2], a[3])
            i += 1
    file = args.args[0]
    socialdistancingDifferentCirclesBounded(minr, maxr, seed, boundaries_file, file)
    

        

