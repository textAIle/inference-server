class TextDetector:

    def __init__(self, vision_client):
        self.vision_client = vision_client

    def detect_text_single_image(self, vision_image):
        texts = self.vision_client.text_detection(image=vision_image)
        texts_list = [texts.full_text_annotation.text]
        for text in texts.text_annotations:
            texts_list.append(text.description)
        return texts_list
