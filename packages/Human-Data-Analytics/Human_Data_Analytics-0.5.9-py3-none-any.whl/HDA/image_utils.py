import cv2, os
import numpy as np
from typing import List
import tensorflow as tf
import pandas as pd

def crop_image(path,
                top:int = 0.05,
                bottom:int = 0.05,
                left:int = 0.05,
                right:int = 0.05) -> None:
    """
    Crop the image at the given path by the given percentage
    and display the image if display is set to True
    Args:
        path:
            (str): full path to the image
            (numpy.ndarray): image as a numpy array
        top(int): percentage to crop from the top
        bottom(int): percentage to crop from the bottom
        left(int): percentage to crop from the left
        right(int): percentage to crop from the right
    """
    if isinstance(path, str):
        image = cv2.imread(path)
    else:
        image = path
    # print(image.shape)

    # get the dimensions of the image
    height, width = image.shape[:2]

    # crop the image
    start_row, start_col = int(height * top), int(width * left)
    end_row, end_col = int(height * (1 - bottom)), int(width * (1 - right))
    cropped_image = image[start_row:end_row, start_col:end_col]

    return cropped_image

def resize_image(path, 
                 width:int = 500, 
                 height:int = 500) -> None:
    """
    Resize the image at the given path to the given width and height
    and display the image if display is set to True
    Args:
        path:
            (str): full path to the image
            (numpy.ndarray): image as a numpy array
        width(int): width of the resized image
        height(int): height of the resized image
    """
    if isinstance(path, str):
        image = cv2.imread(path)
    else:
        image = path
    # print(image.shape)
    
    resized_image = cv2.resize(image, (width, height))

    return resized_image

def CLAHE(path) -> None:
    """
    Apply CLAHE (Contrast Limited Adaptive Histogram Equalization) to the image at the given path
    and display the image if display is set to True
    Args:
        path:
            (str): full path to the image
            (numpy.ndarray): image as a numpy array
    """
    if isinstance(path, str):
        image = cv2.imread(path)
    else:
        image = path
    
    # define the clahe object and apply it to the image
    lab = cv2.cvtColor(image, cv2.COLOR_BGR2LAB)

    clahe = cv2.createCLAHE(clipLimit=2.0,tileGridSize=(8,8))
    lab[...,0] = clahe.apply(lab[...,0])

    clahe_image = cv2.cvtColor(lab, cv2.COLOR_LAB2BGR)

    return clahe_image
    
def create_patches(image, 
                   patch_size:int = 224, 
                   num_patches_per_side:int = 3) -> List[tf.Tensor]:
    """
    Create 9 overlapped patches of size 224x224 from the image at the given path
    and display the image if display is set to True
    Args:
        path(numpy.ndarray): image as a numpy array
        patch_size(int): size of the patch
        num_patches_per_side(int): number of patches to create 
    """
    # get the dimensions of the image
    height, _ = image.shape[:2]

    stride = (patch_size*num_patches_per_side - height) // (num_patches_per_side - 1)
    # create num_patches_per_side**2 overlapped patches of size 224x224
    
    patches = []
    for i in range(num_patches_per_side):
        for j in range(num_patches_per_side):
            start_row, start_col = i * (patch_size - stride), j * (patch_size - stride)
            end_row, end_col = start_row + patch_size, start_col + patch_size
            patches.append(image[start_row:end_row, start_col:end_col])
    
    return patches

def normalize_image(image):
    """
    Normalize the image
    Args:
        image(numpy.ndarray): image as a numpy array
    """
    return image / 255.0


if __name__ == "__main__":
    
    print("This file is not meant to be run directly.")
