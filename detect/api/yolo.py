"""
TPDS Detect API :: YOLOv3 Model
"""

import argparse
import os
import time

import numpy as np
import cv2

# === YOLO config variables === #
# Paths to necessary files
yolo_path = "detect/api/yolo_config"
classes_path = os.path.join(yolo_path, "classes.txt")
# Config vars
conf_thresh = 0.2  # Confidence threshold
nms_thresh = 0.1  # Non-maximum suppression

# === YOLO utility functions === #


def load_model(config_file: str, weights_file: str):
    """
    Loads and instantiates the object detection model using 
    opencv2's dnn (deep neural network) module.
    
    :param config_file (str)  : Path to `.cfg` file used to train the model.
    :param weights_file (str) : Path to `.weights` file to use for inference.
    :return net (cv2.dnn)     : Instantiated and configured model.
    """
    net = cv2.dnn.readNetFromDarknet(config_file, weights_file)
    net.setPreferableBackend(cv2.dnn.DNN_BACKEND_OPENCV)
    net.setPreferableTarget(cv2.dnn.DNN_TARGET_CPU)
    return net


def get_prediction(image, net, img_dim: tuple = (416, 416)):
    """
    Run object detection on image and return detections.
    
    :param image (np.uint8)  : Image array on which to run inference.
    :param net (cv2.dnn)     : Instantiated YOLO model
    :param labels (list)     : List of class labels.
    :return prediction (str) : Predicted object.
    """
    # Get class labels
    with open(classes_path, "r") as clf:
        classes = clf.read().splitlines()

    (H, W) = image.shape[:2]

    # Determine only the output layer names we need from YOLO
    ln = net.getLayerNames()
    ln = [ln[i[0] - 1] for i in net.getUnconnectedOutLayers()]

    # Construct a blob from the input image, then run a forward pass
    # of the detector, giving the bboxes and probabilities.
    blob = cv2.dnn.blobFromImage(image, 1 / 255.0, img_dim, swapRB=True, crop=False)
    net.setInput(blob)
    start = time.time()
    layer_outputs = net.forward(ln)
    # print(layer_outputs)
    end = time.time()
    # pred_time = f"{end - start:.6f} seconds."  # Set up timing message
    pred_time = end - start  # Set up timing message as number
    print(pred_time)  # Print timing message to console

    # Initialize lists for bboxes, confidences, and class_ids
    boxes, confidences, class_ids, class_names = [], [], [], []

    # Loop over each layer of the layer outputs
    for output in layer_outputs:
        # Loop over each of the detections
        for detection in output:
            # Extract the class_id and confidence (proba) of current object
            scores = detection[5:]
            class_id = np.argmax(scores)
            confidence = scores[class_id]

            # Filter out weak predictions
            if confidence > conf_thresh:
                # Scale bbox coord back to size of image
                box = detection[0:4] * np.array([W, H, W, H])
                (center_x, center_y, width, height) = box.astype("int")

                # Use the center coords to calc top and left corner of box
                x = int(center_x - (width / 2))
                y = int(center_y - (height / 2))

                # Update lists
                boxes.append([x, y, int(width), int(height)])
                confidences.append(float(confidence))
                class_ids.append(class_id)
                class_names.append(classes[class_id])

    # Apply non-max suppression (NMS)
    idxs = cv2.dnn.NMSBoxes(boxes, confidences, conf_thresh, nms_thresh)

    # List to hold class_ids that make it past NMS
    nms_class_ids = []
    pred_conf = dict()

    # ensure at least one detection exists
    if len(idxs) > 0:
        # loop over the indexes we are keeping
        for i in idxs.flatten():
            text = f"{classes[class_ids[i]]}: {confidences[i]:.4f}"
            pred_conf[classes[class_ids[i]]] = confidences[i]
            # print(text)
            # print(boxes)
            nms_class_ids.append(classes[class_ids[i]])

        top_object = max(pred_conf, key=pred_conf.get)
        top_conf = pred_conf[top_object]

        print("Top object:", top_object)
        print(pred_conf[top_object])

        return (
            top_object,
            top_conf,
            pred_time,
        )
    else:
        return None, None, pred_time

