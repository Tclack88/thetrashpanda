"""
TDPS Detect API :: Object Detection Endpoint
"""

import base64
import binascii
import json
import io
import os
import random

import cv2
from flask import Blueprint, request
from flask_restplus import Resource, Api, fields
from imageio import imread
import numpy as np
import pandas as pd

from detect.api.yolo import get_prediction, load_model

detect_blueprint = Blueprint("detect", __name__)
api = Api(detect_blueprint)


# === Load Materials into pd.DataFrame === #
csv_path = "detect/api/materials.csv"
df_mat = pd.read_csv(csv_path)


# === YOLO configuration === #
yolo_path = "detect/api/yolo_config"
weights_path = os.path.join(yolo_path, "yolo-obj_14000.weights")
config_path = os.path.join(yolo_path, "yolo-obj.cfg")

# === Instantiate network === #
net = load_model(config_path, weights_path)

# === Format for marshaled response objects === #
# These dictionaries act as templates for response objects
# and can validate the response if needed.

# Format/validate the data model as json
material = {
    "material_id": fields.Integer(),
    "material": fields.String(),
    "cluster": fields.String(),
}
# Format / validate custom json response
resource_fields = {
    "message": fields.String(),
    "pred_time": fields.Float(),
    "confidence": fields.Float(),
    "cluster_name": fields.String(),
    "cluster": fields.String(),
    "materials": fields.List(fields.Integer()),
}
# Format / validate cluster list json response
cluster_fields = {
    "message": fields.String(),
    "cluster_name": fields.String(),
    "cluster": fields.String(),
    "materials": fields.List(fields.Integer()),
}


def from_base64(img_string: str):
    """Converts a base64 image string to numpy uint8 image array."""
    # If base64 has metadata attached, get only data after comma
    if img_string.startswith("data"):
        img_string = img_string.split(",")[-1]
    # Convert string to array and load into opencv
    img_array = imread(io.BytesIO(base64.b64decode(img_string)))
    return cv2.cvtColor(img_array, cv2.COLOR_RGB2BGR)


def snake_to_cd_case(name: str):
    """Converts a snake_case cluster name to Title Case.
    In the case of 'cd_cases', abbreviation is capitalized."""
    split = name.title().split("_")
    if len(split[0]) == 2:
        split[0] = split[0].upper()
    return " ".join(split)


class Ping(Resource):
    """Endpoint to test that the app is working."""

    def get(self):
        return {
            "status": "success",
            "message": "pong!",
        }


class Detect(Resource):
    @api.marshal_with(resource_fields)
    def post(self):
        # Get and parse the json post request
        post_data = request.get_json()
        img_b64 = post_data.get("imgb64")
        response_object = {}

        # Convert to imageio (numpy) array
        # Catch some errors, mostly with input string
        try:
            img = from_base64(img_b64)
        except AttributeError:
            response_object["message"] = "Input payload validation failed"
            return response_object, 400
        except binascii.Error as e:
            response_object["message"] = str(e)
            return response_object, 400
        else:
            response_object["message"] = "success"

        # === Run object detection === #
        prediction, confidence, pred_time = get_prediction(img, net)
        response_object["cluster"] = prediction
        response_object["confidence"] = confidence
        response_object["pred_time"] = pred_time

        # Format into Title Case for display purposes
        if prediction:
            response_object["cluster_name"] = snake_to_cd_case(prediction)

            # Get list of materials for the predicted cluster
            materials = df_mat[df_mat["cluster"] == prediction]

            response_object["materials"] = materials["material_id"].tolist()
            response_object["message"] = "success"
            return response_object, 200

        else:  # No prediction was made
            response_object["message"] = "No object detected."
            response_object["confidence"] = 0.0

            return response_object, 404


class Clusters(Resource):
    @api.marshal_with(cluster_fields)
    def get(self, cluster):
        # Instantiate response object
        response_object = {}
        response_object["cluster"] = cluster  # Grab cluster from URL

        # Format into Title Case for display purposes
        response_object["cluster_name"] = snake_to_cd_case(cluster)

        # Get list of records matching the cluster name
        materials = df_mat[df_mat["cluster"] == cluster]

        response_object["materials"] = materials["material_id"].tolist()
        response_object["message"] = "success"
        return response_object, 200


class ClustersList(Resource):
    @api.marshal_with(material, as_list=True)
    def get(self):
        response_object = []
        for index, row in df_mat.iterrows():
            resp_dict = {
                "material_id": row["material_id"],
                "material": row["material"],
                "cluster": row["cluster"],
            }
            response_object.append(resp_dict)
        return response_object, 200


api.add_resource(Ping, "/ping")
api.add_resource(Detect, "/detect")
api.add_resource(Clusters, "/clusters/<cluster>")
api.add_resource(ClustersList, "/clusters")
