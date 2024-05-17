from ultralytics import YOLO

def crop(img):

    model = YOLO(r'C:\Users\pc\Desktop\lp BigData\s6\moroccan_idCard_scanner\model\train5\weights\best.pt')

    results = model(img, conf=0, max_det=1) 
    box  = results[0].boxes.xyxy.tolist() 
    x1, y1, x2, y2 = box[0]
    cropped_img = img[int(y1):int(y2), int(x1):int(x2)]
    
    return cropped_img


