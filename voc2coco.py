
import os
import xml.etree.ElementTree as ET
import xmltodict
import json
from xml.dom import minidom
from collections import OrderedDict
from tqdm import tqdm 


def xml_file(rootDir):
  xmls = []
  for xml in os.listdir(rootDir):
    if xml.endswith(".xml"):
      xmls.append(xml)
    return xmls
  

def generateVOC2Json(rootDir, xmlFiles, outFile):
  attrDict = dict()
  # Add categories according to you Pascal VOC annotations
  attrDict["categories"]=[{"supercategory":"none","id":0,"name":"table"}]
  images = list()
  annotations = list()
  id1 = 0

  # Some random variables
  cnt_bor = 0
  cnt_cell = 0
  cnt_bless = 0

  # Main execution loop
  for root, dirs, files in os.walk(rootDir):
    image_id = 0
    for file in tqdm(xmlFiles):
      image_id = image_id + 1
      if file in files and file.endswith(".xml"):
        annotation_path = os.path.abspath(os.path.join(root, file))
        image = dict()
        doc = xmltodict.parse(open(annotation_path).read())
        image['file_name'] = str(doc['annotation']['filename'])
        image['height'] = int(doc['annotation']['size']['height'])
        image['width'] = int(doc['annotation']['size']['width'])
        image['id'] = image_id
        print("File Name: {} and image_id {}".format(file, image_id))
        images.append(image)
        if 'object' in doc['annotation']:
          for key,vals in doc['annotation'].items():
            if(key=='object'):
              for value in attrDict["categories"]:
                if(not isinstance(vals, list)):
                  vals = [vals]
                for val in vals:
                  if str(val['name']) == value["name"]:
                    annotation = dict()
                    annotation["iscrowd"] = 0
                    annotation["image_id"] = image_id
                    x1 = int(val["bndbox"]["xmin"])  - 1
                    y1 = int(val["bndbox"]["ymin"]) - 1
                    x2 = int(val["bndbox"]["xmax"]) - x1
                    y2 = int(val["bndbox"]["ymax"]) - y1
                    annotation["bbox"] = [x1, y1, x2, y2]
                    annotation["area"] = float(x2 * y2)
                    annotation["category_id"] = value["id"]

                    # Tracking the count
                    if(value["id"] == 0):
                      cnt_bor += 1

                    annotation["ignore"] = 0
                    annotation["id"] = id1
                    annotation["segmentation"] = [[x1,y1,x1,(y1 + y2), (x1 + x2), (y1 + y2), (x1 + x2), y1]]
                    id1 +=1
                    annotations.append(annotation)
        else:
          print("File: {} doesn't have any object".format(file))
      else:
        print("File: {} not found".format(file))

  attrDict["images"] = images	
  attrDict["annotations"] = annotations
  attrDict["type"] = "instances"

  # Printing out some statistics
  print(len(images))
  print("table : ",cnt_bor)
  print(len(annotations))

  # Save the final JSON file
  # jsonString = json.dumps(attrDict)
  jsonString = json.dumps(attrDict, indent = 4, sort_keys=True)
  with open(outFile, "w") as f:
    f.write(jsonString)



# Path to the pascal voc xml files 
rootDir = "test"
XMLFiles = os.listdir(rootDir)
outFile = "test.json"
# Start execution
generateVOC2Json(rootDir, XMLFiles, outFile)

