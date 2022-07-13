import os
import io
from google.cloud import vision

class SimilarImageSearch:

    def __init__(self, vision_client):
        self.vision_client = vision_client

    def search_similar_images_single_image(self, vision_image):
        annotations = self.vision_client.web_detection(image=vision_image).web_detection
        urls_list = []
        if annotations.full_matching_images:
            for image in annotations.full_matching_images:
                urls_list.append(image.url)
        if annotations.partial_matching_images:
            for image in annotations.partial_matching_images:
                urls_list.append(image.url)
        if annotations.visually_similar_images:
            for image in annotations.visually_similar_images:
                urls_list.append(image.url)
        return urls_list

    def search_similar_images_directory(self, dir_path):
        urls_list = []
        for file in os.listdir(dir_path):
            with io.open(os.path.join(dir_path, file), 'rb') as image_file:
                content = image_file.read()
                print(type(content))
                vision_image = vision.Image(content=content)
                print(type(vision_image))
                try:
                    annotations = self.vision_client.web_detection(image=vision_image).web_detection
                    print(annotations)
                    if annotations.full_matching_images:
                        for image in annotations.full_matching_images:
                            urls_list.append(image.url)
                    if annotations.partial_matching_images:
                        for image in annotations.partial_matching_images:
                            urls_list.append(image.url)
                    if annotations.visually_similar_images:
                        for image in annotations.visually_similar_images:
                            urls_list.append(image.url)
                except:
                    print("No similar images for file", str(file), "found.")
        return urls_list
