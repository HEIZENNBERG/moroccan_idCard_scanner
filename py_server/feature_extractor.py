import cv2
import numpy as np
import pickle

# Load reference card images
old_front = cv2.imread(r'C:\Users\pc\Desktop\lp BigData\s6\card_references\old_front.jpg', cv2.IMREAD_GRAYSCALE)
old_back = cv2.imread(r'C:\Users\pc\Desktop\lp BigData\s6\card_references\old_back.jpg', cv2.IMREAD_GRAYSCALE)
new_front = cv2.imread(r'C:\Users\pc\Desktop\lp BigData\s6\card_references\new_front.jpg', cv2.IMREAD_GRAYSCALE)
new_back = cv2.imread(r'C:\Users\pc\Desktop\lp BigData\s6\card_references\new_back.jpg', cv2.IMREAD_GRAYSCALE)

sift = cv2.SIFT_create()

def extract_features(image):
    keypoints, descriptors = sift.detectAndCompute(image, None)
    keypoints_list = [(kp.pt, kp.size, kp.angle, kp.response, kp.octave, kp.class_id) for kp in keypoints]
    descriptors_list = descriptors.tolist()
    return keypoints_list, descriptors_list


ref_cards = [old_front, old_back, new_front, new_back]
ref_features = [extract_features(card) for card in ref_cards]

with open('reference_features.pkl', 'wb') as f:
    pickle.dump(ref_features, f)

print("Reference card features have been saved.")
