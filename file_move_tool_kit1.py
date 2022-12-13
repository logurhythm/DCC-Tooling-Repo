import os
import shutil
import json
import svn.remote
import svn.local

JSON_LOC_TEST = "C:\Users\Channing.Williams\Documents\Python_Scripts\My Code\test_directory\phenotypeNameList.json"
JSON_LOC = "\\tools.soulmachines.com\tools\PipelineTestFolder\phenotypeNameList.json"
FOLDER_ROOT = "//tools.soulmachines.com/tools/PipelineTestFolder/checkOutFolder/"
NAMING_CONV_TEXTURES = ["Albedo", "Specular", "Roughness", "AllElse"]
NAMING_CONV_DIR_NAMES =["eyes", "face", "neckJunction", "oralCavity", "skin",
                        "tongue", "lowerTeeth", "upperTeeth"]
OC_SUBFOLDER_CONTENTS = ["tongue", "lowerTeeth", "upperTeeth"]
EYE_SUBFOLDER_CONTENTS = ["eyeL", "eyeR", "lacrimalCaruncle", "eyelashes", "eyeshadow", "tearline"]

class folder_location_loader():
    def fll_loader_albedo():
        with open(JSON_LOC) as phenotypeNameList:
            new_target_dir = " "
            old_target_dir = " "
            for key in phenotypeNameList:
                old_target_dir = svn.remote.RemoteClient(
                    key['Address'] + str(folder_static_location.albedoLoc + key['smNum']))
                new_target_dir = old_target_dir
                new_target_dir.checkout(FOLDER_ROOT + key['Name'] + "Albedo")

    def fll_loader_specular():
        with open(JSON_LOC) as phenotypeNameList:
            new_target_dir = " "
            old_target_dir = " "
            for key in phenotypeNameList:
                old_target_dir = svn.remote.RemoteClient(
                    key['Address'] + str(folder_static_location.specularLoc + key['smNum']))
                new_target_dir = old_target_dir
                new_target_dir.checkout(FOLDER_ROOT + key['Name'] + "specularLoc")
                
    def fll_loader_roughness():
        with open(JSON_LOC)as phenotypeNameList:
            new_target_dir = " "
            old_target_dir = " "
            for key in phenotypeNameList:
                old_target_dir = svn.remote.RemoteClient(
                    key['Address'] + str(folder_static_location.roughnessLoc + key['smNum']))
                new_target_dir = old_target_dir
                new_target_dir.checkout(FOLDER_ROOT + key['Name'] + "roughnessLoc")
    
    def fll_loader_allElse():
        with open(JSON_LOC)as phenotypeNameList:
            new_target_dir = " "
            old_target_dir = " "
            for key in phenotypeNameList:
                old_target_dir = svn.remote.RemoteClient(
                    key['Address'] + str(folder_static_location.allElseLoc + key['smNum']))
                new_target_dir = old_target_dir
                new_target_dir.checkout(FOLDER_ROOT + key['Name'] + "roughness")

class phenotype_folder_creation():
    """
    Below creates the directories for the new standarized phenotype database. It will need to be given a target directoy. It can be made anywhere.
    The directories will be created only, not populated.
    :return:
    """
    def create_folders():
        home_directory = input("Enter location where you want directory tree to be createad: ") 
        with open(JSON_LOC) as phenotypeNameList:  # change to proper SVN directory
            json_data = json.load(phenotypeNameList)
            for key in json_data:
                os.chdir(home_directory)
                try:
                    os.path.exists(home_directory + key['Name'])
                    os.mkdir(home_directory + key['Name'])
                    os.chdir(home_directory + key['Name'])
                except:
                    print("duplicate folder name exists for " + key['Name'] + ", skipping. . .")
                    
                [os.mkdir(i) for i in NAMING_CONV_DIR_NAMES if not os.path.isdir(i)]
                # Creating OralCavity directories
                oral_cavity_subfolder_directory = os.path.join(home_directory, key['Name'], "oralCavity")
                os.chdir(oral_cavity_subfolder_directory)
                [os.mkdir(i) for i in OC_SUBFOLDER_CONTENTS if not os.path.isdir(i)]
                # Creating the eyeL, eyeR, etc. sub-directories
                eye_subfolder_directory = os.path.join(home_directory, key['Name'], "eyes")
                os.chdir(eye_subfolder_directory)
                [os.mkdir(i) for i in EYE_SUBFOLDER_CONTENTS if not os.path.isdir(i)]
                # Returning to home_directory to start on the next phenotype
                os.chdir(home_directory)
            
class folder_static_location:
    #Arrtibutes are locations of all the textures on the SVN repo
    #Mapacq has albedo mas, Render Baker has spec and roughness
    
    albedoLoc = "sourceArt/Textures/Ready/Face/Pristine/Mapacq/"
    specularLoc = "sourceArt/Textures/Ready/Face/Pristine/Spec/renderBaker/"
    roughnessLoc = "sourceArt/Textures/Ready/Face/Pristine/Rough/renderBaker/"
    allElseLoc = "sourceArt/Textures/Ready/Body/Pristine/Scantransfer/"
    
    #Test location to collect all of the assets. Don't want to populate target directories until
    #a proper naming convention for them and new folder structure is decided.
    ##note SVN can't check out different directories to the same target folder. Those
    ##folders will need to be nested.
    
    targetFolder = r"C:\"Users\Channing.Williams\Documents\Python_Scripts\My Code\test_directory"

    #Location of the homedirectory if not input by user.
    homeDir = r"\\tools.soulmachines.com\tools\PipelineTestFolder\pristine\textures\\"

class errors_for_folder_locs():

