from vtkplotter import *
import numpy as np

fname = 'imgdata/rawdata_stack13.tif'

minsize, maxsize = 5, 50

vol = load(fname)
pic = Picture(fname).z(-1)

iso = vol.frequencyPassFilter().printInfo().isosurface(threshold=14.3).lw(1)

vol2 = load('imgdata/rawdata-STACKS.tif', spacing=[1,1,4])
show(vol2, vol2.clone().frequencyPassFilter(), N=2)

#print(iso.points())
split = iso.clone().splitByConnectivity(maxdepth=400)

ss=[]
split_rng=[]
for s in split:
    mean = s.centerOfMass()
    r = s.averageSize()
    ss.append(Sphere(mean, r=r, alpha=0.6, c='w'))
    if minsize< r <maxsize:
#        s.smoothMLS1D(f=.9)
        split_rng.append(s)

centers = []
for s in split_rng:
    for p in s.points():
        pt2fit = s.closestPoint(p, N=10)
        cx, cy ,r = fitCircle2D(pt2fit)
        if minsize< r <30:
            centers.append([cx,cy,10])
            
show(split_rng, pic, Points(centers, c='w'),  axes=8,newPlotter=True)
