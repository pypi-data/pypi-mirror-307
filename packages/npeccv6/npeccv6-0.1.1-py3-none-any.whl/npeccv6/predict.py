from tensorflow.keras.models import load_model
from npeccv6.utils import load_config, f1, iou, setup_logger, mean_confidence_score
from npeccv6.postprocessing import postprocess_prediction, process_image_for_roots
from npeccv6.preprocessing import crop_to_petri, padder, preprocess_image
from datetime import datetime
from tensorflow import keras
from typing import Tuple
from tensorflow.keras.utils import custom_object_scope
import numpy as np
import cv2
import argparse
import os


logger = setup_logger(debug=True)

def predict(
    model: keras.models.Model,
    image: np.ndarray = None,
    patch_size: int = 256,
    threshold: float = 0.8,
    scaling_factor: float = 1,
    num_channels: int = 1,
    segment: bool = False,
    expected_nr_plants: int = 5,
) -> Tuple[np.ndarray[int], float]:
    """
    Authorship: Hubert Waleńczak and Nick Belterman

    Predict and post-process the mask for the given image.

    Parameters:
        - model (Model): Trained Keras model for prediction.
        - image (ndarray): Image being predicted
        - save_path (str): Path to save the predicted mask. Default is "Predictions/Image.png".
        - patch_size (int): Size of the patches. Default is 256.
        - threshold (float): Threshold value for binarizing the mask. Default is 0.8.
        - scaling_factor (float): Scaling factor for the image. Default is 1.
        - num_channels (int): Number of channels for the image (1 for grayscale, 3 for color). Default is 1.
        - segment (bool): Wether to segment the roots or not. Default is False.
        - expected_nr_plants (int): The expected number of plants to be found. Default is 5.

    Returns:
        - np.ndarray: Predicted binary mask.
        - float: Mean confidence score of prediction
    """

    # Preprocess image
    patches, i, j, im = preprocess_image(
        image = image, patch_size = patch_size, save_folder = None, scaling_factor = scaling_factor
    )

    logger.info("Starting predicting on patches.")

    # Predict
    preds = model.predict(patches / 255)

    # Calculate mean confidence score
    mean_conf_score = mean_confidence_score(preds, threshold)

    logger.info("Prediction completed. Starting post-processing.")

    # Postprocess prediction WARNING! requires image from preprocessing
    predicted_mask = postprocess_prediction(
        preds, i, j, im, threshold, patch_size, segment, expected_nr_plants
    )

    # Convert binary mask to uint8 image
    predicted_mask = predicted_mask.astype(np.uint8) * 255

    logger.info("Predicted mask saved successfully.")
    return predicted_mask, mean_conf_score



def main(
    image: np.ndarray,
    model_name: str,
    models_path: str,
    save_path: str,
    threshold: float,
) -> None:
    # Make sure save folder exists
    if not os.path.exists(save_path):
        os.makedirs(save_path)

    # Load model config
    config = load_config(model_name = model_name, config_folder = models_path)
    
    # Crop and pad image
    cropped_image, x, y, side_length = crop_to_petri(image)
    padded_image = padder(cropped_image, int(config['patch_size']))
    
    # Move image to model history
    timestamp = datetime.now().strftime("%d_%m_%Y_%H_%M_%S")
    cv2.imwrite(f"{models_path}/{model_name}/hist/{timestamp}_petri.png", padded_image)
    
    # Load the pretrained model
    with custom_object_scope({"f1": f1, "iou": iou}):
        model = load_model(f"{models_path}/{model_name}/{model_name}.keras")

    # Predict the mask
    predicted_mask, mean_conf_score = predict(       
        model = model,
        image = cropped_image,
        patch_size = int(config['patch_size']),
        threshold = threshold,
        scaling_factor = 1,
        num_channels = 1,
        segment = False,
        expected_nr_plants = int(config['expected_plants_num']),
    )
    
    # Save patched prediction to history
    cv2.imwrite(f"{models_path}/{model_name}/hist/{timestamp}_mask.png", predicted_mask)
    
    # Postprocess the image to get info about roots
    try:
        root_lengths, root_tip_coords, marked_image = process_image_for_roots(
            predicted_mask, int(config['expected_plants_num'])
        )
        
        logger.info(f"Root lengths: {root_lengths}")
        logger.info(f"Root tips coordinates in image (px): {root_tip_coords}")
        
        # Save the marked mask
        cv2.imwrite(f"{models_path}/{model_name}/hist/{timestamp}_marked_mask.png", marked_image)
        cv2.imwrite(f"{save_path}/{timestamp}_marked_mask.png", marked_image)
    
    except Exception as e:
        print(e)
        logger.error(e)
    # Log the details
    logger.info(f"Mean confidence score: {mean_conf_score}")
    
    return 0, f"{timestamp}_marked_mask.png"


if __name__ == "__main__":
    # Author: Hubert Waleńczak
    parser = argparse.ArgumentParser(
        description="Predict a root mask from an image using a trained model."
    )
    #parser.add_argument("--image_path", type=str, help="Path to the input image file.")
    parser.add_argument(
        "--save_path",
        type=str,
        default=".",
        help="Where to save the predicted mask.",
    )
    parser.add_argument(
        "-m",
        "--model_name",
        type=str,
        default="main",
        action="store",
        help="What model name to use. Default is main.",
    )
    parser.add_argument(
        "-t",
        "--threshold",
        # dest = "threshold",
        type=float,
        default=0.8,
        action="store",
        help="Threshold for the predicted mask. Defult: 0.8.",
    )
    parser.add_argument(
        "--models_path",
        type=str,
        default="../models",
        help="Path to models direcotry. Defautl is '../models'",
    )
    parser.add_argument(
        "--image_path",
        type=str,
        help="Path to the input image file."
    )
    
    # Parse the arguments
    args = parser.parse_args()
    
    # Load image
    image = cv2.imread(args.image_path, cv2.IMREAD_GRAYSCALE)
    
    main(image, args.model_name, args.models_path, args.save_path, args.threshold)