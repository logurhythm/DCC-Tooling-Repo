import os
import shutil
import subprocess
import logging as log
from functools import partial
import csv
from unicodedata import name
import svn.remote
import svn.local
import pprint
import json
import stat
import errno
import svn

#Directories needed: sourceDirectory and targetDirectory are the svn address needed. Only sourceDirectory will need to be copied to a local machine location.
#sourceDirectory will need to loop through the following locations:
        #####FACE####
        # "http://asset.soulmachines.com" + "/avatar_#name+0???#" + "sourceArt/Textures/Ready/Face/Pristine/Mapacq/" + "SM_neustral_chunk/"#
            #mapacpDirectory = "sourceArt/Textures/Ready/Face/Pristine/Mapacq/"
        # "http://asset.soulmachines.com/" + "/avatar_#name+0???#" + "sourceArt/Textures/Ready/Face/Pristine/Spec/renderBaker/" + "SM_neustral_chunk/"#
            #renderBakerSpecDirectory = "sourceArt/Textures/Ready/Face/Pristine/Spec/renderBaker/"
        # http://asset.soulmachines.com/" + "/avatar_#name+0???#" + "sourceArt/Textures/Ready/Face/Pristine/Rough/renderBaker/" + "SM_neustral_chunk/"#
            #renderBakerRoughDirectory = "sourceArt/Textures/Ready/Face/Pristine/rough/renderBaker/"
        # ###Body####
        # http://asset.soulmachines.com/" + "/avatar_#name+0???#" + "sourceArt/Textures/Ready/Body/Pristine/Scantransfer/" + "#SM_neutral_chunk/"#
            #scantranferDirectory = "sourceArt/Textures/Ready/Body/Pristine/Scantransfer/"

mapacpDirectory = "sourceArt/Textures/Ready/Face/Pristine/Mapacq/"
renderBakerSpecDirectory = "sourceArt/Textures/Ready/Face/Pristine/Spec/renderBaker/"
renderBakerRoughDirectory = "sourceArt/Textures/Ready/Face/Pristine/Rough/renderBaker/"
scantranferDirectory = "sourceArt/Textures/Ready/Body/Pristine/Scantransfer/"
# info = sourceDirectory.info()
# pprint.pprint(info)

def renameToNewNamesLong(): #Run if renameToNewNames doesn't work....which it probably wont
#############################################################################################################################################################################################
    newNameList = ["albedoMap.exr", "normalMap.exr","specularSkindeepMap.exr", "specularMap.exr", "roughnessMap.exr", "specularMap2.exr", "roughnessMap2.exr"]
    newNameListBody = ["albedoMap.1001.exr","albedoMap.1002.exr","albedoMap.1003.exr","normalMap.1001.exr","normalMapl.1002.exr","normalMap.1003.exr", "specularMap.1001.exr","specularMap.1002.exr","specularMap.1003.exr" ]
    newNameListNeckJunction = ["albedoMap.exr", "normalMap.exr","specularMap.exr"]
    rootFolder = "//tools.soulmachines.com/tools/PipelineTestFolder/pristine/textures/"
    failedCheck = []

    with open(r"\\tools.soulmachines.com\tools\PipelineTestFolder\phenotypeNameList.json", "rt") as phenotypeNameList:
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
                            #print(fileName + " for " + key['Name'] +  " VARIFIED")
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
                            #print(fileName + " for " + key['Name'] +  " VARIFIED")
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
                            #print(fileName + " for " + key['Name'] +  " VARIFIED")
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
    print("The follow phenotypes failed file amount check " + str(failedCheck))
                    # elif fileName == newNameList[1]:
                    #     print(print(newNameList[1] + " VARIFIED"))
                    # elif fileName == "specular_cleaned.exr":
                    #     os.rename(fileName, newNameList[2])
                    # elif fileName == "face_spec_lobe1.exr":
                    #     os.rename(fileName, newNameList[3])
                    # elif fileName == "face_rough_lobe1.exr":
                    #     os.rename(fileName, newNameList[4])
                    # elif fileName == "face_spec_lobe2.exr":
                    #     os.rename(fileName, newNameList[5])
                    # elif fileName == "face_rough_lobe2.exr":
                    #     os.rename(fileName, newNameList[6])
                    # if fileName == "albedoMap.1001.exr":
                    #     os.rename(fileName, newNameListBody[0])
                    # elif fileName == "albedoMap.1002.exr":
                    #     os.rename(fileName, newNameListBody[1])
                    # elif fileName == "albedoMap.1003.exr":
                    #     os.rename(fileName, newNameListBody[2])
                    # elif fileName == "body_normal.1001.exr":
                    #     os.rename(fileName, newNameListBody[3])
                    # elif fileName == "body_normal.1002.exr":
                    #     os.rename(fileName, newNameListBody[4])
                    # elif fileName == "body_normal.1003.exr":
                    #     os.rename(fileName, newNameListBody[5])
                    # elif fileName == "body_specular.1001.exr":
                    #     os.rename(fileName, newNameListBody[6])
                    # elif fileName == "body_specular.1002.exr":
                    #     os.rename(fileName, newNameListBody[7])
                    # elif fileName == "body_specular.1003.exr":
                    #     os.rename(fileName, newNameListBody[8])
                    # if fileName == "neckJunction_diffuse.exr":
                    #     os.rename(fileName, newNameListNeckJunction[0])
                    # elif fileName == "neckJunction_normal.exr":
                    #     os.rename(fileName, newNameListNeckJunction[1])
                    # elif fileName == "neckJunction_specular.exr":
                    #     os.rename(fileName, newNameListNeckJunction[2])
                    
            # #Start name change for roughness1 maps
            # if os.path.exists(rootFolder + key['Name'] + "Roughness1"):
            #     os.chdir(rootFolder + key['Name'] + "Roughness1")
            #     for fileName in os.listdir(rootFolder + key['Name'] + "Roughness1"): 
            #         if fileName == "diffuse_cleaned.exr":
            #             os.rename(fileName, newNameList[0])
            #         elif fileName == "nblue_vector_corrected_tangent_cleaned.exr":
            #             os.rename(fileName, newNameList[1])
            #         elif fileName == "specular_cleaned.exr":
            #             os.rename(fileName, newNameList[2])
            #         elif fileName == "face_spec_lobe1.exr":
            #             os.rename(fileName, newNameList[3])
            #         elif fileName == "face_rough_lobe1.exr":
            #             os.rename(fileName, newNameList[4])
            #         elif fileName == "face_spec_lobe2.exr":
            #             os.rename(fileName, newNameList[5])
            #         elif fileName == "face_rough_lobe2.exr":
            #             os.rename(fileName, newNameList[6])
            #         if fileName == "body_diffuse.1001.exr":
            #             os.rename(fileName, newNameListBody[0])
            #         elif fileName == "body_diffuse.1002.exr":
            #             os.rename(fileName, newNameListBody[1])
            #         elif fileName == "body_diffuse.1003.exr":
            #             os.rename(fileName, newNameListBody[2])
            #         elif fileName == "body_normal.1001.exr":
            #             os.rename(fileName, newNameListBody[3])
            #         elif fileName == "body_normal.1002.exr":
            #             os.rename(fileName, newNameListBody[4])
            #         elif fileName == "body_normal.1003.exr":
            #             os.rename(fileName, newNameListBody[5])
            #         elif fileName == "body_specular.1001.exr":
            #             os.rename(fileName, newNameListBody[6])
            #         elif fileName == "body_specular.1002.exr":
            #             os.rename(fileName, newNameListBody[7])
            #         elif fileName == "body_specular.1003.exr":
            #             os.rename(fileName, newNameListBody[8])
            #         if fileName == "neckJunction_diffuse.exr":
            #             os.rename(fileName, newNameListNeckJunction[0])
            #         elif fileName == "neckJunction_normal.exr":
            #             os.rename(fileName, newNameListNeckJunction[1])
            #         elif fileName == "neckJunction_specular.exr":
            #             os.rename(fileName, newNameListNeckJunction[2])
                    
            # #Start name change for roughness2 maps
            # if os.path.exists(rootFolder + key['Name'] + "Roughness2"):
            #     os.chdir(rootFolder + key['Name'] + "Roughness2")
            #     for fileName in os.listdir(rootFolder + key['Name'] + "Roughness2"):
            #         if fileName == "diffuse_cleaned.exr":
            #             os.rename(fileName, newNameList[0])
            #         elif fileName == "nblue_vector_corrected_tangent_cleaned.exr":
            #             os.rename(fileName, newNameList[1])
            #         elif fileName == "specular_cleaned.exr":
            #             os.rename(fileName, newNameList[2])
            #         elif fileName == "face_spec_lobe1.exr":
            #             os.rename(fileName, newNameList[3])
            #         elif fileName == "face_rough_lobe1.exr":
            #             os.rename(fileName, newNameList[4])
            #         elif fileName == "face_spec_lobe2.exr":
            #             os.rename(fileName, newNameList[5])
            #         elif fileName == "face_rough_lobe2.exr":
            #             os.rename(fileName, newNameList[6])
            #         if fileName == "body_diffuse.1001.exr":
            #             os.rename(fileName, newNameListBody[0])
            #         elif fileName == "body_diffuse.1002.exr":
            #             os.rename(fileName, newNameListBody[1])
            #         elif fileName == "body_diffuse.1003.exr":
            #             os.rename(fileName, newNameListBody[2])
            #         elif fileName == "body_normal.1001.exr":
            #             os.rename(fileName, newNameListBody[3])
            #         elif fileName == "body_normal.1002.exr":
            #             os.rename(fileName, newNameListBody[4])
            #         elif fileName == "body_normal.1003.exr":
            #             os.rename(fileName, newNameListBody[5])
            #         elif fileName == "body_specular.1001.exr":
            #             os.rename(fileName, newNameListBody[6])
            #         elif fileName == "body_specular.1002.exr":
            #             os.rename(fileName, newNameListBody[7])
            #         elif fileName == "body_specular.1003.exr":
            #             os.rename(fileName, newNameListBody[8])
            #         if fileName == "neckJunction_diffuse.exr":
            #             os.rename(fileName, newNameListNeckJunction[0])
            #         elif fileName == "neckJunction_normal.exr":
            #             os.rename(fileName, newNameListNeckJunction[1])
            #         elif fileName == "neckJunction_specular.exr":
            #             os.rename(fileName, newNameListNeckJunction[2]) 
                    
            # #Start name change for all body maps
            # if os.path.exists(rootFolder + key['Name'] + "allElse"):
            #     os.chdir(rootFolder + key['Name'] + "allElse")
            #     for fileName in os.listdir(rootFolder + key['Name'] + "allElse"):
            #         if fileName == "diffuse_cleaned.exr":
            #             os.rename(fileName, newNameList[0])
            #         elif fileName == "nblue_vector_corrected_tangent_cleaned.exr":
            #             os.rename(fileName, newNameList[1])
            #         elif fileName == "specular_cleaned.exr":
            #             os.rename(fileName, newNameList[2])
            #         elif fileName == "face_spec_lobe1.exr":
            #             os.rename(fileName, newNameList[3])
            #         elif fileName == "face_rough_lobe1.exr":
            #             os.rename(fileName, newNameList[4])
            #         elif fileName == "face_spec_lobe2.exr":
            #             os.rename(fileName, newNameList[5])
            #         elif fileName == "face_rough_lobe2.exr":
            #             os.rename(fileName, newNameList[6])
            #         if fileName == "body_diffuse.1001.exr":
            #             os.rename(fileName, newNameListBody[0])
            #         elif fileName == "body_diffuse.1002.exr":
            #             os.rename(fileName, newNameListBody[1])
            #         elif fileName == "body_diffuse.1003.exr":
            #             os.rename(fileName, newNameListBody[2])
            #         elif fileName == "body_normal.1001.exr":
            #             os.rename(fileName, newNameListBody[3])
            #         elif fileName == "body_normal.1002.exr":
            #             os.rename(fileName, newNameListBody[4])
            #         elif fileName == "body_normal.1003.exr":
            #             os.rename(fileName, newNameListBody[5])
            #         elif fileName == "body_specular.1001.exr":
            #             os.rename(fileName, newNameListBody[6])
            #         elif fileName == "body_specular.1002.exr":
            #             os.rename(fileName, newNameListBody[7])
            #         elif fileName == "body_specular.1003.exr":
            #             os.rename(fileName, newNameListBody[8])
            #         if fileName == "neckJunction_diffuse.exr":
            #             os.rename(fileName, newNameListNeckJunction[0])
            #         elif fileName == "neckJunction_normal.exr":
            #             os.rename(fileName, newNameListNeckJunction[1])
            #         elif fileName == "neckJunction_specular.exr":
            #             os.rename(fileName, newNameListNeckJunction[2])  

renameToNewNamesLong()