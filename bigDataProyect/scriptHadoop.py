import subprocess


dir1 = "hadoop fs -put '/home/h-user/map-reduce-inverted-index/input/"
dir2 = "' /inverted_index/input"

for i in range(49): 
    d= "doc"+str(i)
    comando = dir1+d+dir2
    subprocess.call(comando, shell=True)