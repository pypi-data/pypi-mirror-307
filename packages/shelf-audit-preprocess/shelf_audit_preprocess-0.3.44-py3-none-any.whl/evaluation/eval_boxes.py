"""
code to find num of small bbox - less than (32x32), medium bbox - (32x32) to (96x 96),  large box - greater than (96x96)
and their area, total area, ratio of each, total ratio, height, width

class call from evaluation_metrics_yolo.py file

"""
from shapely.geometry import Polygon

class BoundingBoxAnalyzer:
    def __init__(self, boxes):
        """
        Initialize with a list of bounding boxes.
        Args:
            boxes: List of bounding boxes [[xmin, ymin, xmax, ymax], ...].
        """
        self.boxes = boxes
        self.small_boxes = []
        self.medium_boxes = []
        self.large_boxes = []
        self.summary = {}

    def create_polygon(self, box):
        """
        Create a polygon from bounding box coordinates.
        Args:
            box: A list of [xmin, ymin, xmax, ymax].

        Returns:
            Shapely Polygon object.
        """
        xmin, ymin, xmax, ymax = box
        return Polygon([(xmin, ymin), (xmin, ymax), (xmax, ymax), (xmax, ymin)])

    def box_area(self, polygon):
        """
        Calculate the area of a given polygon.
        Args:
            polygon: Shapely Polygon object.

        Returns:
            Area of the polygon.
        """
        return polygon.area

    def box_dimensions(self, polygon):
        """
        Calculate the width and height of a given polygon.
        Args:
            polygon: Shapely Polygon object.

        Returns:
            Width and height of the polygon.
        """
        bounds = polygon.bounds  # Returns (xmin, ymin, xmax, ymax)
        width = bounds[2] - bounds[0]
        height = bounds[3] - bounds[1]
        return width, height

    def classify_boxes(self):
        """
        Classify boxes into small, medium, and large categories based on their area.
        """
        for box in self.boxes:
            polygon = self.create_polygon(box)
            area = self.box_area(polygon)
            width, height = self.box_dimensions(polygon)

            if area < 32**2:
                self.small_boxes.append((area, width, height))
            elif 32**2 <= area <= 96**2:
                self.medium_boxes.append((area, width, height))
            else:
                self.large_boxes.append((area, width, height))

        self.summary = {
            "small": self.calculate_summary(self.small_boxes),
            "medium": self.calculate_summary(self.medium_boxes),
            "large": self.calculate_summary(self.large_boxes)
        }

    def calculate_summary(self, box_list):
        """
        Calculate the min, max, and average area, width, and height for a list of boxes.
        Args:
            box_list: List of tuples containing (area, width, height).

        Returns:
            Dictionary with min, max, and average for area, width, and height.
        """
        if not box_list:
            return {
                "total_boxes": 0,"tota_area": 0,
                "min_area": 0, "max_area": 0, "avg_area": 0,
                "min_width": 0, "max_width": 0, "avg_width": 0,
                "min_height": 0, "max_height": 0, "avg_height": 0
            }

        areas = [box[0] for box in box_list]
        widths = [box[1] for box in box_list]
        heights = [box[2] for box in box_list]

        return {
            "total_boxes": len(box_list),
            "tota_area": sum(areas),
            "min_area": min(areas),
            "max_area": max(areas),
            "avg_area": sum(areas) / len(areas),
            "min_width": min(widths),
            "max_width": max(widths),
            "avg_width": sum(widths) / len(widths),
            "min_height": min(heights),
            "max_height": max(heights),
            "avg_height": sum(heights) / len(heights)
        }

    def get_summary(self):
        """
        Get the summary of classified boxes.
        Returns:
            Dictionary containing the summary of small, medium, and large boxes.
        """
        self.classify_boxes()
        return self.summary

if __name__ == '__main__':
    pass
