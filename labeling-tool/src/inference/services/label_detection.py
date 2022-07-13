import os
import io
from google.cloud import vision

class LabelDetector:

    def __init__(self, vision_client):
        self.vision_client = vision_client

    def detect_label_single_image(self, vision_image):
        labels = self.vision_client.label_detection(image=vision_image)
        labels_dict = {}
        for label in labels.label_annotations:
            if (label.description not in labels_dict.keys()) or ((
                    label.description in labels_dict.keys()) and (labels_dict[label.description] < label.score)):
                labels_dict[label.description] = label.score

        annotations = self.vision_client.web_detection(image=vision_image).web_detection
        if annotations.best_guess_labels:
            for label in annotations.best_guess_labels:
                labels_dict[label.label] = 1
        if annotations.web_entities:
            for entity in annotations.web_entities:
                labels_dict[entity.description] = entity.score

        return labels_dict

    def detect_label_directory(self, dir_path, conf_threshold):
        labels_dict = {}
        for file in os.listdir(dir_path):
            with io.open(os.path.join(dir_path, file), 'rb') as image_file:
                print("Detecting labels for file", str(file), "...")
                content = image_file.read()
                vision_image = vision.Image(content=content)
                # get labels
                try:
                    labels = self.vision_client.label_detection(image=vision_image)
                    for label in labels.label_annotations:
                        label_key = label.description.lower()
                        if (label_key not in labels_dict.keys()) or ((label_key in labels_dict.keys()) and (labels_dict[label_key] < label.score)):
                            if (label.score >= conf_threshold):
                                print("Adding label", label_key)
                                labels_dict[label_key] = label.score
                            else:
                                print("Confidence for label", label_key, "too low.")
                except:
                    console.log("An error occurred when fetching labels")
                # get annotations
                try:
                    annotations = self.vision_client.web_detection(image=vision_image).web_detection
                    if annotations.best_guess_labels:
                        for label in annotations.best_guess_labels:
                            labels_dict[label.label.lower()] = 1
                    if annotations.web_entities:
                        for entity in annotations.web_entities:
                            entity_key = entity.description.lower()
                            if (entity_key not in labels_dict.keys()) or ((entity_key in labels_dict.keys()) and (labels_dict[entity_key] < entity.score)):
                                if (entity.score >= conf_threshold):
                                    print("Adding label", entity_key)
                                    labels_dict[entity_key] = entity.score
                                else:
                                    print("Confidence for label", entity_key, "too low.")
                except:
                    console.log("An error occurred when fetching annotations")
        print("Labels found:", labels_dict)
        return labels_dict