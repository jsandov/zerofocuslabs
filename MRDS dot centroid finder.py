import cv2
import numpy as np
import vmbpy

vmb = vmbpy.VmbSystem.get_instance()
with vmb:
    cams = vmb.get_all_cameras()
    for cam in cams:
        print(cam)

from dataclasses import dataclass
from typing import Optional, Tuple


@dataclass
class DotResult:
    """Store blob analysis results"""
    centroid: Optional[Tuple[float, float]]
    area: float
    timestamp: float


class DotDetector:
    def __init__(self, threshold: int = 200):
        """
        Initialize camera and blob detection parameters
        Args:
            threshold: Brightness threshold (0-255) for blob detection
            This will need dialed in and could possibly use data from the camera config settings to set.
        """
        self.camera = None
        self.threshold = threshold
        self.frame_ready = False
        self.current_frame = None

    def start_camera(self):
        """Initialize and configure the Alvium camera
        this may be changed in the future to allow for control through the GUI"""
        with vmbpy.get_instance() as vimba:
            cams = vimba.get_all_cameras()
            if not cams:
                raise RuntimeError('No Cameras Found')

            self.camera = cams[0]
            self.camera.open()

            # Configure camera settings
            self.camera.set_pixel_format(PixelFormat.Mono12)

            # Set up trigger mode
            self.camera.TriggerSelector.set('FrameStart')
            self.camera.TriggerMode.set('On')
            self.camera.TriggerSource.set('Line0')  # Adjust based on your trigger source

            # Optional: Set exposure and gain
            self.camera.ExposureAuto.set('Off')
            self.camera.ExposureTime.set(10000)  # 10ms exposure
            self.camera.GainAuto.set('Off')
            self.camera.Gain.set(0)

            # Start the camera
            self.camera.start_streaming(self.frame_callback)

    def frame_callback(self, frame):
        """Callback function when a frame is captured"""
        self.current_frame = frame.as_opencv_image()
        self.frame_ready = True

    def find_centroid(self) -> Optional[DotResult]:
        """
        Process the current frame and find the centroid of bright blobs
        Returns:
            BlobResult object containing centroid coordinates and blob properties
        """
        if not self.frame_ready or self.current_frame is None:
            return None

        # Reset frame ready flag
        self.frame_ready = False

        # Create binary image using threshold
        _, binary = cv2.threshold(self.current_frame, self.threshold, 255, cv2.THRESH_BINARY)

        # Find contours
        contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        if not contours:
            return DotResult(None, 0, frame.timestamp)

        # Find the largest blob
        """Set to find largest blob in current configuration.
        Upon results of testing, this may also need dialed in to keep from grabbing the wrong blob
        """
        largest_contour = max(contours, key=cv2.contourArea)
        area = cv2.contourArea(largest_contour)

        # Calculate centroid
        M = cv2.moments(largest_contour)
        if M["m00"] == 0:
            return DotResult(None, area, frame.timestamp)

        cx = M["m10"] / M["m00"]
        cy = M["m01"] / M["m00"]

        return DotResult((cx, cy), area, frame.timestamp)

    def get_annotated_frame(self) -> Optional[np.ndarray]:
        """
        Return the current frame with blob detection visualization
        Returns:
            Annotated frame as numpy array
        """
        if self.current_frame is None:
            return None

        # Create color version of frame for visualization
        display_frame = cv2.cvtColor(self.current_frame, cv2.COLOR_GRAY2BGR)

        # Find and draw blob information
        result = self.find_centroid()
        if result and result.centroid:
            cx, cy = result.centroid
            # Draw centroid
            cv2.circle(display_frame, (int(cx), int(cy)), 5, (0, 255, 0), -1)
            # Draw text with coordinates
            text = f"({int(cx)}, {int(cy)})"
            cv2.putText(display_frame, text, (int(cx) + 10, int(cy)),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)

        return display_frame

    def stop(self):
        """Stop the camera and clean up"""
        if self.camera:
            self.camera.stop_streaming()
            self.camera.close()


def main():
    # Create detector with custom threshold if needed
    detector = DotDetector(threshold=200)

    try:
        detector.start_camera()
        print("Camera started. Waiting for trigger signals...")

        while True:
            # Process frame when available
            if detector.frame_ready:
                result = detector.find_centroid()
                if result and result.centroid:
                    print(f"Centroid: {result.centroid}, Area: {result.area:.2f}")

                # Optional: Display frame with annotations
                frame = detector.get_annotated_frame()
                if frame is not None:
                    cv2.imshow('Blob Detection', frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    except KeyboardInterrupt:
        print("\nStopped by user")
    finally:
        detector.stop()
        cv2.destroyAllWindows()


if __name__ == "__main__":
    main()