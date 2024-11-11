# imports
import os
import mlflow
import argparse

import pandas as pd
from pathlib import Path

from sklearn.svm import SVC
from sklearn.model_selection import train_test_split


from npeccv6.model_func import create_model
from npeccv6.train import load_and_preprocess_data
from npeccv6.preprocessing import preprocess_train


import argparse
import datetime
from typing import List, Tuple

import mlflow
import numpy as np
from keras.callbacks import EarlyStopping, History, TensorBoard
from keras.preprocessing.image import ImageDataGenerator

from npeccv6.model_func import load_pretrained_model
from npeccv6.preprocessing import preprocess_train
from npeccv6.utils import read_config, setup_logger


# define functions
def main(args):
    # enable auto logging
    mlflow.autolog()

    # setup parameters
    params = {
        "model_name": "sweep",
        "learning_rate": args.learning_rate,
        "patch_size": args.patch_size,
    }
    
    train_generator, val_generator, steps_per_epoch, validation_steps = process_data(
        args.folder,
        args.patch_size,
        args.patched_data_folder,
    )
    
    # train model
    model = train_model(params, train_generator, val_generator, steps_per_epoch, validation_steps, args.patiance, args.epochs)
    # Output the model and test data
    # write to local folder first, then copy to output folder

    mlflow.tensorflow.save_model(model, "model")

    from distutils.dir_util import copy_tree

    # copy subdirectory example
    from_directory = "model"
    to_directory = args.model_output

    copy_tree(from_directory, to_directory)


def process_data(
        folder:str,
        patch_size:int,
        patched_data_folder:str,
    ):

    preprocess_train(
        images_folder=folder,
        patch_size=patch_size,
        scaling_factor=1,
        save_folder=patched_data_folder,
        clear_dest=True
    )

    # load data from model folder
    train_generator, val_generator, steps_per_epoch, validation_steps = (
        load_and_preprocess_data(
            mask_class="root",
            patch_size=patch_size,
            patch_dir=patched_data_folder,
            seed=42,
            batch_size=16,
        )
    )
    
    return train_generator, val_generator, steps_per_epoch, validation_steps


def train_model(params, train_generator, val_generator, steps_per_epoch, validation_steps, patience, epochs):
    
    early_stop = EarlyStopping(
        monitor="val_iou", patience=patience, restore_best_weights="True", mode="max"
    )
    t
    # train model
    model = create_model(**params)
    history = model.fit(
        train_generator,
        steps_per_epoch=steps_per_epoch,
        epochs=epochs,
        validation_data=val_generator,
        validation_steps=validation_steps,
        callbacks=[early_stop],
    )

    # return model
    return model


def parse_args():
    # setup arg parser
    parser = argparse.ArgumentParser()

    # add arguments
    parser.add_argument("--learning_rate", type=float, default=0.001)
    parser.add_argument("--patch_size", type=float, default=256)
    parser.add_argument("--folder", type=str, default="./data")
    parser.add_argument("--patched_data_folder", type=str, default="./patched_data")
    parser.add_argument("--model_output", type=str, help="Path of output model")
    parser.add_argument("--patiance", type=int, default=5)
    parser.add_argument("--epochs", type=int, default=20)

    # parse args
    args = parser.parse_args()

    # return args
    return args


# run script
if __name__ == "__main__":
    # parse args
    args = parse_args()

    # run main function
    main(args)