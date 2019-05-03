from os import listdir
from os.path import isfile, join
import glob 


mypath = "../temp/almost_index" 
[print(f) for f in listdir(mypath) if isfile(join(mypath, f))]

print(glob.glob('../temp/index/data/*'))

