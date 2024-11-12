""" 
code to draw bbox including the TP FP FN as labels 

parameter to pass:
* prediction txt file (un normalized)
* ground truth txt file (un normalized)
* image file (original image)
"""
import cv2
import numpy as np
from shapely.geometry import Polygon
import os

class BoxMatcher:
    def __init__(self, confidence_threshold=0.5, iou_threshold=0.5, class_label="label"):
        self.confidence_threshold = confidence_threshold
        self.iou_threshold = iou_threshold
        self.class_label = class_label

    def load_boxes(self, filepath):
        """
        Load bounding boxes from a file.

        Parameters
        ----------
        filepath : str
            Path to the file containing bounding boxes.

        Returns
        -------
        np.ndarray
            Array of bounding boxes.
        """
        with open(filepath, 'r') as f:
            boxes = [line.strip().split(' ') for line in f.readlines()]
        boxes = [[float(item) for item in sublist] for sublist in boxes]
        return np.array(boxes)

    def denormalize(self, boxes, image_width, image_height):
        """
        Convert normalized coordinates to absolute coordinates.

        Parameters
        ----------
        boxes : np.ndarray
            Array of normalized bounding boxes.
        image_width : int
            Width of the image.
        image_height : int
            Height of the image.

        Returns
        -------
        np.ndarray
            Array of denormalized bounding boxes.
        """
        return boxes

    def iou(self, box_1, box_2):
        """
        Compute the Intersection over Union (IoU) of two bounding boxes.

        Parameters
        ----------
        box1 : list or tuple of floats
            [xmin, ymin, xmax, ymax]
        box2 : list or tuple of floats
            [xmin, ymin, xmax, ymax]

        Returns
        -------
        float
            IoU value in [0, 1]
        """
        poly_1 = Polygon([(box_1[0], box_1[1]), (box_1[2], box_1[1]), (box_1[2], box_1[3]), (box_1[0], box_1[3])])
        poly_2 = Polygon([(box_2[0], box_2[1]), (box_2[2], box_2[1]), (box_2[2], box_2[3]), (box_2[0], box_2[3])])
        inter = poly_1.intersection(poly_2).area 
        area = poly_1.union(poly_2).area
        if area == 0.0: return 0.0
        iou = inter/area
        return iou

    def match_boxes(self, pred_boxes, gt_boxes):
        """
        Match predicted and ground truth boxes based on IoU threshold.

        Parameters
        ----------
        pred_boxes : np.ndarray
            Array of predicted bounding boxes.
        gt_boxes : np.ndarray
            Array of ground truth bounding boxes.

        Returns
        -------
        tuple
            Lists of true positives, false positives, and false negatives.
        """
        tp_boxes = []
        fp_boxes = []
        fn_boxes = []
        matched_gt = set()

        for pred_box in pred_boxes:
            best_iou = 0
            best_gt_idx = -1
            for gt_idx, gt_box in enumerate(gt_boxes):
                if gt_idx in matched_gt:
                    continue
                current_iou = self.iou(pred_box[1:], gt_box[1:])
                if current_iou >= best_iou:
                    best_iou = current_iou
                    best_gt_idx = gt_idx

            if 0<best_iou >= self.iou_threshold:
                tp_boxes.append(pred_box)
                matched_gt.add(best_gt_idx)
            elif best_iou <= self.iou_threshold :
                fp_boxes.append(pred_box)
                matched_gt.add(best_gt_idx)

        for gt_idx, gt_box in enumerate(gt_boxes):
            if gt_idx not in matched_gt:
                fn_boxes.append(gt_box)
        #print(f"lgt:{len(gt_boxes)},lprd {len(pred_boxes)},lfp:{len(fp_boxes)},lfn {len(fn_boxes)},ltp:{len(tp_boxes)}")
        assert max(len(pred_boxes),len(gt_boxes)) == len(tp_boxes) + len(fp_boxes) + len(fn_boxes)
        return tp_boxes, fp_boxes, fn_boxes

    def annotate_image(self, image, tp_boxes, fp_boxes, fn_boxes):
        """
        Annotate an image with true positive, false positive, and false negative boxes.

        Parameters
        ----------
        image : np.ndarray
            Image to annotate.
        tp_boxes : list
            List of true positive boxes.
        fp_boxes : list
            List of false positive boxes.
        fn_boxes : list
            List of false negative boxes.

        Returns
        -------
        np.ndarray
            Annotated image.
        """
        for box in tp_boxes:
            x1, y1, x2, y2 = int(round(box[1])), int(round(box[2])), int(round(box[3])), int(round(box[4]))
            cv2.rectangle(image, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.putText(image, f"TP_{self.class_label}", (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

        for box in fp_boxes:
            x1, y1, x2, y2 = int(round(box[1])), int(round(box[2])), int(round(box[3])), int(round(box[4]))
            cv2.rectangle(image, (x1, y1), (x2, y2), (0, 0, 255), 2)
            cv2.putText(image, f"FP_{self.class_label}", (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)

        for box in fn_boxes:
            x1, y1, x2, y2 = int(round(box[1])), int(round(box[2])), int(round(box[3])), int(round(box[4]))
            cv2.rectangle(image, (x1, y1), (x2, y2), (255, 0, 0), 2)
            cv2.putText(image, f"FN_{self.class_label}", (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)

        return image

    def process_and_annotate_image(self, pred_file, gt_file, input_image_path, output_image_path):
        """
        Process and annotate an image with bounding boxes.

        Parameters
        ----------
        pred_file : str
            Path to the file containing predicted boxes.
        gt_file : str
            Path to the file containing ground truth boxes.
        input_image_path : str
            Path to the input image.
        output_image_path : str
            Path to save the annotated image.

        Returns
        -------
        tuple
            Lists of true positives, false positives, and false negatives.
        """
        pred_boxes = self.load_boxes(pred_file)
        gt_boxes = self.load_boxes(gt_file)

        if len(pred_boxes) > 0:
            pred_boxes = pred_boxes[pred_boxes[:, -1] >= self.confidence_threshold]
            pred_boxes = pred_boxes[:, :-1]

        image = cv2.imread(input_image_path)
        image_height, image_width = image.shape[:2]

        if len(gt_boxes) > 0:
            if gt_boxes.ndim == 1:
                gt_boxes = np.expand_dims(gt_boxes, axis=0)
            gt_boxes = self.denormalize(gt_boxes, image_width, image_height)

        tp_boxes, fp_boxes, fn_boxes = self.match_boxes(pred_boxes, gt_boxes)
        annotated_image = self.annotate_image(image, tp_boxes, fp_boxes, fn_boxes)

        cv2.imwrite(output_image_path, annotated_image)

        return tp_boxes, fp_boxes, fn_boxes



if __name__ == "__main__":
    import glob
    pred_files = glob.glob("../sample/pred_label/*.txt")
    gt_files = glob.glob("../sample/gt_txt_label/*.txt")
    img_files = glob.glob("../sample/img/*.jpg")
    print(len(gt_files))
    # try:
    os.makedirs("./results/det_eval_0_26/", exist_ok=True)
    # except Exception as e: 
    #     print(e)
    result_dict = {}
    for i in img_files:
        base_name = os.path.basename(i).split(".")[0]
        # print("eerror")
        result_dict[base_name] = {"img":i}
    for i in pred_files:
        base_name = os.path.basename(i).split(".")[0]
        if base_name in result_dict:
            result_dict[base_name]["pred"] = i
    for i in gt_files:
        base_name = os.path.basename(i).split(".")[0]
        if base_name in result_dict:
            result_dict[base_name]["gt"] = i

    matcher = BoxMatcher(confidence_threshold=0.5, iou_threshold=0.5, class_label="prod")
    for key,val in result_dict.items():
        print(val["img"])
        if len(val) == 3:
            tp_boxes, fp_boxes, fn_boxes = matcher.process_and_annotate_image(
            pred_file=val["pred"],
            gt_file=val["gt"],
            input_image_path=val["img"],
            output_image_path="./results/det_eval_0_26/" +key+".jpg"
        )
