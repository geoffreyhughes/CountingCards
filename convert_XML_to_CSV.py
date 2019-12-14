# This script is largely taken from here:
# https://github.com/geaxgx/playing-card-detection/blob/master/convert_voc_yolo.py

# MIT License
#
# Copyright (c) 2018 geaxgx
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.


# Imports
import xml.etree.ElementTree as ET
import pickle
import os
from os import listdir, getcwd
from os.path import join
import sys
from glob import glob



def convert(size, box):
    dw = 1./size[0]
    dh = 1./size[1]
    x = (box[0] + box[1])/2.0
    y = (box[2] + box[3])/2.0
    w = box[1] - box[0]
    h = box[3] - box[2]
    x = x*dw
    w = w*dw
    y = y*dh
    h = h*dh
    return (x,y,w,h)

# Convert XML to CSV
def convert_annotation(xml_fn):
    in_file = open(xml_fn)
    txt_fn=xml_fn.replace(".xml",".txt")
    out_file = open(txt_fn, 'w')
    tree=ET.parse(in_file)
    root = tree.getroot()
    size = root.find('size')
    w = int(size.find('width').text)
    h = int(size.find('height').text)

    for obj in root.iter('object'):
        difficult = obj.find('difficult').text
        cls = obj.find('name').text
        if cls not in classes or int(difficult) == 1:
            continue
        cls_id = classes.index(cls)
        xmlbox = obj.find('bndbox')
        b = (float(xmlbox.find('xmin').text), float(xmlbox.find('xmax').text), float(xmlbox.find('ymin').text), float(xmlbox.find('ymax').text))
        bb = convert((w,h), b)
        #out_file.write(str(cls_id) + " " + " ".join([str(a) for a in bb]) + '\n')
        out_file.write(f"{cls_id} {bb[0]:0.6f} {bb[1]:0.6f} {bb[2]:0.6f} {bb[3]:0.6f}\n")
        #print(f"{txt_fn} created")
    in_file.close()
    out_file.close()


# Check for correct files / directories
if len(sys.argv) != 4:
    print(f"Usage: {sys.argv[0]} images_dir classes.names list.txt")
    print(f"Ex: {sys.argv[0]} data/cards/train data/cards.names data/train.txt")
    print("From xml files in images_dir, convert them in txt files with annotation information and build list.txt file")
    sys.exit(1)
images_dir=sys.argv[1]
classes_fn=sys.argv[2]
list_fn=sys.argv[3]
if not os.path.isfile(classes_fn):
    print(f"Classes file {classes_fn} is not a file")
    sys.exit(1)
if not os.path.isdir(images_dir):
    print(f"{images_dir} is not a directory")
    sys.exit(1)
with open(classes_fn,"r") as f:
    classes=f.read().split("\n")
classes=[c for c in classes if c!='']
print(classes,len(classes))

list_file = open(list_fn,"w")

# Convert all XML files using glob
for i,xml_fn in enumerate(glob(images_dir+"/*.xml")):
    img_fn=xml_fn.replace(".xml",".jpg")
    convert_annotation(xml_fn)
    list_file.write(f"{img_fn}\n")
    if (i+1)%100==0:
        print(i+1)
list_file.close()
