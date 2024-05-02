import cv2
from datetime import datetime
import data_extrator


def transform_date(input_date):
    input_date = input_date.replace(',', '.',)
    
    try:
        date_obj = datetime.strptime(input_date, '%d.%m.%Y')
    except ValueError:
        try:
            date_obj = datetime.strptime(input_date, '%d,%m,%Y')
        except ValueError:
            return "Invalid date format"
    
    formatted_date = date_obj.strftime('%d-%m-%Y')
    
    return formatted_date


def new_front_extractor(image_path):

    yolo_boxes = [
        (0.566990, 0.261682, 0.431068, 0.099688),
        (0.577670, 0.355140, 0.452427, 0.068536),
        (0.666990, 0.423676, 0.180583, 0.093458),
        (0.592233, 0.531153, 0.415534, 0.102804),
        (0.196117, 0.939252, 0.213592, 0.121495)
    ]




    results = data_extrator.extract_from_image(image_path, yolo_boxes)

    data_dict = {}

    data_dict['firstName'] = results[0][0][1] 
    data_dict['secondName'] = results[1][0][1] 
    data_dict['DOB'] = results[2][0][1] 
    data_dict['COB'] = results[3][0][1] 
    data_dict['CIN'] = results[4][0][1] 

    data_dict['DOB'] = transform_date(data_dict['DOB'])

    return data_dict