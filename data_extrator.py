import cv2
import os

os.environ['KMP_DUPLICATE_LIB_OK']='True'
import easyocr

def preprocess_image(image_path):   
    image = cv2.imread(image_path)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    binary = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 11, 2)

    blurred = cv2.GaussianBlur(binary, (5, 5), 0)


    unsharp_mask = cv2.addWeighted(gray, 1.7, blurred, -0.5, 0)

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
        output_path = os.path.join(output_dir, f"cropped_{i}.jpg")
        cv2.imwrite(output_path, cropped_image)
        cropped_images.append(cropped_image)
    return cropped_images


def perform_ocr(images):
    reader = easyocr.Reader(['fr'], gpu=False)  
    ocr_results = []
    for img in images:
        result = reader.readtext(img, paragraph=True)
        ocr_results.append(result)
    return ocr_results



def extract_from_image(image , yolo_boxes):
    # image = preprocess_image(image)
    image = cv2.imread(image)

    pixel_boxes = [yolo_to_pixel(image, box) for box in yolo_boxes]

    dir = r"C:\Users\pc\Desktop\lp BigData\s6\cropped"
    cropped_images = crop_boxes(image, pixel_boxes, dir)
    res = perform_ocr(cropped_images)
    return res
