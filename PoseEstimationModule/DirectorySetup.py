import os

baseDirectory = 'E:\Thesis\Mediapipe Tutorial'
keyPointsStoreDirectory = 'Keypoints'
imageStoreDirectory = 'Images'
videoStoreDirectory = 'Videos'
signListDirectory = 'SignList'

KeyPointsStoreDirectory = os.path.join(baseDirectory, keyPointsStoreDirectory)
ImageStoreDirectory = os.path.join(baseDirectory, imageStoreDirectory)
VideoStoreDirectory = os.path.join(baseDirectory, videoStoreDirectory)
SignListDirectory = os.path.join(baseDirectory, signListDirectory)

DataDirectories = [KeyPointsStoreDirectory, ImageStoreDirectory, VideoStoreDirectory, SignListDirectory]


if __name__ == '__main__':
    for directory in DataDirectories:
        if not os.path.exists(directory):
            os.mkdir(directory)


