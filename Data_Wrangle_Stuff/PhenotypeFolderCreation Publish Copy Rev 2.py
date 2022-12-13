import os
import logging as log
import json
from file_move_tool_kit1 import folder_static_locations as ftl


#Below creates the directories for the new standarized phenotype database. It will need to be given a target directoy. It can be made anywhere.
#The directories will be created only, not populated.

def phenotypeFolderCreation():

    homeDirectory = r"\\tools.soulmachines.com\tools\PipelineTestFolder\pristine\textures\\" #change to proper SVN directory
    with open(r"\\tools.soulmachines.com\tools\PipelineTestFolder\phenotypeNameList.json", "rt") as phenotypeNameList: #change to proper SVN directory
            jsonData = json.load(phenotypeNameList)
            for key in jsonData: #For every json entry 
                os.chdir(homeDirectory)              
                if os.path.exists(homeDirectory + key['Name']):
                #     print("duplicate folder name exists for " + key['Name'] + ", skipping. . .")        
                # else:
                    # os.mkdir(homeDirectory + key['Name'])
                    os.chdir(homeDirectory + key['Name'])
                    subfolderContents = ["eyes", "face", "neckJunction", "oralCavity", "skin"]
                    [os.mkdir(i) for i in subfolderContents if not os.path.isdir(i)]
                    #Creating OralCavity sub directories
                    oralCavitySubfolderDirectory = os.path.join(homeDirectory, key['Name'], "oralCavity")
                    oralCavitySubfolderContents = ["tongue", "lowerTeeth", "upperTeeth"]
                    os.chdir(oralCavitySubfolderDirectory)
                    [os.mkdir(i) for i in oralCavitySubfolderContents if not os.path.isdir(i)]
                    # Creating the eyeL, eyeR, etc. sub directories
                    eyeSubfolderDirectory = os.path.join(homeDirectory, key['Name'], "eyes")
                    eyeSubfolderContents = ["eyeL", "eyeR", "lacrimalCaruncle", "eyelashes", "eyeshadow", "tearline"]
                    os.chdir(eyeSubfolderDirectory)
                    [os.mkdir(i) for i in eyeSubfolderContents if not os.path.isdir(i)]
                    # Returning to homeDirectory to start on the next phenotype
                    os.chdir(homeDirectory)

phenotypeFolderCreation()
