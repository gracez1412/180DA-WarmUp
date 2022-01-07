import cv2 
image = cv2.imread("C:/users/lolly/OneDrive/Documents/UCLA Textbooks/180DA-WarmUp/detective-conan.jpg")
conversions = {
    "gray": cv2.COLOR_BGR2GRAY,
    "RGB": cv2.COLOR_BGR2RGB,
    "HSV": cv2.COLOR_BGR2HSV
}

def convertColorScheme(scheme): 
    convertedImage = cv2.cvtColor(image, conversions[scheme])
    cv2.imwrite("C:/users/lolly/OneDrive/Documents/UCLA Textbooks/180DA-WarmUp/detective-conan-" + scheme + ".jpg", convertedImage)

def main():
    convertColorScheme("gray")
    convertColorScheme("RGB")
    convertColorScheme("HSV")

if __name__ == "__main__":
    main() 

