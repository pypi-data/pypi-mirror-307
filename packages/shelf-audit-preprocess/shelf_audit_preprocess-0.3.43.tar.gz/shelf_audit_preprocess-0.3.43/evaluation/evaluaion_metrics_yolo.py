"""
code that will find all evaluations parameters TP,FP, FN, Precision, Recall, F1 score, MAp for diff confidence by calculating iou 

./py file is called by metrics_code.ipynb
path will pass in that notebook

"""
import os
import glob
import numpy as np
import pandas as pd
from shapely.geometry import Polygon
from . import eval_boxes
import cv2

def get_dirname(dir_path:str,strip_str:str="/"):
    parsed_url = dir_path.rstrip("/")
    return os.path.basename(parsed_url)

def read_text(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()
    return lines

def extract_fields(file_lines: list[str], start_bbox_ind,end_bbox_ind,label_ind,confidence_val_ind)-> (list,list,list,int):
    assert end_bbox_ind - start_bbox_ind == 4
    bboxes = []
    labels = []
    confidence_vals = []
    for line in file_lines:
        parts = list(map(float, line.strip().split()))
        bboxes.append(parts[start_bbox_ind:end_bbox_ind])
        if confidence_val_ind:
            confidence_vals.append(parts[confidence_val_ind])
        labels.append(parts[label_ind])
    return {"all":(bboxes,labels,confidence_vals)}

def filter_confidence_val(field_dict,confidence_value):
    bboxes,labels,confidence_vals = field_dict["all"]
    fil_bboxes = []
    fil_labels = []
    fil_confidence_vals = []
    for i in range(len(bboxes)):
        if confidence_vals[i] >= confidence_value:
            fil_bboxes.append(bboxes[i])
            fil_labels.append(labels[i])
            fil_confidence_vals.append(confidence_vals[i])
    return fil_bboxes,fil_labels,fil_confidence_vals

def parse_txt(file_path):
    """
    Parse the txt file to extract bounding boxes for ground truth.
    
    Returns a list of bounding boxes, confidence score and count.
    """
    with open(file_path, 'r') as file:
        lines = file.readlines()
        
    boxes = []
    count = 0
    for line in lines:
        parts = list(map(float, line.strip().split()))
        boxes.append(parts)
        count+=1
    
    return boxes, count

def iou(box_1, box_2):
    """
    Calculate the Intersection over Union (IoU) of two bounding boxes.
    Each box is defined as [x_center, y_center, width, height].
    """

    poly_1 = Polygon([(box_1[0], box_1[1]), (box_1[2], box_1[1]), (box_1[2], box_1[3]), (box_1[0], box_1[3])])
    poly_2 = Polygon([(box_2[0], box_2[1]), (box_2[2], box_2[1]), (box_2[2], box_2[3]), (box_2[0], box_2[3])])
    
    inter = poly_1.intersection(poly_2).area 
    area = poly_1.union(poly_2).area
    if area == 0.0: return 0.0
    iou = inter/area
    return iou

def confusion_matrix(predictions, ground_truths, iou_threshold=0.5):
    """
    Calculate the confusion matrix for object detection.
    
    Returns TP, FP, and FN.
    """
    tp_boxes = []
    fp_boxes = []
    fn_boxes = []
    matched_gt = set()

    for pred_box in predictions:
        best_iou = 0
        best_gt_idx = -1
        for gt_idx, gt_box in enumerate(ground_truths):
            if gt_idx in matched_gt:
                continue
            current_iou = iou(pred_box, gt_box)
            if current_iou >= best_iou:
                best_iou = current_iou
                best_gt_idx = gt_idx

        if 0< best_iou >= iou_threshold:
            tp_boxes.append(pred_box)
            matched_gt.add(best_gt_idx)
        elif best_iou <= iou_threshold :
            fp_boxes.append(pred_box)
            matched_gt.add(best_gt_idx)

    for gt_idx, gt_box in enumerate(ground_truths):
        if gt_idx not in matched_gt:
            fn_boxes.append(gt_box)

    assert max(len(predictions),len(ground_truths)) == len(tp_boxes) + len(fp_boxes) + len(fn_boxes)
    return tp_boxes, fp_boxes, fn_boxes



def precision_recall_f1(TP, FP, FN):
    """
    Calculate precision, recall, and F1 score.
    """
    precision = TP / (TP + FP) if (TP + FP) > 0 else 0
    recall = TP / (TP + FN) if (TP + FN) > 0 else 0
    f1_score = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0
    
    return precision, recall, f1_score

def average_precision(precisions, recalls):
    precisions = np.array(precisions)
    recalls = np.array(recalls)
    
    recalls = np.concatenate(([0.], recalls, [1.]))
    precisions = np.concatenate(([0.], precisions, [0.]))
    
    for i in range(precisions.size - 1, 0, -1):
        precisions[i - 1] = np.maximum(precisions[i - 1], precisions[i])
    
    indices = np.where(recalls[1:] != recalls[:-1])[0]
    ap = np.sum((recalls[indices + 1] - recalls[indices]) * precisions[indices + 1])
    
    return ap

def compute_map(predictions, ground_truths, iou_thresholds):
    aps = []
    
    for iou_threshold in iou_thresholds:
        precisions = []
        recalls = []
        
        for pred, gt in zip(predictions, ground_truths):
            tp_boxes, fp_boxes, fn_boxes  = confusion_matrix(pred, gt, iou_threshold)
            tp, fp, fn = len(tp_boxes), len(fp_boxes), len(fn_boxes)
            precision, recall, f1_score = precision_recall_f1(tp, fp, fn)
            
            precisions.append(precision)
            recalls.append(recall)
        
        ap = average_precision(precisions, recalls)
        aps.append(ap)
    
    return np.mean(aps)

def bbox_summary(summary, image_area, temp_dict, conf_val_str):
     sizes = ["small", "medium", "large"]
     total_area = 0
    
     for size in sizes:
        temp_dict[f"{size}_bbox_total_boxes_"+conf_val_str] = summary[size]["total_boxes"]
        temp_dict[f"{size}_bbox_total_area_"+conf_val_str] = summary[f"{size}"]["tota_area"]
        temp_dict[f"{size}_bbox_min_area_"+conf_val_str] = summary[f"{size}"]["min_area"]
        temp_dict[f"{size}_bbox_max_area_"+conf_val_str] = summary[f"{size}"]["max_area"]
        temp_dict[f"{size}_bbox_avg_area_"+conf_val_str] = summary[f"{size}"]["avg_area"]
        temp_dict[f"{size}_bbox_min_width_"+conf_val_str] = summary[f"{size}"]["min_width"]
        temp_dict[f"{size}_bbox_max_width_"+conf_val_str] = summary[f"{size}"]["max_width"]
        temp_dict[f"{size}_bbox_avg_width_"+conf_val_str] = summary[f"{size}"]["avg_width"]
        temp_dict[f"{size}_bbox_min_height_"+conf_val_str] = summary[f"{size}"]["min_height"]
        temp_dict[f"{size}_bbox_max_height_"+conf_val_str] = summary[f"{size}"]["max_height"]
        temp_dict[f"{size}_bbox_avg_height_"+conf_val_str] = summary[f"{size}"]["avg_height"]
        
        total_area += summary[f"{size}"]["tota_area"]
        temp_dict[f"{size}_bbox_ratio_to_orignal_"+conf_val_str] = summary[f"{size}"]["tota_area"] / image_area
    
     temp_dict["bbox_total_area_"+conf_val_str] = total_area
     temp_dict["bbox_ratio_to_orignal_"+conf_val_str] = total_area / image_area

def generate_metrics(original_file_name:str, input_pred_file:str, input_ground_truth_file:str, input_image_file:str, confidence_val_list: list):
    if not confidence_val_list:
        confidence_val_list= [.50]
    result_dict = {"original_file_name" : original_file_name,
                  "pred_file_name": input_pred_file,
                  "ground_truth_file_name": input_ground_truth_file}
    pred_lines = read_text(input_pred_file)
    ground_truth_lines = read_text(input_ground_truth_file)
    pred_fields = extract_fields(pred_lines,1,5,0,5)
    ground_truth_fields = extract_fields(ground_truth_lines,1,5,0,None)
    ground_truth_bboxes = ground_truth_fields["all"][0]
    result_dict.update({"pred_num_boxes" : len(pred_fields["all"][0]),
                        "ground_truth_num_boxes" : len(ground_truth_bboxes)})

    image = cv2.imread(input_image_file)
    image_width, image_height = image.shape[0], image.shape[1]
    image_area = image_width * image_height
    iou_thresholds = np.arange(0.5, 1.0, 0.05)
    for conf_val in confidence_val_list:
        temp_dict = {}
        conf_val_str = str(round(conf_val,2))
        pred_bbox_list,pred_label_list, pred_conf_val_list = filter_confidence_val(pred_fields,conf_val)
        
        analyzer = eval_boxes.BoundingBoxAnalyzer(pred_bbox_list)        #####
        summary = analyzer.get_summary()  #####
        
        temp_dict["num_bbox_"+conf_val_str] = len(pred_bbox_list)
        # Calculate confusion matrix
        tp_boxes, fp_boxes, fn_boxes = confusion_matrix(pred_bbox_list, ground_truth_bboxes)
        TP, FP, FN = len(tp_boxes), len(fp_boxes), len(fn_boxes)
        temp_dict["TP_"+conf_val_str] = TP
        temp_dict["FP_"+conf_val_str] = FP
        temp_dict["FN_"+conf_val_str] = FN
        precision, recall, f1_score = precision_recall_f1(TP, FP, FN)
        temp_dict["precision_"+conf_val_str] = precision
        temp_dict["recall_"+conf_val_str] = recall
        temp_dict["f1score_"+conf_val_str]= f1_score
        temp_dict["map50_"+conf_val_str] = compute_map([pred_bbox_list], [ground_truth_bboxes], [0.5])
        temp_dict["map50-95_"+conf_val_str] = compute_map([pred_bbox_list], [ground_truth_bboxes], iou_thresholds)
        ################################
        bbox_summary(summary, image_area, temp_dict, conf_val_str)
        
        result_dict.update(temp_dict)
    return result_dict


def get_paths(dir_path,image_suffix = "_image",json_suffix="_json",labels_suffix="_labels",prediction_suffix="_predictions"):
    folder_name = get_dirname(dir_path)
    image_path = os.path.join(dir_path,folder_name+image_suffix)
    json_path= os.path.join(dir_path,folder_name+json_suffix)
    labels_path = os.path.join(dir_path,folder_name+labels_suffix)
    prediction_path = os.path.join(dir_path,folder_name+prediction_suffix)
    return image_path,json_path,labels_path,prediction_path
        
def get_file_path_dict(pred_folder_path, labels_folder_path, image_folder_path):
    pred_files = list(glob.glob(pred_folder_path.rstrip("/")+"/*.txt"))
    labels_files = list(glob.glob(labels_folder_path.rstrip("/")+"/*.txt"))
    image_files = list(glob.glob(image_folder_path.rstrip("/")+"/*.jpg"))
    
    result_dict = {}
    for f in pred_files:
        filename = os.path.basename(f)
        if filename not in result_dict:
            result_dict[filename] = {"pred":f}
            
    for f in labels_files:
        filename = os.path.basename(f)
        if filename not in result_dict:
            result_dict[filename] = {"label":f}
        else:
            result_dict[filename].update({"label":f})

    for f in image_files:
        filename = os.path.basename(f).split(".")[0]+".txt"
        if filename not in result_dict:
            result_dict[filename] = {"image":f}
        else:
            result_dict[filename].update({"image":f})

    return result_dict
    

def generate_metrics_dataframe(base_folder_path: str,confidence_val_list:list = [0.5,0.6,0.8], write_df:bool = True):
    image_path,json_path,labels_path,prediction_path = get_paths(base_folder_path)
    base_name = os.path.basename(base_folder_path.rstrip("/"))
    result_list = []
    file_path_dict = get_file_path_dict(prediction_path,labels_path, image_path)
    for file_name, path_dict in file_path_dict.items():
        if len(path_dict) != 3:
            print(f"paths vals: {path_dict}, filename: {file_name}")
            continue
        result_list.append(generate_metrics(file_name, path_dict["pred"], path_dict["label"], path_dict["image"], confidence_val_list))
    df = pd.DataFrame(result_list)
    df["merge_key"] = df["original_file_name"].str.split("_frame").apply(lambda x: x[0])
    if write_df:
        df.to_excel(base_name+"_metrics.xlsx",index=False)
    return df
    
if __name__ == '__main__':
    pass
