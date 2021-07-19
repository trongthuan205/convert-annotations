import os
import xml.etree.cElementTree as ET
from PIL import Image

def create_root(file_prefix, width, height):
    root = ET.Element("annotation")
    ET.SubElement(root, "filename").text = "{}.jpg".format(file_prefix)
    ET.SubElement(root, "folder").text = "images"
    size = ET.SubElement(root, "size")
    ET.SubElement(size, "width").text = str(width)
    ET.SubElement(size, "height").text = str(height)
    ET.SubElement(size, "depth").text = "3"
    return root


def create_object_annotation(root, voc_labels):
    for voc_label in voc_labels:
        obj = ET.SubElement(root, "object")
        ET.SubElement(obj, "name").text = voc_label[0]
        ET.SubElement(obj, "pose").text = "Unspecified"
        ET.SubElement(obj, "truncated").text = str(0)
        ET.SubElement(obj, "difficult").text = str(0)
        bbox = ET.SubElement(obj, "bndbox")
        ET.SubElement(bbox, "xmin").text = str(voc_label[1])
        ET.SubElement(bbox, "ymin").text = str(voc_label[2])
        ET.SubElement(bbox, "xmax").text = str(voc_label[3])
        ET.SubElement(bbox, "ymax").text = str(voc_label[4])
    return root


def create_file(file_prefix, width, height, voc_labels, DESTINATION_DIR):
    root = create_root(file_prefix, width, height)
    root = create_object_annotation(root, voc_labels)
    tree = ET.ElementTree(root)
    tree.write("{}/{}.xml".format(DESTINATION_DIR, file_prefix))
    
    
def read_file(file_path, img_path, anno_yolo_path, class_name, DESTINATION_DIR):
    file_prefix = file_path.split(".txt")[0]
    image_file_name = "{}.jpg".format(file_prefix)
    img = Image.open("{}/{}".format(img_path, image_file_name))
    w, h = img.size
    with open(os.path.join(anno_yolo_path, file_path), 'r') as file:
        lines = file.readlines()
        voc_labels = []
        for line in lines:
            voc = []
            line = line.strip()
            data = line.split()
            voc.append(class_name[int(line[0])])
            bbox_width = float(data[3]) * w
            bbox_height = float(data[4]) * h
            center_x = float(data[1]) * w
            center_y = float(data[2]) * h
            voc.append(center_x - (bbox_width / 2))
            voc.append(center_y - (bbox_height / 2))
            voc.append(center_x + (bbox_width / 2))
            voc.append(center_y + (bbox_height / 2))
            voc_labels.append(voc)
        create_file(file_prefix, w, h, voc_labels, DESTINATION_DIR)
    print("Processing complete for file: {}".format(file_path))


def convert_yolo2voc(img_path, anno_yolo_path, class_name, DESTINATION_DIR):
    if not os.path.exists(DESTINATION_DIR):
        os.makedirs(DESTINATION_DIR)
    for filename in os.listdir(anno_yolo_path):
        if filename.endswith('txt'):
            read_file(filename, img_path, anno_yolo_path, class_name, DESTINATION_DIR)
        else:
            print("Skipping file: {}".format(filename))
            
class_name = {0: 'table ', 1: 'figure', 2: 'caption', 'formula'}

DESTINATION_DIR = 'annotation_voc'
convert_yolo2voc('img', 'annotation_yolo', class_name, DESTINATION_DIR)