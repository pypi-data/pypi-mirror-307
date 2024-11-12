import pickle
import json


def pkl_to_json(vectors_path, metadata_path, output_json_path):
    # Load vector and metadata storage from pickle files
    with open(vectors_path, 'rb') as f:
        vector_storage = pickle.load(f)
        
    with open(metadata_path, 'rb') as f:
        metadata_storage = pickle.load(f)
    
    # Create the desired JSON structure
    data = []
    for vector_id, vector in vector_storage.items():
        entry = {
            "id": str(vector_id),
            "name": metadata_storage[vector_id],
            "vector": vector.tolist()  # Convert numpy array to list for JSON serialization
        }
        data.append(entry)
    
    # Create the final JSON structure
    json_structure = {
        "total": len(data),
        "data": data
    }
    
    # Save the JSON structure to a file
    with open(output_json_path, 'w') as json_file:
        json.dump(json_structure, json_file, indent=2)
    
    print(f"Conversion complete! JSON saved to {output_json_path}")

if __name__ == "__main__":
    pass
