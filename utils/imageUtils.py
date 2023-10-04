import numpy as np
from PIL import Image
from PyQt5.QtGui import QImage, QPixmap
from numpy import ndarray
import cv2
import os


# 计算两点之间的距离
def eucliDist(A,B,v):
    x_f,x,x_b=A[0],A[1],A[2]
    y_f,y,y_b=B[0],B[1],B[2]
    d_f=np.sqrt(np.power((x - x_f), 2)+np.power((y - y_f), 2))
    d_b=np.sqrt(np.power((x - x_b), 2)+np.power((y - y_b), 2))
    return d_f/16.7<v and d_b/16.7<v

def get_points(i,X,Y):
    x=X[i]
    y=Y[i]
    length=len(X)
    if i==0:
        x_f=0
        y_f=0
    else:
        x_f=X[i-1]
        y_f=Y[i-1]
    if i==length-1:
        x_b=0
        y_b=0
    else:
        x_b=X[i+1]
        y_b=Y[i+1]
    x_list=[x_f,x,x_b]
    y_list=[y_f,y,y_b]
    return x_list,y_list
def filt_points(data,th):
    index=np.where(data>0)
    X=index[0]
    Y=index[1]
    length=len(X)
    filt_X=[]
    filt_Y=[]
    for i in range(length):
        x_list,y_list=get_points(i,X,Y)
        point=eucliDist(x_list,y_list,th)
        if not point:
            filt_X.append(X[i])
            filt_Y.append(Y[i])
    filt_index=(np.array(filt_X),np.array(filt_Y))
    data[filt_index]=0
    return data

def createPixmapFromArray(img: ndarray) -> QPixmap:
    height, width = img.shape[:2]
    if len(img.shape) == 2:
        pixelSize = 1
        fmt = QImage.Format_Grayscale8
    elif len(img.shape) == 3:
        pixelSize = 3
        fmt = QImage.Format_RGB888
    else:
        raise Exception(f"wrong image shape: {img.shape}")
    qImg = QImage(img.data, width, height, pixelSize * width, fmt)
    return QPixmap(qImg)


def getImageFileSize(file: str):
    img = Image.open(file)
    return img.size


def imRead(file: str, resize,targetHeight: int = 0) -> ndarray:
    img = Image.open(file)
    if (img.mode != 'RGB'):
        img = img.convert("RGB")
    if targetHeight:
        ratio = (targetHeight / float(img.size[1]))
        wSize = int((float(img.size[0]) * float(ratio)))
        img = img.resize((wSize, targetHeight), Image.ANTIALIAS)
    scale=1.0
    if resize:
        hSize = int((float(img.size[1]) * float(resize)))
        wSize = int((float(img.size[0]) * float(resize)))
        img = img.resize((wSize, hSize), Image.ANTIALIAS)
    npImg = np.array(img)
    if len(npImg.shape) == 2:
        npImg = np.stack((npImg,) * 3, axis=-1)
    return npImg


def drawBBoxesOnImage(image: np.ndarray, bboxes, scaleFactor: float = 1.) -> np.ndarray:
    r"""scaleFactor stands for (display size/image size)"""
    for label in bboxes:
        x1, y1, x2, y2 = [int(i * scaleFactor + 0.5) for i in label["bbox"]]
        cv2.rectangle(img=image, pt1=(x1, y1), pt2=(x2, y2), color=(0, 0, 255))
    return image


def heatmapColormap(image: np.ndarray, code) -> np.ndarray:
    r"""The Input Image should be single channel 0-1 float.
    The output is a 3-channel BGR(Not RGB) 0-255 uint8 image.
    """
    return cv2.applyColorMap((image * 255).astype(np.uint8), code)


def superimposeHeatmapToImage(heatmap: np.ndarray, image: np.ndarray) -> np.ndarray:
    assert heatmap.shape[:2] == image.shape[:2]
    # if len(image.sha)
    return cv2.addWeighted(image, 0.7, heatmap, 0.3, 0)

def pointToImage(onehot: np.ndarray, image: np.ndarray) -> np.ndarray:
    assert onehot.shape[:2] == image.shape[:2]
    # if len(image.sha)
    image[np.where(onehot == 1)] = [0, 255, 0]
    return image

def pointToHeatmap(pointList, gaussianSize=99, normalize=True, heatmapShape=(800, 800)):
    canvas = np.zeros(heatmapShape)
    for p in pointList:
        if p[1] < heatmapShape[0] and p[0] < heatmapShape[1]:
            canvas[p[1]][p[0]] = 1
    canvas = canvas.transpose((2, 0, 1))[0]
    #canvas=filt_points(canvas, th=1)
    onehot=canvas.astype(np.uint8)
    canvas=np.stack((canvas,canvas,canvas))
    canvas = canvas.transpose((1,2,0))
    g = cv2.GaussianBlur(canvas, (gaussianSize, gaussianSize), 0, 0)
    if normalize:
        g = cv2.normalize(g, None, alpha=0, beta=1,
                          norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_32F)
    return heatmapColormap(g, cv2.COLORMAP_JET),g,onehot


def crossHair(img: ndarray, center: tuple) -> ndarray:
    c = (255,0,0)
    upper = (center[0] + 40, center[1])
    lower = (center[0] - 40, center[1])
    left = (center[0], center[1] - 40)
    right = (center[0], center[1] + 40)
    cv2.circle(img, center, radius=30, color=c, thickness=3)
    cv2.line(img, pt1=center, pt2=upper, color=c, thickness=3)
    cv2.line(img, pt1=center, pt2=lower, color=c, thickness=3)
    cv2.line(img, pt1=center, pt2=left, color=c, thickness=3)
    cv2.line(img, pt1=center, pt2=right, color=c, thickness=3)
    return img
