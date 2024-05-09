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


def old_front_extractor(image_path):
    yolo_boxes = [
        (0.210268, 0.329132, 0.408036, 0.126050),
        (0.217411, 0.454482, 0.433036, 0.096639),
        (0.321429, 0.537115, 0.201786, 0.102241),
        (0.232589, 0.649860, 0.411607, 0.103641),
        (0.829464, 0.807423, 0.221429, 0.110644)
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