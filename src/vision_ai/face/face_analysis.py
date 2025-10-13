from azure.ai.vision.face.models import (
    FaceAttributeTypeDetection01,
    FaceDetectionModel,
    FaceRecognitionModel,
)
from vision_ai.face.client import client


with open("asset/images/face.png", "rb") as image_data:
    response = client.detect(
        image_content=image_data.read(),
        detection_model=FaceDetectionModel.DETECTION01,
        recognition_model=FaceRecognitionModel.RECOGNITION01,
        return_face_id=False,
        return_face_attributes=[
            FaceAttributeTypeDetection01.ACCESSORIES,
            FaceAttributeTypeDetection01.HEAD_POSE,
            FaceAttributeTypeDetection01.OCCLUSION,
        ],
    )

print(response)
