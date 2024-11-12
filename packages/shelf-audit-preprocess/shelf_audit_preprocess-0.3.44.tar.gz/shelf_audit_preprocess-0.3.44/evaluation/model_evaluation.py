from .evaluaion_metrics_yolo import generate_metrics_dataframe
from .final_code_collection_json import generate_metadata
import pandas as pd


def init_config(config):
    '''set default values if config has null value'''
    defaults = {
        'base_path': '',
        'metadata_json': '',
    }

    return tuple(config.get(key, default) for key, default in defaults.items())

def main(configs):
    '''main func'''
    base_path, metadata_json = init_config(configs)
    pd.set_option("display.max_columns", 200)
    df_metrics = generate_metrics_dataframe(base_path,[0.5,0.6,0.8],True)
    df_metadata = generate_metadata(metadata_json,True)
    pd.merge(df_metrics,df_metadata,on="merge_key")

if __name__ == '__main__':
    pass
