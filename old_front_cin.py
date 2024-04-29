import cv2
from datetime import datetime
import data_extrator


def transform_date(input_date):
    input_date = input_date.replace(',', '.')
    
    try:
        date_obj = datetime.strptime(input_date, '%d.%m.%Y')
    except ValueError:
        try:
            date_obj = datetime.strptime(input_date, '%d,%m,%Y')
        except ValueError:
            return "Invalid date format"
    
    formatted_date = date_obj.strftime('%d-%m-%Y')
    
    return formatted_date




image_path = r'C:\Users\pc\Desktop\lp BigData\s6\Image_crop.jpg'

yolo_boxes = [
    (0.177232, 0.327731, 0.331250, 0.053221),
    (0.212500, 0.454482, 0.410714, 0.057423),
    (0.319643, 0.528711, 0.173214, 0.054622),
    (0.215625, 0.655462, 0.377679, 0.058824),
    (0.821429, 0.803221, 0.183929, 0.057423)
]

results = data_extrator.extract_from_image(image_path, yolo_boxes)

data_dict = {}

data_dict['firstName'] = results[0][0][1] 
data_dict['secondName'] = results[1][0][1] 
data_dict['DOB'] = results[2][0][1] 
data_dict['COB'] = results[3][0][1] 
data_dict['CIN'] = results[4][0][1] 

data_dict['DOB'] = transform_date(data_dict['DOB'])

print(data_dict)