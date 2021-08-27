#!/SYSTEM/Python/3.6.3/bin/python3

import sys
import getopt
import os
import time

try:
    opts, args = getopt.getopt(sys.argv[1:],"s:i:")
except getopt.GetoptError as err:
    print (str(err))
    sys.exit(1)

try:
    os.system("rm -r result")
    os.system("rm -r captures")
    os.system("rm -r user_input.gaml")
except:
    pass

os.system("mkdir result")
os.system("mkdir result/video1")
os.system("mkdir result/video2")
os.system("mkdir result/video3")
os.system("mkdir result/video4")

try:
    os.system("unzip {}".format(opts[0][1]))
    gama_file = opts[1][1]
except:
    print (str(err))
    sys.exit(1)

files = os.listdir("./")

print(os.listdir("./"))
for file in files:
    if file.endswith(".xml"):
        xml_file = file



with open(gama_file, "r") as f:
    contents = f.readlines()



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
video1_path = cwd+"/result/video1/"
video2_path = cwd+"/result/video2/"
video3_path = cwd+"/result/video3/"
video4_path = cwd+"/result/video4/"

files = os.listdir(img_path)
for file in files:
    if file.startswith("video1"):
        dir=img_path+file+" "+video1_path+file
        os.system("cp {}".format(dir))
    elif file.startswith("video2"):
        dir=img_path+file+" "+video2_path+file
        os.system("cp {}".format(dir))
    elif file.startswith("video3"):
        dir=img_path+file+" "+video3_path+file
        os.system("cp {}".format(dir))
    elif file.startswith("video4"):
        dir=img_path+file+" "+video4_path+file
        os.system("cp {}".format(dir))


files = os.listdir(video1_path)
for file in files:
    name = file.split("-")[-1].split(".")[0]
    new_file = '%03d' % (int(name))
    os.rename(video1_path+file, video1_path+new_file+".png")

files = os.listdir(video2_path)
for file in files:
    name = file.split("-")[-1].split(".")[0]
    new_file = '%03d' % (int(name))
    os.rename(video2_path+file, video2_path+new_file+".png")

files = os.listdir(video3_path)
for file in files:
    name = file.split("-")[-1].split(".")[0]
    new_file = '%03d' % (int(name))
    os.rename(video3_path+file, video3_path+new_file+".png")

files = os.listdir(video4_path)
for file in files:
    name = file.split("-")[-1].split(".")[0]
    new_file = '%03d' % (int(name))
    os.rename(video4_path+file, video4_path+new_file+".png")




time.sleep(5)
os.system("ffmpeg -r 30 -f image2 -i ./result/video1/%03d.png -vcodec mpeg4 -y ./result/video1.mp4")
os.system("ffmpeg -r 30 -f image2 -i ./result/video2/%03d.png -vcodec mpeg4 -y ./result/video2.mp4")
os.system("ffmpeg -r 30 -f image2 -i ./result/video3/%03d.png -vcodec mpeg4 -y ./result/video3.mp4")
os.system("ffmpeg -r 30 -f image2 -i ./result/video4/%03d.png -vcodec mpeg4 -y ./result/video4.mp4")

os.system("rm -r result/video1/")
os.system("rm -r result/video2/")
os.system("rm -r result/video3/")
os.system("rm -r result/video4/")

os.system("sh merge_video.sh")

os.system("rm -r result/video1.mp4/")
os.system("rm -r result/video2.mp4/")
os.system("rm -r result/video3.mp4/")
os.system("rm -r result/video4.mp4/")
