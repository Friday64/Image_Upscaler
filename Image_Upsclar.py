from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QLabel, QSlider, QFileDialog, QComboBox
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
        layout = QVBoxLayout()

        self.btnLoad = QPushButton('Load Image')
        self.btnLoad.clicked.connect(self.loadImage)
        layout.addWidget(self.btnLoad)

        self.labelOriginal = QLabel(self)
        layout.addWidget(self.labelOriginal)

        self.labelUpscaled = QLabel(self)
        layout.addWidget(self.labelUpscaled)

        self.comboBoxResolution = QComboBox(self)
        self.comboBoxResolution.addItems(["1080p", "2K", "4K"])
        layout.addWidget(self.comboBoxResolution)

        self.btnUpscale = QPushButton('Upscale Image')
        self.btnUpscale.clicked.connect(self.upscaleImage)
        layout.addWidget(self.btnUpscale)

        self.setLayout(layout)

    def loadImage(self):
        fname, _ = QFileDialog.getOpenFileName(self, 'Open file', '/home', "Image files (*.jpg *.png)")
        if fname:
            self.filePath = fname
            self.originalPixmap = QPixmap(fname)
            self.labelOriginal.setPixmap(self.originalPixmap)
            self.originalImage = cv2.imread(fname)

    def upscaleImage(self):
        resolution = self.comboBoxResolution.currentText()
        if resolution == "1080p":
            width, height = 1920, 1080
        elif resolution == "2K":
            width, height = 2560, 1440
        elif resolution == "4K":
            width, height = 3840, 2160

        # Resize the image to the selected resolution
        upscaledImage = cv2.resize(self.originalImage, (width, height), interpolation=cv2.INTER_LINEAR)

        # Apply sharpening filter to improve clarity
        gaussian_blur = cv2.GaussianBlur(upscaledImage, (0, 0), 3)
        upscaledImage = cv2.addWeighted(upscaledImage, 1.5, gaussian_blur, -0.5, 0)

        # Contrast enhancement using histogram equalization
        img_yuv = cv2.cvtColor(upscaledImage, cv2.COLOR_BGR2YUV)
        img_yuv[:, :, 0] = cv2.equalizeHist(img_yuv[:, :, 0])
        upscaledImage = cv2.cvtColor(img_yuv, cv2.COLOR_YUV2BGR)

        # Convert the upscaled image for display and show it in the label
        qImg = QImage(upscaledImage.data, upscaledImage.shape[1], upscaledImage.shape[0], QImage.Format_RGB888).rgbSwapped()
        upscaledPixmap = QPixmap.fromImage(qImg)
        self.labelUpscaled.setPixmap(upscaledPixmap)

        # Save the upscaled image to the desktop
        desktopPath = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')
        savePath = os.path.join(desktopPath, 'upscaled_image.jpg')  # Save as a new file
        cv2.imwrite(savePath, upscaledImage)

# Uncomment these lines to run the application
if __name__ == '__main__':
    app = QApplication([])
    ex = ImageUpscaler()
    ex.show()
    app.exec_()
