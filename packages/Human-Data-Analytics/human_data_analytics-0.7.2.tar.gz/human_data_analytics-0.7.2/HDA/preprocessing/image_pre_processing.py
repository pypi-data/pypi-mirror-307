import os
from typing import List, Dict
import numpy as np
from pandas import Series
import matplotlib.pyplot as plt
import cv2
import tensorflow as tf
import gc
import random

os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'

from ..image_utils import crop_image, resize_image, normalize_image, CLAHE, create_patches
from .data_augmentation import data_augmentation, random_zoom, random_rotate, random_blur

def pre_process(image_n : str, path : str, num_patches_per_side:int = 3, 
                                        crop_list: Dict[str,int] = {'top': 0.2, 'bottom':0.05, 'left':0.2, 'right':0.2},
                                        processed_full_image: bool = False) -> np.ndarray:
    '''
    function that preprocesses an image given its filename
    '''

    image_path = os.path.join(path, image_n)
    cropped_image = crop_image(image_path, **crop_list)
    resized_image = resize_image(cropped_image)
    modified_image = CLAHE(resized_image)
    patches = create_patches(modified_image, num_patches_per_side = num_patches_per_side)
    normalized_patches = [normalize_image(patch) for patch in patches]
    if processed_full_image:
        return normalize_image(modified_image), normalized_patches

    return normalized_patches

def display_image_preprocess(extracted_image_path: str, num_patches_per_side:int = 3, 
                                            crop_list: Dict[str,int] = {'top': 0.05, 'bottom':0.05, 'left':0.05, 'right':0.05}
                                                                                                    ) -> tuple[np.ndarray, List[np.ndarray]]:
  
  """
  function that preprocesses an image given its filename with the aim to"""
  
  images_filename = sorted(os.listdir(extracted_image_path),
                                  key = lambda x: int(x.split('.')[0]))[0]
  
  processed_image, processed_patches = pre_process(images_filename, extracted_image_path, 
                                                   num_patches_per_side = num_patches_per_side, crop_list=crop_list, processed_full_image = True)

  image_rgb = cv2.imread(os.path.join(extracted_image_path, images_filename), cv2.IMREAD_COLOR)

  return image_rgb, processed_image, processed_patches

def plot_processed_image(extracted_image_path: str, num_patches_per_side:int = 3, 
                            crop_list: Dict[str,int] = 
                                                 {
                                                  'top': 0.05, 'bottom':0.05, 
                                                    'left':0.05, 'right':0.05
                                                                            },
                                    fig_size: List[int] = [10, 7], augmentations_list:List[bool] = [True, True, False, True], fontsize:List[int] = [12, 14]) -> None:
    """
    Plot the original image and a composite image of patches extracted from it.

    Parameters:
    - extracted_image_path: Path to the image from which patches are extracted.
    """

    # Load the original image and patches
    large_image, large_processed_image, small_images = display_image_preprocess(extracted_image_path, num_patches_per_side = num_patches_per_side, crop_list=crop_list)
    patch_per_side = num_patches_per_side
    rows, cols = (patch_per_side, patch_per_side)
    
    if large_image.shape[2] == 3:
        large_image = cv2.cvtColor(large_image, cv2.COLOR_BGR2RGB)

    #Calculate target size for each patch and resize
    large_height, large_width, _ = large_processed_image.shape
    small_height, small_width = large_height // rows, large_width // cols
    small_images_resized = [cv2.resize(img, (small_width, small_height)) for img in small_images]

    #Space between patches
    padding = 3
    composite_height = (rows * small_height) + ((rows + 1) * padding)
    composite_width = (cols * small_width) + ((cols + 1) * padding)


    composite_image = np.zeros((composite_height, composite_width, 3))

    #Place each patch in the composite image
    for i, img in enumerate(small_images_resized[:rows * cols]):
        row = i // cols
        col = i % cols
        start_y = row * (small_height + padding) + padding
        start_x = col * (small_width + padding) + padding
        composite_image[start_y:start_y + small_height, start_x:start_x + small_width] = img

    index = int(num_patches_per_side*((num_patches_per_side-1)/2)+ (num_patches_per_side+1)/2)
    patch = small_images[index]
    augmentations = iter(augmentations_list)
    plotted = []
    title_list = []
    if next(augmentations):
        plotted.append(patch[::-1,:, :])
        title_list.append("V or H Flip")
    if next(augmentations):
        plotted.append(random_rotate(patch))
        title_list.append("Rotation")
    if next(augmentations):
        plotted.append(random_zoom(patch))
        title_list.append("Zoom")
    if next(augmentations):
        plotted.append(random_blur(patch, sigma_interval = [1,2]))
        title_list.append("Blur")

    fig, axes = plt.subplots(1,3, figsize=(fig_size[0], fig_size[1]))

    axes[0].imshow(large_image)
    axes[0].axis('off')

    axes[1].imshow(large_processed_image)
    axes[1].axis('off')

    axes[2].imshow(composite_image)
    axes[2].axis('off')
    
    fig.text(0.17, 0.85, "Original Image", ha='center', va='center', fontsize=fontsize[0])
    fig.text(0.5, 0.85, "After cropping, resizing and CLAHE", ha='center', va='center', fontsize=fontsize[0])
    fig.text(0.83, 0.85, "Patches", ha='center', va='center', fontsize=fontsize[0]) 

    plt.tight_layout()

    fig_2, axes_2 = plt.subplots(1,len(plotted)+1, figsize=(fig_size[0], fig_size[1]))

    axes_2[0].imshow(patch)
    axes_2[0].axis('off')
    axes_2[0].set_title("Original Patch", fontsize=fontsize[1], pad=6)
    
    j = 1
    for img, title in zip(plotted, title_list):
        
        axes_2[j].imshow(img)
        axes_2[j].axis('off')
        axes_2[j].set_title(title, fontsize=fontsize[1], pad=6)
        j += 1
    
    # Show the figure
    plt.tight_layout(pad=2)

    plt.show()

def data_generator_patch(extracted_image_path: str,
                         gender: List[int], label: List[int],
                          train: bool = True, admissible_augmentations = [0,3,4],
                             prob: List[int] = [1/3]*3, num_patches_per_side: int = 3,
                                        data_size:int = 16000, pad = False, crop_list: Dict[str,int] = 
                                                 {
                                                  'top': 0.2, 'bottom':0.05, 'left':0.2, 'right':0.2
                                                                                                    }) -> tuple[tuple[tf.Tensor, tf.Tensor], tf.Tensor]:

    images_filenames = sorted(os.listdir(extracted_image_path),
                              key = lambda x: int(x.split('.')[0]))

    index_list_ = list(range(len(images_filenames)))

    if train:
        index_list = np.random.choice(index_list_, size = data_size)
        all_samples = np.random.choice(admissible_augmentations, p = prob, size = len(index_list))
    else:
        index_list = index_list_
        
    for num, index in enumerate(index_list):
        processed = pre_process(images_filenames[index], extracted_image_path, num_patches_per_side = num_patches_per_side, crop_list = crop_list)
        
        if train:
            index_patch = random.sample(range(len(processed)), 1)[0]
            processed = processed[index_patch:index_patch+1]
            sample_step = all_samples[num:num+1]
            processed_patch = data_augmentation(processed, sample_step)

        else:
            
            processed_patch = processed
            
            if num == (len(index_list) - 1) and pad:
                padding = tf.zeros(shape = processed_patch[0].shape)

                for i in range(len(processed_patch) + 15):
                    
                    if i >= len(processed):
                        yield (padding, 0), 0
                    else:
                        yield (processed_patch[i], gender[index]), label[index]

                    continue

                continue


        for patch in processed_patch:
            yield (patch, gender[index]), label[index]

        # del processed

        # del processed_patch

        # if num % 1000 == 0:
        #     gc.collect()