import cv2
import numpy as np
from dataclasses import dataclass
from typing import Optional, Tuple

@dataclass
class DotResult:
    centroid: Optional[Tuple[float, float]]
    area: float
    timestamp: float

class DotDetector:
    def __init__(self, threshold: int = 200):
        self.threshold = threshold

    def find_centroid(self, frame, timestamp) -> Optional[DotResult]:
        if frame is None:
            return None

        _, binary = cv2.threshold(frame, self.threshold, 255, cv2.THRESH_BINARY)
        contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        if not contours:
            return DotResult(None, 0, timestamp)

        largest_contour = max(contours, key=cv2.contourArea)
        area = cv2.contourArea(largest_contour)

        M = cv2.moments(largest_contour)
        if M["m00"] == 0:
            return DotResult(None, area, timestamp)

        cx = M["m10"] / M["m00"]
        cy = M["m01"] / M["m00"]

        return DotResult((cx, cy), area, timestamp)

    def get_annotated_frame(self, frame, result) -> Optional[np.ndarray]:
        if frame is None:
            return None

        display_frame = cv2.cvtColor(frame, cv2.COLOR_GRAY2BGR)

        if result and result.centroid:
            cx, cy = result.centroid
            cv2.circle(display_frame, (int(cx), int(cy)), 5, (0, 255, 0), -1)
            text = f"({int(cx)}, {int(cy)})"
            cv2.putText(display_frame, text, (int(cx) + 10, int(cy)),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)

        return display_frame
