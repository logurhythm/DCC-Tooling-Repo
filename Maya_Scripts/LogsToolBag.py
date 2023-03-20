import math
import traceback
import maya.cmds as cmds
import mtoa.utils as mutils
import maya.OpenMaya as om
from PySide2 import QtCore



def batch_fbx_export():
    """
    Exports a list of selected objects as FBX's to the current projects asset directory. Can do OBJ's also if that flag is set.
    Need to add some sort of commbo box for that when added to the GUI.
    """
    #Test file path. Change to user Input with validation test
    file_path = cmds.workspace(q=True, rd=True)

    #Options include Groups, Point Groups, Materials, Smoothing, Normals
    options = "groups=1;ptgroups=1;materials=1;smoothing=0;normals=1"

    #Section List used to store the selected objects
    selection_list = cmds.ls(sl=True)
    if selection_list:
        for selected_objects in selection_list:
            name = selected_objects
            cmds.file(file_path + "/assets/" + name, 
            force=True, 
            options=options, 
            type="FBX export", 
            preserveReferences=True, 
            exportSelected=True)
    else:
        om.MGlobal.displayError("No objects have been selected")
        #Need to write a catch for an object that just has a component selected


def create_photoshoot_set():
    """
    Creates a 3 point lighting setup with a skydome for an ambient light. Also created the camera with affixed motion path.
    """
    LightIntensity = 1000
    LightExposure = 5
    LightVolumeSamples = 5
    # Sets the timeline parameters
    start_time = cmds.playbackOptions(query=True, minTime=True)
    end_time = cmds.playbackOptions(query=True, maxTime=True)

    # Create a NURBS circle and Camera
    cmds.circle(center=(0, 0, 0), normal=(0, 1, 0), radius=100, degree=3, sections=30, constructionHistory=True)
    cmds.camera(centerOfInterest=5, focalLength=35, lensSqueezeRatio=1, cameraScale=1,
                horizontalFilmAperture=1.41732, horizontalFilmOffset=0, verticalFilmAperture=0.94488,
                verticalFilmOffset=0, filmFit='fill', overscan=1, motionBlur=0, shutterAngle=144,
                nearClipPlane=0.1, farClipPlane=10000, orthographic=False, orthographicWidth=30,
                panZoomEnabled=False, horizontalPan=0, verticalPan=0, zoom=1)

    #Selects the camera first, circle second and runs the "Attach to Motion Path" Functions found the Constrain menu 
    cmds.select("camera1", "nurbsCircle1")
    cmds.pathAnimation(fractionMode=True, follow=True, followAxis='x', upAxis='y', worldUpType='vector',
                    worldUpVector=[0, 1, 0], inverseUp=False, inverseFront=False, bank=False,
                    startTimeU=start_time, endTimeU=end_time)
    cmds.select("camera1")
    cmds.rename( "Shot_Cam")
    cmds.select("nurbsCircle1")
    cmds.rename("Shot_Cam_Path")
    cmds.group( 'Shot_Cam', 'Shot_Cam_Path', n='Photoshoot_Stuff' )

    #Create the Skydome
    mutils.createLocator("aiSkyDomeLight", asLight=True)
    cmds.select("aiSkyDomeLight1")
    cmds.rename("Ambient_Light")
    cmds.setAttr("Ambient_Light.intensity", .3)
    cmds.setAttr("Ambient_Light.resolution", 1000)
    cmds.setAttr("Ambient_Light.exposure", -1)
    #Settings first KeyLight
    mutils.createLocator("aiAreaLight", asLight=True)
    cmds.select("aiAreaLight1")
    cmds.rename("Key_Light")
    cmds.setAttr("Key_Light.exposure", LightExposure)
    cmds.setAttr("Key_Light.aiSamples", LightVolumeSamples)
    cmds.setAttr("Key_LightShape.aiVolumeSamples", LightVolumeSamples)
    cmds.setAttr("Key_Light.intensity", LightIntensity)
    cmds.setAttr("Key_Light.translate", 0, 100, 100)
    cmds.setAttr("Key_Light.scale", 40, 40, 450)
    cmds.setAttr("Key_Light.rotate", -40, 0, 0)
    #Settings first Fill Light Main
    mutils.createLocator("aiAreaLight", asLight=True)
    cmds.select("aiAreaLight1")
    cmds.rename("Fill_Light")
    cmds.setAttr("Fill_Light.exposure", LightExposure)
    cmds.setAttr("Fill_Light.aiSamples", LightVolumeSamples)
    cmds.setAttr("Fill_LightShape.aiVolumeSamples", LightVolumeSamples)
    cmds.setAttr("Fill_Light.intensity", LightIntensity)
    cmds.setAttr("Fill_Light.translate", 0, 30, -100)
    cmds.setAttr("Fill_Light.scale", 40, 40, 450)
    cmds.setAttr("Fill_Light.rotate", -180, 0, 0)
    #Settings first Fill Light Secondary
    mutils.createLocator("aiAreaLight", asLight=True)
    cmds.select("aiAreaLight1")
    cmds.rename("Fill_Light_Secondary")
    cmds.setAttr("Fill_Light_Secondary.exposure", LightVolumeSamples)
    cmds.setAttr("Fill_Light_Secondary.aiSamples", LightVolumeSamples)
    cmds.setAttr("Fill_Light_Secondary.aiVolumeSamples", LightVolumeSamples)
    cmds.setAttr("Fill_Light_Secondary.intensity", LightIntensity)
    cmds.setAttr("Fill_Light_Secondary.translate", -130, -20, 0)
    cmds.setAttr("Fill_Light_Secondary.scale", 40, 40, 450)
    cmds.setAttr("Fill_Light_Secondary.rotate", -260, 90, -60)

def get_bounding_box_center():
    """
    Gets objects bounding box center. Use this to snap objects to the center of a selection. Need expand this to
    vert selection for joint placement.
    """
    # Select the object you want to query
    selection = cmds.ls(sl=True)
    if not selection:
        om.MGlobal.displayError("No objects have been selected")
    else:
        bbox_center = cmds.xform(query=True, boundingBox=True, worldSpace=True)
        print(bbox_center)
        # Calculate the center point of the bounding box
        center_point = [
            (bbox_center[0] + bbox_center[3]) / 2.0,
            (bbox_center[1] + bbox_center[4]) / 2.0,
            (bbox_center[2] + bbox_center[5]) / 2.0
        ]
        print(center_point)

def get_radians():
    """
    Query the move tool's current orientation mode and get its coords. It needs to be in radians. math.degrees
    actually gives you the result in radians...not degrees. Which is confusing af.
    """
    orientation_mode = cmds.manipMoveContext("Move", query=True, oa=True)

    for x in orientation_mode:
        print(math.degrees(x))
        
def make_edges_equal():
    def get_edge_length(edge):

        if not cmds.selectPref(query=True, trackSelectionOrder=True):
            cmds.selectPref(trackSelectionOrder=True)
        """
        Getting the edge length of the 2 selected edges. The string for the edge selections needs to be
        formated properly. Currently they will return something like this: pCube.e[#]. The string will need to be
        stripped of the "." and index.

        something to note here: edge is the element of the index that was passed into this function. A type check will
        return unicode. But a string is what will be split. 

        param: edge selection (list)
        return: edge_length (list)
        
        """
        print(edge) #Before Split
        mesh_name = edge.split('.')[0]
        related_verts = cmds.polyInfo(edge, edgeToVertex = True)[0].split(':')[-1].split(' ')
        related_verts = [x for x in related_verts if x.isdigit()]
        edge_length = get_distance('{0}.vtx[{1}]'.format(mesh_name, related_verts[0]), '{0}.vtx[{1}]'.format(mesh_name, related_verts[1]))
        return edge_length
        
    def get_distance(point_a, point_b):
        point_a_position = cmds.xform(point_a, query = True, worldSpace = True, translation = True)
        point_b_position = cmds.xform(point_b, query = True, worldSpace = True, translation = True)
        vector_result = [point_a_position[0] - point_b_position[0], point_a_position[1] - point_b_position[1], point_a_position[2] - point_b_position[2]]
        squared_result = [x ** 2 for x in vector_result]
        distance = math.sqrt(squared_result[0] + squared_result[1] + squared_result[2])
        return distance

    edges = cmds.ls(fl = True, os = True)

    try:
        edge_reference = edges[0]
        edge_target = edges[1]
        # get edge lengths
        edge_reference_length = get_edge_length(edge_reference)
        edge_target_length = get_edge_length(edge_target)
        # scale correctly
        scale_factor = edge_reference_length / edge_target_length
        cmds.scale(scale_factor, scale_factor, scale_factor, edge_target, absolute = True, componentSpace = True)
    except:
        om.MGlobal.displayError("No edges, or only one edge was selected. Select exactly 2")
        traceback.print_exc()


def selection_on_point():
    """
    Allows for primative generation at a selected vert. Accepts multiple vert selections.
    Currently only creates polyCube. Will tweak to take a selection.

    """
    #Tie the selection to a variable.
    mySelection = cmds.ls(selection = True, fl = True)
    print(mySelection)
    generated_shapes_list = []
    group_name="mesh_one_verts"

    for vertSelection in mySelection:
        vertSelection = cmds.xform(vertSelection, q=True, worldSpace=True, translation=True)
        generated_shape = cmds.polyCube()[0]
        cmds.move(vertSelection[0], vertSelection[1], vertSelection[2], generated_shape)
        generated_shapes_list.append(generated_shape)
    cmds.group(generated_shapes_list, name=group_name)

def center_object_world_origin():
    """
    Centers object selections at the wolrd origin. Use with batch_playblast.

    """
    selected_object=cmds.ls(selection = True, fl = True)
    for x in selected_object:
        cmds.xform(x, translation=[0, 0, 0], worldSpace=True, absolute=True)

def batch_playblast():
    """
    Creates a playblst of selected object. If fed a list of objecsts, it will hide all of them, then unhide them one by one to
    conduct the playblast. Will save it in the projects movies folder (so make sure the project folder is set and the folder is there)
    Saves at 1080p

    """
    selected_objects = cmds.ls(selection = True, fl = True)
    for objects in selected_objects:
        cmds.setAttr(objects+".visibility", 0)
    for objects in selected_objects:
        cmds.setAttr(objects+".visibility", 1)
        cmds.select(cl=True)
        cmds.playblast(format="avi", filename="movies/" + objects + ".avi", 
        sequenceTime=0, 
        clearCache=1, 
        viewer=1, 
        showOrnaments=1, 
        fp=4, 
        percent=100, 
        compression="none", 
        quality=100, 
        widthHeight=[1920, 1080])
        cmds.setAttr(objects+".visibility", 0)
    for objects in selected_objects:
        cmds.setAttr(objects+".visibility", 1)

def autosave_prefix_name_remover(string_to_remove):
    """
    Takes list of selected objects from the outliner and parses from for the prefix append, like when maya crashes or autosaves and you load it into a new scene.
    This is still fairly manual, need to provide a input box for the user to specificy the prefix.

    """    
    renameList = cmds.ls(selection = True)
    for names in renameList:
        print(names)
        if string_to_remove in names:
            new_name = names.replace(string_to_remove, "")
            cmds.rename(names, new_name)  # Rename the object

