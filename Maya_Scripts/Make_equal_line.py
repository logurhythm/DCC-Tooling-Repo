import maya.cmds as cmds
import math

"""
Takes 2 selected edges (only 2), and make them of equal length. 
First selected edge will be the reference edge, the second is the target edge.
"""

#Ensuring trackSelectedOrder flag is used.
if not cmds.selectPref(query=True, trackSelectionOrder=True):
    cmds.selectPref(trackSelectionOrder=True)

def get_edge_length(edge):
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
    print(mesh_name + " after the split") #After Split
    
    """
    Get the related verts, and format our return to something manageable. The vert will look
    something like this : [u'EDGE      9:      5      7  Hard\n']. 
    A single occurance of ":" will need to be removed and 
    ALL ocurrances of white spaces will need to be removed (max split parameter of -1)
    Check here > https://www.w3schools.com/python/ref_string_split.asp for reminders
    """
    related_verts = cmds.polyInfo(edge, edgeToVertex = True)[0].split(':')[-1].split(' ')
    
    """
    Below will now print something like this: 
    [u'', u'', u'', u'', u'', u'', u'4', u'', u'', u'', u'', u'', u'6', u'', u'Hard\n']
    """
    print(related_verts)
    
    """
    We have an entire list that polyInfo returned of edgeToVertex relations. Since we only passed
    a single edge, we only get 2 verticies. Now we need to strip everything from this list except
    for strings that contain a digit.
    """
    related_verts = [x for x in related_verts if x.isdigit()]
    print(related_verts)
    
    """
    related_verts should look like this: [u'#', u'#']. Now it needs to be pass into the get_distance
    function. The xform method expects the verticie coordinates as a string as follows: meshName.vtx[#]. For example
    pCube1.vtx[0].
    """
    edge_length = get_distance('{0}.vtx[{1}]'.format(mesh_name, related_verts[0]), '{0}.vtx[{1}]'.format(mesh_name, related_verts[1]))
    return edge_length
    

def get_distance(point_a, point_b):
    """
    Vector math needs to be done with the passed values. Hooray calculus.
    See link below for all the math stuff
    https://www.redcrab-software.com/en/Calculator/Vector/4/Distance
    """
    
    point_a_position = cmds.xform(point_a, query = True, worldSpace = True, translation = True)
    point_b_position = cmds.xform(point_b, query = True, worldSpace = True, translation = True)
    vector_result = [point_a_position[0] - point_b_position[0], point_a_position[1] - point_b_position[1], point_a_position[2] - point_b_position[2]]
    squared_result = [x ** 2 for x in vector_result]
    distance = math.sqrt(squared_result[0] + squared_result[1] + squared_result[2])
    return distance
    
    
### the actual code:

# let's say the first item in the selection should be the reference edge, and the second the target edge.

edges = cmds.ls(fl = True, os = True)

if edges:
    edge_reference = edges[0]
    edge_target = edges[1]
    
    # get edge lengths
    edge_reference_length = get_edge_length(edge_reference)
    edge_target_length = get_edge_length(edge_target)
    
    # scale correctly
    scale_factor = edge_reference_length / edge_target_length
    cmds.scale(scale_factor, scale_factor, scale_factor, edge_target, absolute = True, componentSpace = True)    