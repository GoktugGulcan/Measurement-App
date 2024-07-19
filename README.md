Image Measurement and Zoom Application
This application allows users to measure specific areas of an image and zoom in/out for better precision. The application provides functionality for loading an image, drawing rectangles to measure areas, and zooming/panning within the image.

Features
Image Loading: Load images using a file dialog.
Drawing Rectangles: Click and drag to draw rectangles on the image to measure specific areas.
Zooming and Panning: Zoom in/out and pan around the image to focus on specific details.
Measurement Display: Display the dimensions of the selected area in millimeters.
Requirements
Python 3.x
OpenCV
NumPy
Tkinter (for the file dialog)
Installation
Ensure Python 3.x is installed on your system.
Install the required libraries using pip:
bash
Kodu kopyala
pip install opencv-python-headless numpy
Usage
Running the Application:

bash
Kodu kopyala
python image_measurement.py
Loading an Image:

A file dialog will appear when the application starts. Select an image file (supported formats: .jpg, .jpeg, .png, .bmp).
Drawing Rectangles:

Click and drag on the image to draw a rectangle. The dimensions of the selected area will be displayed on the image in millimeters.
Zooming:

Use the mouse wheel to zoom in and out. The zoom is centered around the mouse cursor.
Panning:

Hold the Ctrl key and click and drag to pan around the image.
Code Structure
Global Variables:

drawing, x_init, y_init: Variables to manage the drawing state and initial click positions.
top_left_pt, bottom_right_pt: Coordinates of the drawn rectangle.
zoom_scale: Current zoom level.
is_dragging, drag_start_x, drag_start_y, drag_offset_x, drag_offset_y: Variables to manage panning.
img_display: The current displayed image.
min_zoom_scale, max_zoom_scale: Limits for zooming.
Functions:

update_display(): Updates the displayed image based on the current zoom level and panning offsets.
mouse_callback(event, x, y, flags, param): Handles mouse events for drawing, panning, and zooming.
main(): Main function to initialize the application, load the image, and set up the display and mouse callback.
