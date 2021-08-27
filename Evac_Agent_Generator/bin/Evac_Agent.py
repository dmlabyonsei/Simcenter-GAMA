#!/SYSTEM/Python/3.6.3/bin/python3

import sys
import getopt
import os
import time

try:
      opts, args = getopt.getopt(sys.argv[1:],"i:",["inp="])
except getopt.GetoptError as err:
      print (str(err))
      sys.exit(1)

try:
    os.system("rm -r result")
    os.system("rm -r user_input.gaml")
    os.system("rm -r captures")
except:
    pass

os.system("mkdir result")

for opt,arg in opts:
    if  opt in ("-i", "--inp"):
        f_inputdeck = open(arg, "r")

inputdeck_lines = f_inputdeck.readlines()

for line in inputdeck_lines:
    opt  = line.split()[0]
    if  opt in "adult":
        c1 = "\tint nb_adult <- %d;" %(int(line.split()[2]))
    elif  opt in "elderly":
        c2 = "\tint nb_elderly <- %d;" %(int(line.split()[2]))
    elif  opt in "leader":
        c3 = "\tint nb_leader <- %d;" %(int(line.split()[2]))


files = os.listdir("./")
print(os.listdir("./"))
for file in files:
    if file.endswith(".gaml"):
        gama_file = file
    elif file.endswith(".xml"):
        xml_file = file

with open(gama_file, "r") as f:
    contents = f.readlines()

del contents[9]
contents.insert(9, c1)

del contents[11]
contents.insert(11, c2)

del contents[13]
contents.insert(13, c3)


f_name = "user_input.gaml"
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
