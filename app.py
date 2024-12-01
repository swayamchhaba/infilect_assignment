import cv2
import base64
import numpy as np
from flask import Flask, request, jsonify

# Initialize Flask app
app = Flask(__name__)

# Paths to the model files
prototxt_path = "model/deploy.prototxt"
model_path = "model/mobilenet_iter_73000.caffemodel"

# Load the class labels
LABELS = ["background", "aeroplane", "bicycle", "bird", "boat", "bottle", "bus", "car", "cat", "chair",
          "cow", "diningtable", "dog", "horse", "motorbike", "person", "pottedplant", "sheep", "sofa", "train", "tvmonitor"]

# Load the pre-trained model
net = cv2.dnn.readNetFromCaffe(prototxt_path, model_path)

@app.route('/upload', methods=['POST'])
def upload_image():
    # Ensure an image is uploaded
    if 'image' not in request.files:
        return jsonify({"error": "No image uploaded. Please provide an image file."}), 400

    image = request.files['image']
    if image.filename == '':
        return jsonify({"error": "No image selected."}), 400

    # Read the image from memory
    np_img = np.frombuffer(image.read(), np.uint8)
    img = cv2.imdecode(np_img, cv2.IMREAD_COLOR)

    # Perform detection
    annotated_img = detect_objects(img)

    # Encode the processed image to base64
    _, buffer = cv2.imencode('.jpg', annotated_img)
    encoded_image = base64.b64encode(buffer).decode('utf-8')

    # Return the base64-encoded image
    return jsonify({"image_with_visualizations": encoded_image})


def detect_objects(image):
    """
    Detect multiple objects in the image and draw bounding boxes around them.
    """
    h, w = image.shape[:2]

    # Prepare the input blob for the model
    blob = cv2.dnn.blobFromImage(cv2.resize(image, (300, 300)), 0.007843, (300, 300), 127.5)
    net.setInput(blob)
    detections = net.forward()

    # Iterate through the detections
    for i in range(detections.shape[2]):
        confidence = detections[0, 0, i, 2]

        # Filter out weak detections
        if confidence > 0.2:  # Confidence threshold
            idx = int(detections[0, 0, i, 1])
            label = LABELS[idx]
            box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
            (startX, startY, endX, endY) = box.astype("int")

            # Draw bounding box and label
            cv2.rectangle(image, (startX, startY), (endX, endY), (0, 255, 0), 2)
            text = f"{label}: {confidence:.2f}"
            cv2.putText(image, text, (startX, startY - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

    return image


if __name__ == "__main__":
    app.run(debug=True)
