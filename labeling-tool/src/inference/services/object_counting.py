from statistics import mode
import os
import io
from google.cloud import vision


class ObjectCounter:

    def __init__(self, vision_client):
        self.vision_client = vision_client

    def count_single_image(self, vision_image):
        objects = self.vision_client.object_localization(image=vision_image).localized_object_annotations
        count = len(objects)
        return count

    def count_multiple_images(self, vision_images):
        objects = []
        for vision_image in vision_images:
            objects = self.vision_client.object_localization(image=vision_image).localized_object_annotations
            objects.append(len(objects))
        count = mode(objects)
        return count

    def count_directory(self, dir_path):
        object_counts = []
        for file in os.listdir(dir_path):
#             print("Counting objects in file", str(file), "...")
            with io.open(os.path.join(dir_path, file), 'rb') as image_file:
                content = image_file.read()
                vision_image = vision.Image(content=content)
                count = self.count_single_image(vision_image)
                object_counts.append(count)
#                 print(str(count), "object(s) found in file", str(file) + ".")
        count = mode(object_counts)
#         print(str(count), "object(s) found in total.")
        return count