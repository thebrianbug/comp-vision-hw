# Brian McIlwain
# Comp vision hw2

import cv2
import numpy as np

def is_Grayscale(img):
    for x in range(0, img.shape[0]):
      for y in range(0, img.shape[1]):
        if img[x, y, 0] != img[x, y, 1] or img[x, y, 1] != img[x, y, 2]:
            return False

    return True

def my_Normalize(img):
    # if already grayscale has no effect
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    img = cv2.normalize(src=img, dst=img, alpha=0, beta=1, norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_64F)

    return img

def GaussianFilter(sigma):
    halfSize = 3 * round(sigma)
    maskSize = 2 * round(halfSize) + 1 
    print halfSize, maskSize
    mat = np.ones((maskSize,maskSize)) / (float)( 2 * np.pi * (sigma**2))
    xyRange = np.arange(-halfSize, halfSize+1)
    xx, yy = np.meshgrid(xyRange, xyRange)    
    x2y2 = (xx**2 + yy**2)    
    exp_part = np.exp(-(x2y2/(2.0*(sigma**2))))
    mat = mat * exp_part

    return mat

def my_DerivativesOfGaussian(img, sigma):
    Gsigma = GaussianFilter(sigma)

    Sx = np.matrix([[1, 0, -1],
                    [2, 0, -2],
                    [1, 0, -1]])

    Sy = np.matrix([[1, 2, 1],
                    [0, 0, 0],
                    [-1, -2, -1]])

    # Gx = Gsigma * Sx
    Gx = cv2.filter2D(Gsigma, -1, Sx)
    Gy = cv2.filter2D(Gsigma, -1, Sy)
    
    # Ix = img * Gx
    Ix = cv2.filter2D(img, -1, Gx)
    Iy = cv2.filter2D(img, -1, Gy)

    Ixn = np.ones(Ix.shape[0])
    Iyn = np.ones(Iy.shape[0])

    Ixn = cv2.normalize(src=Ix, dst=Ixn, alpha=0, beta=1, norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_64F)
    Iyn = cv2.normalize(src=Iy, dst=Iyn, alpha=0, beta=1, norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_64F)

    cv2.imshow('Ix_Normalized', Ixn)
    cv2.imshow('Iy_Normalized', Iyn)

    return Ix, Iy

img = cv2.imread('hw2/testImages/TestImg1.jpg')

img = my_Normalize(img)
cv2.imshow('my_Normalize', img)

Ix,Iy = my_DerivativesOfGaussian(img, .8)

cv2.waitKey(0)
cv2.destroyAllWindows()