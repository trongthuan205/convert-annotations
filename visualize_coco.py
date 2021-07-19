
# importing prerequisites
import json
import numpy as np
import os 
from PIL import Image
from PIL import ImageFont, ImageDraw
from glob import glob
import matplotlib.pyplot as plt


# Define color code
colors = {'table': (255, 0, 0)}

# Function to viz the annotation
def markup(image, annotations):
    ''' Draws the segmentation, bounding box, and label of each annotation
    '''
    draw = ImageDraw.Draw(image, 'RGBA')
    for annotation in annotations:
        # # Draw segmentation
        # draw.polygon(annotation['segmentation'][0],
        #              fill=colors[samples['categories'][annotation['category_id'] - 1]['name']] + (64,))
        # Draw bbox
        draw.rectangle(
            (annotation['bbox'][0],
             annotation['bbox'][1],
             annotation['bbox'][0] + annotation['bbox'][2],
             annotation['bbox'][1] + annotation['bbox'][3]),
            outline=colors[samples['categories'][annotation['category_id'] - 1]['name']] + (255,),
            width=2
        )
        # Draw label
        w, h = draw.textsize(text=samples['categories'][annotation['category_id'] - 1]['name'],
                             font=font)
        if annotation['bbox'][3] < h:
            draw.rectangle(
                (annotation['bbox'][0] + annotation['bbox'][2],
                 annotation['bbox'][1],
                 annotation['bbox'][0] + annotation['bbox'][2] + w,
                 annotation['bbox'][1] + h),
                fill=(64, 64, 64, 255)
            )
            draw.text(
                (annotation['bbox'][0] + annotation['bbox'][2],
                 annotation['bbox'][1]),
                text=samples['categories'][annotation['category_id'] - 1]['name'],
                fill=(255, 255, 255, 255),
                font=font
            )
        else:
            draw.rectangle(
                (annotation['bbox'][0],
                 annotation['bbox'][1],
                 annotation['bbox'][0] + w,
                 annotation['bbox'][1] + h),
                fill=(64, 64, 64, 255)
            )
            draw.text(
                (annotation['bbox'][0],
                 annotation['bbox'][1]),
                text=samples['categories'][annotation['category_id'] - 1]['name'],
                fill=(255, 255, 255, 255),
                font=font
            )
    return np.array(image)

# Parse the JSON file and read all the images and labels
with open('test.json', 'r') as fp:
    samples = json.load(fp)
# Index images
images = {}
for image in samples['images']:
    images[image['id']] = {'file_name': os.path.join("test", image['file_name']), 
                           'annotations': []}
for ann in samples['annotations']:
    images[ann['image_id']]['annotations'].append(ann)
    
    
# Visualize annotations
from tqdm import tqdm
import cv2
font = ImageFont.truetype("DejaVuSans.ttf", 15) 
for i, (_, image) in tqdm(enumerate(images.items())):
    with Image.open(image['file_name']) as img:
        filename = os.path.join('visualize/', 
                                image['file_name'].split('/')[-1])
        gt = markup(img, image['annotations'])
        cv2.imwrite(filename, gt)

