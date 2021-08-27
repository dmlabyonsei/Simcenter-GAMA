#!/SYSTEM/Python/3.6.3/bin/python3
import os
import sys
import getopt
import time


try:
    opts, args = getopt.getopt(sys.argv[1:],"i:" ,["inp="])
except getopt.GetoptError as err:
    print (str(err))
    sys.exit(1)
try:
    os.system("rm -rf result")

except:
    pass

try:
    os.system("rm -rf city")
except:
    pass


os.system("unzip {} -d ./result/".format(opts[0][1]))

name = opts[0][1].split("/")[-1].split(".")[0]

os.mkdir("./city")


from shapely.geometry import shape
import fiona
from shapely.ops import unary_union
import networkx as nx

G = nx.Graph()
geoms =[shape(feature['geometry']) for feature in fiona.open("./result/{}.shp".format(name))]

for line in geoms:
    for seg_start, seg_end in zip(list(line.coords),list(line.coords)[1:]):
        G.add_edge(seg_start, seg_end)

nx.write_shp(G, "./result/")
