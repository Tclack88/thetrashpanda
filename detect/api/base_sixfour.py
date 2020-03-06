"""
TPDS API :: Example Base64 Image String
"""

import base64
import io
import os

import cv2
import numpy as np
from imageio import imread, imwrite


def from_base64(img_string: str):
    """Converts a base64 image string to numpy uint8 image array."""
    # If base64 has metadata attached, get only data after comma
    if img_string.startswith("data"):
        img_string = img_string.split(",")[-1]

    # imageio array is a numpy array
    img = imread(io.BytesIO(base64.b64decode(img_string)))

    return img


def to_base64(img_filepath: str) -> str:
    """Returns base64 representation of an image."""
    with open(img_filepath, "rb") as img:
        img_data = img.read()

    b64_bytes = base64.b64encode(img_data)
    b64_string = b64_bytes.decode()

    return b64_string


def dir_base64(dirpath: str):
    """Convert images in dirpath to base64 strings."""
    for file in os.listdir(dirpath):
        filepath = os.path.join(dirpath, file)

        # Encode image into string
        img_string = to_base64(filepath)

        # Create the filename
        base = os.path.basename(filepath)
        common = os.path.splitext(base)[0]
        # Write file
        write_filepath = os.path.join(dirpath, f"{common}.txt")
        with open(write_filepath, "w") as wf:
            wf.write(img_string)


# === Convert all images in directory to base64 === #
# img_dirpath = "detect/api/tests/images/"
# dir_base64(img_dirpath)


# === Other methods used to encode / decode strings === #

# image_string_file = "base_sixfour.txt"
# image_basename = "lightbulb-02"
# test_img_filepath = f"../test_images/plastic_film/{image_basename}.jpg"

# # Encode image as base64 string
# encoded_string = to_base64(test_img_filepath)

# # Save encoded base64 image to file
# with open(f"../test_images/{image_basename}.txt", "w") as wf:
#     wf.write(encoded_string)

# Decode base64 array to image
# with open(image_string_file, "r") as f:
#     img_string = f.read()

# decoded_image = from_base64(img_string)
# decoded_image = string_to_image(img_string)

# # Save image
# imwrite("from_string.png", decoded_image)

# # Display image
# cv2.imshow("image", decoded_image)
# cv2.waitKey(0) & 0xFF
# cv2.destroyAllWindows()
