from flask import Flask, request, jsonify
import base64
import numpy as np 
import os
import cv2
import new_back_cin, new_front_cin, old_back_cin, old_front_cin, card_type,  crop

def CIN_Reader(image):

    img_type = card_type.classify(image)
    cropped_image = crop.crop(image)

    if img_type == 1:
        dict_res = old_front_cin.old_front_extractor(cropped_image)
    elif img_type == 2:
        dict_res = old_back_cin.old_back_extractor(cropped_image)
    elif img_type == 3:
        dict_res = new_front_cin.new_front_extractor(cropped_image)
    else:
        dict_res = new_back_cin.new_back_extractor(cropped_image)

    return dict_res



app = Flask(__name__)

@app.route('/image', methods=['POST'])
def process_images():
    if request.method == 'POST':
        data = request.get_json()
        images = data.get('images')
        if images:
            results = []
            for index, base64_image in enumerate(images):
                # Decode base64 string to bytes
                image_bytes = base64.b64decode(base64_image)
                # Convert bytes to OpenCV image format
                image_np = cv2.imdecode(np.frombuffer(image_bytes, np.uint8), cv2.IMREAD_COLOR)
                # Run the main function on the image
                dict_result = CIN_Reader(image_np)
                results.append(dict_result)
            return jsonify({'results': results})
        else:
            return jsonify({'error': 'No image data received'})
    else:
        return jsonify({'error': 'Invalid request method'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
