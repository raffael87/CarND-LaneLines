# **Finding Lane Lines on the Road** 

## Writeup Template

**Finding Lane Lines on the Road**

The goals / steps of this project are the following:
* Make a pipeline that finds lane lines on the road
* Possible to use a video as input
* Reflect on your work in a written report


[//]: # (Image References)

[image1]: ./my_examples/grayscale.jpg "Grayscale"
[image2]: ./my_examples/gaussian.jpg "Gaussian Blur"
[image3]: ./my_examples/canny.jpg "Canny Filter"
[image4]: ./my_examples/roi.jpg "ROI"
[image5]: ./my_examples/hough.jpg "Hough Lines"
[image6]: ./my_examples/result.jpg "Result"

---

### Reflection

### 1. Describe your pipeline. As part of the description, explain how you modified the draw_lines() function.

The pipeline has 8 steps. As input it takes a color image and returns an image with the lane markings.

Step 1:
In order to process the image, it has to be converted into grayscale first.
![alt text][image1]

Step 2:
Smoothen the image to eliminate noise using the gaussian blur function from opencv.
Kernel size was chosen in a way to not over smoothen the image. 
![alt text][image2]

Step 3:
Step three applies the canny to get edges. Here it was important to not lose to much information from the lines.
Dashed lane markings should preserve their shape.
![alt text][image3]

Step 4:
This step defines the region of interests and removes everything which is outside. This removes alos a lot of noise from the edge image.
![alt text][image4]

Step 5:
With the roi image, the hough lines are calculated. In this step no image is being modified. 
The "correct" values were found after comparing different values with the same images as input in order to see improvement.
For me it was important not to lose the dashed line. This is more dificult when they are more fare away. So to not over estimulate the system, 
not all of the dashed lines are detected. Here I was thinking already for later if we want somehow classify the lanes.

Step 6:
This step is more for debug purpose. Here the hough lines are being added to the original image. This is important to be able to compare the results.
![alt text][image5]

Step 7:
Here the lines from the hough transformation are being classified into left and right lines. 
To classify them, the slope is for each line is calculated. Negative slopes means the line is being classified for left. 
For the first apporach it is ok because we do not expect lines with a negativ slope being on the right side of the camera.
If the slope is positive, then the line is classified as right.
But not all lines are taken into account. Only lines above a certain threshold are taken into consideration. This helps that we get only
lines that are going fast to the horizon.
Once the lines are classfied, for the left lines and respective the right lines, a polyline is calculated. These lines are then being cropped.
The y values for the bottom are the end of the image (where car is) and the respective x value is taken from the polyline.
The same applies for the top line. Here the x is taken where the horizon is defined.

Step 8
The image with the lines is laid over the original image.
![alt text][image6]

### 2. Identify potential shortcomings with your current pipeline

- Pipeline is not parametrized. At the moment parameters for the functions can not be set dynamical.
- Biggest short coming are curvatures. At the moment the pipeline is not able to detect them.
- If there is a run time issue, the area of the image could be reduced to the roi.


### 3. Suggest possible improvements to your pipeline
The challenge video shows the limitations of the current implementation.
In order to also detect lanes in this environment, the approach has to be more dynamic. With the curve in front, the detection of 
the hough lines has to be improved. As for the straight line test images with curvature can help.
Maybe also a mix of two systems can be an approach. One for straight lanes and one for curves.

### 4. Files:
- pipeline.py is the pipeline function
- helper.py holds all the helper functions for drawing, calcualtion and debugging
- images.py calls pipeline for test images
- videos,py calls the pipeline for each video
