import cv2
import numpy as np
import matplotlib.pyplot as plt
from tkinter import Tk
from tkinter.filedialog import askopenfilename

# Function to open a file dialog and select an image
def select_image(title):
    Tk().withdraw()  # Hide the root window
    filename = askopenfilename(title=title, filetypes=[("Image Files", "*.png;*.jpg;*.jpeg;*.bmp")])
    if filename:
        return cv2.imread(filename)  # Load image in color (default)
    else:
        print("No file selected")
        exit()

# Function to compute Mean Squared Error between the template and the window
def mse(window, template):
    return np.sum((window - template) ** 2) / float(window.size)

# Select the template and image using file dialog
template = select_image("Select the template image")
image = select_image("Select the image to search in")

# Check if both images are loaded properly
if template is None or image is None:
    print("Error loading images")
    exit()

# Get template dimensions
template_height, template_width = template.shape[:2]

# Prepare an empty list to store the match scores and locations
match_scores = []

# Slide the window across the image (row by row, column by column)
for y in range(image.shape[0] - template_height + 1):
    for x in range(image.shape[1] - template_width + 1):
        # Extract the current window from the image
        window = image[y:y + template_height, x:x + template_width]
        
        # Compute the MSE score between the window and the template
        score = mse(window, template)
        
        # Store the score and location
        match_scores.append((score, (x, y)))

# Sort the match scores by the best match (lowest MSE means better match)
match_scores.sort(key=lambda x: x[0])

# Get the best match location (lowest MSE)
best_score, best_location = match_scores[0]
print(f"Best match at {best_location} with score {best_score}")

# Draw a rectangle around the best match location
image_with_match = image.copy()
cv2.rectangle(image_with_match, best_location, 
              (best_location[0] + template_width, best_location[1] + template_height), 
              (0, 255, 0), 2)

# Visualize the result with the best match highlighted
plt.imshow(cv2.cvtColor(image_with_match, cv2.COLOR_BGR2RGB))  # Convert to RGB for display
plt.title(f'Best Match Location at {best_location}')
plt.axis('off')  # Hide axes
plt.show()
