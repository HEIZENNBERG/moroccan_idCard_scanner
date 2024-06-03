import cv2
import numpy as np
import pickle
from PIL import Image, ImageEnhance

# Load precomputed features from the pickle file
with open('reference_features.pkl', 'rb') as f:
    ref_features = pickle.load(f)

# Initialize SIFT detector
sift = cv2.SIFT_create()

def preprocess_image(image_path):   
    # image = cv2.imread(image_path)
    
    pil_image = Image.fromarray(cv2.cvtColor(image_path, cv2.COLOR_BGR2RGB))
    
    enhancer = ImageEnhance.Contrast(pil_image)
    contrast_img = enhancer.enhance(1.5)

    enhancer = ImageEnhance.Brightness(contrast_img)
    bright_img = enhancer.enhance(1.5)

    sharper = ImageEnhance.Sharpness(bright_img)
    sharper_img = sharper.enhance(1.5)

    enhanced_image = cv2.cvtColor(np.array(sharper_img), cv2.COLOR_RGB2BGR)
    
    gray = cv2.cvtColor(enhanced_image, cv2.COLOR_BGR2GRAY)
    binary = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 11, 2)

    blurred = cv2.GaussianBlur(binary, (5, 5), 0)


    unsharp_mask = cv2.addWeighted(gray, 2, blurred, -1, 0)
   
    return unsharp_mask

def extract_features(image):
    keypoints, descriptors = sift.detectAndCompute(image, None)
    return keypoints, descriptors

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
    for keypoints_ref, descriptors_ref in ref_features:
        descriptors_ref = np.array(descriptors_ref, dtype=np.float32)  # Convert descriptors back to numpy array
        score = match_features(descriptors_input, descriptors_ref)
        scores.append(score)
    most_similar_card_type = np.argmax(scores) + 1  # Card types are numbered from 1 to 4
    return most_similar_card_type

def classify(input_card_image):
    processed_image = preprocess_image(input_card_image)
    most_similar_card_type = find_most_similar_card(processed_image)
    return most_similar_card_type, processed_image



