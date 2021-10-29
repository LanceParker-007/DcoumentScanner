from cv2 import cv2
from tkinter import *
import cv2
from PIL import Image
from PIL import ImageTk
from tkinter import filedialog, Tk
import utlis
import numpy as np


def selectImage():
    # Grab a reference  to the image panels
    global panelA, panelB
    # open a file chooser dialog and allow the user to select
    # an input image
    path = filedialog.askopenfilename()
    # Ensure a file path was selected
    if(len(path) > 0):
        # load the image from disk, convert it to grayscale,
        # and detect
        # edges in it
        widImg = 480
        heiImg = 660
        image = cv2.imread(path)
        image = cv2.resize(image, (widImg, heiImg))
        imgContours = image.copy()
        imgBigContour = image.copy()
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        blur = cv2.GaussianBlur(gray, (3, 3), 0)
        edged = cv2.Canny(blur, 50, 50)
        # edged = cv2.addWeighted(edged, 1.5, image, -0.5, 0, image)

        # FInd and draw all contours
        contours, hierarchy = cv2.findContours(
            edged, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cv2.drawContours(imgContours, contours, -1, (0, 255, 0), 10)

        # Find the Biggest Contour
        biggest, maxArea = utlis.biggestContour(contours)
        if(biggest.size != 0):
            biggest = utlis.reorder(biggest)
            # Draw the biggest contour
            cv2.drawContours(imgBigContour, biggest, -1, (0, 255, 0), 20)
            imgBigContour = utlis.drawRectangle(
                imgBigContour, biggest, 2)
            pts1 = np.float32(biggest)
            pts2 = np.float32(
                [[0, 0], [widImg, 0], [0, heiImg], [widImg, heiImg]])
            matrix = cv2.getPerspectiveTransform(pts1, pts2)
            imgWarped = cv2.warpPerspective(
                image, matrix, (widImg, heiImg))
            # Remove 20 pixels from each side
            imgWarped = imgWarped[10:imgWarped.shape[0] -
                                  10, 10:imgWarped.shape[1]-10]
            imgWarped = cv2.resize(imgWarped, (widImg, heiImg))
            imgWarped = cv2.cvtColor(imgWarped, cv2.COLOR_BGR2RGB)
            # imgWarped = cv2.addWeighted(imgBigContour, 2, blur, -1, 0, blur)
        # edged = imgWarped
        # OpenCV represents image in BGR order; Howeve PIL represents
        # image in RGB order, so we need to swap the channels
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        # image = cv2.addWeighted(image, 1.5, blur, -0.5, 0,)

        # Convert the images to PIL format...
        image = Image.fromarray(image)
        imgWarped = Image.fromarray(imgWarped)

        # ...and then to IMageTk format
        image = ImageTk.PhotoImage(image)
        imgWarped = ImageTk.PhotoImage(imgWarped)

        # if the panels are None, initialize them
        if(panelA is None or panelB is None):
            # the first panel will store our original image
            panelA = Label(root, image=image, bd=10,
                           bg='cyan', relief=GROOVE)
            panelA.image = image
            panelA.place(x=0, y=100)
            # while the second panel will store the edge map
            panelB = Label(root, image=imgWarped, bd=10,
                           bg='red', relief=GROOVE)
            panelB.image = imgWarped
            panelB.place(x=500, y=100)
            #  otherwise, update the image panels
        else:
            panelA.configure(image=image)
            panelB.configure(image=imgWarped)
            panelA.image = image
            panelB.image = imgWarped

# initialize the window toolkit along with the two image panels


root = Tk()
panelA = None
panelB = None
me = Menu(root)
root.config(menu=me, background='yellowgreen')
root.geometry("1512x780+0+0")
filemenu = Menu(me)
me.add_cascade(label="File ", menu=filemenu)
filemenu.add_command(label="New")
filemenu.add_separator()
filemenu.add_command(label="Exit", command=root.quit)
helpmenu = Menu(me)
me.add_cascade(label="Help", menu="helpmenu")
# create a button, then when pressed, will trigger a file chooser
# dialog and allow the user to select an input image; then add the
# Frame_1 = LabelFrame(root, text='Orginal')
btn = Button(root, text="Select an image", command=selectImage,
             bd=10, bg='orange', padx=10, pady=10, relief=GROOVE, font='arial 25 bold')
btn.place(x=0, y=0, relwidth=1)
# kick off the GUI
root.mainloop()
