import cv2
import data_extrator



def old_back_extractor(image_path):
    yolo_boxes = [
        (0.359693, 0.235141, 0.715770, 0.076523),
        (0.363082, 0.303863, 0.725260, 0.077266),
        (0.478762, 0.522660, 0.945775, 0.127043),
        (0.827384, 0.628529, 0.121103, 0.141159)
    ]

    results = data_extrator.extract_from_image(image_path, yolo_boxes)

    data_dict = {}

    data_dict['father_name'] = results[0][-1][1].replace("fils de", "").strip()
    data_dict['mother_name'] = results[1][-1][1].replace("et de", "").strip()
    data_dict['address'] = results[2][-1][1].replace("Adresse", "").strip()
    data_dict['gender'] = results[3][-1][1] 


    return data_dict
  




