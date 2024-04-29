import cv2
import data_extrator


def new_back_extractor(path):
    yolo_boxes = [
        (0.302267, 0.287575, 0.445844, 0.050100),
        (0.292191, 0.345691, 0.455919, 0.046092),
        (0.532116, 0.551102, 0.895466, 0.056112),
        (0.912469, 0.213427, 0.044081, 0.098196)
    ]

    results = data_extrator.extract_from_image(path, yolo_boxes)

    data_dict = {}

    data_dict['father_name'] = results[0][0][1] 
    data_dict['mother_name'] = results[1][0][1] 
    data_dict['adress'] = results[2][0][1] 
    data_dict['gender'] = results[3][0][1] 

    return data_dict