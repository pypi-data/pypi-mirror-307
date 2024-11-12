import os
import yaml
import pickle
from PIL import Image
from transformers import CLIPModel, CLIPProcessor
from concurrent.futures import ThreadPoolExecutor
import usearch
from usearch.index import Index
import mlflow
from utils import load_config, pkl_to_json


class VectorizeImage:
    vector_id = 0
    vector_storage = {}
    metadata_storage = {}
    def __init__(self, config):
        self.config = config
        self.index = Index(ndim=512)
        self.model = CLIPModel.from_pretrained(self.config['model_name'])
        self.processor = CLIPProcessor.from_pretrained(self.config['model_name'])
        

    def extract_clip_vector(self, image_path):
        image = Image.open(image_path).convert("RGB")
        inputs = self.processor(images=image, return_tensors="pt", padding=True)
        outputs = self.model.get_image_features(**inputs)
        return outputs.detach().numpy().flatten()

    def upload_image_vector(self, image_path):
        try:
            vector = self.extract_clip_vector(image_path)
            VectorizeImage.vector_id = VectorizeImage.vector_id+1
            vector_id = VectorizeImage.vector_id
            VectorizeImage.vector_storage[vector_id] = vector
            VectorizeImage.metadata_storage[vector_id] = os.path.basename(image_path)
            self.index.add(vector_id, vector)
            print(f"Uploaded: {image_path}")
        except Exception as e:
            print(f"Failed to upload {image_path}: {e}")

    def process_folder(self, folder_path):
        if not os.path.exists(folder_path) or len(os.listdir(folder_path)) == 0:
            print("No images available in", folder_path)
            return
        
        # Walk through the directory recursively
        for root, dirs, files in os.walk(folder_path):
            image_paths = [os.path.join(root, f) for f in files if f.lower().endswith(('.png', '.jpg', '.jpeg'))]

            print(f"Processing folder: {root}")
            image_paths = image_paths[:5000]
            if not image_paths:
                print(f"No images found in folder: {root}")
                continue

            with ThreadPoolExecutor(max_workers=self.config['max_workers']) as executor:
                executor.map(self.upload_image_vector, image_paths)

    def save_data(self):
        
        with open(self.config['vectors_path'], 'wb') as f:
            pickle.dump(VectorizeImage.vector_storage, f)
        with open(self.config['metadata_path'], 'wb') as f:
            pickle.dump(VectorizeImage.metadata_storage, f)
        print(f"Stored image vectors and metadata in {self.config['vectors_path']} and {self.config['metadata_path']}")

    def run(self, folder_path):
        self.process_folder(folder_path)
        self.save_data()

def init_config(config):
    '''set default config values if config has null value'''
    defaults = {
        'tracking_url': '',
        'vectorization_run_name': '',
        'max_workers': '',
        'pangea_recursive_path': '',
        'pkl_to_json_vectors_path': '',
        'pkl_to_json_metadata_path': '',
        'pkl_to_json_output_path': '',
        'artifact_path': '',
        'webscraping_save_path': '',
        'inhouse_labeling_save_path': '',
        'model_name': '',
        'vectors_path': '',
        'metadata_path': '',
    }

    return {key: config.get(key, default) for key, default in defaults.items()}

def main(config):
    config = init_config(config)
    mlflow.set_tracking_uri(config['tracking_url'])
    # Set MLflow experiment name
    mlflow.set_experiment("Data Processing and Vectorization")

    # Start MLflow run
    with mlflow.start_run(run_name=config['vectorization_run_name']):
        # Logging the config file as an artifact
        # mlflow.log_artifact("config.yaml", artifact_path="config")
        mlflow.log_param("No of workers", config['max_workers'])
        mlflow.log_param("Image path", config['pangea_recursive_path'])

        vec = VectorizeImage(config)

        # Running vectorization on different datasets and logging their completion
        vec.run(config['pangea_recursive_path'])
        mlflow.log_param("Pangea Vectorization Completed", True)

        vectors_path = config['pkl_to_json_vectors_path'] # Path to your vector pickle file
        metadata_path = config['pkl_to_json_metadata_path'] # Path to your metadata pickle file
        output_json_path = config['pkl_to_json_output_path']  # Path to save the JSON file

        pkl_to_json(vectors_path, metadata_path, output_json_path)

        mlflow.log_artifact(output_json_path, artifact_path=config['artifact_path'])

if __name__ == "__main__":
    pass
