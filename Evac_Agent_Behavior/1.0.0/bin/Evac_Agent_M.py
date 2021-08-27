#!/SYSTEM/Python/3.6.3/bin/python3

import sys
import getopt
import os
import time

try:
    opts, args = getopt.getopt(sys.argv[1:],"i:f:",["inp=","gama="])
except getopt.GetoptError as err:
    print (str(err))
    sys.exit(1)

try:
    os.system("rm -r result")
    os.system("rm -r captures")
    os.system("rm -r modified_user_input.gaml")
except:
    pass

os.system("mkdir result")

print(opts[1][1])


for opt,arg in opts:
    if  opt in ("-i", "--inp"):
        f_inputdeck = open(arg, "r")


inputdeck_lines = f_inputdeck.readlines()


for line in inputdeck_lines:
    opt  = line.split()[0]
    if  opt in "EarthQuake_Occur_cycle":
        c1 = "\tint earthquakestart <- %d;\n" %(int(line.split()[2]))
    elif  opt in "Probability_to_Notice_EarthQuake":
        c2 = "\tfloat proba_detect_Earthquake <- %f;\n" %(float(line.split()[2]))
    elif  opt in "Probability_to_get_fear":
        c3 = "\tfloat proba_detect_fear <- %f\n;" %(float(line.split()[2]))
    elif  opt in "Elder_speed_ratio":
        c4 = "\tfloat elderly_speed <- %f\n;" %(float(line.split()[2]))
    elif  opt in "Speaker_influence_range":
        c5 = "\tfloat speaker_distance <- %f\n;" %(float(line.split()[2]))
    

files = os.listdir("./")
input_gama_file = opts[1][1]

print(os.listdir("./"))
for file in files:
    if file.endswith("Agent.gaml"):
        gama_file = file
    elif file.endswith(".xml"):
        xml_file = file

with open(input_gama_file, "r") as k:
    contents_i = k.readlines()
d1 = "".join(contents_i[9])
d2 = "".join(contents_i[10])
d3 = "".join(contents_i[11])

with open(gama_file, "r") as f:
    contents = f.readlines()

del contents[5]
contents.insert(5, c2)

del contents[6]
contents.insert(6, c3)

del contents[8]
contents.insert(8, c1)

del contents[16]
contents.insert(16, c4)

del contents[17]
contents.insert(17, c5)

del contents[12]
contents.insert(12, d1)

del contents[13]
contents.insert(13, d2)

del contents[14]
contents.insert(14, d3)

f_name = "modified_user_input.gaml"
with open(f_name, "w") as f:
    contents = "".join(contents)
    f.write(contents)
    f.close()
    print("Got User Input!")

os.system("cp {} result".format(f_name))
print(os.listdir("result"))
print("Done!")

cwd = os.getcwd()
os.system("sh gama-headless.sh {}/Evac_Agent.xml captures".format(cwd))

img_path = cwd+"/captures/snapshot/"
files = os.listdir(img_path)
for file in files:
    name = file.split("-")[-1].split(".")[0]
    new_file = '%03d' % (int(name))
    os.rename(img_path+file, img_path+new_file+".png")

time.sleep(5)
os.system("ffmpeg -r 30 -f image2 -i ./captures/snapshot/%03d.png -vcodec mpeg4 -y ./result/result.mp4")
