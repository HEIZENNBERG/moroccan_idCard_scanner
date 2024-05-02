import cv2
import os
from PIL import Image, ImageEnhance
import numpy as np

os.environ['KMP_DUPLICATE_LIB_OK']='True'
import easyocr


def preprocess_image(image_path):   
    # image = cv2.imread(image_path)
    
    pil_image = Image.fromarray(cv2.cvtColor(image_path, cv2.COLOR_BGR2RGB))
    
    enhancer = ImageEnhance.Contrast(pil_image)
    contrast_img = enhancer.enhance(1.5)

    enhancer = ImageEnhance.Brightness(contrast_img)
    bright_img = enhancer.enhance(1.2)

    sharper = ImageEnhance.Sharpness(bright_img)
    sharper_img = sharper.enhance(2)

    enhanced_image = cv2.cvtColor(np.array(sharper_img), cv2.COLOR_RGB2BGR)
    
    gray = cv2.cvtColor(enhanced_image, cv2.COLOR_BGR2GRAY)
    binary = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 11, 2)

    blurred = cv2.GaussianBlur(binary, (5, 5), 0)


    unsharp_mask = cv2.addWeighted(gray, 2, blurred, -1, 0)
    
    return unsharp_mask



def yolo_to_pixel(image, box):
    image_height, image_width = image.shape[:2]
    x_center, y_center, width, height = box
    x_min = int((x_center - width / 2) * image_width)
    y_min = int((y_center - height / 2) * image_height)
    x_max = int((x_center + width / 2) * image_width)
    y_max = int((y_center + height / 2) * image_height)
    return (x_min, y_min, x_max, y_max)


def crop_boxes(image, boxes, output_dir):
    cropped_images = []
    for i, box in enumerate(boxes):
        x_min, y_min, x_max, y_max = box
        cropped_image = image[y_min:y_max, x_min:x_max]


        # this need to go
        output_path = os.path.join(output_dir, f"cropped_{i}.jpg")


        cv2.imwrite(output_path, cropped_image)
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
    image = preprocess_image(image)
    # image = cv2.imread(image)

    pixel_boxes = [yolo_to_pixel(image, box) for box in yolo_boxes]

    dir = r"C:\Users\pc\Desktop\lp BigData\s6\cropped"
    cropped_images = crop_boxes(image, pixel_boxes, dir)
    res = perform_ocr(cropped_images)
    return res
