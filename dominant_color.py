import cv2
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans

def find_histogram(clt):
    numLabels = np.arange(0, len(np.unique(clt.labels_)) + 1)
    (hist, _) = np.histogram(clt.labels_, bins=numLabels)

    hist = hist.astype("float")
    hist /= hist.sum()
    
    max_value = max(hist)

    return np.argmax(hist)

def plot_colors2(hist, centroids):
    bar = np.zeros((50, 300, 3), dtype="uint8")
    startX = 0

    for(percent, color) in zip(hist, centroids):
        # plot the relative percentage of each cluster
        endX = startX + (percent * 300)
        cv2.rectangle(bar, (int(startX), 0), (int(endX), 50), color.astype("uint8").tolist(), -1)
        startX = endX

    # return the bar chart
    return bar

def main():
    # img = cv2.imread('C:/users/lolly/OneDrive/Documents/UCLA Textbooks/180DA-WarmUp/Images/detective-conan.jpg')
    # img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    # img = img.reshape((img.shape[0] * img.shape[1], 3)) # represent as row*column,channel number
    # clt = KMeans(n_clusters=3)
    # clt.fit(img)

    # print(clt.cluster_centers_)
    # hist = find_histogram(clt)
    # bar = plot_colors2(hist, clt.cluster_centers_)

    # plt.axis("off")
    # plt.imshow(bar)
    # plt.show()
    
    range_above = 20
    range_below = 20

    cap = cv2.VideoCapture(0)
    cap.set(3,160)
    cap.set(4,80)

    while(True):
        # capture frame-by-frame
        ret, frame = cap.read()

        # our operations on the frame code here
        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        image_reshaped = image.copy()
        image_reshaped = image_reshaped.reshape((image.shape[0] * image.shape[1], 3))
        clt = KMeans(n_clusters=3)
        clt.fit(image_reshaped)

        index = find_histogram(clt)
        color = clt.cluster_centers_[index]
        color = (int(color[0]), int(color[1]), int(color[2]))
        lower_color_bounds = (color[0]-range_below, color[1]-range_below, color[2]-range_below)
        upper_color_bounds = (color[0]+range_above, color[1]+range_above, color[2]+range_above)
        
        mask = cv2.inRange(image, lower_color_bounds, upper_color_bounds)

        mask_rgb = cv2.cvtColor(mask, cv2.COLOR_GRAY2RGB)
        image = mask_rgb & image
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        contours, hierarchy = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        for cnt in contours:
            x, y, w, h = cv2.boundingRect(cnt)
            if(w > 20 & h > 10):
                cv2.rectangle(image, (x,y), (x+w,y+h),(255,255,255),2)
                coord_str = '(' + str(color[0]) + ', ' + str(color[1]) + ',' + str(color[2]) + ')'
                cv2.putText(image, coord_str, (x, y+h-10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,255,255), 2)

        # display the resulting frame
        cv2.imshow('frame', image)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    main()