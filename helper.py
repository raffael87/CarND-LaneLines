import math
import numpy as np
import cv2

def grayscale(img):
    """Applies the Grayscale transform
    This will return an image with only one color channel
    but NOTE: to see the returned image as grayscale
    (assuming your grayscaled image is called 'gray')
    you should call plt.imshow(gray, cmap='gray')"""
    return cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    # Or use BGR2GRAY if you read an image with cv2.imread()
    # return cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
def canny(img, low_threshold, high_threshold):
    """Applies the Canny transform"""
    return cv2.Canny(img, low_threshold, high_threshold)

def gaussian_blur(img, kernel_size):
    """Applies a Gaussian Noise kernel"""
    return cv2.GaussianBlur(img, (kernel_size, kernel_size), 0)

def region_of_interest(img, vertices):
    """
    Applies an image mask.
    
    Only keeps the region of the image defined by the polygon
    formed from `vertices`. The rest of the image is set to black.
    `vertices` should be a numpy array of integer points.
    """
    #defining a blank mask to start with
    mask = np.zeros_like(img)   
    
    #defining a 3 channel or 1 channel color to fill the mask with depending on the input image
    if len(img.shape) > 2:
        channel_count = img.shape[2]  # i.e. 3 or 4 depending on your image
        ignore_mask_color = (255,) * channel_count
    else:
        ignore_mask_color = 255
        
    #filling pixels inside the polygon defined by "vertices" with the fill color    
    cv2.fillPoly(mask, vertices, ignore_mask_color)
    
    #returning the image only where mask pixels are nonzero
    masked_image = cv2.bitwise_and(img, mask)
    return masked_image

def draw_raw_lines(img, lines, color=[255, 0, 0], thickness=2):
    img = np.zeros((img.shape[0], img.shape[1], 3), dtype=np.uint8)
    for line in lines:
        for x1,y1,x2,y2 in line:
            cv2.line(img, (x1, y1), (x2, y2), [0,255,0], thickness)

    return img

def draw_lines(img, lines, horizon=0, color=[255, 0, 0], thickness=6):
    """
    Think about things like separating line segments by their 
    slope ((y2-y1)/(x2-x1)) to decide which segments are part of the left
    line vs. the right line.  Then, you can average the position of each of 
    the lines and extrapolate to the top and bottom of the lane.
   """ 
    # right lane: positive slope
    # left lane: negative slope
    # (0,0) is top left!
   
    img = np.zeros((img.shape[0], img.shape[1], 3), dtype=np.uint8)

    x_left = [] 
    x_right = []
    y_left = []
    y_right = []

    for line in lines:
        for x1,y1,x2,y2 in line:
            slope = ((y2 - y1) / (x2 -x1))
            if math.fabs(slope) >= 0.6:
                if slope <= 0 :
                    x_left.extend([x1, x2])
                    y_left.extend([y1, y2])
                else :
                    x_right.extend([x1, x2])
                    y_right.extend([y1, y2])
    

    if (len(x_left) > 0 and len(x_right) > 0):
        # apply least squares polynomial fit to the arrays
        coeff_left = np.polyfit(y_left, x_left, 1)
        coeff_right = np.polyfit(y_right, x_right, 1)
        
        polyline_left = np.poly1d(coeff_left)
        polyline_right = np.poly1d(coeff_right)
       
        # cut the line on the limits, get x from the lines
        line_top_y = horizon
        line_bottom_y = img.shape[0] 

        line_left_x_bottom = polyline_left(line_bottom_y)      
        line_left_x_top = polyline_left(line_top_y)      
        
        line_right_x_bottom = polyline_right(line_bottom_y)      
        line_right_x_top = polyline_right(line_top_y)      

        cv2.line(img, (int(line_left_x_bottom), line_bottom_y), (int(line_left_x_top), line_top_y), color, thickness)
        cv2.line(img, (int(line_right_x_bottom), line_bottom_y), (int(line_right_x_top), line_top_y), color, thickness)

    return img

def hough_lines(img, rho, theta, threshold, min_line_len, max_line_gap):
    # `img` should be the output of a Canny transform.
    lines = cv2.HoughLinesP(img, rho, theta, threshold, np.array([]), minLineLength=min_line_len, maxLineGap=max_line_gap)
    return lines 

# Python 3 has support for cool math symbols.

def weighted_img(img, initial_img, α=0.8, β=1., γ=0.):
    return cv2.addWeighted(initial_img, α, img, β, γ)

def debug_image(debug, filenamepath, extension, image):
    if debug:
        cv2.imwrite(filenamepath + "_" + extension + ".jpg", cv2.cvtColor(image, cv2.COLOR_RGB2BGR))
