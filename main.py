import cv2
from camera_handler import CameraHandler
from dot_detector import DotDetector

def main():
    camera_handler = CameraHandler()
    detector = DotDetector(threshold=200)

    try:
        camera_handler.start_camera()
        print("Camera started. Waiting for trigger signals...")

        while True:
            if camera_handler.frame_ready:
                frame = camera_handler.current_frame
                timestamp = camera_handler.camera.get_frame().get_timestamp()
                camera_handler.frame_ready = False

                result = detector.find_centroid(frame, timestamp)
                if result and result.centroid:
                    print(f"Centroid: {result.centroid}, Area: {result.area:.2f}")

                annotated_frame = detector.get_annotated_frame(frame, result)
                if annotated_frame is not None:
                    cv2.imshow('Blob Detection', annotated_frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    except KeyboardInterrupt:
        print("\nStopped by user")
    finally:
        camera_handler.stop()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
