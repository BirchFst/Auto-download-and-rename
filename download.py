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

    a = 0
    for url in urls:
        print("Start downloading...")
        a+=1
        wget.download(url,out="./download/"+str(a)+".jpg")