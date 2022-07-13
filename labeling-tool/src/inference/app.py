import os
import traceback
from datetime import datetime
import cv2
import numpy as np
from pathlib import Path
import time

from flask import Flask, request, jsonify, Response
from google.cloud import vision

from services.label_detection import LabelDetector
from services.text_detection import TextDetector
from services.object_counting import ObjectCounter
from services.logo_detection import LogoDetector
from services.similar_image_search import SimilarImageSearch

# initializing Google Vision client
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'env.json'
vision_client = vision.ImageAnnotatorClient()

# initialize service objects
object_counter = ObjectCounter(vision_client)
label_detector = LabelDetector(vision_client)
text_detector = TextDetector(vision_client)
logo_detector = LogoDetector(vision_client)
similar_image_search = SimilarImageSearch(vision_client)

# path to images
images_path = "../../public/data/items"

# minimum number of images in folder to classify
min_images = 3

# initialize Flask app
app = Flask(__name__)


@app.route("/")
def hello():
    return "Hello world!"


@app.route("/receiveImage", methods=["POST"])
def receive_image():
    # get shoe id
    shoe_id = request.args.get('shoe_id')
    image_name = request.args.get('image_name')
    # create dir for shoe_id if not existing already
    dir_path = os.path.join(images_path, shoe_id)
    if not os.path.exists(dir_path):
        os.mkdir(dir_path)
    # get image from request
    nparr = np.frombuffer(request.data, np.uint8)
    image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    # save image to dir for shoe id
    image_path = os.path.join(dir_path, image_name + ".jpg")
    cv2.imwrite(image_path, image)
    return jsonify("Image saved to " + image_path)


def get_latest_dir():
    image_folder_paths = sorted(Path(images_path).iterdir(), reverse=True)
    latest_dir = image_folder_paths[0]
    # check if quality was already assigned in attributes.json
    return latest_dir


def get_all_images_in_dir(dir_path):
    image_paths = []
    for relative_path in os.listdir(dir_path):
        file_path = os.path.join(dir_path, relative_path)
        if os.path.isfile(file_path):
            if not file_path.endswith(".json"):
                item_id = os.path.basename(os.path.normpath(dir_path))
                image_path = os.path.join(item_id, relative_path)
                image_paths.append(image_path)
    return image_paths


def get_attributes_in_dir(dir_path):
    attribute_path = ""
    for relative_path in os.listdir(dir_path):
        file_path = os.path.join(dir_path, relative_path)
        if os.path.isfile(file_path):
            if file_path.endswith(".json"):
                item_id = os.path.basename(os.path.normpath(dir_path))
                attribute_path = os.path.join(item_id, relative_path)
    return attribute_path


def get_num_images_in_dir(dir_path):
    num_images = 0
    for relative_path in os.listdir(dir_path):
        file_path = os.path.join(dir_path, relative_path)
        if os.path.isfile(file_path):
            if not file_path.endswith(".json"):
                num_images += 1
    return num_images


@app.route("/streamUpdate")
def stream_update():

    def get_data():
        current_dir = get_latest_dir()
        current_num_images = get_num_images_in_dir(current_dir)
        while True:
            while True:
                latest_dir = get_latest_dir()
                if current_dir != latest_dir:
                    current_dir = latest_dir
                    break
                elif current_num_images != get_num_images_in_dir(latest_dir):
                    current_num_images = get_num_images_in_dir(latest_dir)
                    break
#             labels_dict = label_detector.detect_label_directory(current_dir)
            print("Change detected. Current directory is", current_dir)
            yield f'data: {current_dir} \n\n'

    response = Response(get_data(), mimetype="text/event-stream")
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response



### INFERENCE METHODS ###

@app.route("/getLatestImages", methods=["GET"])
def get_latest_images():
    print("Collecting latest images...")
    latest_dir = get_latest_dir()
    image_paths = get_all_images_in_dir(latest_dir)
    print(image_paths)
    json_response = jsonify(image_paths)
    response = json_response
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response


@app.route("/getLatestAttributes", methods=["GET"])
def get_latest_attributes():
    print("Collecting latest ttributes...")
    latest_dir = get_latest_dir()
    attributes_path = get_attributes_in_dir(latest_dir)
    print(attributes_path)
    json_response = jsonify(attributes_path)
    response = json_response
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response


@app.route("/countObjects", methods=["GET"])
def count_objects():
    print("Counting objects...")
    current_dir = get_latest_dir()
    object_count = object_counter.count_directory(current_dir)
    print(str(object_count), "object(s) found.")
    response = Response(str(object_count))
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response

@app.route("/detectLabels", methods=["GET"])
def detect_labels():
    print("Detecting labels...")
    current_dir = get_latest_dir()
    labels_dict = label_detector.detect_label_directory(current_dir, 0.8)
    json_response = jsonify(labels_dict)
    response = json_response
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response

@app.route("/findSimilarImages", methods=["GET"])
def find_similar_images():
    print("Searching for similar images...")
    current_dir = get_latest_dir()
    print(current_dir)
    urls_list = similar_image_search.search_similar_images_directory(current_dir)
    print(urls_list)
    json_response = jsonify(urls_list)
    response = json_response
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response


@app.route("/assignQuality", methods=["POST"])
def assign_quality():
    print("Assigning quality...")
    current_dir = get_latest_dir()

    urls_list = similar_image_search.search_similar_images_directory(current_dir)
    print(urls_list)
    json_response = jsonify(urls_list)
    response = json_response
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response



### UNUSED

@app.route("/detectText", methods=["POST"])
def detect_text():
    image = request.data
    vision_image = vision.Image(content=image)
    texts_list = text_detector.detect_text_single_image(vision_image)
    return jsonify(texts_list)


@app.route("/detectLogos", methods=["POST"])
def detect_logos():
    image = request.data
    vision_image = vision.Image(content=image)
    logos_dict = logo_detector.detect_logos_single_image(vision_image)
    return jsonify(logos_dict)



### OTHER

@app.errorhandler(Exception)
def handle_exception(e):
    return jsonify(stackTrace=traceback.format_exc())


if __name__ == '__main__':
#     app.run(debug=True, host='localhost', port=2224)
    app.run(host='0.0.0.0', port=2224, debug=True, threaded=True)
