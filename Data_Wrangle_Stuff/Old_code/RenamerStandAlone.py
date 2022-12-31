import os
import json
import settings

"""
THIS IS CURRENTLY A METHOD IN AUX_TOOLS.PY

"""

def SpecAndRoughMapRenamer():
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

SpecAndRoughMapRenamer()