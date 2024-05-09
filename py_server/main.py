import cv2
import new_back_cin, new_front_cin, old_back_cin, old_front_cin, card_type,  crop

image = cv2.imread(r"C:\Users\pc\Desktop\lp BigData\s6\moroccan_idCard_scanner\py_server\image_0.jpg")

img_type = card_type.classify(image)

print(img_type)

cropped_image, original_img = crop.preprocess_and_crop(image)


cv2.imwrite(r"C:\Users\pc\Desktop\lp BigData\s6\moroccan_idCard_scanner\ids\ress.jpg", cropped_image)

if img_type == 1:
    dict_res = old_front_cin.old_front_extractor(cropped_image)
elif img_type == 2:
    dict_res = old_back_cin.old_back_extractor(cropped_image)
elif img_type == 3:
    dict_res = new_front_cin.new_front_extractor(cropped_image)
else:
    dict_res = new_back_cin.new_back_extractor(cropped_image)


print(dict_res)
