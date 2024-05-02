import cv2
from datetime import datetime
import data_extrator


image_path = r'C:\Users\pc\Desktop\lp BigData\s6\cni-verso.jpg'

def old_back_extractor(image_path):
    yolo_boxes = [
        (0.376466, 0.229328, 0.530151, 0.086563),
        (0.367253, 0.304264, 0.558626, 0.089147),
        (0.531407, 0.512920, 0.823283, 0.131783),
        (0.839196, 0.618863, 0.092127, 0.080103)
    ]



    results = data_extrator.extract_from_image(image_path, yolo_boxes)

    data_dict = {}

    data_dict['father_name'] = results[0][0][1] 
    data_dict['mother_name'] = results[1][0][1] 
    data_dict['adress'] = results[2][0][1] 
    data_dict['gender'] = results[3][0][1] 


    return data_dict