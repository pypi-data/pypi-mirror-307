import argparse
import glob
import os
from typing import Tuple

import cv2
import numpy as np
from numpy import ndarray
from patchify import patchify

from npeccv6.utils import setup_logger

logger = setup_logger(debug=True)


# TO-DO: Improve docstrings
def crop_to_petri(im: np.ndarray) -> Tuple[np.ndarray, int, int, int]:
    """
    Authorship: Amyr Lourenz, Marwa Rouah, Hubert Waleńczak

    Detect and crop image to the petri dish as square.

    Parameters:
        - im (np.ndarray): Input image (grayscale).

    Returns:
        - Tuple[np.ndarray, int, int, int]: Cropped image containing the petri dish,
                                            X-coordinate of the top-left corner of the petri dish ROI,
                                            Y-coordinate of the top-left corner of the petri dish ROI,
                                            Width of the petri dish ROI.
    """

    logger.debug("Starting petri dish detection and cropping.")
    _, output_im = cv2.threshold(im, 100, 255, cv2.THRESH_BINARY)
    _, _, stats, _ = cv2.connectedComponentsWithStats(output_im)
    stats = stats[1:]
    max_area_index = np.argmax(stats[:, 4])
    x, y, w, h, _ = stats[max_area_index]
    side_length = max(w, h)
    crop_im = im[y : y + side_length, x : x + side_length]
    logger.debug("Petri dish cropping completed.")
    return crop_im, x, y, side_length


def padder(image: np.ndarray, patch_size: int) -> np.ndarray:
    """
    Authorship: Marwa Rouah

    Adds padding to an image to make its dimensions divisible by a specified patch size.

    This function calculates the amount of padding needed for both the height and width of an image
    so that its dimensions become divisible by the given patch size. The padding is applied evenly to both sides
    of each dimension (top and bottom for height, left and right for width). If the padding amount is odd,
    one extra pixel is added to the bottom or right side. The padding color is set to black (0, 0, 0).

    Parameters:
        - image (np.ndarray): The input image as a NumPy array. Expected shape is (height, width, channels).
        - patch_size (int): The patch size to which the image dimensions should be divisible. It's applied to both height and width.

    Returns:
        - np.ndarray: The padded image as a NumPy array with the same number of channels as the input.
          Its dimensions are adjusted to be divisible by the specified patch size.

    Example:
        - padded_image = padder(cv2.imread('example.jpg'), 128)

    """
    logger.debug(
        f"Starting padding for image of shape {image.shape} to make dimensions divisible by {patch_size}."
    )

    h, w = image.shape[:2]
    height_padding = ((h // patch_size) + 1) * patch_size - h
    width_padding = ((w // patch_size) + 1) * patch_size - w

    top_padding = height_padding // 2
    bottom_padding = height_padding - top_padding

    left_padding = width_padding // 2
    right_padding = width_padding - left_padding

    logger.debug(
        f"Calculated padding: top={top_padding}, bottom={bottom_padding}, left={left_padding}, right={right_padding}"
    )

    padded_image = cv2.copyMakeBorder(
        image,
        top_padding,
        bottom_padding,
        left_padding,
        right_padding,
        cv2.BORDER_CONSTANT,
        value=[0, 0, 0],
    )

    logger.info(f"Padding completed. New image shape is {padded_image.shape}.")

    return padded_image


def preprocess_image(
    image: ndarray,
    patch_size: int = 256,
    save_folder: str = '/tmp',
    file_name: str = 'tmp',
    suffix: str = '.png',
    scaling_factor: float = 1,
) -> None:
    """
    Authorship: Hubert Waleńczak

    Pre-processes an image, creates patches, and saves them.

    Parameters:
        - image (ndarray): Image cropped to petri dish.
        - patch_size (int): Size of the patches to be created.
        - save_folder (str): Folder to save the patches.
        - file_name (str): Name of the file before patch number e.g.: image_1
        - suffix (str): Suffix to be added after patch number e.g.: _root_mask.png
        - scaling_factor (float): A factor to scale the image by

    Returns:
        None

    Notes:
        - Needs a image already cropped to petri dish
        - Rescales the image if specified.
    """
    logger.debug("pre-processing image")
    logger.debug(f"Patch size: {patch_size}")

    # Pad images and masks to be devidabe by patch size
    logger.debug("Pre-process image - padding")
    image = padder(image, patch_size)

    # Rescale if specified
    if scaling_factor != 1:
        logger.info(f"Rescaling with factor of {scaling_factor}")
        image = cv2.resize(image, (0, 0), fx=scaling_factor, fy=scaling_factor)
        # root_mask = cv2.resize(root_mask, (0, 0), fx=scaling_factor, fy=scaling_factor)

    # Create patches for image
    patches = patchify(image, (patch_size, patch_size), step=patch_size)
    i = patches.shape[0]
    j = patches.shape[1]
    patches = patches.reshape(-1, patch_size, patch_size)

    # Save patches for image
    # TO-DO: Save in correct place
    # e.g. im_path: ../data/test/test/image.png
    # e.g. image_patch_path: ../data/test/test_images/test/image.png

    # save_folder = save_folder.split("/", 9)[-1]
    # save_folder = save_folder.rsplit("/", 1)[0]
    # logger.debug(f"process_image - {save_folder = }")
    # save_folder = datastore_uri + save_folder
    
    if save_folder is not None:
        save_folder = save_folder.replace("\\", "/")
        os.makedirs(save_folder, exist_ok=True)
        logger.debug(f"process_image - {save_folder = }")

        for j, patch in enumerate(patches):
            image_patch_path_numbered = save_folder + f"/{file_name}_" + str(j) + suffix
            cv2.imwrite(image_patch_path_numbered, patch)

    return patches, i, j, image


def preprocess_train(
    images_folder: str = "./data",
    patch_size: int = 256,
    scaling_factor: float = 1,
    save_folder: str = "./data_patched",
    clear_dest: bool = False,
) -> None:
    """
    Authorship: Hubert Waleńczak

    Generate and save patches for images and corresponding masks.

    Parameters:
        - images_folder (str): Path to the root of data folder.
        - patch_size (int): Size of the patches to be created.
        - scaling_factor (float): A factor to scale the images and masks.
        - save_folder (str): Directory to save the patched images.

    Returns:
        None
    """
    
    logger.info(f"Preprocess train - {images_folder = }")
    # Get all image names in folder
    folder_list = glob.glob(images_folder + "/*")
    logger.debug(f"Exploring folder_list - {folder_list} for images and masks folders")

    folder_list = [file.replace("\\", "/") for file in folder_list]

    folder_list = [file.replace(images_folder + "/", "") for file in folder_list]
    logger.info(f"Folders - {folder_list = }")

    # Get train test and masks folders
    train_folder = images_folder + "/train"
    test_folder = images_folder + "/test"
    masks_folder = images_folder + "/masks"

    # Get train and test image namesfrom numpy import ndarray
    train_file_list = sorted(glob.glob(train_folder + "/*"))
    test_file_list = sorted(glob.glob(test_folder + "/*"))
    logger.debug(f"{train_file_list = }")
    logger.debug(f"{test_file_list = }")

    # Create temporary folders
    # os.makedirs("tmp/npeccv6/images/train", exist_ok=True)
    # os.makedirs("tmp/npeccv6/images/test", exist_ok=True)
    # os.makedirs("tmp/npeccv6/masks/train", exist_ok=True)
    # os.makedirs("tmp/npeccv6/masks/test", exist_ok=True)

    # TO-DO: Add other masks
    # TO-DO: Convert to function
    logger.info("Processing train")
    for im_path in train_file_list:
        # Load and crop image
        image = cv2.imread(im_path, cv2.IMREAD_GRAYSCALE)
        crop_im, x, y, side_length = crop_to_petri(image)

        # Get base file name
        file_name = os.path.basename(im_path).rsplit(".", 1)[0]
        logger.debug(f"File name - {file_name}")

        # Masks paths
        mask_path_root = os.path.join(masks_folder, file_name + "_root_mask.tif")
        logger.debug(f"Root mask path - {mask_path_root}")
        #mask_path_seed = os.path.join(masks_folder, file_name + "_seed_mask.tif")
        #logger.debug(f"Seed mask path - {mask_path_root}")

        # Prepare masks and preprocess image and masks
        if os.path.exists(mask_path_root):
            mask_root = cv2.imread(mask_path_root, cv2.IMREAD_GRAYSCALE)[
                y : y + side_length, x : x + side_length
            ]
            preprocess_image(
                crop_im,
                patch_size,
                f"{save_folder}/train/images",
                file_name,
                ".png",
                scaling_factor,
            )
            preprocess_image(
                mask_root,
                patch_size,
                f"{save_folder}/train/root",
                file_name,
                #"_root_mask.tif",
                ".png",
                scaling_factor,
            )
            # preprocess_image(mask_seed, patch_size, f"{save_folder}/train/seed", file_name, "_seed_mask.tif", scaling_factor)
            # TO-DO: add/remove masks
            # TO-DO: detect classes
        else:
            logger.warning(f"Mask files for {file_name} not found.")

    logger.info("Processing test")
    for im_path in test_file_list:
        # Load and crop image
        image = cv2.imread(im_path, cv2.IMREAD_GRAYSCALE)
        crop_im, x, y, side_length = crop_to_petri(image)

        # Get base file name
        file_name = os.path.basename(im_path).rsplit(".", 1)[0]
        logger.debug(f"File name - {file_name}")

        # Masks paths
        mask_path_root = os.path.join(masks_folder, file_name + "_root_mask.tif")
        logger.debug(f"Root mask path - {mask_path_root}")

        # Prepare masks and preprocess image and masks
        if os.path.exists(mask_path_root):
            mask_root = cv2.imread(mask_path_root, cv2.IMREAD_GRAYSCALE)[
                y : y + side_length, x : x + side_length
            ]
            preprocess_image(
                crop_im,
                patch_size,
                f"{save_folder}/test/images",
                file_name,
                ".png",
                scaling_factor,
            )
            preprocess_image(
                mask_root,
                patch_size,
                f"{save_folder}/test/root",
                file_name,
                #"_root_mask.tif",
                ".png",
                scaling_factor,
            )
            #preprocess_image(mask_seed,patch_size,f"{save_folder}/test/seed",file_name,"_seed_mask.tif",scaling_factor,)

        else:
            logger.warning(f"Mask files for {file_name} not found.")


def main():
    parser = argparse.ArgumentParser(
        description="Preprocess images and masks into patches."
    )
    parser.add_argument(
        "--images_folder",
        type=str,
        default="./data",
        help="Path to the root of data folder.",
    )
    parser.add_argument(
        "--patch_size", type=int, default=256, help="Size of the patches to be created."
    )
    parser.add_argument(
        "--scaling_factor",
        type=float,
        default=1,
        help="A factor to scale the images and masks.",
    )
    parser.add_argument(
        "--save_folder",
        type=str,
        default="./data_patched",
        help="Directory to save the patched images.",
    )

    args = parser.parse_args()

    preprocess_train(
        args.images_folder, args.patch_size, args.scaling_factor, args.save_folder
    )


if __name__ == "__main__":
    main()
