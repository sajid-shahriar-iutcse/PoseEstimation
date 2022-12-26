import os
import DirectorySetup
from PoseEstimationClass import PoseEstimation
import cv2
import numpy as np


VideoStoreDirectory = DirectorySetup.VideoStoreDirectory
KeyPointsStoreDirectory = DirectorySetup.KeyPointsStoreDirectory
ImageStoreDirectory = DirectorySetup.ImageStoreDirectory
SignListDirectory = DirectorySetup.SignListDirectory

numberOfVideos = 30
numberOfFrames = 30

# Get List of Signs from ./SignList/signList.txt
def getListOfSigns():
    signListFilePath = os.path.join(SignListDirectory, 'signList.txt')
    if os.path.exists(signListFilePath):
        signListFile = open(signListFilePath, 'r', encoding='UTF-8')
        signList = []
        for line in signListFile:
            signList.append(line)

    signListFile.close()
    return signList


#get List of Videos
def getVideoList():
    signList = getListOfSigns()
    videoList =[]
    #iterate over the sign list
    for sign in signList:
        sign = sign.split('_')
        videoName = sign[1]
        videoPath = os.path.join(VideoStoreDirectory,videoName)
        for file in os.listdir(videoPath):
            absoluteVideoPath = os.path.join(videoPath, file)
            videoList.append(absoluteVideoPath)

    return videoList


def getVideoName(absoluteVideoPath):
    videoName = absoluteVideoPath.split('\\')
    videoName = videoName[5]
    videoName = videoName.split('.')
    videoName = videoName[0]
    return videoName
def createKeyPointsSubSubDirectory(absoluteVideoPath):
    videoName = getVideoName(absoluteVideoPath)
    keypointsSubdirectory = videoName.split('_')[0]

    keypointsSubdirectory = os.path.join(KeyPointsStoreDirectory, keypointsSubdirectory)
    if not os.path.exists(keypointsSubdirectory):
        os.mkdir(keypointsSubdirectory)

    keypointsSubSubdirectory = os.path.join(keypointsSubdirectory, videoName)
    if not os.path.exists(keypointsSubSubdirectory):
        os.mkdir(keypointsSubSubdirectory)

    return (keypointsSubSubdirectory, videoName)

def createImageSubSubDirectory(absoluteVideopath):
    videoName = getVideoName(absoluteVideopath)
    imageSubdirectory = videoName.split('_')[0]

    imageSubdirectory = os.path.join(ImageStoreDirectory, imageSubdirectory)
    if not os.path.exists(imageSubdirectory):
        os.mkdir(imageSubdirectory)

    imageSubSubdirectory = os.path.join(imageSubdirectory, videoName)
    if not os.path.exists(imageSubSubdirectory):
        os.mkdir(imageSubSubdirectory)

    return (imageSubSubdirectory, videoName)

def extractKeyPointsFromVideos():
    videoList = getVideoList()
    poseEstimation = PoseEstimation()
    for video in videoList:
        #Get the video name and keypoints subdirectory
        keypointsSubSubDirectory, videoName = createKeyPointsSubSubDirectory(video)
        imageSubSubDirectory, videoName = createImageSubSubDirectory(video)

        capture = cv2.VideoCapture(video)
        count = 0
        while capture.isOpened():
            success, frame = capture.read()
            # Extract KeyPoints
            if success:
                count += 1
                keypoints = poseEstimation.extractKeyPoints(frame)

                keypointsPath = os.path.join(keypointsSubSubDirectory, videoName+'_'+str(count))
                imagePath = os.path.join(imageSubSubDirectory, videoName + '_' + str(count)+'.jpg')

                np.save(keypointsPath, keypoints)

                imagePath = os.path.join(imagePath)
                cv2.imwrite(imagePath, frame)

                cv2.imshow('VideoFeed', frame)

                key = cv2.waitKey(10)
                if key == ord('q'):
                    break

        capture.release()
        cv2.destroyAllWindows()

if __name__ == '__main__':
    extractKeyPointsFromVideos()



