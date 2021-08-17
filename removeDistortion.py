from calibrate import Calibrate
import cv2 as cv
import os


class RemoveDistortion:
    def __init__(self, calibrate=None):
        if calibrate == None:
            self.calibrate = Calibrate()
            calibrate.calibrate_camera()
        else:
            self.calibrate = calibrate

    def undistort(self, filename):
        img = cv.imread(os.path.join("test_images/", filename))
        filename = os.path.splitext(filename)[0]
        # undistort
        dst = cv.undistort(
            img,
            self.calibrate.cameraMatrix,
            self.calibrate.distCoeffs,
            None,
            self.calibrate.OptimizedcameraMatrix,
        )
        # crop the image
        x, y, w, h = self.calibrate.RegionOfInterest
        dst = dst[y : y + h, x : x + w]
        cv.imwrite(os.path.join("test_images/", filename + "_undistorted.png"), dst)

    def undistort_method_2(self, filename):
        img = cv.imread(os.path.join("test_images/", filename))
        filename = os.path.splitext(filename)[0]
        # undistort
        x, y, w, h = self.calibrate.RegionOfInterest
        mapx, mapy = cv.initUndistortRectifyMap(
            self.calibrate.cameraMatrix,
            self.calibrate.distCoeffs,
            None,
            self.calibrate.OptimizedcameraMatrix,
            (w, h),
            5,
        )
        dst = cv.remap(img, mapx, mapy, cv.INTER_LINEAR)
        # crop the image
        dst = dst[y : y + h, x : x + w]
        cv.imwrite(
            os.path.join("test_images/", filename + "_undistorted_method_2.png"), dst
        )

    def difference(self, filename, compare):
        original = cv.imread(os.path.join("test_images/", filename))
        undistorted = cv.imread(os.path.join("test_images/", compare))
        height = undistorted.shape[0]
        width = undistorted.shape[1]

        original = original[0:height, 0:width]
        subtract = cv.subtract(original, undistorted)
        filename = os.path.splitext(filename)[0]
        cv.imwrite(os.path.join("test_images/", filename + "subtract.png"), subtract)
