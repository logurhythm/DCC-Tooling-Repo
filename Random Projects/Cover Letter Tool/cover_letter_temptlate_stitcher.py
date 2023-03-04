import sys
import os
import cls_logic as clsl
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QRect, Qt
import qdarkstyle

TEST_DIR = r"C:"   
class main_window(QDialog):

    def __init__(self): #Constructor used to instance
        super(main_window, self).__init__()

        self.setWindowTitle("Cover Letter Temptlate Stitcher")  #Title for window
        self.setFixedSize(350,200)
        self.setWindowFlags(self.windowFlags() ^ Qt.WindowContextHelpButtonHint) #Hides ? button
        menuFrame = QFrame()
   
    #Widget Creations
        self.job_title = self.line_edit_creation("job_title", "Whats the Job Title?")
        self.company_name = self.line_edit_creation("company_name", "Whats the Company Name?")
        self.intro = self.line_edit_creation("intro", "Intro")
        self.Body = self.line_edit_creation("body", "Body")
        self.Conclusion = self.line_edit_creation("output_runtime_loc", "Output Runtime Location")
        
        self.fp_btn_intro = QPushButton("...")
        self.fp_btn_body = QPushButton("...")
        self.fp_btn_conclusion = QPushButton("...")
        self.confirmButton = self.button_creation("confirmButton", "Create")
        self.cancelButton = self.button_creation("cancelButton", "Close")
        
        self.docx = QCheckBox("docx - not yet functioning")
        self.pdf = QCheckBox("pdf - not yet functioning")

    #Layout Creations
        layout1 = QVBoxLayout()
        layout1.addWidget(self.job_title)
        layout1.addWidget(self.company_name)

        fp_layout_intro = QHBoxLayout()
        fp_layout_body = QHBoxLayout()
        fp_layout_conclusion = QHBoxLayout()
        fp_layout_intro.addWidget(self.intro)
        fp_layout_intro.addWidget(self.fp_btn_intro)
        fp_layout_body.addWidget(self.Body)
        fp_layout_body.addWidget(self.fp_btn_body)
        fp_layout_conclusion.addWidget(self.Conclusion)
        fp_layout_conclusion.addWidget(self.fp_btn_conclusion)
     
        layout1.setContentsMargins(30,0,30,0)
        layout1.setSpacing(3)
        menuFrame.setLayout(layout1)
        
        layout2 = QHBoxLayout()
        layout2.addWidget(self.confirmButton)
        layout2.addWidget(self.cancelButton)       
        
        layout3 = QHBoxLayout()
        layout3.addWidget(self.docx)
        layout3.addWidget(self.pdf)
        
        layout1.addLayout(fp_layout_intro)
        layout1.addLayout(fp_layout_body)
        layout1.addLayout(fp_layout_conclusion)
        layout1.addLayout(layout3)
        layout1.addLayout(layout2)

        
        #Set dialog layout
        self.setLayout(layout1)

        # Create Connections
        self.cancelButton.clicked.connect(self.close)
        self.fp_btn_intro.clicked.connect(self.openBrowserIntro)
        self.fp_btn_body.clicked.connect(self.openBrowserBody)
        self.fp_btn_conclusion.clicked.connect(self.openBrowserConclusion)
        self.confirmButton.clicked.connect(self.execute_cls_logic)
        
    # Widget Temptlates
    def openBrowserIntro(self):
        file_path = QFileDialog.getOpenFileName(self, "Select File", TEST_DIR, "Word (*docx)")
        if file_path:
            self.intro.setText(os.path.basename(file_path[0]))
        if clsl.TEMPLATE_LIST:
            clsl.TEMPLATE_LIST.insert(0, file_path[0])
        else:
            clsl.TEMPLATE_LIST.insert(0, file_path[0])
    def openBrowserBody(self):
        file_path = QFileDialog.getOpenFileName(self, "Select File", TEST_DIR, "Word (*docx)")
        if file_path:
            self.Body.setText(os.path.basename(file_path[0]))  
        if clsl.TEMPLATE_LIST:
            clsl.TEMPLATE_LIST.insert(1,os.path.basename(file_path[0]) )
        else:
            clsl.TEMPLATE_LIST.insert(1,os.path.basename(file_path[0]))
    def openBrowserConclusion(self):
        file_path = QFileDialog.getOpenFileName(self, "Select File", TEST_DIR, "Word (*docx)")
        if file_path:
            self.Conclusion.setText(os.path.basename(file_path[0]))
        if clsl.TEMPLATE_LIST:
            clsl.TEMPLATE_LIST.insert(2,os.path.basename(file_path[0]) )
        else:
            clsl.TEMPLATE_LIST.insert(2,os.path.basename(file_path[0]))
        
    def line_edit_creation(self, lineName, placeHolderText):
        theLineEdit = QLineEdit()
        theLineEdit.setGeometry(QRect(90, 260, 291, 41))
        theLineEdit.setPlaceholderText(placeHolderText)
        theLineEdit.setObjectName(lineName)
        return theLineEdit
    
    def button_creation(self, buttonName, textThatsOnTheButton):
        theButton = QPushButton(textThatsOnTheButton)
        theButton.setFixedSize(100,25)
        theButton.setObjectName(buttonName)
        return theButton
    
    def execute_cls_logic(self):
        companyName = self.company_name.text()
        jobtitle = self.job_title.text()
        clsl.template_list_loader(companyName, jobtitle)
    
if __name__=='__main__':
    # Create the Qt Application (always needed)
    app = QApplication(sys.argv)
    app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5()) #sets style sheet
    
    # Create and show the form
    form = main_window()
    form.setFixedSize(350,300)
    form.show()

# Run the main Qt loop
    sys.exit(app.exec_())
        
    