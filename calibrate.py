# https://docs.opencv.org/4.5.2/dc/dbb/tutorial_py_calibration.html
# OpenCV reference page

import os
import glob
import cv2 as cv
import numpy as np
import h5py


class Calibrate:
    def __init__(self):
        self.chessBoardSize = (7, 9)
        # This value should be change according to the chessBoardSize being used to calibrate the camera
        self.objpoints = None
        self.imgpoints = None
        self.cameraMatrix = None
        self.OptimizedcameraMatrix = None
        self.distCoeffs = None
        self.rvecs = None
        self.tvecs = None
        self.RegionOfInterest = None

    def calibrate_camera(self):
        # termination criteria
        criteria = (cv.TERM_CRITERIA_EPS + cv.TERM_CRITERIA_MAX_ITER, 30, 0.001)

        # prepare object points, like (0,0,0), (1,0,0), (2,0,0) ....,(6,5,0)
        objp = np.zeros(
            (self.chessBoardSize[0] * self.chessBoardSize[1], 3), np.float32
        )
        objp[:, :2] = np.mgrid[
            0 : self.chessBoardSize[0], 0 : self.chessBoardSize[1]
        ].T.reshape(-1, 2)

        # Arrays to store object points and image points from all the images.
        self.objpoints = []  # 3d point in real world space
        self.imgpoints = []  # 2d points in image plane.

        count = 0
        images = glob.glob(os.path.join("calibratrion_images/", "*.jpg"))
        for image in images:
            img_color = cv.imread(image)
            gray = cv.cvtColor(img_color, cv.COLOR_BGR2GRAY)
            # Find the chess board corners
            ret, corners = cv.findChessboardCorners(gray, self.chessBoardSize, None)
            # If found, add object points, image points (after refining them)
            if ret == True:
                count = count + 1
                self.objpoints.append(objp)
                corners2 = cv.cornerSubPix(gray, corners, (11, 11), (-1, -1), criteria)
                self.imgpoints.append(corners)
                # Draw and display the corners
                cv.drawChessboardCorners(img_color, self.chessBoardSize, corners2, ret)
                cv.imshow("img", img_color)
                cv.waitKey(1)
            else:
                print("Not found")
        cv.destroyAllWindows()
        print(f"Camera Calbirated using {count} images")
        # Calibration
        (
            retval,
            self.cameraMatrix,
            self.distCoeffs,
            self.rvecs,
            self.tvecs,
        ) = cv.calibrateCamera(
            self.objpoints, self.imgpoints, gray.shape[::-1], None, None
        )
        h, w = img_color.shape[:2]
        newcameramtx, roi = cv.getOptimalNewCameraMatrix(
            self.cameraMatrix, self.distCoeffs, (w, h), 1, (w, h)
        )
        self.OptimizedcameraMatrix = newcameramtx
        self.RegionOfInterest = roi

    def mean_error(self):
        mean_error = 0
        for i in range(len(self.objpoints)):
            imgpoints2, _ = cv.projectPoints(
                self.objpoints[i],
                self.rvecs[i],
                self.tvecs[i],
                self.cameraMatrix,
                self.distCoeffs,
            )
            error = cv.norm(self.imgpoints[i], imgpoints2, cv.NORM_L2) / len(imgpoints2)
            mean_error += error
        print("total error: {}".format(mean_error / len(self.objpoints)))

    def storeCalibrationResult(self, filename):
        objpoints = np.array(self.objpoints)
        imgpoints = np.array(self.imgpoints)
        cameraMatrix = np.array(self.cameraMatrix)
        distCoeffs = np.array(self.distCoeffs)
        rvecs = np.array(self.rvecs)
        tvecs = np.array(self.tvecs)
        RegionOfInterest = np.array(self.RegionOfInterest)
        file = h5py.File(filename, "w")
        group = file.create_group("Calibration")
        dataset = group.create_dataset(
            "ImagePoints", imgpoints.shape, dtype=imgpoints.dtype
        )
        dataset[...] = imgpoints
        dataset = group.create_dataset(
            "ObjectPoints", objpoints.shape, dtype=objpoints.dtype
        )
        dataset[...] = objpoints
        dataset = group.create_dataset(
            "CameraMatrix", cameraMatrix.shape, dtype=cameraMatrix.dtype
        )
        dataset[...] = cameraMatrix
        dataset = group.create_dataset(
            "DistortionCoefficient", distCoeffs.shape, dtype=distCoeffs.dtype
        )
        dataset[...] = distCoeffs
        dataset = group.create_dataset("RotationVector", rvecs.shape, dtype=rvecs.dtype)
        dataset[...] = rvecs
        dataset = group.create_dataset(
            "TranslationVector", tvecs.shape, dtype=tvecs.dtype
        )
        dataset[...] = tvecs
        dataset = group.create_dataset(
            "RegionOfInterest", RegionOfInterest.shape, dtype=RegionOfInterest.dtype
        )
        dataset[...] = RegionOfInterest
        file.close()
