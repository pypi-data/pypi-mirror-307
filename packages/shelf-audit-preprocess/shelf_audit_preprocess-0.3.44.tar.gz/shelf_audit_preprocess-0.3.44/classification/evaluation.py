import numpy as np
import pickle
import os
import pandas as pd
import cv2
import mlflow
from transformers import CLIPModel, CLIPProcessor
from .utils import pkl_to_json


# Define the Index and Matches classes
class Index:
    def __init__(self, ndim):
        self.ndim = ndim
        self.vectors = {}

    def add(self, vector_id, vector):
        self.vectors[vector_id] = vector

    def search(self, query_vector, top_k):
        query_vector_norm = query_vector / np.linalg.norm(query_vector)
        similarities = {k: np.dot(query_vector_norm, v / np.linalg.norm(v)) for k, v in self.vectors.items()}
        sorted_similarities = sorted(similarities.items(), key=lambda item: item[1], reverse=True)
        top_matches = sorted_similarities[:top_k]
        return Matches(keys=[k for k, v in top_matches], distances=[v for k, v in top_matches])

class Matches:
    def __init__(self, keys, distances):
        self.keys = keys
        self.distances = distances

def load_vector_db(vector_db_path):
    with open(vector_db_path, 'rb') as file:
        data = pickle.load(file)
    index = Index(ndim=512)
    for vector_id, vector in data.items():
        index.add(vector_id, vector)
    return index

def load_metadata(metadata_path):
    with open(metadata_path, 'rb') as file:
        metadata = pickle.load(file)
    return metadata

def extract_embeddings(image_path, processor, model):
    image = cv2.imread(image_path, cv2.COLOR_BGR2RGB)
    inputs = processor(images=image, return_tensors="pt", padding=True)
    outputs = model.get_image_features(**inputs)
    return outputs.detach().numpy().flatten()

def calculate_mrr(test_images, test_images_path, vector_db_path, metadata_path, processor, model, output_file, top_k=10):
    index = load_vector_db(vector_db_path)
    metadata = load_metadata(metadata_path)
    reciprocal_ranks = []
    results = []

    for test_image in test_images:
        test_upc = extract_upc_from_filename(test_image)
        image_path = os.path.join(test_images_path, test_image)
        test_vector = extract_embeddings(image_path, processor, model)
        matches = index.search(test_vector, top_k)
        item_ids, scores = matches.keys, matches.distances
        retrieved_image_names = [extract_upc_from_filename_metadata(metadata[item_id]) for item_id in item_ids]

        try:
            rank = retrieved_image_names.index(test_upc) + 1
            reciprocal_ranks.append(1 / rank)
        except ValueError:
            rank = None
            reciprocal_ranks.append(0)

        results.append({
            'Query_UPC': test_upc,
            'Rank': rank,
            'Reciprocal_Rank': 1 / rank if rank else 0,
            'Retrieved_UPCs': retrieved_image_names,
            'Scores': scores,
        })

    mrr = np.mean([result['Reciprocal_Rank'] for result in results])
    results_df = pd.DataFrame(results)
    results_df.to_csv(output_file, index=False)
    return mrr, output_file

def extract_upc_from_filename(filename):
    return os.path.splitext(filename)[0]

def extract_upc_from_filename_metadata(filename):
    return filename.split('.')[0]

def init_config(config):
    '''set default config values if config has null value'''
    defaults = {
            'model_name': '',
            'device': '',
            'test_images_path': '',
            'tracking_uri': '',
            'experiment_name': '',
            'run_name': '',
            'vector_db_path': '',
            'metadata_path': '',
            'top_k': '',
            'output_eval_file': '',
            'pkl_to_json_vectors_path': '',
            'pkl_to_json_metadata_path': '',
            'pkl_to_json_output_path': '',
        }

    return {key: config.get(key, default) for key, default in defaults.items()}

def main(config):
    # Load model and processor
    config = init_config(config)
    model = CLIPModel.from_pretrained(config['model_name'])
    processor = CLIPProcessor.from_pretrained(config['model_name'])

    # Set the device
    device = config['device']

    # Test images
    test_images_path = config['test_images_path']
    test_images = os.listdir(test_images_path)

    # Set MLflow tracking URI
    mlflow.set_tracking_uri(config['tracking_uri'])

    # Set MLflow experiment name
    mlflow.set_experiment(config['experiment_name'])

    # Start MLflow run with the specified experiment name
    with mlflow.start_run(run_name=config['run_name']):
        # Log config file
        # mlflow.log_artifact(config_path, artifact_path="config")

        # Calculate MRR and get the evaluation file path
        mrr, eval_file_path = calculate_mrr(
            test_images,
            test_images_path,
            config['vector_db_path'],
            config['metadata_path'],
            processor,
            model,
            config['output_eval_file'],
            top_k=config['top_k']
        )

        print(f"MRR: {mrr}")

        # Log MRR to MLflow
        mlflow.log_metric("MRR", mrr)
        # mlflow.log_metric("MRR", 20)

        # Log evaluation file
        mlflow.log_artifact(eval_file_path, artifact_path="evaluation")
        mlflow.log_artifact(config['vector_db_path'], artifact_path="evaluation")
        mlflow.log_artifact(config['metadata_path'], artifact_path="evaluation")

        vectors_path = config['pkl_to_json_vectors_path'] # Path to your vector pickle file
        metadata_path = config['pkl_to_json_metadata_path'] # Path to your metadata pickle file
        output_json_path = config['pkl_to_json_output_path']  # Path to save the JSON file

        pkl_to_json(vectors_path, metadata_path, output_json_path)

        mlflow.log_artifact(output_json_path, artifact_path="evaluation")

if __name__ == '__main__':
    pass
