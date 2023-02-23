import sys
import os
from PySide2 import QtCore
from PySide2 import QtWidgets
from shiboken2 import wrapInstance

import maya.OpenMayaUI as omui

def maya_main_window():
    """
    Return the Maya main window widget as a Python object
    """
    main_window_ptr = omui.MQtUtil.mainWindow()
    if sys.version_info.major >= 3:
        return wrapInstance(int(main_window_ptr), QtWidgets.QWidget)
    else:
        return wrapInstance(long(main_window_ptr), QtWidgets.QWidget)


class LogsToolBagGUI(QtWidgets.QDialog):

    def __init__(self, parent=maya_main_window()):
        super(LogsToolBagGUI, self).__init__(parent)

        self.setWindowTitle("Test Dialog")
        self.setMinimumWidth(200)
        self.setWindowFlags(self.windowFlags() ^ QtCore.Qt.WindowContextHelpButtonHint)

        
        self.create_widgets()
        self.create_layouts()
        self.creat_connections()
        
            
    def create_widgets(self):
        self.export_btn = QtWidgets.QPushButton("Batch FBX Export")
        self.photo_btn = QtWidgets.QPushButton("Create Photoshoot Set")
        self.close_btn = QtWidgets.QPushButton("Close")
        self.bbox_btn = QtWidgets.QPushButton("Get BBox Center")
        self.getrads_btn = QtWidgets.QPushButton("Get Pointer Radians")
        self.getedgelen_btn = QtWidgets.QPushButton("Get Edge Length")
        self.getdist_btn = QtWidgets.QPushButton("Get Dist Between Verts")
        self.geoonpnt_btn = QtWidgets.QPushButton("Create Geo on Vert Point")
        self.ctronwo_btn = QtWidgets.QPushButton("Center at World Origin")
        self.batchpb_btn = QtWidgets.QPushButton("Batch Playblast")
        self.prefixremove_btn = QtWidgets.QPushButton("Remove Prefix Name")
        
    def create_layouts(self):
        button_layout = QtWidgets.QVBoxLayout()
        button_layout.addStretch()#Forces buttons to not stretch
        button_layout.addWidget(self.export_btn)
        button_layout.addWidget(self.photo_btn)
        button_layout.addWidget(self.bbox_btn)
        button_layout.addWidget(self.getrads_btn)
        button_layout.addWidget(self.getedgelen_btn)
        button_layout.addWidget(self.getdist_btn)
        button_layout.addWidget(self.geoonpnt_btn)
        button_layout.addWidget(self.ctronwo_btn)
        button_layout.addWidget(self.batchpb_btn)
        button_layout.addWidget(self.prefixremove_btn)
        button_layout.addWidget(self.close_btn)
    
        
        form_layout = QtWidgets.QFormLayout()
        form_layout.addWidget(self.close_btn)
        
        main_layout = QtWidgets.QVBoxLayout(self)
        main_layout.addLayout(button_layout)
        main_layout.addLayout(form_layout)
    
    #Signals    
    def creat_connections(self):
        self.close_btn.clicked.connect(self.close)
        
    
if __name__ == "__main__":
    
    try:
        test_dialog.close()
        test_dialog.deleteLater()
    except:
        pass
        
    test_dialog = LogsToolBagGUI()
    test_dialog.show()

