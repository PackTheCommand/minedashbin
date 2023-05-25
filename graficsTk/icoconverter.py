from sys import argv

from PIL import Image
file=argv[1]
img = Image.open(file)
img.save(file.split("\\")[-1]+".py.ico",format = 'ICO', sizes=[(32,32),(64,64),(128,128),(512,512)])
