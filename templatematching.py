import cv2 as cv
import numpy as np
from matplotlib import pyplot as plt

# Load the image
img_rgb = cv.imread('1.jpg')
assert img_rgb is not None, "file could not be read, check with os.path.exists()"
img_gray = cv.cvtColor(img_rgb, cv.COLOR_BGR2GRAY)

# List of template filenames
templates = ['crN.png', 'crE.png', 'crS.png', 'crW.png']

# Define the threshold for a valid match
threshold = 0.6

# Store all bounding boxes
all_bboxes = []

# Loop through each template
for template_filename in templates:
    template = cv.imread(template_filename, cv.IMREAD_GRAYSCALE)
    assert template is not None, f"file {template_filename} could not be read, check with os.path.exists()"

    # Get the dimensions of the template
    w, h = template.shape[::-1]

    # Perform template matching
    res = cv.matchTemplate(img_gray, template, cv.TM_CCOEFF_NORMED)

    # Get the locations of matches where the score is above the threshold
    loc = np.where(res >= threshold)

    # Collect all the bounding boxes
    for pt in zip(*loc[::-1]):  # Reverse the order for (x, y)
        all_bboxes.append((pt[0], pt[1], pt[0] + w, pt[1] + h))

# Apply Non-Maximum Suppression
def non_max_suppression(bboxes, overlap_thresh=0.3):
    if len(bboxes) == 0:
        return []

    # Convert bounding boxes to numpy array for easier manipulation
    bboxes = np.array(bboxes)
    x1, y1, x2, y2 = bboxes[:, 0], bboxes[:, 1], bboxes[:, 2], bboxes[:, 3]

    # Compute area of the bounding boxes
    areas = (x2 - x1 + 1) * (y2 - y1 + 1)

    # Sort bounding boxes by the bottom-right y-coordinate
    order = np.argsort(y2)

    # List to hold the final selected bounding boxes
    selected_bboxes = []

    while len(order) > 0:
        i = order[-1]
        selected_bboxes.append(bboxes[i])

        # Compute intersection over union (IoU) with the remaining boxes
        xx1 = np.maximum(x1[i], x1[order[:-1]])
        yy1 = np.maximum(y1[i], y1[order[:-1]])
        xx2 = np.minimum(x2[i], x2[order[:-1]])
        yy2 = np.minimum(y2[i], y2[order[:-1]])

        # Compute width and height of the intersection
        w = np.maximum(0, xx2 - xx1 + 1)
        h = np.maximum(0, yy2 - yy1 + 1)

        # Compute IoU
        inter_area = w * h
        iou = inter_area / (areas[i] + areas[order[:-1]] - inter_area)

        # Keep boxes that do not overlap too much
        order = order[np.where(iou <= overlap_thresh)[0]]

    return selected_bboxes

# Apply non-max suppression to the collected bounding boxes
filtered_bboxes = non_max_suppression(all_bboxes, overlap_thresh=0.2)

# Print number of identifications
print(f"Number of identifications found: {len(filtered_bboxes)}")

# List to store the center coordinates of each bounding box
centers = []

# Draw the final bounding boxes on the image and compute the center coordinates
for (x1, y1, x2, y2) in filtered_bboxes:
    # Draw the rectangle on the image
    cv.rectangle(img_rgb, (x1, y1), (x2, y2), (0, 0, 255), 2)

    # Compute the center of the bounding box
    center_x = (x1 + x2) / 2
    center_y = (y1 + y2) / 2

    # Add the center to the list
    centers.append((center_x, center_y))

# Display the result
plt.imshow(cv.cvtColor(img_rgb, cv.COLOR_BGR2RGB))  # Convert to RGB for matplotlib
plt.title(f'Matches Found (Threshold = {threshold}) with NMS')
plt.axis('off')  # Hide axes for clarity
plt.show()

# Output the list of centers
centers = [(int(center_x), int(center_y)) for center_x, center_y in centers]
print("Center coordinates of bounding boxes:", centers)
