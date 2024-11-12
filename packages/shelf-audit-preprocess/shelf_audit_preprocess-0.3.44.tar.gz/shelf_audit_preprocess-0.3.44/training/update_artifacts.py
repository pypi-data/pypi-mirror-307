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

def change_format_android(downloaded_artifact_path):
    try :
        model = YOLO(downloaded_artifact_path)
        model.export(
            format="tflite",
            nms=True,
            agnostic_nms=True,
            half=False,
            int8=False,
            dynamic=False,
            simplify=False,
            opset=12,
            verbose=False
        )
        exported_path = os.path.dirname(downloaded_artifact_path) + f"/best_saved_model/best_float32.tflite"
        return exported_path
    except Exception as e:
        print(f"Android formatting failed for file : {downloaded_artifact_path} with error : {e}")
        return None

def change_format_ios(downloaded_artifact_path):
    try:
        model = YOLO(downloaded_artifact_path)
        model.export(format="coreml",nms=True, imgsz=640)
        exported_path = os.path.dirname(downloaded_artifact_path) + "/best.mlpackage"
        zipped_file_path = zip_directory(zip_filename="best.mlpackage.zip", directory_path=exported_path)
        return zipped_file_path
    except Exception as e:
        print(f"IOS formatting failed for file : {downloaded_artifact_path} with error : {e}")
        return None

def get_valid_runs(client,exp, config) :
    runs = client.search_runs(experiment_ids=[exp.experiment_id], order_by=[f"metrics.{config['metrics_parameter']} DESC"])
    valid_runs = [run for run in runs if(len(client.list_artifacts(run.info.run_id, 'weights')))]
    print(len(runs)-len(valid_runs))
    return valid_runs

def download_best_artifact(config, client, best_run, downloaded_artifact_path):
    try :
        print(os.getcwd())
        if(not os.path.exists(downloaded_artifact_path)):
            os.makedirs(downloaded_artifact_path)
        downloaded_artifact_path = client.download_artifacts(run_id=best_run.info.run_id, path=config['artifact_path'], dst_path=downloaded_artifact_path)
        if(downloaded_artifact_path):
            print(f"Artifact successfully downloaded for best run : {best_run.info.run_id} at {downloaded_artifact_path} .")
            return downloaded_artifact_path
        else:
            print(f"Artifact download failed for best run : {best_run.info.run_id}")
            return None
    except Exception as e:
        print(f"Faild to download artifact for run : {best_run.info.run_id} with error : {e}")
        return None

def upload_best_artifact_file(local_artifact_file_path, upload_artifact_blob_path, config):
    try:
        # Create a BlobServiceClient object using the connection string
        blob_service_client = BlobServiceClient.from_connection_string(config['azure_storage_connection_string'])

        # Create a ContainerClient object to interact with the specific container
        container_client = blob_service_client.get_container_client(config['container_name'])

        # Create a BlobClient object to interact with the blob
        blob_client = container_client.get_blob_client(upload_artifact_blob_path)

        # Upload the file
        with open(local_artifact_file_path, "rb") as data:
            blob_client.upload_blob(data, overwrite=True)

        print(f"File '{local_artifact_file_path}' uploaded to blob '{upload_artifact_blob_path}' in container '{config['container_name']}'.")
    except Exception as e:
        print(f"File '{local_artifact_file_path}' upload failed to blob '{upload_artifact_blob_path}' in container '{config['container_name']}' with error : {e}.")
    
def update_artifacts(experiment_name,model_version,tracking_uri, config):
    client = mlflow.MlflowClient(tracking_uri=tracking_uri)
    experiment = client.get_experiment_by_name(experiment_name)
    if experiment is None:
        raise ValueError(f"Experiment with name '{experiment_name}' not found.")
    valid_runs = get_valid_runs(client,experiment, config)
    if(len(valid_runs)):
        best_run = valid_runs[0]
        print(best_run.info.run_id)
        downloaded_artifact_path = os.path.join(os.getcwd(),"artifacts",best_run.info.run_id)
        downloaded_artifact_path = download_best_artifact(config, client=client,best_run=best_run, downloaded_artifact_path=downloaded_artifact_path)
        if(downloaded_artifact_path):
            ios_artifact_path = change_format_ios(downloaded_artifact_path)
            android_artifact_path = change_format_android(downloaded_artifact_path)
            if(ios_artifact_path):
                ios_upload_file_path = config['ios_artifact_upload_folder_path'] + f"{config['model_name']}_{model_version}_best.mlpackage.zip"
                upload_best_artifact_file(ios_artifact_path, ios_upload_file_path, config)
            if(android_artifact_path):
                android_upload_file_path = config['android_artifact_upload_folder_path'] + f"{config['model_name']}_best_{model_version}_float32.tflite"
                upload_best_artifact_file(android_artifact_path, android_upload_file_path, config)
    else:
        print("No valid run found!")
    

if __name__ == "__main__":
    pass
