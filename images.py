import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np
import cv2
import helper
import os
import pipeline as ppl
import datetime

folder = "test_images/"
raw_images = os.listdir(folder)

image_dir = "test_images_output/" + datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S') + "/"
os.makedirs(image_dir)

for image_name in raw_images:
    path = image_dir + os.path.splitext(image_name)[0]

    image = mpimg.imread(folder + image_name)
    image_lr_lines = ppl.pipeline(image, path)

    plt.imshow(image_lr_lines)
    #plt.show()
