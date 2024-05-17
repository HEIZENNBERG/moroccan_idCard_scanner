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
        (0.558591, 0.265587, 0.362849, 0.098411),
        (0.543896, 0.357274, 0.331952, 0.084963),
        (0.663338, 0.435819, 0.213640, 0.072127),
        (0.606820, 0.546760, 0.457046, 0.100856),
        (0.221929, 0.912592, 0.200452, 0.174817)
    ]

    results = data_extrator.extract_from_image(image_path, yolo_boxes)

    data_dict = {}

    data_dict['firstName'] = data_extrator.safe_get(results, 0, 1)
    data_dict['secondName'] = data_extrator.safe_get(results,1 , 1)
    data_dict['COB'] = data_extrator.safe_get(results, 3, 1)
    data_dict['CIN'] = data_extrator.safe_get(results, 4, 1) 

    if data_extrator.safe_get(results, 2, 1) is not None:
        data_dict['DOB'] = transform_date(data_extrator.safe_get(results, 2, 1))
    else:
        data_dict['DOB'] = data_extrator.safe_get(results, 2, 1)

    return data_dict