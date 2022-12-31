import os
import logging as log
import json
import settings


"""
A dummy tool that can be ran loacally to show how some of the data wrangling exercises from my old company were done.
These can be ran on your machine, ensure you edit the proper directory paths in settings.py.

Below creates a the directory structure with porper naming conveNtions. Refer to settings.py for
directory locations.
"""

class Phenotype_Folder_Creation_Rev_2():
    
    global homeDirectory 
    homeDirectory = settings.FOLDER_ROOT

    """
    Creates the names folders based on the data from the JSON list
    :param:
    :return:
    """

    def phenotypeFolderNameCreation():
        with open(settings.JSON_LIST, "rt") as phenotypeNameList:
            jsonData = json.load(phenotypeNameList)
            for key in jsonData: #For every json entry
                os.chdir(homeDirectory)            
                if not os.path.exists(homeDirectory + '/' + key['Name']):
                    os.mkdir(homeDirectory + '/' + key['Name'])
                else:
                    print(key['Name'] + " directory is already created")
    phenotypeFolderNameCreation()

    def phenotypeFolderAttributesCreation():
        """
        Creates the names of the sub folders based on the data from the JSON list
        :param:
        :return:
        """

        with open(settings.JSON_LIST, "rt") as phenotypeNameList:
            jsonData = json.load(phenotypeNameList)
            for key in jsonData:    
                if os.path.exists(homeDirectory + '/' + key['Name']):
                    os.chdir(homeDirectory + '/' + key['Name'])
                    subfolderContents = settings.NAMING_CONV_DIR_NAMES
                    [os.mkdir(i) for i in subfolderContents if not os.path.isdir(i)]

                    #Creating OralCavity sub directories
                    oralCavitySubfolderDirectory = os.path.join(homeDirectory, key['Name'], "oralCavity")
                    oralCavitySubfolderContents = settings.ORAL_CAVITY_DIR_NAMES
                    os.chdir(oralCavitySubfolderDirectory)
                    [os.mkdir(i) for i in oralCavitySubfolderContents if not os.path.isdir(i)]

                    # Creating the eyeL, eyeR, etc. sub directories
                    eyeSubfolderDirectory = os.path.join(homeDirectory, key['Name'], "eyes")
                    eyeSubfolderContents = settings.EYE_SUBFOLDER_CONTENTS
                    os.chdir(eyeSubfolderDirectory)
                    [os.mkdir(i) for i in eyeSubfolderContents if not os.path.isdir(i)]
                    # Returning to homeDirectory to start on the next phenotype
                    os.chdir(homeDirectory)

    phenotypeFolderAttributesCreation()