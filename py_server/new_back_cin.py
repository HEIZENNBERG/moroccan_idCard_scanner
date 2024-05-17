import cv2
import data_extrator



def new_back_extractor(path):
    yolo_boxes = [
        (0.342489, 0.266487, 0.497503, 0.077338),
        (0.335574, 0.336031, 0.522090, 0.085731),
        (0.484057, 0.532974, 0.775259, 0.095923),
        (0.911839, 0.222445, 0.045340, 0.092184)
    ]

    results = data_extrator.extract_from_image(path, yolo_boxes)

    data_dict = {}

    data_dict['father_name'] = data_extrator.safe_get(results, 0, 1)
    data_dict['mother_name'] = data_extrator.safe_get(results, 1, 1)
    data_dict['address'] = data_extrator.safe_get(results, 2, 1)
    data_dict['gender'] = data_extrator.safe_get(results, 3, 1)

    return data_dict

