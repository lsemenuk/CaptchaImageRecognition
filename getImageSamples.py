import itertools
import os
import numpy as np
import cv2
import glob

imgexts = ['*.jpg', '*.png'] #set file types to be globbed

def getFilenames(exts):
    #os.chdir('/Directory/to/Documents/pictures")
    fnames = [glob.glob(ext) for ext in exts]
    fnames = list(itertools.chain.from_iterable(fnames))
    return fnames

def ctrSrt(cntrs):
    for i in range(len(cntrs)):
        for j in range(len(cntrs) - 1):
            coordsi = cv2.boundingRect(cntrs[j])
            coordsj = cv2.boundingRect(cntrs[j+1])
            if (coordsi[0] > coordsj[0]):
                cntrs[j+1], cntrs[j] = cntrs[j], cntrs[j+1]

imNum = 0
for fname in getFilenames(imgexts):
    img = cv2.imread(fname, 0) #loads as gray scale
    img = cv2.GaussianBlur(img,(3,3),0)
    backup = img.copy()
    (thresh, backup) = cv2.threshold(backup, 128, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
    backup = 255-backup #invert colors

    #room for character recognition improvement
    kernel = np.ones((5,1),np.uint8)
    erosion = cv2.morphologyEx(backup, cv2.MORPH_CLOSE, kernel)
    erosion = cv2.morphologyEx(backup, cv2.MORPH_OPEN, kernel)


    contours, heirarchy = cv2.findContours(erosion, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    threshHoldArea = 40 #filter out results that are possibly too ssmall
    rectsToCrop = [] #storing good contours
    for i, contour in enumerate(contours):
        area = cv2.contourArea(contour)
        if(area > threshHoldArea):
            rectsToCrop.append(contour)
            x, y, w, h = cv2.boundingRect(contour)
            #cv2.rectangle(img, (x, y), (x + w, y + h), (255, 255, 0), 1)
            #cv2.imshow("test", img)
            #cv2.waitKey()

    ctrSrt(rectsToCrop) #sorted list of contours from low x coord to high x coord to correspong the original imgages name
    if (len(rectsToCrop) == 5):
        for letter in range(len(rectsToCrop)):
            x, y, w, h = cv2.boundingRect(rectsToCrop[letter])
            path = '/Users/logansemenuk/Documents/Captcha Beater/Cropped Samples/' + str(fname[letter]) #assuming folders for desired outputs are already created
            cv2.imwrite(os.path.join(path, str(imNum) + ".jpg"), img[y: y+h, x: x+w].copy()) #cropping captcha at each character
            imNum += 1 #naming imgs using numbers to avoid duplicates

