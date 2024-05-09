import cv2
import numpy as np

def preprocess_and_crop(img):
    # Convert to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    # Initialize Canny parameters
    canny_low = 100
    canny_high = 75

    while True:
        # Blur the image
        print(canny_low , " : ", canny_high)
        blurred = cv2.GaussianBlur(gray, (11, 11), 0)
        
        # Apply Canny edge detection
        edges = cv2.Canny(blurred, canny_low, canny_high)

        # Dilate the edges
        imgDial = cv2.dilate(edges, (1, 1), iterations=2)
        
        # Find contours
        contours, _ = cv2.findContours(imgDial, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # Find the largest contour
        max_area = 0
        max_contour = None
        for contour in contours:
            area = cv2.contourArea(contour)
            if area > max_area:
                max_area = area
                max_contour = contour
        
        # If no contour is found or if bounding box width is too small, adjust Canny parameters
        x, y, w, h = cv2.boundingRect(max_contour)
        if canny_low < 0 or canny_high < 0:
            break  
        elif w < img.shape[1] * 0.6: 
            if h < img.shape[0] * 0.8:
                canny_low -= 20
                canny_high -= 20
        else:
            break
    
    # Crop the card region
    roi = img[y:y+h, x:x+w]

    # Resize the cropped card
    resized_img = cv2.resize(roi, (1120, 714))
    cv2.imwrite(r'C:\Users\pc\Desktop\lp BigData\s6\test_crop\processed.jpg', edges) 

    # Draw rectangle around the card
    cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 2)

    return resized_img, img

# # Example usage
# image_path = r"C:\Users\pc\Desktop\lp BigData\s6\moroccan_idCard_scanner\ids\new_card\id_2_3.jpg"
# img = cv2.imread(image_path)
# cropped_image, original_with_rect = preprocess_and_crop(img)

# # Save the cropped image
# cv2.imwrite(r'C:\Users\pc\Desktop\lp BigData\s6\test_crop\Image_crop.jpg', cropped_image)

# # Save the original image with rectangle drawn around the card
# cv2.imwrite(r'C:\Users\pc\Desktop\lp BigData\s6\test_crop\Image_cont.jpg', original_with_rect)
