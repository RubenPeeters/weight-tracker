# import the necessary packages
import os
import random
import re
from typing import ByteString, Sequence
from google.cloud import vision

import cv2 as cv
import pandas as pd

from models.measurement import Measurement

pattern = "\d+\.\d+|\d+\,\d+|\.\d+|\,\d+"


def append_model_to_csv(m, path):
    d = m.model_dump()
    df = pd.DataFrame(data=d, index=[0])
    df.to_csv(path, mode="a", header=not os.path.exists(path))


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


def opencv_to_bytes(img):
    return cv.imencode(".jpg", img)[1].tobytes()


def analyze_cloud_vision(img):
    client = vision.ImageAnnotatorClient.from_service_account_file(
        "keys/credentials.json"
    )
    features = [vision.Feature.Type.TEXT_DETECTION]

    response = analyze_image_from_opencv_img(opencv_to_bytes(img), features, client)
    matches = get_matches(response)
    # matches = {float("{:.1f}".format(random.uniform(50, 150)))}
    print(f"{matches=}")
    if len(matches) != 1:
        raise ValueError(f"Found more than one value. {matches}")
    return matches


def analyze_mock(img):
    return {float("{:.1f}".format(random.uniform(50, 150)))}


def analyze_and_write_to_csv(f, img, path):
    matches = f(img)
    if len(matches) != 1:
        raise ValueError(f"Found more than one value. {matches}")
    match = float(matches.pop())
    m = Measurement(value=match, clothes=bool(random.getrandbits(1)))
    append_model_to_csv(m, path=path)
