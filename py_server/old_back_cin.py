import cv2
import data_extrator

def safe_get(results, outer_index, inner_index):
    try:
        return results[outer_index][-1][inner_index]
    except (IndexError, KeyError):
        return None

def old_back_extractor(image_path):
    yolo_boxes = [
        (0.407193, 0.242917, 0.577339, 0.084388),
        (0.404584, 0.311332, 0.606411, 0.074141),
        (0.545844, 0.532248, 0.845695, 0.135021),
        (0.838427, 0.641953, 0.125606, 0.108499)
    ]

    results = data_extrator.extract_from_image(image_path, yolo_boxes)

    data_dict = {}

    data_dict['father_name'] = safe_get(results, 0, 1).replace("fils de", "").strip()
    data_dict['mother_name'] = safe_get(results, 1, 1).replace("et de", "").strip()
    data_dict['address'] = safe_get(results, 2, 1).replace("Adresse", "").strip()
    data_dict['gender'] = safe_get(results, 3, 1)
    
    return data_dict
  




