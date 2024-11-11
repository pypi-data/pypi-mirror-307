import argparse
import shutil
import os
from npeccv6.utils import setup_logger, create_config_json, clean_model_folder
from npeccv6.model_func import create_model
from typing import List

logger = setup_logger(debug=True)

def main(
    model_name: str = 'default',
    patch_size: int = 256,
    #output_classes: int = 1,
    #optimizer: str = "adam",
    #loss: str = "binary_crossentropy",
    output_activation: str = "sigmoid",
    learning_rate: int = 0.001,
    expected_plants_num: int = 5,
    models_folder: str = "../models",
    # TO-DO: classes
):
    """
    WARNING! THIS FUNCTION WILL OVERWRITE EXISTING MODELS

    This function prepares the model folder by cleaning it if it exists, creates a new model,
    saves the model's configuration to a JSON file, and logs all the actions performed.
    """

    # Set model details
    model_folder = f"{models_folder}/{model_name}"

    # Prepare the model folder: clean it if it exists
    clean_model_folder(model_folder, 'data')

    # Create model
    model = create_model(
        model_name=model_name,
        patch_size=patch_size,
        #output_classes=output_classes,
        #optimizer=optimizer,
        #loss=loss,
        output_activation=output_activation,
        learning_rate=learning_rate,
        # TO-DO: add learning rate
    )
    model_save_path = f"{model_folder}/{model_name}.keras"
    model.save(model_save_path)
    
    # Save the configuration to a JSON file
    config = create_config_json(
        model_name=model_name,
        patch_size=patch_size,
        #output_classes=output_classes,
        #optimizer=optimizer,
        #loss=loss,
        output_activation=output_activation,
        learning_rate=learning_rate,
        model_path=model_folder,
        expected_plants_num=expected_plants_num,
        # TO-DO: classes
    )
    
    # Create folders data and patched_data
    paths = [f"{model_folder}/data/test", f"{model_folder}/data/train", f"{model_folder}/data/masks", f"{model_folder}/patched_data/test", f"{model_folder}/patched_data/train", f"{model_folder}/tmp", f"{model_folder}/hist"]
    for path in paths:
        if not os.path.exists(path):
            os.makedirs(path)

    # Log the final state and completion of the main function
    logger.info(f"Configuration saved for model '{model_name}'.")

    return 0


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Create new model. WARNING! Will overwrite existing model!"
    )
    parser.add_argument(
        "--model_name",
        type=str,
        default="default",
        help="Path to the root of data folder.",
    )
    parser.add_argument(
        "--patch_size", type=int, default=256, help="Size of the patches to be created."
    )
    '''
    parser.add_argument(
        "--output_classes",
        type=int,
        default=1,
        help="Number of output classes.",
    )
    parser.add_argument(
        "--optimizer",
        type=str,
        default='adam',
        help="Directory to save the patched images.",
    )
    parser.add_argument(
        "--loss",
        type=str,
        default='binary_crossentropy',
        help="Directory to save the patched images.",
    )
    '''
    parser.add_argument(
        "--output_activation",
        type=str,
        default='sigmoid',
        help="What activation function to use on last layer.",
    )
    parser.add_argument(
        "--learning_rate",
        type=float,
        default=0.001,
        help="What learning rate to use while training.",
    )
    parser.add_argument(
        "--expected_plants_num",
        type=float,
        default=5,
        help="Number of expected plants.",
    )
    parser.add_argument(
        "--models_folder",
        type=str,
        default="../models",
        help="Path to folder with models.",
    )

    args = parser.parse_args()

    main(
        model_name = args.model_name,
        patch_size = args.patch_size,
        #output_classes = args.output_classes,
        #optimizer = args.optimizer,
        #loss = args.loss,
        output_activation = args.output_activation,
        learning_rate = args.learning_rate,
        expected_plants_num = args.expected_plants_num,
        models_folder = args.models_folder,
    )
