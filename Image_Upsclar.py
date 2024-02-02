# Refactoring and optimizing the provided code

from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QLabel, QComboBox, QFileDialog
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtCore import Qt
import cv2
import os
import numpy as np

class ImageUpscaler(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.layout = QVBoxLayout()
        self.createLoadButton()
        self.createOriginalImageLabel()
        self.createUpscaledImageLabel()
        self.createResolutionComboBox()
        self.createUpscaleButton()
        self.setLayout(self.layout)

    def createLoadButton(self):
        self.btnLoad = QPushButton('Load Image')
        self.btnLoad.clicked.connect(self.loadImage)
        self.layout.addWidget(self.btnLoad)

    def createOriginalImageLabel(self):
        self.labelOriginal = QLabel(self)
        self.layout.addWidget(self.labelOriginal)

    def createUpscaledImageLabel(self):
        self.labelUpscaled = QLabel(self)
        self.layout.addWidget(self.labelUpscaled)

    def createResolutionComboBox(self):
        self.comboBoxResolution = QComboBox(self)
        self.comboBoxResolution.addItems(["1080p", "2K", "4K"])
        self.layout.addWidget(self.comboBoxResolution)

    def createUpscaleButton(self):
        self.btnUpscale = QPushButton('Upscale Image')
        self.btnUpscale.clicked.connect(self.upscaleImage)
        self.layout.addWidget(self.btnUpscale)

    def loadImage(self):
        fname, _ = QFileDialog.getOpenFileName(self, 'Open file', '/home', "Image files (*.jpg *.png)")
        if fname:
            self.filePath = fname
            self.originalPixmap = QPixmap(fname)
            self.labelOriginal.setPixmap(self.originalPixmap)
            self.originalImage = cv2.imread(fname)

    def upscaleImage(self):
        resolution_map = {
            "1080p": (1920, 1080),
            "2K": (2560, 1440),
            "4K": (3840, 2160)
        }
        resolution = self.comboBoxResolution.currentText()
        target_width, target_height = resolution_map.get(resolution, (1920, 1080))

        try:
            # Resize the image to the selected resolution
            upscaledImage = cv2.resize(self.originalImage, (target_width, target_height), interpolation=cv2.INTER_LINEAR)

            # Apply sharpening filter
            upscaledImage = self.applySharpeningFilter(upscaledImage)

            # Convert for display and show
            self.displayUpscaledImage(upscaledImage)

            # Save the upscaled image
            self.saveUpscaledImage(upscaledImage)
        except Exception as e:
            print(f"Error in upscaling image: {e}")

    def applySharpeningFilter(self, image):
        gaussian_blur = cv2.GaussianBlur(image, (0, 0), 3)
        return cv2.addWeighted(image, 1.5, gaussian_blur, -0.5, 0)

    def displayUpscaledImage(self, upscaledImage):
        qImg = QImage(upscaledImage.data, upscaledImage.shape[1], upscaledImage.shape[0], QImage.Format_RGB888).rgbSwapped()
        upscaledPixmap = QPixmap.fromImage(qImg)
        self.labelUpscaled.setPixmap(upscaledPixmap)

    def saveUpscaledImage(self, upscaledImage):
        desktopPath = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')
        savePath = os.path.join(desktopPath, 'upscaled_image.jpg')
        cv2.imwrite(savePath, upscaledImage)

# Uncomment these lines to run the application
if __name__ == '__main__':
    app = QApplication([])
    ex = ImageUpscaler()
    ex.show()
    app.exec_()
