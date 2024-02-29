from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QLabel, QComboBox, QFileDialog
from PyQt5.QtGui import QPixmap, QImage
import cv2
import os

class ImageUpscaler(QWidget):
    RESOLUTION_MAP = {
        "1080p": (1920, 1080),
        "2K": (2560, 1440),
        "4K": (3840, 2160)
    }

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.layout = QVBoxLayout()
        self.createWidgets()
        self.setLayout(self.layout)

    def createWidgets(self):
        self.btnLoad = QPushButton('Load Image')
        self.btnLoad.clicked.connect(self.loadImage)
        self.layout.addWidget(self.btnLoad)

        self.labelOriginal = QLabel(self)
        self.layout.addWidget(self.labelOriginal)

        self.labelUpscaled = QLabel(self)
        self.layout.addWidget(self.labelUpscaled)

        self.comboBoxResolution = QComboBox(self)
        self.comboBoxResolution.addItems(self.RESOLUTION_MAP.keys())
        self.layout.addWidget(self.comboBoxResolution)

        self.btnUpscale = QPushButton('Upscale Image')
        self.btnUpscale.clicked.connect(self.upscaleImage)
        self.layout.addWidget(self.btnUpscale)

    def loadImage(self):
        fname, _ = QFileDialog.getOpenFileName(self, 'Open file', '/home', "Image files (*.jpg *.png)")
        if fname:
            self.filePath = fname
            self.displayImage(self.filePath, self.labelOriginal)
            self.originalImage = cv2.imread(fname)

    def upscaleImage(self):
        try:
            resolution = self.comboBoxResolution.currentText()
            target_width, target_height = self.RESOLUTION_MAP.get(resolution, self.RESOLUTION_MAP["1080p"])
            new_width, new_height = self.calculateAspectRatio(self.originalImage, target_width, target_height)
            upscaledImage = self.resizeImage(self.originalImage, new_width, new_height)
            upscaledImage = self.applySharpeningFilter(upscaledImage)
            self.displayImage(upscaledImage, self.labelUpscaled, is_cv_image=True)
            self.saveUpscaledImage(upscaledImage)
        except Exception as e:
            print(f"Error in upscaling image: {e}")

    def calculateAspectRatio(self, image, target_width, target_height):
        height, width, _ = image.shape
        scaling_factor = min(target_width / width, target_height / height)
        new_width = int(width * scaling_factor)
        new_height = int(height * scaling_factor)
        return new_width, new_height

    def resizeImage(self, image, width, height):
        return cv2.resize(image, (width, height), interpolation=cv2.INTER_LINEAR)

    def applySharpeningFilter(self, image):
        gaussian_blur = cv2.GaussianBlur(image, (0, 0), 3)
        return cv2.addWeighted(image, 1.5, gaussian_blur, -0.5, 0)

    def displayImage(self, imagePathOrCvImage, label, is_cv_image=False):
        if is_cv_image:
            qImg = QImage(imagePathOrCvImage.data, imagePathOrCvImage.shape[1], imagePathOrCvImage.shape[0], QImage.Format_RGB888).rgbSwapped()
            pixmap = QPixmap.fromImage(qImg)
        else:
            pixmap = QPixmap(imagePathOrCvImage)
        label.setPixmap(pixmap)

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
