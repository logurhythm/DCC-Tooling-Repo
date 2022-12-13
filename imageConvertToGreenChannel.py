from multiprocessing.spawn import import_main_path
import sys
import os
os.environ["OPENCV_IO_ENABLE_OPENEXR"] = "1"
import cv2
import json
import shutil

#Iterates through directories in pristines which contain the neckJunction normalMap, creates a copy, extracts the green channel, and saves
#that as roughnessMap.exr. Having a hard time getting it to work during the imwrite portion, seems to work with others but not me.
SOUCRE_LOC = "//tools.soulmachines.com/tools/PipelineTestFolder/pristine/textures/"
    
def write_32bit_exr_PIZ(export_path, image):
    """
    PIZ compression function that compresses the 64bit image to 32bit.
    :param: export_path. String located in settings.py. Replace with hard coded local global variable to test.
    :param: image location. String located in settings.py. Replace with local hard coded global variable to test.
    :return:

    """
    cv2.imwrite(export_path, image,
                [cv2.IMWRITE_EXR_TYPE, cv2.IMWRITE_EXR_TYPE_FLOAT,
                 cv2.IMWRITE_EXR_COMPRESSION, cv2.IMWRITE_EXR_COMPRESSION_PIZ])

def imageConvertToGreenChannel():
    """
    One-off conversion function to create the green channel. See Tarun's code for the entire RGB conversion stuff.
    This should be called before the compression function above. Also using hardcoded location for the JSON file
    
    """
    with open(r"\\tools.soulmachines.com\tools\PipelineTestFolder\phenotypeNameList1.json", "rt") as phenotypeNameList:
        jsonData = json.load(phenotypeNameList)
        for key in jsonData: #For every json entry
            os.chdir(SOUCRE_LOC + key['Name'] + '/skin/')
            for fileName in os.listdir(SOUCRE_LOC + key['Name'] + '/skin/'):
                currentDir = SOUCRE_LOC + key['Name'] + '/skin/'
                if fileName == "normalMap.1001.exr":
                    shutil.copy(currentDir + 'normalMap.1001.exr', currentDir + 'roughnessMap.1001.exr')  #copies the files and placs it in same directory as a copy
                if fileName == "normalMap.1002.exr":
                    shutil.copy(currentDir + 'normalMap.1002.exr', currentDir + 'roughnessMap.1002.exr')  #copies the files and placs it in same directory as a copy
                if fileName == "normalMap.1003.exr":
                    shutil.copy(currentDir + 'normalMap.1003.exr', currentDir + 'roughnessMap.1003.exr')  #copies the files and placs it in same directory as a copy
                    
imageConvertToGreenChannel()


