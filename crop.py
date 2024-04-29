import cv2
from PIL import Image, ImageEnhance
import numpy as np

def preprocess_and_crop(image_path):
    # Load the image
    img = cv2.imread(image_path)
    
    # Enhance brightness
    pil_image = Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
    enhancer = ImageEnhance.Brightness(pil_image)
    bright_img = enhancer.enhance(0.6)
    enhanced_image = cv2.cvtColor(np.array(bright_img), cv2.COLOR_RGB2BGR)

    # Convert to grayscale
    gray = cv2.cvtColor(enhanced_image, cv2.COLOR_BGR2GRAY)
    
    # Apply adaptive thresholding
    binary = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 11, 2)

    # Blur the image
    blurred = cv2.GaussianBlur(binary, (5, 5), 0)
    cv2.imwrite(r'C:\Users\pc\Desktop\lp BigData\s6\test_crop\gray.jpg', blurred) 

    # Find contours
    contours, _ = cv2.findContours(blurred, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Find the largest contour
    max_area = 0
    max_contour = None
    for contour in contours:
        area = cv2.contourArea(contour)
        if area > max_area:
            max_area = area
            max_contour = contour

    # Find bounding box of the largest contour
    x, y, w, h = cv2.boundingRect(max_contour)

    # Crop the card region
    roi = img[y:y+h, x:x+w]

    # Resize the cropped card
    resized_img = cv2.resize(roi, (1120, 630))

    # Draw rectangle around the card
    cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 2)

    return resized_img, img




# Example usage
image_path = r'C:\Users\pc\Desktop\lp BigData\s6\test_crop\crop3.jpg'
cropped_image, original_with_rect = preprocess_and_crop(image_path)

# Save the cropped image
cv2.imwrite(r'C:\Users\pc\Desktop\lp BigData\s6\test_crop\Image_crop.jpg', cropped_image)

# Save the original image with rectangle drawn around the card
cv2.imwrite(r'C:\Users\pc\Desktop\lp BigData\s6\test_crop\Image_cont.jpg', original_with_rect)
