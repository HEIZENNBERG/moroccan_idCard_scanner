from flask import Flask, request, jsonify
import base64
import os

app = Flask(__name__)

@app.route('/image', methods=['POST'])
def process_images():
    if request.method == 'POST':
        data = request.get_json()
        images = data.get('images')
        if images:
            for index, base64_image in enumerate(images):
                # Decode base64 string to bytes
                image_bytes = base64.b64decode(base64_image)
                # Save the image to a file
                filename = f'image_{index}.jpg'
                with open(filename, 'wb') as f:
                    f.write(image_bytes)
            return jsonify({'message': f'{len(images)} images received and saved successfully'})
        else:
            return jsonify({'error': 'No image data received'})
    else:
        return jsonify({'error': 'Invalid request method'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
