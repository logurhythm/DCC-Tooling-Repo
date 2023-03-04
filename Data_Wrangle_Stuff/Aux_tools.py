import os
import json
import settings
import svn.remote
import svn.local
os.environ["OPENCV_IO_ENABLE_OPENEXR"] = "1"
import cv2
import shutil


"""
UPDATE: THIS CODE WAS BUILT FOR AN OLD COMPANY DATABASE PROJECT. UNLESS YOU HAVE A SVN REPOSITORY TO TEST ON, SOME
OF THESE WILL NOT FUNCTION. SEE PFCR2 SCRIPT FOR FOLDER CREATION, NAMING, AND MOVING SCRIPTS.

This is a one-off script which does not intend to be used for future pipeline tool dev. Contains various tools to aid
in data wrangling project. 

:return:
"""
def fll_loader():
    """
    checks out selected folder of the users choice to the new target location. See settings.NAMING_CONV_TEXTURES
    :param:
    :return:
    """
    choice = input("Enter texture choice:")
    with open(settings.JSON_LOC) as phenotypeNameList:
        new_target_dir = " "
        old_target_dir = " "
        for key in phenotypeNameList:
            old_target_dir = svn.remote.RemoteClient(
                key['Address'] + str(folder_static_location + '/' + 
                settings.NAMING_CONV_TEXTURES[choice] + '/' + key['smNum']))
            new_target_dir = old_target_dir
            new_target_dir.checkout(settings.FOLDER_ROOT + key['Name'] + settings.NAMING_CONV_TEXTURES[choice])

def SpecAndRoughMapRenamer():
    """
    A last minute tool to rename roughness and spec maps. Unsure these are aligned with whats in the Miro board.
    :param:
    :return:
    """
    rootFolder = settings.FOLDER_ROOT
    directoryLoc = settings.NAMING_CONV_DIR_NAMES

    with open(settings.JSON_LIST, "rt") as phenotypeNameList:
        jsonData = json.load(phenotypeNameList)
        for key in jsonData: #For every json entry
            for bodyPart in directoryLoc:
                #Start name change for specular maps
                if os.path.exists(rootFolder + key['Name']):
                    os.chdir(rootFolder + key['Name'] + bodyPart)
                    print("checking " + key['Name'])
                    for fileName in os.listdir(rootFolder + key['Name'] + bodyPart):
                        if fileName == "specularMap2.exr":
                            print("found " + fileName)
                            os.rename(fileName, "specular2Map.exr")
                            print("changed to " + fileName)
                        elif fileName == "roughnessMap2.exr":
                            print("found " + fileName)
                            os.rename(fileName, "roughness2Map.exr")
                            print("changed to " + fileName)
                            
def nameValidator():

    """
    This is a quick validation script to ensure the new repository assets match the criteria in the miro board.
    Logs all failed phenotypes by name.
    :param:
    :return:
    """

    newNameList = ["albedoMap.exr", "normalMap.exr","specularSkindeepMap.exr", "specularMap.exr", "roughnessMap.exr", "specularMap2.exr", "roughnessMap2.exr"]
    newNameListBody = ["albedoMap.1001.exr","albedoMap.1002.exr","albedoMap.1003.exr","normalMap.1001.exr","normalMapl.1002.exr","normalMap.1003.exr", "specularMap.1001.exr","specularMap.1002.exr","specularMap.1003.exr" ]
    newNameListNeckJunction = ["albedoMap.exr", "normalMap.exr","specularMap.exr"]
    rootFolder = settings.FOLDER_ROOT
    failedCheck = []

    with open(settings.JSON_LIST, "rt") as phenotypeNameList:
        jsonData = json.load(phenotypeNameList)
        for key in jsonData: #For every json entry
            #Start name change for specular maps
            passCheckCounter = 0
            if os.path.exists(rootFolder + key['Name']):
                nameCounter = 0
                os.chdir(rootFolder + key['Name'] + "/skin/")
                for fileName in os.listdir(rootFolder + key['Name'] + "/skin"):
                    for listName in newNameListBody:
                        if fileName == listName:
                            nameCounter += 1
                            if nameCounter == 8:
                                print("All skin files for " + key['Name'] + " are VARIFIED")
                                nameCounter = 0
                                passCheckCounter += 1
            if os.path.exists(rootFolder + key['Name'] + '/neckJunction'):
                nameCounter = 0
                os.chdir(rootFolder + key['Name'] + '/neckJunction')
                for fileName in os.listdir(rootFolder + key['Name'] + "/neckJunction"):
                    for listName in newNameListNeckJunction:
                        if fileName == listName:
                            nameCounter += 1
                            if nameCounter == 2:
                                print("All neckJunction files for " + key['Name'] + " are VARIFIED")
                                nameCounter = 0
                                passCheckCounter += 1
            if os.path.exists(rootFolder + key['Name'] + '/face'):
                nameCounter = 0
                os.chdir(rootFolder + key['Name'] + '/face')
                for fileName in os.listdir(rootFolder + key['Name'] + "/face"):
                    for listName in newNameList:
                        if fileName == listName:
                            nameCounter += 1
                            if nameCounter == 7:
                                print("All face files for " + key['Name'] + " are VARIFIED")
                                nameCounter = 0
                                passCheckCounter += 1   
            if passCheckCounter != 3:
                print("Total file count not expected, check face, skin and neckJunction for proper file count")
                failedCheck.append(key['Name'])
            if passCheckCounter == 3:
                print("File count matches expected amount")
    print("The following phenotypes failed file amount check " + str(failedCheck))


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
            os.chdir(settings.FOLDER_ROOT + key['Name'] + '/skin/')
            for fileName in os.listdir(settings.FOLDER_ROOT + key['Name'] + '/skin/'):
                currentDir = settings.FOLDER_ROOT + key['Name'] + '/skin/'
                if fileName == "normalMap.1001.exr":
                    shutil.copy(currentDir + 'normalMap.1001.exr', currentDir + 'roughnessMap.1001.exr')  #copies the files and placs it in same directory as a copy
                if fileName == "normalMap.1002.exr":
                    shutil.copy(currentDir + 'normalMap.1002.exr', currentDir + 'roughnessMap.1002.exr')  #copies the files and placs it in same directory as a copy
                if fileName == "normalMap.1003.exr":
                    shutil.copy(currentDir + 'normalMap.1003.exr', currentDir + 'roughnessMap.1003.exr')  #copies the files and placs it in same directory as a copy
                    


