import sys
import os
from PySide2 import QtCore
from PySide2 import QtWidgets
from shiboken2 import wrapInstance
import LogsToolBag as ltb

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


class LogsWorkBench(QtWidgets.QDialog):

    def __init__(self, parent=maya_main_window()):
        super(LogsWorkBench, self).__init__(parent)

        self.setWindowTitle("Log's Workbench")
        self.setMinimumWidth(200)
        self.setWindowFlags(self.windowFlags() ^ QtCore.Qt.WindowContextHelpButtonHint)

        
        self.create_widgets()
        self.create_layouts()
        self.create_connections()
        
            
    def create_widgets(self):
        """
        TODO: Create a seperate file to pull desriptions from.
        """
        self.export_btn = QtWidgets.QPushButton("Batch FBX Export")
        self.export_btn.setToolTip("Takes a list of your selected objects and exports them as FBX. Uses the name provided in the outliner. Saves to current porject asset folder")
        self.photo_btn = QtWidgets.QPushButton("Create Photoshoot Set")
        self.photo_btn.setToolTip("Creates a 3 point lighting setup, using aiAreaLights, as well as a aiSkyDome for ambient light. Also creates a shot cam with motion path")
        self.close_btn = QtWidgets.QPushButton("Close")
        self.bbox_btn = QtWidgets.QPushButton("Get BBox Center")
        self.getrads_btn = QtWidgets.QPushButton("Get Pointer Radians")
        self.makeedgeeql_btn = QtWidgets.QPushButton("Make Edges Equal")
        self.geoonpnt_btn = QtWidgets.QPushButton("Create Geo on Vert Point")
        self.ctronwo_btn = QtWidgets.QPushButton("Center at World Origin")
        self.batchpb_btn = QtWidgets.QPushButton("Batch Playblast")
        self.prefixremove_btn = QtWidgets.QPushButton("Remove Prefix Name")
        
    def create_layouts(self):
        """
        Notes to self: col1 and col2 need to be under col as childs.
        """
        button_layout_col1 = QtWidgets.QVBoxLayout()
        button_layout_col1.addStretch()#Forces buttons to not stretch
        button_layout_col1.addWidget(self.export_btn)
        button_layout_col1.addWidget(self.photo_btn)
        button_layout_col1.addWidget(self.bbox_btn)
        button_layout_col1.addWidget(self.getrads_btn)
        button_layout_col1.addWidget(self.makeedgeeql_btn)
        
        
        button_layout_col2 = QtWidgets.QVBoxLayout()
        button_layout_col2.addStretch()
        button_layout_col2.addWidget(self.geoonpnt_btn)
        button_layout_col2.addWidget(self.ctronwo_btn)
        button_layout_col2.addWidget(self.batchpb_btn)
        button_layout_col2.addWidget(self.prefixremove_btn)
        
        button_layout_col = QtWidgets.QHBoxLayout()
        button_layout_col.addLayout(button_layout_col1)
        button_layout_col.addLayout(button_layout_col2)
    
        
        form_layout = QtWidgets.QFormLayout()
        form_layout.addWidget(self.close_btn)
        
        
        main_layout = QtWidgets.QVBoxLayout(self)
        main_layout.addLayout(button_layout_col)
        main_layout.addLayout(form_layout)
     
    def create_connections(self):
        self.close_btn.clicked.connect(self.close)
        self.photo_btn.clicked.connect(ltb.create_photoshoot_set)
        self.export_btn.clicked.connect(ltb.batch_fbx_export)
        self.bbox_btn.clicked.connect(ltb.get_bounding_box_center)
        self.getrads_btn.clicked.connect(ltb.get_radians)
        self.makeedgeeql_btn.clicked.connect(ltb.make_edges_equal)
        self.geoonpnt_btn.clicked.connect(ltb.selection_on_point)
        self.ctronwo_btn.clicked.connect(ltb.center_object_world_origin)
        self.batchpb_btn.clicked.connect(ltb.batch_playblast)
        self.prefixremove_btn.clicked.connect(ltb.autosave_prefix_name_remover)
               
    
if __name__ == "__main__":
    
    try:
        test_dialog.close()
        test_dialog.deleteLater()
    except:
        pass
        
    test_dialog = LogsWorkBench()
    test_dialog.show()
