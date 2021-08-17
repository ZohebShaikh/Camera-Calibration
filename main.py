from calibrate import Calibrate
from removeDistortion import RemoveDistortion

if __name__ == "__main__":
    calibrate = Calibrate()
    calibrate.calibrate_camera()
    calibrate.mean_error()
    calibrate.storeCalibrationResult("Logitech_WebCam.hdf5")
    undistort = RemoveDistortion(calibrate)
    undistort.undistort("04_58_Pro.jpg")
    undistort.undistort_method_2("04_58_Pro.jpg")
    undistort.undistort("test_2.jpg")
    undistort.undistort_method_2("test_2.jpg")
    undistort.difference("test_2.jpg", "test_2.jpg_undistorted_method_2.png")
    undistort.undistort("distorted.png")
