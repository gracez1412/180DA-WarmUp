import cv2 
import numpy as np
from matplotlib import pyplot as plt

# image = cv2.imread('C:/users/lolly/OneDrive/Documents/UCLA Textbooks/180DA-WarmUp/detective-conan.jpg')
conversions = {
    'gray': cv2.COLOR_BGR2GRAY,
    'RGB': cv2.COLOR_BGR2RGB,
    'HSV': cv2.COLOR_BGR2HSV
}

def convertColorScheme(file, scheme): 
    image = cv2.imread(file)
    convertedImage = cv2.cvtColor(image, conversions[scheme])
    cv2.imwrite('C:/users/lolly/OneDrive/Documents/UCLA Textbooks/180DA-WarmUp/flowers-' + scheme + '.jpg', convertedImage)

def thresholding(file, type):
    if(type == "fixed"):
        # https://docs.opencv.org/4.x/d7/d4d/tutorial_py_thresholding.html
        image = cv2.imread(file, 0)
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
        plt.savefig('flowers-thresholds.png')

    elif (type == "adaptive"):
        image = cv2.imread(file, 0)
        image = cv2.medianBlur(image, 5)
        ret, thresh1 = cv2.threshold(image, 127, 255, cv2.THRESH_BINARY)
        thresh2 = cv2.adaptiveThreshold(image, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 11, 2)
        thresh3 = cv2.adaptiveThreshold(image, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)

        titles = ['Original Image', 'Global Thresholding (v = 127)', 'Adaptive Mean Thresholding', 'Adaptive Gaussian Thresholding']
        images = [image, thresh1, thresh2, thresh3]

        for i in range(4):
            plt.subplot(2,2,i+1),plt.imshow(images[i],'gray')
            plt.title(titles[i])
            plt.xticks([]),plt.yticks([])
        
        # plt.show()
        plt.savefig('flowers-adaptive-thresholds.png')

def edgeDetection(file):
    image = cv2.imread(file, 0)
    edges = cv2.Canny(image,100,200)

    plt.subplot(121),plt.imshow(image,cmap = 'gray')
    plt.title('Original Image'), plt.xticks([]), plt.yticks([])
    plt.subplot(122),plt.imshow(edges,cmap = 'gray')
    plt.title('Edge Image'), plt.xticks([]), plt.yticks([])

    # plt.show()
    plt.savefig('detective-conan-edge.png')

def templateMatching(file, type):
    if (type == 'single'):
        image = cv2.imread(file,0)
        image2 = image.copy()
        template = cv2.imread('C:/users/lolly/OneDrive/Documents/UCLA Textbooks/180DA-WarmUp/detective-conan-template.jpg',0)
        w, h = template.shape[::-1]
        # All the 6 methods for comparison in a list
        methods = ['cv2.TM_CCOEFF', 'cv2.TM_CCOEFF_NORMED', 'cv2.TM_CCORR',
                    'cv2.TM_CCORR_NORMED', 'cv2.TM_SQDIFF', 'cv2.TM_SQDIFF_NORMED']

        plt.figure(0)
        for i in range(6):
            image = image2.copy()
            method = eval(methods[i])
            # Apply template Matching
            res = cv2.matchTemplate(image,template,method)
            min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
            # If the method is TM_SQDIFF or TM_SQDIFF_NORMED, take minimum
            if method in [cv2.TM_SQDIFF, cv2.TM_SQDIFF_NORMED]:
                top_left = min_loc
            else:
                top_left = max_loc
            bottom_right = (top_left[0] + w, top_left[1] + h)
            cv2.rectangle(image,top_left, bottom_right, 255, 2)
            plt.subplot2grid((6,2),(i,0)),plt.imshow(res,cmap = 'gray')
            plt.title(methods[i]), plt.xticks([]), plt.yticks([])
            plt.subplot2grid((6,2),(i,1)),plt.imshow(image,cmap = 'gray')
            plt.title('Detected Point'), plt.xticks([]), plt.yticks([])
            plt.suptitle(methods[i])
            
        # plt.show()
        plt.savefig('detective-conan-template-matching-single.png')

    elif(type == 'multiple'):
        image_rgb = cv2.imread(file)
        image_gray = cv2.cvtColor(image_rgb, cv2.COLOR_BGR2GRAY)
        template = cv2.imread('C:/users/lolly/OneDrive/Documents/UCLA Textbooks/180DA-WarmUp/flowers-2-template.jpg',0)
        w, h = template.shape[::-1]
        res = cv2.matchTemplate(image_gray,template,cv2.TM_CCOEFF_NORMED)
        threshold = 0.8
        loc = np.where( res >= threshold)
        for pt in zip(*loc[::-1]):
            cv2.rectangle(image_rgb, pt, (pt[0] + w, pt[1] + h), (0,0,255), 2)
        cv2.imwrite('res.png',image_rgb)

def convexHull(file):
    # https://learnopencv.com/convex-hull-using-opencv-in-python-and-c/
    image = cv2.imread(file, cv2.IMREAD_COLOR)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blur = cv2.blur(gray, (5,5))
    ret, thresh = cv2.threshold(blur, 127, 255, cv2.THRESH_BINARY)

    # contour retrieval mode, contour approximation method
    contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    # print(contours)

    # create hull array for convex hull points
    hull = []

    # calculate points for each contour
    for i in range(len(contours)):
        # creating convex hull object for each contour
        hull.append(cv2.convexHull(contours[i],False))

    # create an empty black image
    # drawing = np.zeros((thresh.shape[0], thresh.shape[1], 3), np.uint8)

    # draw contours and hull points 
    for i in range(len(contours)):
        color_contours = (0, 0, 255)    # red for contours
        color = (255, 0 , 0)    # blue for convex hull
        # draw ith contour
        cv2.drawContours(image, contours, i, color_contours, 1, 8, hierarchy)
        # draw ith convex hull object
        cv2.drawContours(image, hull, i, color, 1, 8)

    cv2.imwrite('C:/users/lolly/OneDrive/Documents/UCLA Textbooks/180DA-WarmUp/Images/hand-convex-hull-2.jpg', image)


def main():
    file = 'C:/users/lolly/OneDrive/Documents/UCLA Textbooks/180DA-WarmUp/Images/hand.jpg'
    # convertColorScheme(file, 'gray')
    # convertColorScheme(file, 'RGB')
    # convertColorScheme(file, 'HSV')
    # thresholding(file, "adaptive")
    # edgeDetection(file)
    # templateMatching(file, 'multiple')
    convexHull(file)

if __name__ == '__main__':
    main() 

