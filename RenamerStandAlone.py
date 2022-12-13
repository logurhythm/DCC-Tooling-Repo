import os
import shutil
import subprocess
import logging as log
from functools import partial
import csv
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
    newNameListBody = ["albedoMap.1001.exr","albedoMap.1002.exr","albedoMap.1003.exr","normalMap.1001.exr","normalMap.1002.exr","normalMap.1003.exr", "specularMap.1001.exr","specularMap.1002.exr","specularMap.1003.exr" ]
    newNameListNeckJunction = ["albedoMap.exr", "normalMap.exr","specularMap.exr"]
    rootFolder = "//tools.soulmachines.com/tools/PipelineTestFolder/pristine/textures/"

    with open(r"\\tools.soulmachines.com\tools\PipelineTestFolder\phenotypeNameList.json", "rt") as phenotypeNameList:
        jsonData = json.load(phenotypeNameList)
        for key in jsonData: #For every json entry
            
            #Start name change for specular maps
            if os.path.exists(rootFolder + key['Name']):
                os.chdir(rootFolder + key['Name'] + "/face")
                print("checking " + key['Name'])
                for fileName in os.listdir(rootFolder + key['Name'] + "/face/"):
                    if fileName == "specularMap2.exr":
                        print("found " + fileName)
                        os.rename(fileName, "specular2Map.exr")
                        print("changed to " + fileName)
                    elif fileName == "roughnessMap2.exr":
                        print("found " + fileName)
                        os.rename(fileName, "roughness2Map.exr")
                        print("changed to " + fileName)

renameToNewNamesLong()