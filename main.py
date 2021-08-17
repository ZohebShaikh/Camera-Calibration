from calibrate import Calibrate
from removeDistortion import RemoveDistortion

if __name__ == "__main__":

    calibrate = Calibrate(
        7, 9
    )  # 7 and 9 are the dimensions of the chessboard used for camera calibration

    calibrate.calibrate_camera(1000)  # we will have a 5 second delay in opencv

    print(
        f" Total error is : {calibrate.mean_error()}"
    )  # the error should be closer to zero for more accuracy

    calibrate.storeCalibrationResult(
        "Logitech_WebCam.hdf5"
    )  # HDF5 filename to store the camera configuration
    # This file contains can use in MATLAB or opencv for correcting distorted images

    undistort = RemoveDistortion(
        calibrate
    )  # giving the calibration object if it is not give it will run calibration again

    undistort.undistort("04_58_Pro.jpg")
    undistort.undistort_method_2("04_58_Pro.jpg")

    undistort.undistort("test_2.jpg")
    undistort.undistort_method_2("test_2.jpg")
    undistort.difference("test_2.jpg", "test_2_undistorted_method_2.png")

    undistort.undistort("distorted.png")
