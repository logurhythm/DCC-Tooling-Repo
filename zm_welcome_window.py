import sys
from PyQt5.QtWidgets import *
from PyQt5.QtWidgets import QWidget, QApplication, QFrame, QSplitter, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout, QFileDialog, QLabel
#from PyQt5.QtGui import QImage, QPixmap - Saving for later for icon stuff
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import qdarkstyle
   
class main_window(QDialog):
    
    def __init__(self): #Constructor used to instance
        super(main_window, self).__init__()
        self.setWindowTitle("Zeroth Mile Portal")  #Title for window
        self.setFixedSize(350,200)
        menuFrame = QFrame()
   
        # Username Label and entry box widgets
        self.runtimeVersion = self.line_edit_creation("runtimeSVNloc", "Runtime SVN URL")
        self.geometryLocation = self.combo_box_creation("Phenotype Geometry")
        self.textureLocation = self.combo_box_creation("Phenotype Texture")
        self.assetDatabase = self.line_edit_creation("Output Runtime Location", "Output Runtime Location")
        
        self.confirmButton = self.button_creation("confirmButton", "OK")
        self.cancelButton = self.button_creation("cancelButton", "Cancel")
        
        self.forceRebuildCheckBox = self.check_box_creation("Force Rebuild")
        
        layout1 = QVBoxLayout()
        layout1.addWidget(self.runtimeVersion)
        layout1.addWidget(self.geometryLocation)
        layout1.addWidget(self.textureLocation)
        layout1.addWidget(self.assetDatabase)
     
        layout1.setContentsMargins(30,0,30,0)
        layout1.setSpacing(3)
        menuFrame.setLayout(layout1)
        
        layout2 = QHBoxLayout()
        layout2.addWidget(self.confirmButton)
        layout2.addWidget(self.cancelButton)       
        
        layout3 = QGridLayout()
        layout3.addWidget(self.forceRebuildCheckBox, 2, 3)
        layout3.setSpacing(3)
        
        layout1.addLayout(layout2)
        layout1.addLayout(layout3)

        
         # Set dialog layout
        self.setLayout(layout1)
        
        self.cancelButton.clicked.connect(self.exitApp)
        self.confirmButton.clicked.connect(self.printInputsToUser)
        
    # Greets the user
    def runtimeVersionBrwoser(self):
        #need to figure out how to launch from the browser window or accept input address
        file_name = QFileDialog.getOpenFileName(self,'Open File', r'C:')
        self.edit.setText(file_name[0])
    
    def line_edit_creation(self, lineName, placeHolderText):
        theLineEdit = QLineEdit()
        theLineEdit.setGeometry(QRect(90, 260, 291, 41))
        theLineEdit.setPlaceholderText(placeHolderText)
        theLineEdit.setObjectName(lineName)
        return theLineEdit
    
    def combo_box_creation(self, phenotypeNamePlaceHolder):
        theComboBox = QComboBox()
        theComboBox.addItems(["Populated Phenotype Name Goes Here 1", "Populated Phenotype Name Goes Here 2", "Populated Phenotype Name Goes Here 3" ,"And so on and so on . . ." ])
        return theComboBox
    
    def button_creation(self, buttonName, textThatsOnTheButton):
        theButton = QPushButton(textThatsOnTheButton)
        theButton.setFixedSize(100,25)
        theButton.setObjectName(buttonName)
        return theButton
    
    def check_box_creation(self, checkBoxLabel):
        theCheckBox = QCheckBox(checkBoxLabel)
        return theCheckBox
    
    def openNewProject():
        #Open blank Collector Instance: Need to figure out how to launch an instance of the main window.
        pass
    
    def exitApp(self):
        self.close()
    
    #Input Confirmation Check
    def printInputsToUser(self):
        print("Runtime Version Entered: " + self.runtimeVersion.text())
        # print("Geomentry Location Entered: " + self.geometryLocation.text())
        # print("Texture Location Entered: " + self.textureLocation.text())
        print("Asset Database Entered: " + self.assetDatabase.text())
        

        
if __name__=='__main__':
    # Create the Qt Application (always needed)
    app = QApplication(sys.argv)
    app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5()) #sets style sheet
    
    # Create and show the form
    form = main_window()
    form.setFixedSize(350,300)
    form.show()
    # form = login_window()
    # form.show()   

# Run the main Qt loop
    sys.exit(app.exec_())
        
    