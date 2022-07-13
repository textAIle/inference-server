class LogoDetector:

    def __init__(self, vision_client):
        self.vision_client = vision_client

    def detect_logos_single_image(self, vision_image):
        logos = self.vision_client.logo_detection(image=vision_image)
        logos_dict = {}
        for logo in logos.logo_annotations:
            if (logo.description not in logos_dict.keys()) or (
                    (logo.description in logos_dict.keys()) and (logos_dict[logo.description] < logo.score)):
                logos_dict[logo.description] = logo.score
        return logos_dict
