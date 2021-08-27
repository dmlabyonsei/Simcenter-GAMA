#!/SYSTEM/Python/3.6.3/bin/python3

import os
import sys
import getopt
import time

try:
    opts, args = getopt.getopt(sys.argv[1:],"i:s:m:" ,["inp="])
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

print(opts[0][1])

os.system("unzip {} -d ./result/".format(opts[0][1]))

road_name = opts[0][1].split("/")[-1].split(".")[0]

try:
    os.system("unzip {} -d ./result/".format(opts[1][1]))
    shelter_name = opts[1][1].split("/")[-1].split(".")[0]
except:
    pass

try:
    os.system("unzip {} -d ./result/".format(opts[2][1]))
    speaker_name = opts[2][1].split("/")[-1].split(".")[0]
except:
    pass



#os.mkdir("./result")
os.mkdir("./city")

import matplotlib
matplotlib.use('Agg')



from shapely.geometry import shape
import fiona
from shapely.ops import unary_union
import networkx as nx

G = nx.Graph()

geoms =[shape(feature['geometry']) for feature in fiona.open("./result/{}.shp".format(road_name))]

for line in geoms:
    for seg_start, seg_end in zip(list(line.coords),list(line.coords)[1:]):
        G.add_edge(seg_start, seg_end)
        G.add_node(seg_end, pos = seg_end)
        G.add_node(seg_start, pos = seg_start)
import matplotlib.pyplot as plt

try:

    geoms =fiona.open("./result/{}.shp".format(speaker_name))
    Speaker = nx.Graph()
    for g, i in zip(geoms, range(len(geoms))):
        Speaker.add_node("speaker_{}".format(i), pos = g["geometry"]["coordinates"])
    pos=nx.spring_layout(Speaker)
except:
    pass
try:
    geoms =fiona.open("./result/{}.shp".format(shelter_name))
    Shelter = nx.Graph()
    for g, i in zip(geoms, range(len(geoms))):
        Shelter.add_node("shelter_{}".format(i), pos = g["geometry"]["coordinates"])
except:
    pass



nx.draw(G, nx.get_node_attributes(G, 'pos'), node_size=0)

try:
    nx.draw(Shelter, nx.get_node_attributes(Shelter, 'pos'), node_color='red', node_size=20,  label='Shelter')
except:
    pass

try:
    
    nx.draw(Speaker, nx.get_node_attributes(Speaker, 'pos'), node_color=(50/255, 205/255, 50/255), nodelist=Speaker.nodes,node_size=3000,alpha=0.3,  label='Speaker')
    
except:
    pass
import matplotlib



from matplotlib.lines import Line2D
legend_elements = [Line2D([0], [0], marker='o', color=(1,255/255, 255/255), label='Speaker',
                          markerfacecolor=(50/255, 205/255, 50/255), markersize=30,alpha = 0.3),
                  Line2D([0], [0], marker='o', color="r", label='Shelter',
                          markerfacecolor="r", markersize=30,)]

# Create the figure

matplotlib.pyplot.legend(handles=legend_elements, fontsize = 'x-large', frameon=False, loc='lower center', ncol=2)

fig = matplotlib.pyplot.gcf()
fig.suptitle('Preview of {}'.format(road_name), fontsize=30)
fig = matplotlib.pyplot.gcf() 
fig.set_size_inches(18.5, 10.5, True)

fig.savefig('./result/Preview.png', dpi=300)