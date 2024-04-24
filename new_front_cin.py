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




image_path = r'C:\Users\pc\Desktop\lp BigData\s6\moroccan_idCard_scanner\ids\new_card\id_2_3.jpg'

yolo_boxes = [
    (0.540037, 0.281792, 0.379888, 0.060694),
    (0.548417, 0.390173, 0.381750, 0.052023),
    (0.648976, 0.432081, 0.158287, 0.043353),
    (0.590317, 0.546243, 0.435754, 0.046243),
    (0.213222, 0.913295, 0.184358, 0.069364)
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