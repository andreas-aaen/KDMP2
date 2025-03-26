import cv2
import numpy as np
import matplotlib.pyplot as plt
from tkinter import Tk, filedialog

# Open file dialog to select image
Tk().withdraw()  # Hide root window
image_path = filedialog.askopenfilename(title="Select an image", filetypes=[("Image Files", "*.png;*.jpg;*.jpeg")])

# Load image
image = cv2.imread(image_path)
image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
image_hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

# Define yellow color range for the crowns
lower_yellow = np.array([20, 100, 100])
upper_yellow = np.array([35, 255, 255])

# Create a mask for yellow regions
mask = cv2.inRange(image_hsv, lower_yellow, upper_yellow)

# Apply morphological operations to reduce noise
kernel = np.ones((3, 3), np.uint8)
mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)

# Find contours in the mask
contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# Draw bounding boxes around detected crowns
output_image = image_rgb.copy()
for contour in contours:
    x, y, w, h = cv2.boundingRect(contour)
    cv2.rectangle(output_image, (x, y), (x + w, y + h), (255, 0, 0), 2)  # Blue rectangles

# Display the result
plt.figure(figsize=(10, 6))
plt.imshow(output_image)
plt.axis("off")
plt.title("Detected Crowns")
plt.show()
