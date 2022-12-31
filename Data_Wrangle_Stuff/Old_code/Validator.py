import os
import settings
import svn.remote
import svn.local
import json

"""
UPDATE: THIS CODE WAS BUILT FOR AN OLD COMPANY DATABASE PROJECT. UNLESS YOU HAVE A SVN REPOSITORY TO TEST ON, THIS WILL 
NOT FUNCTION. SEE PFCR2 SCRIPT FOR FOLDER CREATION, NAMING, AND MOVING SCRIPTS.

This is a quick validation script to ensure the new repository assets match the criteria in the miro board.
Logs all failed phenotypes by name.

"""

def renameToNewNamesLong():

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

renameToNewNamesLong()