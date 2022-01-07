import cv2 
import numpy as np
from matplotlib import pyplot as plt

image = cv2.imread('C:/users/lolly/OneDrive/Documents/UCLA Textbooks/180DA-WarmUp/detective-conan.jpg')
conversions = {
    'gray': cv2.COLOR_BGR2GRAY,
    'RGB': cv2.COLOR_BGR2RGB,
    'HSV': cv2.COLOR_BGR2HSV
}

def convertColorScheme(scheme): 
    convertedImage = cv2.cvtColor(image, conversions[scheme])
    cv2.imwrite('C:/users/lolly/OneDrive/Documents/UCLA Textbooks/180DA-WarmUp/detective-conan-' + scheme + '.jpg', convertedImage)

def thresholding():
    # https://docs.opencv.org/4.x/d7/d4d/tutorial_py_thresholding.html
    image = cv2.imread('C:/users/lolly/OneDrive/Documents/UCLA Textbooks/180DA-WarmUp/detective-conan-gray.jpg', 0)
    ret,thresh1 = cv2.threshold(image, 127, 255, cv2.THRESH_BINARY)
    ret,thresh2 = cv2.threshold(image, 127, 255, cv2.THRESH_BINARY_INV)  
    ret,thresh3 = cv2.threshold(image, 127, 255, cv2.THRESH_TRUNC)
    ret,thresh4 = cv2.threshold(image, 127, 255, cv2.THRESH_TOZERO)
    ret,thresh5 = cv2.threshold(image, 127, 255, cv2.THRESH_TOZERO_INV)

    titles = ['Original Image', 'BINARY', 'BINARY_INV', 'TRUNC', 'TOZERO', 'TOZERO_INV']
    images = [image, thresh1, thresh2, thresh3, thresh4, thresh5]

    for i in range(6):
        plt.subplot(2,3,i+1),plt.imshow(images[i], 'gray', vmin=0, vmax=255)
        plt.title(titles[i])
        plt.xticks([]),plt.yticks([])

    # plt.show()
    plt.savefig('detective-conan-gray-thresholds.png')

def main():
    # convertColorScheme('gray')
    # convertColorScheme('RGB')
    # convertColorScheme('HSV')
    thresholding()

if __name__ == '__main__':
    main() 

