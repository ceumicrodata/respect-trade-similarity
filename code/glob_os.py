from os import listdir
from os.path import isfile, join

mypath = "../temp/almost_index" 
[print(f) for f in listdir(mypath) if isfile(join(mypath, f))]


