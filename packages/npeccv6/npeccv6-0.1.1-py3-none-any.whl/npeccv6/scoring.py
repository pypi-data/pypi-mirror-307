import json
import base64
import os
import cv2
import numpy as np
import keras

try:
    # Attempt relative imports (if run as a package module)
    from .model_func import load_pretrained_model
    from .predict import predict

except ImportError:
    # Fallback to absolute imports (if run as a standalone script)
    from model_func import load_pretrained_model
    from predict import predict


def init():
    # Define the model as a global variable to be used later in the predict function
    global model
    # Get the path where the model is saved, it is set in the environment variable AZUREML_MODEL_DIR by the deployment configuration
    base_path = os.getenv("AZUREML_MODEL_DIR")
    print(f"base_path: {base_path}")

    # TO DO Load config

    # View files in the model_path directory
    print("List files in the model_path directory")
    # List files and dirs in the model_path directory
    list_files(base_path)

    model_path = os.path.join(base_path, 'test.keras')  # local
    # path="../models/test.keras"
    # model_path = os.path.join(base_path, "INPUT_model", 'model.keras')  # azure

    # Load the model
    model = keras.load_model(model_path)
    print("Model loaded successfully")


def list_files(startpath):
    for root, dirs, files in os.walk(startpath):
        level = root.replace(startpath, "").count(os.sep)
        indent = " " * 4 * (level)
        print("{}{}/".format(indent, os.path.basename(root)))
        subindent = " " * 4 * (level + 1)
        for f in files:
            print("{}{}".format(subindent, f))


def run(data):
    # Load the JSON data from the POST request, print the data to see the structure and content
    data = json.loads(data)

    # Get the base64-encoded image data, print the data to see make sure it is correct
    base64_image = data["data"]

    # Decode the base64 string into bytes
    image_bytes = base64.b64decode(base64_image)

    # TO DO Preprocess image

    # Convert the bytes to a NumPy array
    nparr = np.frombuffer(image_bytes, np.uint8)

    # Decode the NumPy array to an image using OpenCV
    image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    # Get prediction
    pred, conf_score = predict(model, image)

    # Print the predicted label
    print(f"Confidence Score: {conf_score}")

    # Return Prediction
    return json.dumps(pred.tolist())


if __name__ == "__main__":
    init()
