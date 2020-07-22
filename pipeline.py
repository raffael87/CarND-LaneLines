import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np
import cv2
import helper

def pipeline(image, save_path=""):
    # Debug option
    debug = 0
    if save_path:
        debug = 1

    # 1. Transform image to grayscale
    image_gray = helper.grayscale(image)

    helper.debug_image(debug, save_path,"gray", image_gray)

    # 2. Smoothen image
    image_cleaned = helper.gaussian_blur(image_gray, 5)

    helper.debug_image(debug, save_path,"cleaned", image_cleaned)

    # 3. Apply Canny
    threshold_low = 50
    threshold_high = 150
    image_edges = helper.canny(image_cleaned, threshold_low, threshold_high);

    helper.debug_image(debug, save_path,"canny", image_edges)

    # 4. Set a ROI
    left_bottom = (0, image.shape[0])
    left_top = (430, 330)
    right_top = (530, 330)
    right_bottom = (image.shape[1], image.shape[0])
    roi = np.array([[left_bottom, left_top, right_top, right_bottom]], dtype=np.int32)
    image_roi = helper.region_of_interest(image_edges, roi)

    helper.debug_image(debug, save_path,"roi", image_roi)

    # 5. Calculate Hough lines
    rho = 3
    theta = np.pi/180
    threshold = 20
    min_line_length = 15
    max_line_gap = 10
    lines = helper.hough_lines(image_roi, rho, theta, threshold, min_line_length, max_line_gap)

    # 6 debug option
    image_hough = helper.draw_raw_lines(image_roi, lines)
    image_hough = helper.weighted_img(image_hough, image)
    helper.debug_image(debug, save_path, "hough", image_hough)
 
    # 7 Calculate poly lines
    horizon = 350
    image_lr_lines = helper.draw_lines(image_roi, lines, horizon)

    # 8 Add lines to original image
    image_overlay = helper.weighted_img(image_lr_lines, image)

    helper.debug_image(debug, save_path,"overlay", image_overlay)

    return image_overlay
