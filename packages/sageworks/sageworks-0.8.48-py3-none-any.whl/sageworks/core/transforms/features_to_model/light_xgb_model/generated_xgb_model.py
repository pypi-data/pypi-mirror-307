# Imports for XGB Model
import xgboost as xgb
import awswrangler as wr

# Model Performance Scores
from sklearn.metrics import (
    mean_absolute_error,
    r2_score,
    mean_squared_error,
    precision_recall_fscore_support,
    confusion_matrix,
)

# Classification Encoder
from sklearn.preprocessing import LabelEncoder

# Scikit Learn Imports
from sklearn.model_selection import train_test_split

from io import StringIO
import json
import argparse
import joblib
import os
import pandas as pd
from typing import List


# Function to check if dataframe is empty
def check_dataframe(df: pd.DataFrame, df_name: str) -> None:
    """
    Check if the provided dataframe is empty and raise an exception if it is.

    Args:
        df (pd.DataFrame): DataFrame to check
        df_name (str): Name of the DataFrame
    """
    if df.empty:
        msg = f"*** The training data {df_name} has 0 rows! ***STOPPING***"
        print(msg)
        raise ValueError(msg)


def expand_proba_column(df: pd.DataFrame, class_labels: List[str]) -> pd.DataFrame:
    """
    Expands a column in a DataFrame containing a list of probabilities into separate columns.

    Args:
        df (pd.DataFrame): DataFrame containing a "pred_proba" column
        class_labels (List[str]): List of class labels

    Returns:
        pd.DataFrame: DataFrame with the "pred_proba" expanded into separate columns
    """

    # Sanity check
    proba_column = "pred_proba"
    if proba_column not in df.columns:
        raise ValueError('DataFrame does not contain a "pred_proba" column')

    # Construct new column names with '_proba' suffix
    new_col_names = [f"{label}_proba" for label in class_labels]

    # Expand the proba_column into separate columns for each probability
    proba_df = pd.DataFrame(df[proba_column].tolist(), columns=new_col_names)

    # Drop the original proba_column and reset the index in prep for the concat
    df = df.drop(columns=[proba_column])
    df = df.reset_index(drop=True)

    # Concatenate the new columns with the original DataFrame
    df = pd.concat([df, proba_df], axis=1)
    print(df)
    return df


def match_features_case_insensitive(df: pd.DataFrame, model_features: list) -> pd.DataFrame:
    """
    Matches and renames the DataFrame's column names to match the model's feature names (case-insensitive).
    Prioritizes exact case matches first, then falls back to case-insensitive matching if no exact match exists.

    Args:
        df (pd.DataFrame): The DataFrame with the original columns.
        model_features (list): The desired list of feature names (mixed case allowed).

    Returns:
        pd.DataFrame: The DataFrame with renamed columns to match the model's feature names.
    """
    # Create a mapping for exact and case-insensitive matching
    exact_match_set = set(df.columns)
    column_map = {}

    # Build the case-insensitive map (if we have any duplicate columns, the first one wins)
    for col in df.columns:
        lower_col = col.lower()
        if lower_col not in column_map:
            column_map[lower_col] = col

    # Create a dictionary for renaming
    rename_dict = {}
    for feature in model_features:
        # Check for an exact match first
        if feature in exact_match_set:
            rename_dict[feature] = feature

        # If not an exact match, fall back to case-insensitive matching
        elif feature.lower() in column_map:
            rename_dict[column_map[feature.lower()]] = feature

    # Rename the columns in the DataFrame to match the model's feature names
    return df.rename(columns=rename_dict)


if __name__ == "__main__":
    """The main function is for training the XGBoost model"""

    # Harness Template Parameters
    target = "iq_score"
    feature_list = ["height", "weight", "salary", "age", "likes_dogs"]
    model_type = "regressor"
    model_metrics_s3_path = "s3://sandbox-sageworks-artifacts/models/training/stress-model-3"
    train_all_data = "False"
    validation_split = 0.2

    # Sagemaker specific arguments. Defaults are set in the environment variables.
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--output-data-dir", type=str, default=os.environ["SM_OUTPUT_DATA_DIR"]
    )
    parser.add_argument("--model-dir", type=str, default=os.environ["SM_MODEL_DIR"])
    parser.add_argument("--train", type=str, default=os.environ["SM_CHANNEL_TRAIN"])
    args = parser.parse_args()

    # Read the training data into DataFrames
    training_files = [
        os.path.join(args.train, file)
        for file in os.listdir(args.train)
        if file.endswith(".csv")
    ]
    print(f"Training Files: {training_files}")

    # Combine files and read them all into a single pandas dataframe
    all_df = pd.concat([pd.read_csv(file, engine="python") for file in training_files])

    # Check if the dataframe is empty
    check_dataframe(all_df, "training_df")

    # Features/Target output
    print(f"Target: {target}")
    print(f"Features: {str(feature_list)}")

    # Do we want to train on all the data?
    if train_all_data == "True":
        print("Training on ALL of the data")
        df_train = all_df.copy()
        df_val = all_df.copy()

    # Does the dataframe have a training column?
    elif "training" in all_df.columns:
        print("Found training column, splitting data based on training column")
        df_train = all_df[all_df["training"] == 1].copy()
        df_val = all_df[all_df["training"] == 0].copy()
    else:
        # Just do a random training Split
        print("WARNING: No training column found, splitting data with random state=42")
        df_train, df_val = train_test_split(
            all_df, test_size=validation_split, random_state=42
        )
    print(f"FIT/TRAIN: {df_train.shape}")
    print(f"VALIDATION: {df_val.shape}")

    # Now spin up our XGB Model
    if model_type == "classifier":
        xgb_model = xgb.XGBClassifier()

        # Encode the target column
        label_encoder = LabelEncoder()
        df_train[target] = label_encoder.fit_transform(df_train[target])
        df_val[target] = label_encoder.transform(df_val[target])

    else:
        xgb_model = xgb.XGBRegressor()
        label_encoder = None  # We don't need this for regression

    # Grab our Features, Target and Train the Model
    y = df_train[target]
    X = df_train[feature_list]
    xgb_model.fit(X, y)

    # Make Predictions on the Validation Set
    print(f"Making Predictions on Validation Set...")
    preds = xgb_model.predict(df_val[feature_list])
    if model_type == "classifier":
        # Also get the probabilities for each class
        print("Processing Probabilities...")
        probs = xgb_model.predict_proba(df_val[feature_list])
        df_val["pred_proba"] = [p.tolist() for p in probs]

        # Expand the pred_proba column into separate columns for each class
        print(df_val.columns)
        df_val = expand_proba_column(df_val, label_encoder.classes_)
        print(df_val.columns)

        # Decode the target and prediction labels
        df_val[target] = label_encoder.inverse_transform(df_val[target])
        preds = label_encoder.inverse_transform(preds)

    # Save predictions to S3 (just the target, prediction, and '_proba' columns)
    df_val["prediction"] = preds
    output_columns = [target, "prediction"]
    output_columns += [col for col in df_val.columns if col.endswith("_proba")]
    wr.s3.to_csv(
        df_val[output_columns],
        path=f"{model_metrics_s3_path}/validation_predictions.csv",
        index=False,
    )

    # Report Performance Metrics
    if model_type == "classifier":
        # Get the label names and their integer mapping
        label_names = label_encoder.classes_

        # Calculate various model performance metrics
        scores = precision_recall_fscore_support(
            df_val[target], preds, average=None, labels=label_names
        )

        # Put the scores into a dataframe
        score_df = pd.DataFrame(
            {
                target: label_names,
                "precision": scores[0],
                "recall": scores[1],
                "fscore": scores[2],
                "support": scores[3],
            }
        )

        # We need to get creative with the Classification Metrics
        metrics = ["precision", "recall", "fscore", "support"]
        for t in label_names:
            for m in metrics:
                value = score_df.loc[score_df[target] == t, m].iloc[0]
                print(f"Metrics:{t}:{m} {value}")

        # Compute and output the confusion matrix
        conf_mtx = confusion_matrix(df_val[target], preds, labels=label_names)
        for i, row_name in enumerate(label_names):
            for j, col_name in enumerate(label_names):
                value = conf_mtx[i, j]
                print(f"ConfusionMatrix:{row_name}:{col_name} {value}")

    else:
        # Calculate various model performance metrics (regression)
        rmse = mean_squared_error(df_val[target], preds, squared=False)
        mae = mean_absolute_error(df_val[target], preds)
        r2 = r2_score(df_val[target], preds)
        print(f"RMSE: {rmse:.3f}")
        print(f"MAE: {mae:.3f}")
        print(f"R2: {r2:.3f}")
        print(f"NumRows: {len(df_val)}")

    # Now save the model to the standard place/name
    xgb_model.save_model(os.path.join(args.model_dir, "xgb_model.json"))
    if label_encoder:
        joblib.dump(label_encoder, os.path.join(args.model_dir, "label_encoder.joblib"))

    # Also save the features (this will validate input during predictions)
    with open(os.path.join(args.model_dir, "feature_columns.json"), "w") as fp:
        json.dump(feature_list, fp)


def model_fn(model_dir):
    """Deserialized and return fitted model"""

    # Load our XGBoost model from the model directory
    model_path = os.path.join(model_dir, "xgb_model.json")
    with open(model_path, "r") as f:
        model_json = json.load(f)
    saved_model_type = json.loads(model_json.get('learner').get('attributes').get('scikit_learn')).get('_estimator_type')
    if saved_model_type == "classifier":
        model = xgb.XGBClassifier()
    elif saved_model_type == "regressor":
        model = xgb.XGBRegressor()
    else:
        msg = f"Model type ({saved_model_type}) not recognized. Expected 'classifier' or 'regressor'"
        raise ValueError(msg)

    model.load_model(model_path)
    return model


def input_fn(input_data, content_type):
    """We only take CSV Input"""
    if content_type == "text/csv":
        # Read the input buffer as a CSV file.
        input_df = pd.read_csv(StringIO(input_data))
        return input_df
    else:
        raise ValueError(f"{content_type} not supported by script!")


def output_fn(output_df, accept_type):
    """We only give CSV Output"""
    if accept_type == "text/csv":
        return output_df.to_csv(index=False), "text/csv"  # Return a CSV String and the content type
    else:
        raise RuntimeError(
            f"{accept_type} accept type is not supported by this script."
        )


def predict_fn(df, model) -> pd.DataFrame:
    """Make Predictions with our XGB Model

    Args:
        df (pd.DataFrame): The input DataFrame
        model: The model use for predictions

    Returns:
        pd.DataFrame: The DataFrame with the predictions added
    """

    # Grab our feature columns (from training)
    model_dir = os.environ["SM_MODEL_DIR"]
    with open(os.path.join(model_dir, "feature_columns.json")) as fp:
        model_features = json.load(fp)
    print(f"Model Features: {model_features}")

    # Load our Label Encoder if we have one
    label_encoder = None
    if os.path.exists(os.path.join(model_dir, "label_encoder.joblib")):
        label_encoder = joblib.load(os.path.join(model_dir, "label_encoder.joblib"))

    # We're going match features in a case-insensitive manner, accounting for all the permutations
    # - Model has a feature list that's any case ("Id", "taCos", "cOunT", "likes_tacos")
    # - Incoming data has columns that are mixed case ("ID", "Tacos", "Count", "Likes_Tacos")
    matched_df = match_features_case_insensitive(df, model_features)

    # Predict the features against our XGB Model
    predictions = model.predict(matched_df[model_features])

    # If we have a label encoder, decode the predictions
    if label_encoder:
        predictions = label_encoder.inverse_transform(predictions)

    # Set the predictions on the DataFrame
    df["prediction"] = predictions

    # Does our model have a 'predict_proba' method? If so we will call it and add the results to the DataFrame
    if getattr(model, "predict_proba", None):
        probs = model.predict_proba(matched_df[model_features])
        df["pred_proba"] = [p.tolist() for p in probs]

        # Expand the pred_proba column into separate columns for each class
        df = expand_proba_column(df, label_encoder.classes_)

    # All done, return the DataFrame with new columns for the predictions
    return df
