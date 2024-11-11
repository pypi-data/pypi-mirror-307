import cv2
from typing import List, Dict
import numpy as np
import random

def random_flip(image: np.ndarray, set_flip:int = None) -> np.ndarray:
    flip = random.choice([0, 1])

    if set_flip:
        flip = set_flip
    
    if flip == 0:
        flipped_image = image[:, ::-1, :]

    else:
        flipped_image = image[::-1, :, :]

    return flipped_image


def random_rotate(image: np.ndarray, max_angle: int = 30) -> np.ndarray:

    (height, width) = image.shape[:2]

    #random angle between between +- max_angle
    angle = random.uniform(-max_angle, max_angle)
    rotation_matrix = cv2.getRotationMatrix2D((width // 2, height // 2), angle, 1.0)
    rotated_image = cv2.warpAffine(image, rotation_matrix, (width, height))

    return rotated_image

def random_zoom(image: np.ndarray) -> np.ndarray:
    height, weight = image.shape[:2]

    #random center points and zoom factor between 1.1 and 1.33
    scale_factor = random.uniform(1.1, 1.33)
    center_x = random.randint(0, weight - 1)
    center_y = random.randint(0, height - 1)
    
    #Resize the image
    new_w = int(weight * scale_factor)
    new_h = int(height * scale_factor)
    zoomed_image = cv2.resize(image, (new_w, new_h), interpolation=cv2.INTER_LINEAR)

    #Calculate the crop
    crop_x1 = max(center_x - weight // 2, 0)
    crop_x2 = min(crop_x1 + weight, new_w)
    crop_y1 = max(center_y - height // 2, 0)
    crop_y2 = min(crop_y1 + height, new_h)
    if crop_x2 - crop_x1 < weight:
        crop_x1 = max(crop_x2 - weight, 0)
    if crop_y2 - crop_y1 < height:
        crop_y1 = max(crop_y2 - height, 0)

    cropped_zoomed_image = zoomed_image[crop_y1:crop_y2, crop_x1:crop_x2]

    return cropped_zoomed_image

def random_blur(image: np.ndarray, sigma_interval:List[float] = [0.2, 1.0]) -> np.ndarray:
    sigma = random.uniform(sigma_interval[0], sigma_interval[1])

    #kernel size, odd number
    kernel_size = int(2 * np.ceil(2 * sigma) + 1)

    blurred_image = cv2.GaussianBlur(image, (kernel_size, kernel_size), sigma)

    return blurred_image


def data_augmentation(images_list: List[np.ndarray], augmentations_functions: List[int]) -> np.ndarray:

    # augmentations_functions = list(map(mapping.get, augmentations))

    augmented_images = [globals()[fun](image) if fun != 'identity' else image  for fun, image in zip(augmentations_functions, images_list)]
    
    return augmented_images