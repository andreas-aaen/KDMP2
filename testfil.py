import cv2 as cv
import numpy as np

def templateMatching(Image):

    Image = cv.imread('1.jpg')
    img_gray = cv.cvtColor(Image, cv.COLOR_BGR2GRAY)

    # List of template filenames
    templates = ['crN.png', 'crE.png', 'crS.png', 'crW.png']

    # Define the threshold for a valid match
    threshold = 0.6

    # Store all bounding boxes
    all_bboxes = []

    # Loop through each template
    for template_filename in templates:
        template = cv.imread(template_filename, cv.IMREAD_GRAYSCALE)
        assert template is not None, f"file {template_filename} could not be read"

        w, h = template.shape[::-1]
        res = cv.matchTemplate(img_gray, template, cv.TM_CCOEFF_NORMED)
        loc = np.where(res >= threshold)

        for pt in zip(*loc[::-1]):
            all_bboxes.append((pt[0], pt[1], pt[0] + w, pt[1] + h))

    # Non-Maximum Suppression to avoid counting duplicates
    def non_max_suppression(bboxes, overlap_thresh=0.3):
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

    # Filter bounding boxes
    filtered_bboxes = non_max_suppression(all_bboxes, overlap_thresh=0.2)

    # Output the total number of matches
    print(f"Total matches found: {len(filtered_bboxes)}")


templateMatching('1.jpg')

