import wget
import time
import os

if not os.path.exists("./download"):
    os.mkdir("./download")

if not os.path.exists("./url.txt"):
    open("./url.txt",'w').close()

    print("Put your url in the url.txt file and restart!")

else:
    urls = open("./url.txt").readlines()

    for url in urls:
        print("Start downloading...")
        wget.download(url,out="./output")