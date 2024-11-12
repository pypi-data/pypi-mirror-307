import os
import random
import glob


def init_config(config):
    defaults = {
            'image_dir': '',
            'train_txt': '',
            'val_txt': '',
            'test_txt': '',
            'train_data_size': 0.8,
        }

    return tuple(config.get(key, default) for key, default in defaults.items())

def main(configs):
    image_dir, train_txt, val_txt, test_txt, train_data_size = init_config(configs)

    image_files = glob.glob(os.path.join(image_dir, '*.*'))

    random.shuffle(image_files)

    split_idx = int(train_data_size * len(image_files))
    train_files = image_files[:split_idx]
    val_test_files = image_files[split_idx:]

    with open(train_txt, 'w') as f:
        for file in train_files:
            f.write(f'{file}\n')

    with open(val_txt, 'w') as f:
        for file in val_test_files:
            f.write(f'{file}\n')

    with open(test_txt, 'w') as f:
        for file in val_test_files:
            f.write(f'{file}\n')
            
    print(f'Split {len(image_files)} images into {len(train_files)} train, {len(val_test_files)} val, and {len(val_test_files)} test.')

if __name__ == '__main__':
    pass
