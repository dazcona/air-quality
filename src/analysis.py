import cv2
import os
import sys
import glob
import numpy as np
import pandas as pd
from flask import flash
import csv
import matplotlib.pyplot as plt


def analyse(directory):
    """ Analyse directory of images """

    # Normalize images
    noramlized_path = normalize_images(directory)

    # Extract values
    csv_filename = extract_values(noramlized_path)

    return csv_filename

def normalize_images(path):
    """ Normalize the images """

    print('Normalizing images for {}'.format(path))

    # Create normalized dir
    normalized_path = os.path.join(path, "normalized")
    os.mkdir(normalized_path)

    try:

        for filename in glob.glob('{}/*.jpg'.format(path)):

            print('Normalizing: {}'.format(filename))
            
            name = filename.split('/')[-1]
            # Read image
            img = cv2.imread(filename)
            # BGR to RGB
            imgRGB_original = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            
            # Finding the average colour values of the core portion 
            R1 = imgRGB_original[2400:2600, 2250:2450, 0].mean()
            G1 = imgRGB_original[2400:2600, 2250:2450, 1].mean()
            B1 = imgRGB_original[2400:2600, 2250:2450, 2].mean()
            
            # Adjusting the colours in the image
            arr = np.array(imgRGB_original)
            
            # Grab the image dimensions
            # h1 = arr.shape[0]
            # w1 = arr.shape[1]

            # # loop over the image, pixel by pixel
            # for y in range(0, h1):
            #     for x in range(0, w1):
            #         arr[y, x, 0] = arr[y, x, 0] + (52 - R1) # add or substract the difference of Red
            #         arr[y, x, 1] = arr[y, x, 1] + (52 - G1) # add or substract the difference of green
            #         arr[y, x, 2] = arr[y, x, 2] + (52 - B1) # add or substract the difference of Blue
            # Do them all at once for each channel!
            arr[:, :, 0] =+ (52 - R1)
            arr[:, :, 1] =+ (52 - G1)
            arr[:, :, 2] =+ (52 - B1)
            
            # Saving the Normalised Images
            print('Saving the image...')
            plt.imsave(os.path.join(normalized_path, name), arr)

    except Exception as e:
        
        print("An exception occurred normalizing the images!")
        print(e)
        flash("An exception occurred normalizing the images!")

    return normalized_path


def extract_values(path):
    """ Extract values and write a CSV file """

    print('Extracting the values for {}'.format(path))

    csv_filename = "{}/values.csv".format(path)

    with open(csv_filename, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["Image Name", "Dot Number", "R Value", "G Value", "B Value"])

    try:

        for filename in glob.glob('{}/*.jpg'.format(path)):

            print('Extracting values for: {}'.format(filename))

            name = filename.split('/')[-1]
            # Read image
            img = cv2.imread(filename)
            # BGR to RGB
            imgRGB_original = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

            # Initialization of the values
            dotNames = ['one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine', 'ten', 
                'eleven', 'twelve', 'thirteen', 'fourteen', 'fifteen', 'sixteen']
            corX = [1235, 1535, 1835, 2135]
            corY = [2800, 3100, 3400, 3700]
            values = []
            count = 0

            # Extracting the 5*5 square pixel mean colour values of each dot
            for dotx in corX:
                for doty in corY:
                    valueR = imgRGB_original[dotx:dotx + 5,doty:doty + 5, 0].mean()
                    valueG = imgRGB_original[dotx:dotx + 5,doty:doty + 5, 1].mean()
                    valueB = imgRGB_original[dotx:dotx + 5,doty:doty + 5, 2].mean()
                    x = [name, dotNames[count], valueR, valueG, valueB]
                    values.append(x)
                    count= count + 1

            # Saving the values into a csv file
            with open(csv_filename, "a+", newline="") as f:
                writer = csv.writer(f)
                writer.writerows(values)

    except Exception as e:
        
        print("An exception occurred extracting the values!")
        print(e)
        flash("An exception occurred extracting the values!")

    return csv_filename