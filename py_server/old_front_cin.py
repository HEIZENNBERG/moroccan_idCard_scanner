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
        (0.260700, 0.336825, 0.516537, 0.149879),
        (0.210846, 0.456487, 0.417802, 0.094279),
        (0.330739, 0.540693, 0.231518, 0.117647),
        (0.255107, 0.657131, 0.509241, 0.081386),
        (0.773833, 0.812248, 0.195525, 0.209508)
    ]




    results = data_extrator.extract_from_image(image_path, yolo_boxes)

    data_dict = {}

    data_dict['firstName'] = data_extrator.safe_get(results, 0, 1)
    data_dict['secondName'] = data_extrator.safe_get(results, 1, 1) 
    data_dict['COB'] = data_extrator.safe_get(results, 3, 1).replace("à", "").strip()
    data_dict['CIN'] =data_extrator.safe_get(results, 4, 1)
    
    if data_extrator.safe_get(results, 2, 1) is not None:
        data_dict['DOB'] = transform_date(data_extrator.safe_get(results, 2, 1))
    else:
        data_dict['DOB'] = None

    return data_dict


