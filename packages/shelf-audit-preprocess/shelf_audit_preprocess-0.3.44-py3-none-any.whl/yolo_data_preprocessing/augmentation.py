import os 
import json 
import cv2 
import albumentations as A
import matplotlib.pyplot as plt 
import albumentations.augmentations.transforms as transforms
from albumentations.core.transforms_interface import ImageOnlyTransform
import numpy as np
import random
from tqdm import tqdm 
#### src path ###

"""
augs planned to implement 
1. gauss blur --done
2. zoom_crop  -- done 
4. emboss --done
5. sharpen  transforms
6. lazy_pixelate --done
7. multiply -- done
8. flip_lr - done
9. permute_channel -- done
10. coarse_dropout -- done
11. random_scale -- done
12. jpeg_compression -- done
13. gray scale -- done
14. motion blur --done
15. PixelDropout inside transforms -- done 
16. Shear -- done  

"""

def save_img_annot_pair(aug_imgs_path,aug_labels_path,aug_image,aug_bboxes,filename_without_ext,prob, aug_name):
    cv2.imwrite(os.path.join(aug_imgs_path, os.path.basename(filename_without_ext) +"_" + f"{aug_name}" + "_"+ f"{prob}" + ".jpg"), aug_image)
    with open(os.path.join(aug_labels_path, os.path.basename(filename_without_ext) +"_" + f"{aug_name}" + "_"+ f"{prob}" + ".txt"),"w") as f:
            
        for bbox in aug_bboxes:
            xc, yc, w, h, class_id = bbox
            f.write(f"{class_id} {xc} {yc} {w} {h}\n")


def gauss_blur(image,bboxes,kernel_size:int,blur_limit:tuple, prob: float, aug_imgs_path, aug_labels_path, filename_without_ext, aug_name):
    try:
        aug = A.Compose([
            A.GaussianBlur(blur_limit =blur_limit,sigma_limit=(0.1, 2.0),kernel_size= (kernel_size, kernel_size), p = prob)], 
            bbox_params = A.BboxParams(format= "yolo", label_fields=["class_labels"])
        )
        aug = aug(image = image, bboxes = bboxes, class_labels=['object']*len(bboxes))

        aug_image = aug["image"]
        aug_bboxes = aug["bboxes"]
        
        save_img_annot_pair(aug_imgs_path,aug_labels_path,aug_image,aug_bboxes,filename_without_ext,prob, aug_name="gauss_blur")
    except Exception as e: 
        print(e)


def shear(image, bboxes,shear:tuple, prob:float,aug_imgs_path,aug_labels_path,filename_without_ext, aug_name="shear"):
    try:
        aug = A.Compose([
        A.Affine(shear=shear, p=prob),
        ], bbox_params=A.BboxParams(format='yolo', label_fields=['class_labels']))

        aug = aug(image = image, bboxes = bboxes, class_labels=['object']*len(bboxes))

        aug_image = aug["image"]
        aug_bboxes = aug["bboxes"]

        save_img_annot_pair(aug_imgs_path,aug_labels_path,aug_image,aug_bboxes,filename_without_ext,prob, aug_name="shear")
    except Exception as e: 
        print(e)

class LimitObjects(A.DualTransform):
    def __init__(self, max_objects, always_apply=False, p=1.0):
        super().__init__(always_apply, p)
        self.max_objects = max_objects

    def apply(self, image, **params):
        return image

    def apply_to_bbox(self, bbox, **params):
        return bbox

    def get_params_dependent_on_targets(self, params):
        return {}

    def get_transform_init_args_names(self):
        return ('max_objects',)

    def __call__(self, **kwargs):
        image = kwargs['image']
        bboxes = kwargs['bboxes']
        class_labels = kwargs['class_labels']

        if random.random() < self.p:
            if len(bboxes) > self.max_objects:
                selected_indices = random.sample(range(len(bboxes)), self.max_objects)
                selected_bboxes = [bboxes[i] for i in selected_indices]
                

                # Calculate the bounding box that contains all selected bboxes
                x_min = min([bbox[0] for bbox in selected_bboxes])
                y_min = min([bbox[1] for bbox in selected_bboxes])
                x_max = max([bbox[2] for bbox in selected_bboxes])
                y_max = max([bbox[3] for bbox in selected_bboxes])
                print(image.shape)

                x_min, y_min, x_max, y_max = int(x_min), int(y_min), int(x_max), int(y_max)
                crop_width = x_max - x_min
                crop_height = y_max - y_min

                # Check if the crop dimensions are valid
                if crop_width <= 0 or crop_height <= 0:
                    return {
                        'image': image,
                        'bboxes': bboxes,
                        'class_labels': class_labels
                    }

                # Crop the image to the bounding box containing all selected objects
                image = image[y_min:y_max, x_min:x_max]
                new_bboxes = [[bbox[0] - x_min, bbox[1] - y_min, bbox[2] - x_min, bbox[3] - y_min] for bbox in selected_bboxes]
                class_labels = [class_labels[i] for i in selected_indices]
                return {
                    'image': image,
                    'bboxes': new_bboxes,
                    'class_labels': class_labels
                }

        return {
            'image': image,
            'bboxes': bboxes,
            'class_labels': class_labels
        }
def limit_objects(img, bboxes, img_path, aug_imgs_path, aug_labels_path, max_objects = 20, prob=1.0):

    aug = A.Compose([
        LimitObjects(max_objects=20, p=1.0) 
    ], bbox_params=A.BboxParams(format='yolo', label_fields=['class_labels']))

    image = cv2.imread(img_path)
    aug = aug(image = image, bboxes = bboxes, class_labels=['object']*len(bboxes))

    aug_image = aug["image"]
    aug_bboxes = aug["bboxes"]
    filename = os.path.basename(img_path)
    filename_without_ext = os.path.splitext(filename)[0]
    print(os.path.join(aug_imgs_path, os.path.basename(filename_without_ext) +"_lo_"+ f"{max_objects}" +"_"+ f"{prob}" + ".jpg"))
    cv2.imwrite(os.path.join(aug_imgs_path, os.path.basename(filename_without_ext) +"_lo_" + f"{max_objects}" +"_"+ f"{prob}" + ".jpg"), aug_image)
    with open(os.path.join(aug_labels_path, os.path.basename(filename_without_ext)+"_lo_"+ f"{max_objects}" +"_"+ f"{prob}" + ".txt"),"w") as f:
         
        for bbox in aug_bboxes:
            xc, yc, w, h, class_id = bbox
            f.write(f"{class_id} {xc} {yc} {w} {h}\n")

def zoom_crop(image,img_w, img_h, bboxes,erosion_rate:float, prob:float,aug_imgs_path,aug_labels_path,filename_without_ext, aug_name="zomm_crop"):
    try:
        aug =  A.Compose([
        A.RandomSizedBBoxSafeCrop (height=img_h, width=img_w, erosion_rate=erosion_rate, interpolation=1, p=prob)
    ], bbox_params=A.BboxParams(format='yolo', label_fields=['class_labels']))

        aug = aug(image = image, bboxes = bboxes, class_labels=['object']*len(bboxes))

        aug_image = aug["image"]
        aug_bboxes = aug["bboxes"]
        save_img_annot_pair(aug_imgs_path,aug_labels_path,aug_image,aug_bboxes,filename_without_ext,prob, aug_name="zoom_crop")
    except Exception as e: 
        print(e)



class PixelDropout(A.DualTransform):
    def __init__(self, dropout_prob=0.05, always_apply=False, p=1.0):
        super().__init__(always_apply, p)
        self.dropout_prob = dropout_prob

    def apply(self, image, **params):
        mask = np.random.binomial(1, self.dropout_prob, size=image.shape[:2])
        mask = np.repeat(mask[:, :, np.newaxis], 3, axis=2)
        image = image * (1 - mask)
        return image

    def apply_to_bbox(self, bbox, **params):
        return bbox

    def get_transform_init_args_names(self):
        return ('dropout_prob',)

def pixel_dropout(image, bboxes, dropout_prob:float, prob:float,aug_imgs_path,aug_labels_path,filename_without_ext, aug_name="pixel_dropout"):
    try:
        aug = A.Compose([
            PixelDropout(dropout_prob=dropout_prob, p=prob)  
        ], bbox_params=A.BboxParams(format='yolo', label_fields=['class_labels']))
        aug = aug(image = image, bboxes = bboxes, class_labels=['object']*len(bboxes))

        aug_image = aug["image"]
        aug_bboxes = aug["bboxes"]
        save_img_annot_pair(aug_imgs_path,aug_labels_path,aug_image,aug_bboxes,filename_without_ext,prob, aug_name="pixel_dropout")
    except Exception as e: 
        print(e)

def emboss(image, bboxes, alpha:float, strength:float,prob:float,aug_imgs_path,aug_labels_path,filename_without_ext, aug_name="emboss"):
    try:
        aug = A.Compose([A.Emboss(alpha=alpha, strength=strength, p=prob), 
                        ], bbox_params=A.BboxParams(format='yolo', label_fields=['class_labels']))

        aug = aug(image = image, bboxes = bboxes, class_labels=['object']*len(bboxes))

        aug_image = aug["image"]
        aug_bboxes = aug["bboxes"]
        
        save_img_annot_pair(aug_imgs_path,aug_labels_path,aug_image,aug_bboxes,filename_without_ext,prob, aug_name="emboss")
    except Exception as e: 
        print(e)     

def sharpen(image, bboxes,alpha:tuple, lightness:tuple,prob:float,aug_imgs_path, aug_labels_path, filename_without_ext,aug_name="sharpen"):
    try:
        aug = A.Compose([
            A.Sharpen(alpha=(0.2, 0.5), lightness=(0.5, 1.0), p=1.0),
        ], bbox_params=A.BboxParams(format='yolo', label_fields=['class_labels']))

        aug = aug(image = image, bboxes = bboxes, class_labels=[0]*len(bboxes))

        aug_image = aug["image"]
        aug_bboxes = aug["bboxes"]
        
        category_ids = [0]*len(bboxes)
        valid_bboxes = []
        valid_category_ids = []
        
        for bbox, category_id in zip(aug_bboxes, category_ids):
            x_min, y_min, x_max, y_max, class_id = bbox
            if x_max > x_min and y_max > y_min:
                valid_bboxes.append(bbox)
                valid_category_ids.append(category_id)

        save_img_annot_pair(aug_imgs_path,aug_labels_path,aug_image,valid_bboxes,filename_without_ext,prob, aug_name="sharpen")
    except Exception as e: 
        print(e)

class LazyPixelate(ImageOnlyTransform):
    def __init__(self, ratio=(0.05, 0.1), always_apply=False, p=0.5):
        super(LazyPixelate, self).__init__(always_apply, p)
        self.ratio = ratio if isinstance(ratio, tuple) else (ratio, ratio)

    def apply(self, img, **params):
        ratio = np.random.uniform(self.ratio[0], self.ratio[1])
        h, w = img.shape[:2]
        new_h, new_w = int(h * ratio), int(w * ratio)

        # Resize down
        small = cv2.resize(img, (new_w, new_h), interpolation=cv2.INTER_LINEAR)

        # Resize up
        pixelated = cv2.resize(small, (w, h), interpolation=cv2.INTER_NEAREST)

        return pixelated

# Define the custom LazyPixelate augmentation
def lazy_pixelate(img, bboxes,ratio:tuple, prob:float,aug_imgs_path,aug_labels_path,filename_without_ext, aug_name="lazy_pixelate"):
    try:
        aug = A.Compose([
            LazyPixelate(ratio=ratio, p=prob)
        ])

        augmented = aug(image=img)
        aug_image = augmented['image']
        aug_bboxes = bboxes
        save_img_annot_pair(aug_imgs_path,aug_labels_path,aug_image,aug_bboxes,filename_without_ext,prob, aug_name="lazy_pixelate")
    except Exception as e: 
        print(e)

def multiply(image, bboxes,multiplier:tuple,prob:float,aug_imgs_path,aug_labels_path,filename_without_ext, aug_name="multiply"):
    try:
        aug = A.Compose([
            transforms.MultiplicativeNoise(multiplier=multiplier, p=prob)
        ], bbox_params=A.BboxParams(format='yolo', label_fields=['class_labels']))
        aug = aug(image = image, bboxes = bboxes, class_labels=['object']*len(bboxes))

        aug_image = aug["image"]
        aug_bboxes = aug["bboxes"]
        save_img_annot_pair(aug_imgs_path,aug_labels_path,aug_image,aug_bboxes,filename_without_ext,prob, aug_name="multiply")
    except Exception as e: 
        print(e)

def coarse_dropout(image, bboxes,max_holes:int, prob:float,aug_imgs_path,aug_labels_path,filename_without_ext, aug_name="coarse_dropout"):
    try:
        aug = A.Compose([
            A.CoarseDropout(max_holes = max_holes, max_height =24, max_width= 24, min_holes =8, 
            min_height=1, min_width=4,fill_value=0, p = prob)
        ])

        aug = aug(image = image)
        aug_image = aug["image"]
        aug_bboxes = bboxes
        save_img_annot_pair(aug_imgs_path,aug_labels_path,aug_image,aug_bboxes,filename_without_ext,prob, aug_name="coarse_dropout")
    except Exception as e: 
        print(e)

def flip_lr(image, bboxes, prob:float,aug_imgs_path,aug_labels_path,filename_without_ext, aug_name="flip_lr"):
    try:
        aug = A.Compose([
            A.HorizontalFlip(p=prob)],
            bbox_params=A.BboxParams(format='yolo', label_fields=['class_labels']))

        aug = aug(image = image, bboxes = bboxes, class_labels=['object']*len(bboxes))
        aug_image = aug["image"]
        aug_bboxes = aug["bboxes"]
        save_img_annot_pair(aug_imgs_path,aug_labels_path,aug_image,aug_bboxes,filename_without_ext,prob, aug_name="flip_lr")
    except Exception as e: 
        print(e)
    

# Define the PermuteChannels augmentation
class PermuteChannels(A.ImageOnlyTransform):
    def __init__(self, always_apply=False, p=0.5):
        super(PermuteChannels, self).__init__(always_apply, p)

    def apply(self, img, **params):
        return img[..., [2, 1, 0]]  # Swap R and B channels


def permute_channel(image, bboxes, prob:float,aug_imgs_path,aug_labels_path,filename_without_ext, aug_name="permute_channel"):
    try:
        aug = A.Compose([
        PermuteChannels(p=prob),], 
        bbox_params=A.BboxParams(format='yolo', label_fields=['class_labels']))

        aug = aug(image = image, bboxes = bboxes, class_labels=['object']*len(bboxes))

        aug_image = aug["image"]
        aug_bboxes = aug["bboxes"]
        save_img_annot_pair(aug_imgs_path,aug_labels_path,aug_image,aug_bboxes,filename_without_ext,prob, aug_name="permute_channel")
    except Exception as e: 
        print(e)

def motion_blur(image,bboxes, blur_limit:tuple,prob:float,aug_imgs_path,aug_labels_path,filename_without_ext, aug_name="motion_blur"):
    try:
        aug= A.Compose([
            A.MotionBlur(blur_limit=blur_limit, allow_shifted=True, p=prob)
        ], bbox_params=A.BboxParams(format='yolo', label_fields=['class_labels']))

        aug = aug(image = image, bboxes = bboxes, class_labels=['object']*len(bboxes))

        aug_image = aug["image"]
        aug_bboxes = aug["bboxes"]
        save_img_annot_pair(aug_imgs_path,aug_labels_path,aug_image,aug_bboxes,filename_without_ext,prob, aug_name="motion_blur")
    except Exception as e: 
        print(e)

def gray_scale(image, bboxes, prob:float,aug_imgs_path,aug_labels_path,filename_without_ext, aug_name="gray_scale"):
    try:
        aug = A.Compose([
            A.ToGray(p= prob)
        ])
        aug = aug(image = image)

        aug_image = aug["image"]
        aug_bboxes = bboxes
        save_img_annot_pair(aug_imgs_path,aug_labels_path,aug_image,aug_bboxes,filename_without_ext,prob, aug_name="gray_scale")
    except Exception as e: 
        print(e)

def jpeg_compression(image, bboxes, quality_lower:int, quality_upper:int, prob:float,aug_imgs_path,aug_labels_path,filename_without_ext, aug_name="jpeg_comp"):
    try:
        aug = A.Compose([
        A.ImageCompression(quality_lower=quality_lower, quality_upper=quality_upper, p=prob)],
        bbox_params=A.BboxParams(format='yolo', label_fields=['class_labels']))

        aug = aug(image = image, bboxes = bboxes, class_labels=['object']*len(bboxes))

        aug_image = aug["image"]
        aug_bboxes = aug["bboxes"]
        save_img_annot_pair(aug_imgs_path,aug_labels_path,aug_image,aug_bboxes,filename_without_ext,prob, aug_name="jpeg_comp")
    except Exception as e: 
        print(e)

def random_scale(image, bboxes,scale_limit:tuple, prob:float,aug_imgs_path,aug_labels_path,filename_without_ext, aug_name="random_scale"):
    try:
        aug = A.Compose([
        A.RandomScale(scale_limit=scale_limit, p=prob)],
        bbox_params=A.BboxParams(format='yolo', label_fields=['class_labels']))

        aug = aug(image = image, bboxes = bboxes, class_labels=['object']*len(bboxes))

        aug_image = aug["image"]
        aug_bboxes = aug["bboxes"]
        save_img_annot_pair(aug_imgs_path,aug_labels_path,aug_image,aug_bboxes,filename_without_ext,prob, aug_name="random_scale")
    except Exception as e:
        print(e)
   

def load_image_annot_pair(img_path,annot_path,imgs_path, labels_path):
    bboxes = []
    print(img_path, annot_path)
    print(os.path.basename(img_path)[0])


def init_config(config):
    '''set default values if config has null value'''
    defaults = {
        'root': '',
        'kernel_size': 3,
        'prob': 0.5,
        'erosion_rate': 0.45,
        'dropout_prob': 0.2,
        'alpha': 0.25,
        'strength': 0.5,
        'max_holes': 16,
        'gray_scale_prob': 1.0,
        'quality_lower': 30,
        'quality_upper': 100
    }
    
    return tuple(config.get(key, default) for key, default in defaults.items())


def main(configs):
    config_values = init_config(configs)
    root, kernel_size, prob, erosion_rate, dropout_prob, alpha, strength, max_holes, gray_scale_prob, quality_lower, quality_upper = config_values

    imgs_path = os.path.join(root, "images")
    print(imgs_path)
    labels_path = os.path.join(root, "labels")
    aug_imgs_path = os.path.join(root, "aug_images")
    aug_labels_path = os.path.join(root, "aug_labels")

    if not os.path.exists(aug_imgs_path):
        os.makedirs(aug_imgs_path)

    if not os.path.exists(aug_labels_path):
        os.makedirs(aug_labels_path)

    print(aug_imgs_path, aug_labels_path)

    for image in tqdm(os.listdir(imgs_path)):
        annot_path = os.path.join(labels_path, os.path.splitext(image)[0]) + ".txt"
        img_path = os.path.join(imgs_path, image)
        bboxes = []
        img_name_without_ext = os.path.splitext(image)[0]
        with open(annot_path, "r") as f:
            for line in f:
                values = line.strip().split()
                if len(values) != 5:
                    raise ValueError(f"Invalid annotation format: {line}")
                class_id = int(values[0])
                x_center = abs(float(values[1]))
                y_center = abs(float(values[2]))
                width = abs(float(values[3]))
                height = abs(float(values[4]))
                bboxes.append((x_center, y_center, width, height, class_id))

        img = cv2.imread(os.path.join(imgs_path, img_path))
        img_h, img_w = img.shape[0], img.shape[1]

        gauss_blur(img,bboxes,kernel_size=kernel_size,blur_limit=(3,7), prob=prob, aug_imgs_path=aug_imgs_path, aug_labels_path=aug_labels_path, filename_without_ext=img_name_without_ext, aug_name="gauss_blurr")
        shear(img, bboxes,shear=(-10,10), prob=prob,aug_imgs_path=aug_imgs_path, aug_labels_path=aug_labels_path, filename_without_ext=img_name_without_ext, aug_name="shear")    
        zoom_crop(img,img_w, img_h, bboxes,erosion_rate=erosion_rate, prob=prob,aug_imgs_path=aug_imgs_path, aug_labels_path=aug_labels_path, filename_without_ext=img_name_without_ext, aug_name="zoom_crop")    
        pixel_dropout(img, bboxes, dropout_prob=dropout_prob, prob=prob,aug_imgs_path=aug_imgs_path, aug_labels_path=aug_labels_path, filename_without_ext=img_name_without_ext, aug_name="pixel_dropout")
        emboss(img, bboxes,  alpha= alpha, strength = strength,prob =prob,aug_imgs_path=aug_imgs_path, aug_labels_path=aug_labels_path, filename_without_ext=img_name_without_ext, aug_name="emboss")
        lazy_pixelate(img, bboxes,ratio=(0.3,1.0), prob =prob,aug_imgs_path=aug_imgs_path, aug_labels_path=aug_labels_path, filename_without_ext=img_name_without_ext, aug_name="lazy_pixelate")
        multiply(img, bboxes,multiplier =(0.8,2.0),prob=prob,aug_imgs_path=aug_imgs_path, aug_labels_path=aug_labels_path, filename_without_ext=img_name_without_ext, aug_name="multiply")

        coarse_dropout(img, bboxes,max_holes=max_holes, prob=prob,aug_imgs_path=aug_imgs_path, aug_labels_path=aug_labels_path, filename_without_ext=img_name_without_ext, aug_name="coarse_dropout")
        flip_lr(img, bboxes, prob=prob,aug_imgs_path=aug_imgs_path, aug_labels_path=aug_labels_path, filename_without_ext=img_name_without_ext, aug_name="flip_lr")
        permute_channel(img, bboxes, prob=prob,aug_imgs_path=aug_imgs_path, aug_labels_path=aug_labels_path, filename_without_ext=img_name_without_ext, aug_name="permute_channel")

        motion_blur(img,bboxes, blur_limit=(3,7),prob=prob,aug_imgs_path=aug_imgs_path, aug_labels_path=aug_labels_path, filename_without_ext=img_name_without_ext, aug_name="motion_blur")    
        gray_scale(img, bboxes, prob=gray_scale_prob,aug_imgs_path=aug_imgs_path, aug_labels_path=aug_labels_path, filename_without_ext=img_name_without_ext, aug_name="gray_scale")
        jpeg_compression(img, bboxes, quality_lower=quality_lower, quality_upper=quality_upper, prob=prob,aug_imgs_path=aug_imgs_path, aug_labels_path=aug_labels_path, filename_without_ext=img_name_without_ext, aug_name="jpeg_comp")
        random_scale(img, bboxes,scale_limit=(0.5,2.0), prob=prob,aug_imgs_path=aug_imgs_path, aug_labels_path=aug_labels_path, filename_without_ext=img_name_without_ext, aug_name="random_scale")

if __name__ == '__main__':
    pass
