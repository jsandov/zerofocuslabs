import vmbpy
import cv2

class CameraHandler:
    def __init__(self):
        self.camera = None
        self.frame_ready = False
        self.current_frame = None

    def start_camera(self):
        with vmbpy.VmbSystem.get_instance() as vmb:
            cams = vmb.get_all_cameras()
            if not cams:
                raise RuntimeError('No Cameras Found')

            self.camera = cams[0]
            self.camera.open()

            # Configure camera settings
            self.camera.set_pixel_format(vmbpy.PixelFormat.Mono12)

            # Set up trigger mode
            self.camera.TriggerSelector.set('FrameStart')
            self.camera.TriggerMode.set('On')
            self.camera.TriggerSource.set('Line0')

            # Optional: Set exposure and gain
            self.camera.ExposureAuto.set('Off')
            self.camera.ExposureTime.set(10000)
            self.camera.GainAuto.set('Off')
            self.camera.Gain.set(0)

            # Start the camera
            self.camera.start_streaming(self.frame_callback)

    def frame_callback(self, frame):
        self.current_frame = frame.as_opencv_image()
        self.frame_ready = True

    def stop(self):
        if self.camera:
            self.camera.stop_streaming()
            self.camera.close()
