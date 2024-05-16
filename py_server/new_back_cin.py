import cv2
import data_extrator


def new_back_extractor(path):
    yolo_boxes = [
        (0.337531, 0.288577, 0.526448, 0.076152),
        (0.329345, 0.353707, 0.547859, 0.074148),
        (0.535264, 0.547094, 0.901763, 0.096192),
        (0.911839, 0.222445, 0.045340, 0.092184)
    ]

    results = data_extrator.extract_from_image(path, yolo_boxes)

    data_dict = {}

    data_dict['father_name'] = results[0][0][1] if results[0][0][1] else 'None'
    data_dict['mother_name'] = results[1][0][1] if results[1][0][1] else 'None'
    data_dict['address'] = results[2][0][1] if results[2][0][1] else 'None'
    data_dict['gender'] = results[3][0][1] if results[3][0][1] else 'None'

    return data_dict