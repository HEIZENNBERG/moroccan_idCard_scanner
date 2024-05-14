import cv2
import numpy as np
from PIL import Image, ImageEnhance

# Load reference card images
old_front = cv2.imread(r'C:\Users\pc\Desktop\lp BigData\s6\card_references\old_front.jpg', cv2.IMREAD_GRAYSCALE)
old_back = cv2.imread(r'C:\Users\pc\Desktop\lp BigData\s6\card_references\old_back.jpg', cv2.IMREAD_GRAYSCALE)
new_front = cv2.imread(r'C:\Users\pc\Desktop\lp BigData\s6\card_references\new_front.jpg', cv2.IMREAD_GRAYSCALE)
new_back = cv2.imread(r'C:\Users\pc\Desktop\lp BigData\s6\card_references\new_back.jpg', cv2.IMREAD_GRAYSCALE)

# Initialize SIFT detector
sift = cv2.SIFT_create()

def extract_features(image):
    keypoints, descriptors = sift.detectAndCompute(image, None)
    return keypoints, descriptors

def preprocess_image(image_path):   
    # image = cv2.imread(image_path)
    
    pil_image = Image.fromarray(cv2.cvtColor(image_path, cv2.COLOR_BGR2RGB))
    
    enhancer = ImageEnhance.Contrast(pil_image)
    contrast_img = enhancer.enhance(1.5)

    enhancer = ImageEnhance.Brightness(contrast_img)
    bright_img = enhancer.enhance(1.6)

    sharper = ImageEnhance.Sharpness(bright_img)
    sharper_img = sharper.enhance(2)

    enhanced_image = cv2.cvtColor(np.array(sharper_img), cv2.COLOR_RGB2BGR)
    
    gray = cv2.cvtColor(enhanced_image, cv2.COLOR_BGR2GRAY)
    binary = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 11, 2)

    blurred = cv2.GaussianBlur(binary, (5, 5), 0)


    unsharp_mask = cv2.addWeighted(gray, 2, blurred, -1, 0)
    
    return unsharp_mask


def match_features(descriptors1, descriptors2):
    flann = cv2.FlannBasedMatcher(dict(algorithm=1, trees=5), dict(checks=50))
    matches = flann.knnMatch(descriptors1, descriptors2, k=2)
    good_matches = []
    for m, n in matches:
        if m.distance < 0.7 * n.distance:
            good_matches.append(m)
    return len(good_matches)



def find_most_similar_card(input_card):
    scores = []
    keypoints_input, descriptors_input = extract_features(input_card)
    for ref_card in [old_front, old_back, new_front, new_back]:
        keypoints_ref, descriptors_ref = extract_features(ref_card)
        score = match_features(descriptors_input, descriptors_ref)
        scores.append(score)
    most_similar_card_type = np.argmax(scores) + 1  # Card types are numbered from 1 to 4
    return most_similar_card_type




# def detect_rotation(input_image, similar_image):

#     # Detect ORB keypoints and descriptors
#     orb = cv2.ORB_create()
#     kp1, des1 = orb.detectAndCompute(input_image, None)
#     kp2, des2 = orb.detectAndCompute(similar_image, None)

#     # Match keypoints
#     bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
#     matches = bf.match(des1, des2)

#     # Sort matches by distance
#     matches = sorted(matches, key=lambda x: x.distance)

#     # Extract matched keypoints
#     src_pts = np.float32([kp1[m.queryIdx].pt for m in matches]).reshape(-1, 1, 2)
#     dst_pts = np.float32([kp2[m.trainIdx].pt for m in matches]).reshape(-1, 1, 2)

#     # Estimate perspective transformation
#     M, _ = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC)

#     # Calculate rotation angle
#     rotation_angle = np.arctan2(M[1, 0], M[0, 0]) * (180 / np.pi)

#     return rotation_angle




# def rotate_image(image, angle):
#     # Get image dimensions
#     height, width = image.shape[:2]
    
#     # Calculate the rotation matrix
#     rotation_matrix = cv2.getRotationMatrix2D((width/2, height/2), -angle, 1)
    
#     # Apply the rotation to the image
#     rotated_image = cv2.warpAffine(image, rotation_matrix, (width, height))
    
#     return rotated_image





def classify(input_card_image):
    image = preprocess_image(input_card_image)
    most_similar_card_type = find_most_similar_card(image)

    # if most_similar_card_type == 1:
    #     rotation_ref = old_front
    # elif most_similar_card_type == 2:
    #     rotation_ref = old_back
    # elif most_similar_card_type == 3:
    #     rotation_ref = new_front
    # else:
    #     rotation_ref = new_back

    # # Detect rotation angle
    # rotation_angle = detect_rotation(input_card_image, rotation_ref)

    # # Check if rotation is necessary
    # if abs(rotation_angle) > 1.0:  # You can adjust the threshold for rotation angle
    #     # Rotate the input card image
    #     image_rotated = rotate_image(input_card_image, rotation_angle)
    # else:
    #     image_rotated = input_card_image  # No rotation needed

    return most_similar_card_type     #, image_rotated





# # Example usage
# input_card_image = cv2.imread(r'C:\Users\pc\Desktop\lp BigData\s6\test_crop\crop5.jpg')
# most_similar_card_type, image_rotated = classify(input_card_image)



# print("Most similar card type:", most_similar_card_type)
