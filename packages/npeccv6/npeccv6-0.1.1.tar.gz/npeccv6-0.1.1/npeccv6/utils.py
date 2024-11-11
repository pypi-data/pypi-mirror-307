import json
import logging
import os
import shutil
import numpy as np
from typing import Iterable, List

import keras
import tensorflow
from tensorflow.keras import backend as K
from tensorflow.keras.models import load_model

"""
# Check model availability, if not, create new one
if config_folder is None:
    config_folder = models_path

try:
    model = load_pretrained_model(model_name)
    logger.info(f"{model_name} loaded.")
except FileNotFoundError:
    config = read_config(model_name, config_folder)
    if isinstance(config, list):
        config = config[0]
    logger.info("Loaded config {config}")
    model = create_model(
        model_name,
        config["input_shape"],
        config["output_classes"],
        config["optimizer"],
        config["loss"],
        config["output_activation"],
        config["dropout_1"],
        config["dropout_2"],
        config["dropout_3"],
    )
    logger.info(f"Training new model: {model_name}.")
"""


def setup_logger(folder: str = "log", debug: bool = False) -> None:
    """
    Authorship: Nick Belterman

    Set up a logger that writes log messages to a file and the console.

    This function creates a logger that writes log messages to a specified
    file and the console. The log messages include a timestamp, the logger's
    name, the severity level of the log message, and the message itself.

    Parameters:
        - folder (str): The directory where the log file will be created. Defaults to "log".

    Returns:
        logging.Logger: Configured logger instance.

    Example:
        .. code-block:: python

            logger = setup_logger()
            logger.info("This is an info message.")
    """
    # Check if logger with the same name already exists
    logger = logging.getLogger(__name__)
    if logger.handlers:
        # Logger already configured, return it
        return logger

    filename = "buas_cv6.log"
    path = os.path.join(folder, filename)
    os.makedirs(folder, exist_ok=True)

    # Create a logger object
    logger = logging.getLogger(__name__)

    # Set the logging level
    if debug:
        logger.setLevel(logging.DEBUG)
    else:
        logger.setLevel(logging.INFO)

    # Create a handler for writing to a file
    file_handler = logging.FileHandler(path)

    # Create a handler for writing to the console
    console_handler = logging.StreamHandler()

    # Create a formatter and add it to the handlers
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)

    # Add the handlers to the logger
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger


# Set up the logger
logger = setup_logger(debug=True)


def clean_model_folder(model_folder: str, preserve_folder: str = "data") -> None:
    """
    Cleans the model folder but preserves the specified folder.
    
    Args:
        model_folder (str): The path to the model folder to be cleaned.
        preserve_folder (str): The name of the folder to preserve (default is "data").
    """
    if os.path.exists(model_folder):
        logger.warning(f"Model folder '{model_folder}' already exists. Cleaning up...")

        # Loop through the contents of the model folder
        for item in os.listdir(model_folder):
            item_path = os.path.join(model_folder, item)

            # Skip the folder that needs to be preserved
            if item == preserve_folder:
                logger.info(f"Preserving '{item}' folder.")
                continue

            # Remove other files and directories
            if os.path.isdir(item_path):
                shutil.rmtree(item_path)
                logger.info(f"Removed folder: {item_path}")
            else:
                os.remove(item_path)
                logger.info(f"Removed file: {item_path}")

    os.makedirs(model_folder, exist_ok=True)
    logger.info(f"Cleaned and prepared model folder: {model_folder}")


def load_config(model_name: str = None, config_folder: str = "./config"):
    model_config = read_config(model_name, config_folder)
    logger.info(f"model config: {model_config}")

    return model_config


def f1(y_true: Iterable[float], y_pred: Iterable[float]) -> float:
    """
    Authorship: Hubert Waleńczak and Nick Belterman

    Calculate the F1 score.

    F1 score is the harmonic mean of precision and recall.
    It's a commonly used metric in binary classification tasks.

    Parameters:
        - y_true (Iterable[float]): True labels.
        - y_pred (Iterable[float]): Predicted labels.

    Returns:
        - float: The F1 score.
    """

    def recall_m(y_true: Iterable[float], y_pred: Iterable[float]) -> float:
        y_true = tensorflow.cast(y_true, tensorflow.float32)
        y_pred = tensorflow.cast(y_pred, tensorflow.float32)
        TP = K.sum(K.round(K.clip(y_true * y_pred, 0, 1)))
        Positives = K.sum(K.round(K.clip(y_true, 0, 1)))
        recall = TP / (Positives + K.epsilon())
        return recall

    def precision_m(y_true: Iterable[float], y_pred: Iterable[float]) -> float:
        y_true = tensorflow.cast(y_true, tensorflow.float32)
        y_pred = tensorflow.cast(y_pred, tensorflow.float32)
        TP = K.sum(K.round(K.clip(y_true * y_pred, 0, 1)))
        Pred_Positives = K.sum(K.round(K.clip(y_pred, 0, 1)))
        precision = TP / (Pred_Positives + K.epsilon())
        return precision

    try:
        precision, recall = precision_m(y_true, y_pred), recall_m(y_true, y_pred)
    except ValueError:
        logger.error(
            f"An ValueError occurred while calculating precision and recall due to mismatched shapes between {y_true.shape = } and {y_pred.shape =}."
        )

    f1_score = 2 * ((precision * recall) / (precision + recall + K.epsilon()))
    return f1_score


def iou(y_true: Iterable[float], y_pred: Iterable[float]) -> float:
    """
    Authorship: Hubert Waleńczak and Nick Belterman

    Calculate the Intersection over Union (IoU) score.

    Intersection over Union (IoU) is a measure used to evaluate the
    overlap between two boundaries. In the context of object detection
    or segmentation, it's used to evaluate the accuracy of predicted
    bounding boxes or segmentations against the ground truth.

    Parameters:
        - y_true (Iterable[float]): True labels.
        - y_pred (Iterable[float]): Predicted labels.

    Returns:
        float: The IoU score.
    """

    def f(y_true: Iterable[float], y_pred: Iterable[float]) -> float:
        y_true = tensorflow.cast(y_true, tensorflow.float32)
        y_pred = tensorflow.cast(y_pred, tensorflow.float32)
        intersection = K.sum(K.abs(y_true * y_pred), axis=[1, 2, 3])
        total = K.sum(K.square(y_true), [1, 2, 3]) + K.sum(K.square(y_pred), [1, 2, 3])
        union = total - intersection
        return (intersection + K.epsilon()) / (union + K.epsilon())

    # Default value
    iou_score = 0.0
    try:
        iou_score = K.mean(f(y_true, y_pred), axis=-1)
        logger.debug(f"iou return value - {iou_score}")
    except ValueError:
        logger.error(
            f"An ValueError occurred while calculating iou due to mismatched shapes between {y_true.shape = } and {y_pred.shape = }."
        )
    return iou_score


def mean_confidence_score(predicted_probs: np.ndarray, threshold: float = 0.5) -> float:
    """
    Authorship: Nick Belterman

    Calculates the mean confidence score of the predicted probabilities that exceed a given threshold.

    Parameters:
        - predicted_probs (Union[np.ndarray, Any]): A numpy array or similar structure containing the predicted probabilities.
        - threshold (float, optional): The threshold above which the predicted probabilities are considered. Default is 0.5.

    Returns:
        - np.ndarray: The mean confidence score of the pixels above the threshold.
    """
    root_pixels = predicted_probs[predicted_probs > threshold]
    return float(np.mean(root_pixels)) if root_pixels.size > 0 else float(0)


def create_config_json(
    model_name: str,
    patch_size: int = 256,
    output_classes: int = 1,
    #optimizer: str = "adam",
    #loss: str = "binary_crossentropy",
    output_activation: str = "sigmoid",
    learning_rate: float = 0.001,
    model_path: str = "./models",
    expected_plants_num: int = 5,
) -> None:
    """
    Authorship: Nick Belterman and Cristian Stinga

    Create or update a JSON configuration file with model parameters.

    Parameters:
        - model_name (str): The name of the model to be added or updated.
        - input_shape (List[int], optional): Input shape of the model. Default is [256, 256, 1].
        - output_classes (int, optional): Number of output classes. Default is 1.
        - optimizer (str, optional): Optimizer for training. Default is "adam".
        - loss (str, optional): Loss function for training. Default is "binary_crossentropy".
        - output_activation (str, optional): Activation function for output layer. Default is "sigmoid".
        - learning_rate (float, optional): Learning rate for model.
        - model_path (str): Path to models directory.
        - expected_plants_num (int): Number of plants expected in image.

    Returns:
        - Dict
    """
    params = {
        "patch_size": patch_size,
        "output_classes": output_classes,
        #"optimizer": optimizer,
        #"loss": loss,
        "output_activation": output_activation,
        "learning_rate": learning_rate,
        "expected_plants_num": expected_plants_num,
    }

    # Log the action of writing parameters to the JSON file
    logger.info(
        f"main - Writing parameters to model_config.json - {model_name}: {params}"
    )

    # Define the path to the configuration JSON file
    path_config_json = f"{model_path}"
    os.makedirs(path_config_json, exist_ok=True)
    path_config_json = f"{model_path}/config.json"
    try:
        # Try load existing parameters from the JSON file if it exists
        with open(path_config_json, "r", encoding="utf-8") as json_load:
            config_dict = json.load(json_load)

        # Check if the model name already exists in the configuration
        if model_name in config_dict:
            # Log an error if the model name already exists
            logger.warning(f"main - Model with name: {model_name} already exists.")
        else:
            # Add the new model parameters to the configuration dictionary
            config_dict[model_name] = params

        # Write the updated configuration back to the JSON file
        with open(path_config_json, "w", encoding="utf-8") as json_dump:
            json.dump(config_dict, json_dump, indent=4)
            logger.info(f"main - Updated config file and added model: {model_name}.")

    except FileNotFoundError:
        # If the JSON file does not exist, create a new dictionary with the model name as the key and parameters as values
        config_dict = {model_name: params}

        # Write the new configuration dictionary to a new JSON file
        with open(path_config_json, "w", encoding="utf-8") as json_file:
            json.dump(config_dict, json_file)

    except json.JSONDecodeError:
        # Handle JSON decoding error if the file is not properly formatted
        logger.error(
            f"main - JSON decode error while reading the file {path_config_json}."
        )
    return config_dict


def read_config(model_name: str, model_path: str = "./models"):
    """
    Authorship: Nick Belterman

    Reads the configuration for the specified model from a JSON file.

    Parameters:
        model_name (str): The name of the model whose configuration is to be read.
        model_path (str): Path to models directory.

    Returns:
        dict: The configuration dictionary for the specified model.

    Raises:
        FileNotFoundError: If the configuration file does not exist.
        KeyError: If the specified model name is not found in the configuration.
        json.JSONDecodeError: If there is an error decoding the JSON file.
    """
    try:
        logger.info("Loading config file.")
        with open(f"{model_path}/{model_name}/config.json", "r", encoding="utf-8") as f:
            config = json.load(f)

        if model_name not in config:
            raise KeyError(
                f"Model '{model_name}' not found in the configuration. You may need to first initialize the model."
            )

        return config[model_name]
    except FileNotFoundError as fnf_error:
        logger.info(f"Error: The configuration file was not found. {fnf_error}")
        raise
    except KeyError as key_error:
        logger.info(f"Error: {key_error}")
        raise
    except json.JSONDecodeError as json_error:
        logger.info(f"Error: Failed to decode JSON. {json_error}")
        raise
    except Exception as e:
        logger.info(f"An unexpected error occurred: {e}")
        raise
