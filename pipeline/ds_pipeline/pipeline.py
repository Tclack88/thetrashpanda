#!/usr/bin/env python3

import cv2
import hashlib
import imghdr
import numpy as np
import os
from PIL import Image, ImageDraw
from preprocess import image_resize, file_as_bytes, hash_file, rename_files, is_transparent, append_background, blacklist
from dt2.forecut import process_images
from random import randint
import sys
from yolo_label_tools import count_from_top, find_pixel_edges, find_yolo_coordinates

image_dir = 'images'

images = []
texts = []
errors = []
for r, d, f in os.walk(image_dir, topdown=False):
    for file in f:
        path = os.path.join(r, file)
        if imghdr.what(path) != None:
            images.append(path)
        elif path.endswith('.txt'):
            texts.append(path)
        else:
            errors.append(path)
            #print("non-conforming file:",path)
            #print(imghdr.what(path))
            #print()

#TODO: deal with errors


#### Find unlabelled (i.e. new) images
images_basenames = [os.path.splitext(image)[0] for image in images]
images_extensions = [os.path.splitext(image)[1] for image in images]
extensions_dict = dict(zip(images_basenames,images_extensions))
texts_basenames = [os.path.splitext(text)[0] for text in texts]

lonely_images = set(images_basenames) - set(texts_basenames)

unlabeled_images = [li+extensions_dict[li] for li in lonely_images]



#### resize, rename and separate new images
transparent_filepaths = []
opaque_filepaths = []
unique_images = list(set(images) - set(unlabeled_images)) # labeled images (already preprocessed)
for unlabeled_image in unlabeled_images:
    image_resize(unlabeled_image)
    new_name = rename_files(unlabeled_image, unique_images)
    if is_transparent(new_name):
        transparent_filepaths.append(new_name)
    else:
        opaque_filepaths.append(new_name)


#### Take care of transparent images

# Add bounding boxes
class_labels = []
with open('classes.txt') as f:
    for line in f:
        class_labels.append(line.strip('\n'))



for transparent_path in transparent_filepaths:
    class_label = transparent_path.split('/')[-2]
    class_label_number = str(class_labels.index(class_label) + 1) # yolo counts from 1
    coordinates = find_yolo_coordinates(transparent_path)
    coordinates = [str(coordinate) for coordinate in coordinates]
    line = ','.join([class_label_number] +  coordinates)
    file_stem = os.path.splitext(transparent_path)[0]
    with open(f'{file_stem}.txt','w') as f:
        f.write(line)


print(transparent_filepaths)


# Add background!!! 

image_filepaths = transparent_filepaths  # Will contain all the image filepaths
image_folderpaths = [transparent_filepath.split('/')[1] for transparent_filepath in transparent_filepaths]  # Will contain the folder names of all the images
bg_filepaths = []  # Will contain all the background filepaths
bg_folderpaths = []  # Will contain all the folder names of all the backgrounds


for r, d, f in os.walk('bg', topdown=False):
    for file in f:
        # Discard unwanted macOS file
        #if file != '.DS_Store':  TODO: DEAL WITH IT
        # For all the background images
        path = os.path.join(r.replace('bg/', ''), file)
        folder = os.path.join(r.replace('bg/', ''))
        bg_filepaths.append(path)
        bg_folderpaths.append(folder)

print(bg_filepaths)
print(bg_folderpaths)
# Get the number of background categories (to prevent infinite loop
# if all background categories are blacklisted)
number_bg_folders = len(list(set(bg_folderpaths)))



for x in range(0, len(image_filepaths)):
    #print(image_filepaths[x])
    try:
        if (len(blacklist[image_folderpaths[x]]) >= number_bg_folders):
            print('You blacklisted all background types. Skipping image.')
            #continue
        else:
            # Pick a random background
            random_image = randint(0, len(bg_filepaths) - 1)
            # Reroll if selected background is in the blacklist
            while bg_folderpaths[random_image] in blacklist[image_folderpaths[x]]:
                random_image = randint(0, len(bg_filepaths) - 1)
            append_background(image_filepaths[x], bg_filepaths[random_image])
    except KeyError: # Object has no blacklist
        print('key error')
        random_image = randint(0, len(bg_filepaths) - 1)
        append_background(image_filepaths[x], bg_filepaths[random_image])

##### Take care of images without transparent backgrounds


###
# TODO Run Tobias' script on 'images' to remove backgrounds. This creates (if not already existing) an `output` directory with the same file structure of subdirectories and images
###

#sys.argv = ["process_images.py", "-i", "assets/images", "-o", "-p", "--cpus", "2", "-sb"]
#exec(open("process_images.py").read())
#{py process_images.py -i assets/images -p --cpus 2}


for opaque_path in opaque_filepaths:
    process_images(opaque_path)

"""
for opaque_path in opaque_filepaths: # e.g. opaque_path = images/tires/abc.jpg
    file_stem = os.path.splitext(opaque_path)[0] # images/tires/abc
    output_file = f"output/{file_stem}.png"   # output/tires/apc.jpg
    output_path = 'output' #f"output/{'/'.join(file_stem.split('/')[1:])}"   # output/tires/
    sys.argv = ["process_images.py", "-i", f"{opaque_path}", "-o", f"{output_path}", "-p", "--cpus", "2", "-sb", "--single-process"]
    exec(open("process_images.py").read())
    class_label = opaque_path.split('/')[-2] # tires
    class_label_number = str(class_labels.index(class_label) + 1) # yolo counts from 1
    coordinates = find_yolo_coordinates(output_file)
    coordinates = [str(coordinate) for coordinate in coordinates]
    line = ','.join([class_label_number] +  coordinates)
    #print('class_label:', class_label)
    #print('class_label_number:', class_label_number)
    #print('line',line)
    with open(f'{file_stem}.txt','w') as f:
        f.write(line)
"""
