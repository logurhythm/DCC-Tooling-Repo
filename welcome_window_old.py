import sys
import subprocess
from PyQt5.QtWidgets import QWidget, QApplication, QFrame, QSplitter, QTextBrowser, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout, QFileDialog, QLabel
from PyQt5.QtGui import QImage, QPixmap, QDesktopServices, QPalette
from PyQt5.QtCore import QRect
import qdarkstyle
import cv2
import settings


class WelcomeWindow(QWidget):
    
    def __init__(self):

            super(WelcomeWindow, self).__init__()
            self.setWindowTitle("The Collector")
            appImage = self.show_image(settings.small_icon_path)
            menuFrame = QFrame()
            self.setFixedSize(450, 300)
            
            label4 = QLabel(self)
            label4.setOpenExternalLinks(True)
            label4.setText("<a href=" + settings.help_path + ">Help</a>")
            label4.setAlignment(Qt.AlignBottom)
            label4.setToolTip('Collector Design Documentation')

            # Splitter Widgets
            splitter1 = QSplitter(Qt.Horizontal)
            splitter1.addWidget(appImage)
            splitter1.addWidget(menuFrame)
            splitter1.setSizes([30, 200])
            splitter1.setContentsMargins(0,0,0,0)
            for i in range(splitter1.count()):
                splitter1.handle(i).setEnabled(False)
        
            # LineEdit Widgests
            self.edit = QLineEdit()
            self.edit.setGeometry(QRect(90, 260, 291, 41))
            self.edit.setPlaceholderText("Enter File Location")
            
            # Button Widgets
            self.projectBrowser = QPushButton("Open Project")
            self.projectBrowser.setGeometry(QRect(150, 420, 161, 31))
            self.newProject = QPushButton("New Project")
            self.newProject.setGeometry(QRect(150, 420, 161, 31))
            self.exitButton = QPushButton("Exit")
            
            # Layout widgets
            layout = QVBoxLayout()
            layout.addWidget(self.edit)
            layout.addWidget(self.projectBrowser)
            layout.addWidget(self.newProject)
            layout.addWidget(self.exitButton)
            layout.setContentsMargins(30,0,0,0)
            menuFrame.setLayout(layout)

            h_box = QHBoxLayout()
            h_box.addWidget(splitter1)
            h_box.addWidget(label4)
            h_box.setContentsMargins(0,0,0,0)
            self.setLayout(h_box)
            
            # Add button signal to greetings slot
            self.projectBrowser.clicked.connect(self.openBrowser)
            self.newProject.clicked.connect(self.openNewProject)
            self.exitButton.clicked.connect(self.close)
            
    # Greets the user
    def openBrowser(self):
        #need to figure out how to launch from the browser window or accept input address
        file_name = QFileDialog.getOpenFileName(self,'Open File', r'C:')
        self.edit.setText(file_name[0])
        # Confirmation Test: Comment out to disable
        (print("Path Selected : " + str(file_name[0])))
    
    def openNewProject(self):
        # Confirmation Test: Comment out to disable
        print(self.newProject.text() + " was Selected")

    #Functions needed to show the image on the left side of the launcher window. 
    def show_image(self, image_path):
        image_frame = QLabel()
        image = cv2.imread(image_path, cv2.IMREAD_COLOR)
        frame = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        image = QImage(frame, frame.shape[1], frame.shape[0], frame.strides[0], QImage.Format_RGB888)
        image_frame.setPixmap(QPixmap.fromImage(image))
        #this doesnt make the image scale correctly
        #image_frame.setScaledContents(True)
        return image_frame


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
    form = WelcomeWindow()
    form.show()
    sys.exit(app.exec_())
        
    