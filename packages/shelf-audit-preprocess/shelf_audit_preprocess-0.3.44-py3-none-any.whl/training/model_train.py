import argparse
import os
import yaml
from ultralytics import YOLO, RTDETR, YOLOWorld
from ultralytics import settings
from ultralytics.utils.callbacks.mlflow import mlflow
from .update_artifacts import update_artifacts

def init_config(config, artefacts=False):
    '''set default config values if config has null value'''
    if artefacts:
        defaults = {
            'args_file': '',
            'ismlflow': '',
            'model_version': '',
            'update_best_artifacts': '',
            'track_uri': '',
            'test_run': '',
            'metrics_log': '',
        }
    else:
        defaults = {
            'model_name': '',
            'metrics_parameter': '',
            'artifact_path': '',
            'ios_artifact_upload_folder_path': '',
            'android_artifact_upload_folder_path': '',
            'container_name': '',
            'azure_storage_connection_string': '',
        }

    return tuple(config.get(key, default) for key, default in defaults.items())

def main(configs, artifacts_configs):
    '''
    args -- contains all the arguments for training a detection model
    that are passed using cli
    '''

    config_values = init_config(configs)
    artifacts_configs = init_config(artifacts_configs)
    data_args, ismlflow, model_version, update_best_artifacts, experiment_name, tracking_uri, test_run, metrics = config_values
    ######################### load args from the yaml file ############################################
    with open(data_args, "r") as f:
        data = yaml.full_load(f)

    mlflow_keep_active = "False"
    # update_best_artifacts = args.update_best_artifacts
    ######################## mlflow environment setup ########################################
    if ismlflow.lower() == "true":
        mlflow_keep_active = "true"
        # Update a setting
        settings.update({"mlflow": True})
        if not tracking_uri:
            raise Exception("set tracking_uri value or set environment var:: MLFLOW_TRACKING_URI ")

    print("Experiment name:",experiment_name,'\n',
          "Tracking Uri:",tracking_uri, '\n',
          "name of the test experiment:",test_run, '\n',
          "need to log metric? ",metrics,"\n",
          "data:", data, "\n",
          "is mlflow enalbled ?",ismlflow, "\n",
          "model version:", model_version
          )
    ########################## load the version of the traiing model #############################################
    if "world" in model_version.lower():
        model = YOLOWorld(model_version)
        model.train(**data)
    elif "rtdetr" in model_version.lower():
        model = RTDETR(model_version)
        model.train(**data)
    else:
        model = YOLO(model_version)
        model.train(**data)

    if  mlflow_keep_active == "true":
        run = mlflow.active_run()
        print(f"closing mlflow runid: {run.info.run_id}")
        mlflow.end_run()
        print("closing mlflow....")
        if update_best_artifacts.lower() == "true":
            print("Updating best artifacts : ")
            update_artifacts(experiment_name,model_version,tracking_uri, artifacts_configs)
            print("Best Artifacts updated successfully!")

if __name__ == "__main__":
    pass
