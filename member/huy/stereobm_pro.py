from stereovision.calibration import StereoCalibration

__author__ = 'pc'
import numpy as np
import cv2
# from matplotlib import pyplot as plt
def nothing(x):
    pass

video1 = cv2.VideoCapture(1)
video1.set(3,640)
video1.set(4,480)

video2 = cv2.VideoCapture(2)
video2.set(3,640)
video2.set(4,480)

# imgL = cv2.imread('images/im2.png',0)
# imgR = cv2.imread('images/im6.png',0)
cv2.namedWindow('image')
cv2.createTrackbar('PreFilterCap','image',1,63,nothing)
cv2.createTrackbar('PreFilterSize','image',5,255,nothing)
cv2.createTrackbar('PreFilterType','image',0,1,nothing)
cv2.createTrackbar('SmallerBlockSize','image',0,255,nothing)
cv2.createTrackbar('Disp12MaxDiff','image',0,255,nothing)
cv2.createTrackbar('MinDisparity','image',0,400,nothing)
cv2.createTrackbar('NumDisparities','image',0,20,nothing)
cv2.createTrackbar('SpeckleRange','image',0,3,nothing)
cv2.createTrackbar('SpeckleWindowSize','image',0,5000,nothing)
cv2.createTrackbar('TextureThreshold','image',0,2000,nothing)
cv2.createTrackbar('UniquenessRatio','image',0,30,nothing)
stereo = cv2.StereoBM()
stereo.setDisp12MaxDiff(0)
stereo.setPreFilterCap(61)
stereo.setPreFilterSize(5)
stereo.setSmallerBlockSize(0)
stereo.setPreFilterType(1)
stereo.setMinDisparity(-39)
stereo.setNumDisparities(112)
stereo.setSpeckleRange(8)
stereo.setSpeckleWindowSize(0)
stereo.setTextureThreshold (507)
stereo.setUniquenessRatio(0)
NumDis = 16
# This assumes you've already calibrated your camera and have saved the
# calibration files to disk. You can also initialize an empty calibration and
# calculate the calibration, or you can clone another calibration from one in
# memory
calibration = StereoCalibration(input_folder='./export')
while(1):
    ret1, frame1 = video1.read()
    ret2, frame2 = video2.read()

    imgR = cv2.cvtColor(frame1,cv2.COLOR_RGB2GRAY)
    imgL = cv2.cvtColor(frame2,cv2.COLOR_RGB2GRAY)
    # Now rectify two images taken with your stereo camera. The function expects
    # a tuple of OpenCV Mats, which in Python are numpy arrays
    rectified_pair = calibration.rectify((imgL, imgR))

    PreFilterCap = cv2.getTrackbarPos('PreFilterCap','image')
    if PreFilterCap <= 0:
        PreFilterCap = 1
    PreFilterType = cv2.getTrackbarPos('PreFilterType','image')
    PreFilterSize = cv2.getTrackbarPos('PreFilterSize','image')
    if PreFilterSize % 2 == 0:
        PreFilterSize+=1
    if PreFilterSize <= 5:
        PreFilterSize = 5
    MinDisparity = cv2.getTrackbarPos('MinDisparity','image')
    MinDisparity -= 300
    SmallerBlockSize = cv2.getTrackbarPos('SmallerBlockSize','image')
    Disp12MaxDiff = cv2.getTrackbarPos('Disp12MaxDiff','image')
    NumDisparities = cv2.getTrackbarPos('NumDisparities','image')
    if NumDisparities > 0:
        NumDis = NumDisparities*16
    SpeckleRange = cv2.getTrackbarPos('SpeckleRange','image')
    SpeckleWindowSize = cv2.getTrackbarPos('SpeckleWindowSize','image')
    TextureThreshold = cv2.getTrackbarPos('TextureThreshold','image')
    UniquenessRatio = cv2.getTrackbarPos('UniquenessRatio','image')
    stereo.setPreFilterCap(PreFilterCap)
    stereo.setPreFilterSize(PreFilterSize)
    stereo.setPreFilterType(PreFilterType)
    stereo.setSmallerBlockSize(SmallerBlockSize)
    stereo.setDisp12MaxDiff(Disp12MaxDiff)
    stereo.setMinDisparity(MinDisparity)
    stereo.setNumDisparities(NumDis)
    stereo.setSpeckleRange(SpeckleRange)
    stereo.setSpeckleWindowSize(SpeckleWindowSize)
    stereo.setTextureThreshold (TextureThreshold)
    stereo.setUniquenessRatio(UniquenessRatio)

    # disparity = stereo.compute(imgL,imgR,cv2.CV_8U)
    # Compute disparity image
    disparity = stereo.compute(rectified_pair[0], rectified_pair[1])


    disparity_visual = cv2.normalize(disparity,disparity, alpha=0, beta=255, norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_8U)
    cv2.imshow("ima",disparity_visual)
    cv2.imshow("R", imgR)
    cv2.imshow("L", imgL)
    # cv2.fastNlMeansDenoising(imgR,None,3,7,21)
    # cv2.imshow("2", imgR)
    char = cv2.waitKey(1)
    if (char == 27):
        break

cv2.destroyAllWindows()
# np.savetxt("ar.txt",disparity)
# plt.imshow(disparity,'gray')
# plt.show()