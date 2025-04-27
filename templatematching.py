import cv2 as cv
import numpy as np
from matplotlib import pyplot as plt
from collections import Counter
from pathlib import Path

def templateMatching(board_path):  # Take the board path as input
    # Load the selected board image
    img_rgb = cv.imread(str(board_path))  # Read the passed board
    assert img_rgb is not None, f"File {board_path} could not be read, check if the path is correct"
    img_gray = cv.cvtColor(img_rgb, cv.COLOR_BGR2GRAY)

    def GetTemplates():
        templates = []
        Boards = Path.cwd() / "Templates"
        for board in Boards.iterdir():
            if board.is_file():
                templates.append(str(board))  # Add the file path as a string
        return templates

    templates = GetTemplates()

    threshold = 0.6 # Confidence threshold for matching the templates
    all_bboxes = [] # Will contain coordinates for all bounding boxes for detected crowns

    for template_filename in templates:
        template = cv.imread(template_filename, cv.IMREAD_GRAYSCALE)
        assert template is not None, f"Template file {template_filename} could not be read"
        w, h = template.shape[::-1]
        res = cv.matchTemplate(img_gray, template, cv.TM_CCOEFF_NORMED) # Template Matching
        loc = np.where(res >= threshold)

        for pt in zip(*loc[::-1]):
            all_bboxes.append((pt[0], pt[1], pt[0] + w, pt[1] + h)) # Append bounding box if it is a match

    def non_max_suppression(bboxes, overlap_thresh=0.3): # Ensure bounding boxes don't overlap so a crown is counted twice
        if len(bboxes) == 0:
            return []
        bboxes = np.array(bboxes)
        x1, y1, x2, y2 = bboxes[:, 0], bboxes[:, 1], bboxes[:, 2], bboxes[:, 3]
        areas = (x2 - x1 + 1) * (y2 - y1 + 1)
        order = np.argsort(y2)
        selected_bboxes = []

        while len(order) > 0:
            i = order[-1]
            selected_bboxes.append(bboxes[i])
            xx1 = np.maximum(x1[i], x1[order[:-1]])
            yy1 = np.maximum(y1[i], y1[order[:-1]])
            xx2 = np.minimum(x2[i], x2[order[:-1]])
            yy2 = np.minimum(y2[i], y2[order[:-1]])
            w = np.maximum(0, xx2 - xx1 + 1)
            h = np.maximum(0, yy2 - yy1 + 1)
            inter_area = w * h
            iou = inter_area / (areas[i] + areas[order[:-1]] - inter_area)
            order = order[np.where(iou <= overlap_thresh)[0]]

        return selected_bboxes

    filtered_bboxes = non_max_suppression(all_bboxes, overlap_thresh=0.2) # Filter bounding boxes after ensuring there is no overlapping

    compressed_centers = [] # If a coordinate at the centre of a bounding box is (300, 200), make it (3, 2), which corresponds to a tile on the 5x5 board grid.
    for (x1, y1, x2, y2) in filtered_bboxes:
        center_x = int((x1 + x2) / 2)
        center_y = int((y1 + y2) / 2)
        first_digit_x = int(str(center_x)[0])
        first_digit_y = int(str(center_y)[0])
        compressed_centers.append((first_digit_x, first_digit_y))

    # Count occurrences
    counts = Counter(compressed_centers)
    
    # Return as a dictionary
    return dict(counts)
