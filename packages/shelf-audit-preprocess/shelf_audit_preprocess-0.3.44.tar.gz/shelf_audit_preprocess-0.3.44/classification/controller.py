import mlflow
import yaml
from vectorize_images import VectorizeImage
import azure_setup
import os
from utils import load_config, pkl_to_json


def main(config):
    mlflow.set_tracking_uri(config["tracking_url"])
    # Set MLflow experiment name
    mlflow.set_experiment("Data Processing and Vectorization")

    # Start MLflow run
    with mlflow.start_run(run_name="Vectorization Process"):
        # Logging the config file as an artifact
        mlflow.log_artifact("config.yaml", artifact_path="config")
        mlflow.log_param("No of workers", config['vectorize']['max_workers'])
        mlflow.log_param("Image path", config['pangea']['data']['recursive_path'])

        vec = VectorizeImage(config)

        # Running vectorization on different datasets and logging their completion
        vec.run(config['pangea']['data']['recursive_path'])
        mlflow.log_param("Pangea Vectorization Completed", True)

        # vec.run(config['webscraping']['save_path'])
        # mlflow.log_param("WebScraping Vectorization Completed", True)

        # vec.run(config['inhouse_labeling']['save_path'])
        # mlflow.log_param("In-House Labeling Vectorization Completed", True)

        vectors_path = config['pkl_to_json']['vectors_path'] # Path to your vector pickle file
        metadata_path = config['pkl_to_json']['metadata_path'] # Path to your metadata pickle file
        output_json_path = config['pkl_to_json']['output_json_path']  # Path to save the JSON file

        pkl_to_json(vectors_path, metadata_path, output_json_path)

        mlflow.log_artifact(output_json_path, artifact_path="global_json")


if __name__ == "__main__":
    pass
