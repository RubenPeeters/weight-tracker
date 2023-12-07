from typing import ByteString, Sequence
import cv2 as cv
from pathlib import Path
import re

# import the necessary packages
from google.cloud import vision

pattern = "\d+\.\d+|\d+\,\d+|\.\d+|\,\d+"


def get_matches(response: vision.AnnotateImageResponse):
    print("=" * 80)
    all_matches = []
    for annotation in response.text_annotations:
        matches = re.findall(pattern, annotation.description)
        if len(matches) > 0:
            print(f'Matches found: {" - ".join(matches)}')
        all_matches.extend(matches)
    return set(all_matches)


def analyze_image_from_opencv_img(
    img: ByteString, feature_types: Sequence, client: vision.ImageAnnotatorClient
) -> vision.AnnotateImageResponse:
    image = vision.Image(content=img)
    features = [vision.Feature(type_=feature_type) for feature_type in feature_types]
    request = vision.AnnotateImageRequest(image=image, features=features)

    response = client.annotate_image(request=request)

    return response


def print_labels(response: vision.AnnotateImageResponse):
    print("=" * 80)
    for label in response.label_annotations:
        print(
            f"{label.score:4.0%}",
            f"{label.description:5}",
            sep=" | ",
        )


def opencv_to_bytes(img):
    return cv.imencode(".jpg", img)[1].tobytes()


if __name__ == "__main__":
    cwd = Path.cwd()
    example1 = cwd / "images" / "example1.jpg"
    example2 = cwd / "images" / "example2.jpg"
    img = cv.imread(str(example1))

    # Find the text in the cropped image
    client = vision.ImageAnnotatorClient.from_service_account_file(
        "keys/credentials.json"
    )
    features = [vision.Feature.Type.TEXT_DETECTION]

    response = analyze_image_from_opencv_img(opencv_to_bytes(img), features, client)
    matches = get_matches(response)
    print(f"{matches=}")
