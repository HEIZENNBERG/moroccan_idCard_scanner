import cv2
from datetime import datetime
import data_extrator


image_path = r'C:\Users\pc\Desktop\lp BigData\s6\cni-verso.jpg'

def old_back_extractor(image_path):
    yolo_boxes = [
        (0.379816, 0.240956, 0.533501, 0.058140),
        (0.372697, 0.293282, 0.539363, 0.046512),
        (0.517169, 0.514212, 0.804858, 0.116279),
        (0.836265, 0.612403, 0.076214, 0.069767)
    ]


    results = data_extrator.extract_from_image(image_path, yolo_boxes)

    data_dict = {}

    data_dict['father_name'] = results[0][0][1] 
    data_dict['mother_name'] = results[1][0][1] 
    data_dict['adress'] = results[2][0][1] 
    data_dict['gender'] = results[3][0][1] 


    return data_dict