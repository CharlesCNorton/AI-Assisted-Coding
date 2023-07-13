# Interactive Tesseract Viewer

This Python program uses Matplotlib to visualize a rotating 4D tesseract (also known as a hypercube), alongside a stationary tesseract. The rotating tesseract is colored blue, while the stationary one is colored red.

The visualization is accomplished by rotating the tesseract in 4D, then projecting it down to 3D for display. The rotation is done using a 4D rotation matrix, and the projection is done by dividing by the fourth dimension (similar to a perspective projection in 3D graphics).

To use this program, you need Python 3 and Matplotlib. Once you have those installed, you can run the program with `python tesseract.py`.

## Update Notes

This version of the program has improved performance by updating the positions of existing lines instead of redrawing the entire plot in every frame. It also includes a second subplot displaying a stationary tesseract for comparison with the rotating one.

## Future Work

Possible improvements for future versions of this program could include:

- Adding interactive controls to adjust the rotation speed
- Improving the aesthetics of the plot (e.g., by adding labels or changing the color scheme)
- Implementing additional 4D shapes
