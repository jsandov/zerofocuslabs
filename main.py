import cv2
from camera_handler import CameraHandler
from dot_detector import DotDetector


def main():
    camera_handler = CameraHandler()
    detector = DotDetector(threshold=200)

    try:
        print("Starting camera...")
        camera_handler.start_camera()
        print("Camera started. Waiting for trigger signals...")

        while True:
            if camera_handler.frame_ready:
                frame = camera_handler.current_frame

                # Process the frame to find blobs
                result = detector.find_centroid(frame, 0)  # Replace '0' with an actual timestamp if available
                if result and result.centroid:
                    print(f"Centroid: {result.centroid}, Area: {result.area:.2f}")

                # Optional: Display frame with annotations
                annotated_frame = detector.get_annotated_frame(frame, result)
                if annotated_frame is not None:
                    cv2.imshow('Blob Detection', annotated_frame)

            # Exit on 'q' key press
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    except KeyboardInterrupt:
        print("\nStopped by user")
    finally:
        print("Stopping camera...")
        camera_handler.stop()
        cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
