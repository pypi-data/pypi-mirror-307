import mlflow, os, zipfile
from ultralytics import YOLO
from azure.storage.blob import BlobServiceClient


def zip_directory(zip_filename, directory_path):
    zip_filename = os.path.join(os.path.dirname(directory_path), zip_filename)
    with zipfile.ZipFile(zip_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(directory_path):
            for file in files:
                file_path = os.path.join(root, file)
                # Store the file relative to the base directory
                arcname = os.path.relpath(file_path, directory_path)
                zipf.write(file_path, arcname)
    print(f"Directory zipped into {zip_filename}")
    return zip_filename

def change_format_android(config, downloaded_artifact_path):
    try :
        model = YOLO(downloaded_artifact_path)
        model.export(
            format="onnx",
            nms=True,
            agnostic_nms=True,
            half=False,
            int8=False,
            dynamic=False,
            simplify=False,
            opset=12,
            verbose=False
        )
        exported_path = os.path.dirname(downloaded_artifact_path) + config['best_saved_model_path']
        return exported_path
    except Exception as e:
        print(f"Android formatting failed for file : {downloaded_artifact_path} with error : {e}")
        return None

def change_format_ios(config, downloaded_artifact_path):
    try:
        model = YOLO(downloaded_artifact_path)
        model.export(format="coreml",nms=True, imgsz=640)
        exported_path = os.path.dirname(downloaded_artifact_path) + config['best_package_path']
        zipped_file_path = zip_directory(zip_filename=f"{config['best_package_path']}.zip", directory_path=exported_path)
        return zipped_file_path
    except Exception as e:
        print(f"IOS formatting failed for file : {downloaded_artifact_path} with error : {e}")
        return None

def get_valid_runs(client,exp, config) :
    runs = client.search_runs(experiment_ids=[exp.experiment_id], order_by=[f"metrics.{config['MERTICS_PARAMETER']} DESC"])

    valid_runs = [run for run in runs if(len(client.list_artifacts(run.info.run_id, 'evaluation')))]
    print(len(runs)-len(valid_runs))
    return valid_runs

def download_best_artifact(config, client, best_run, downloaded_artifact_path):
    try :
        print(os.getcwd())
        if(not os.path.exists(downloaded_artifact_path)):
            os.makedirs(downloaded_artifact_path)
        print(downloaded_artifact_path, 'downloaded_artifact_path--------')
        downloaded_artifact_path1 = client.download_artifacts(run_id=best_run.info.run_id, path=config['ARTIFACT_PATH1'], dst_path=downloaded_artifact_path)
        downloaded_artifact_path2 = client.download_artifacts(run_id=best_run.info.run_id, path=config['ARTIFACT_PATH2'], dst_path=downloaded_artifact_path)
        if(downloaded_artifact_path1):
            print(f"Artifact successfully downloaded for best run : {best_run.info.run_id} at {downloaded_artifact_path} .")
            return downloaded_artifact_path
        else:
            print(f"Artifact download failed for best run : {best_run.info.run_id}")
            return None
    except Exception as e:
        print(f"Faild to download artifact for run : {best_run.info.run_id} with error : {e}")
        return None

def upload_best_artifact_file(config, local_artifact_file_path, upload_artifact_blob_path):
    try:
        # Create a BlobServiceClient object using the connection string
        blob_service_client = BlobServiceClient.from_connection_string(config['AZURE_STORAGE_CONNECTION_STRING'])

        # Create a ContainerClient object to interact with the specific container
        container_client = blob_service_client.get_container_client(config['CONTAINER_NAME'])

        # Create a BlobClient object to interact with the blob
        blob_client = container_client.get_blob_client(upload_artifact_blob_path)

        # Upload the file
        with open(local_artifact_file_path, "rb") as data:
            blob_client.upload_blob(data, overwrite=True)

        print(f"File '{local_artifact_file_path}' uploaded to blob '{upload_artifact_blob_path}' in container '{config['CONTAINER_NAME']}'.")
    except Exception as e:
        print(f"File '{local_artifact_file_path}' upload failed to blob '{upload_artifact_blob_path}' in container '{config['CONTAINER_NAME']}' with error : {e}.")

def update_artifacts(experiment_name, model_version, tracking_uri, config):
    client = mlflow.MlflowClient(tracking_uri=tracking_uri)
    experiment = client.get_experiment_by_name(experiment_name)
    if experiment is None:
        raise ValueError(f"Experiment with name '{experiment_name}' not found.")
    valid_runs = get_valid_runs(client, experiment, config)
    if(len(valid_runs)):
        best_run = valid_runs[0]
        print(best_run.info.run_id, 'best_run-------------')
        downloaded_artifact_path = os.path.join(os.getcwd(),"artifacts",best_run.info.run_id)
        downloaded_artifact_path = download_best_artifact(config, client=client,best_run=best_run, downloaded_artifact_path=downloaded_artifact_path)

def init_config(config):
    '''set default config values if config has null value'''
    defaults = {
        'experiment_name': '',
        'model_version': '',
        'tracking_uri': '',
    }

    return {key: config.get(key, default) for key, default in defaults.items()}

def main(config):
    config = init_config(config)
    update_artifacts(config['experiment_name'], config['model_version'], config['tracking_uri'], config)

if __name__ == "__main__":
    pass
