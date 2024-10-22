import cv2
import os

import numpy as np

os.environ['KMP_DUPLICATE_LIB_OK']='True'
import easyocr


def yolo_to_pixel(image, box):
    image_height, image_width = image.shape[:2]
    x_center, y_center, width, height = box
    x_min = int((x_center - width / 2) * image_width)
    y_min = int((y_center - height / 2) * image_height)
    x_max = int((x_center + width / 2) * image_width)
    y_max = int((y_center + height / 2) * image_height)
    return (x_min, y_min, x_max, y_max)

def safe_get(results, outer_index, inner_index):
    try:
        return results[outer_index][-1][inner_index]
    except (IndexError, KeyError):
        return "no text detected"


def crop_boxes(image, boxes):
    cropped_images = []
    for i, box in enumerate(boxes):
        x_min, y_min, x_max, y_max = box
        cropped_image = image[y_min:y_max, x_min:x_max]
        cropped_images.append(cropped_image)
    return cropped_images


def image_resize(image, factor):
    height, width = image.shape[:2]

    new_height = int(height * factor)
    new_width = int(width * factor)

    resized_image = cv2.resize(image, (new_width, new_height))
    return resized_image

def perform_ocr(images):
    reader = easyocr.Reader(['fr'], gpu=True)  
    ocr_results = []
    for img in images:
        result = reader.readtext(img, paragraph=True)
        
        if len(result) == 0:
            resized_img = image_resize(img , 2)
            result = reader.readtext(resized_img, paragraph=True)
            

        ocr_results.append(result)
    return ocr_results



def extract_from_image(image , yolo_boxes):

    pixel_boxes = [yolo_to_pixel(image, box) for box in yolo_boxes]

    cropped_images = crop_boxes(image, pixel_boxes)
    res = perform_ocr(cropped_images)
    return res
