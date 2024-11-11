import optuna
import argparse
from optuna.trial import Trial
from npeccv6.train import load_and_preprocess_data, train_model
from npeccv6.utils import read_config
from npeccv6.model_func import create_model
from npeccv6.create_model import main as create_model_main
from npeccv6.preprocessing import preprocess_train
from typing import List

def objective(
    trial: Trial,
    learing_rate: List[float],
    models_folder: str,
    model_name: str,
    ):
    
    # Sample hyperparameters
    lr = trial.suggest_categorical('learning_rate', learning_rate)

    # Create the model with these hyperparameters
    model = create_model(
        model_name="tuning_model",
        patch_size=256,  # Adjust if different patch size needed
        output_classes=1,
        #optimizer=optimizer,
        #loss='binary_crossentropy',
        output_activation="sigmoid",
        learning_rate=lr,
    )

    # load data from model folder
    train_generator, val_generator, steps_per_epoch, validation_steps = (
        load_and_preprocess_data(
            mask_class='root',
            patch_size=config['patch_size'],
            patch_dir=f"{models_folder}/{model_name}/patched_data",
            seed=42,
            batch_size=16,
        )
    )

    # Run the training
    history = train_model(
        model_name="tuning_model",
        train_generator=train_generator,
        val_generator=val_generator,
        steps_per_epoch=steps_per_epoch,
        validation_steps=validation_steps,
        epochs=10,  # Use fewer epochs for faster tuning
        patience=3,
        model=model
    )

    # Get the final validation loss as the target to minimize
    val_iou = history.history['val_iou'][-1]
    return val_iou


def hyperparameter_tune(
    n_trials: int,
    learing_rate: List[float],
    model_name: str,
    models_folder: str,
    ):

    success = create_model_main(
        model_name="tuning_model",
        patch_size=256,  # Adjust if different patch size needed
        output_classes=1,
        #optimizer=optimizer,
        #loss='binary_crossentropy',
        output_activation="sigmoid",
        learning_rate=0.001,
    )
    
    # get model config
    config = read_config(model_name, models_folder)

    # preprocess data to model folder (preprocess_train function)
    preprocess_train(
        images_folder=folder,
        patch_size=config['patch_size'],
        scaling_factor=1,
        save_folder=f"{models_folder}/{model_name}/patched_data",
        clear_dest=False
    )
    
    # Create an Optuna study
    study = optuna.create_study(direction="maximize")
    # Run the optimization
    study.optimize(lambda trial: objective(trial,
                                           learing_rate,
                                           models_folder,
                                           model_name)
                   , n_trials=20)  # Specify the number of trials

    # Print best trial results
    print("Best hyperparameters found:")
    print(study.best_trial.params)

    # Log the best hyperparameters to MLflow
    mlflow.log_params(study.best_trial.params)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Train or tune model.")
    parser.add_argument(
        "--n_trials",
        type=int,
        default=20,
        help="number of trials to make",
    )
    parser.add_argument(
        "--learing_rate",
        type=float,
        default=[0.1, 0.01, 0.001, 0.0001],
        help="List of learing rates",
    )
    parser.add_argument(
        "--model_name",
        type=str,
        default='default',
        help="name of the model to tune",
    )
    parser.add_argument(
        "--models_folder",
        type=str,
        default='../models',
        help="path to models folder",
    )
    
    # Parse arguments
    args = parser.parse_args()

    hyperparameter_tune(
        args.n_trials,
        args.learing_rate,
        args.model_name,
        args.models_folder,
    )