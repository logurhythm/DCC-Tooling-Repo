import maya.cmds as cmds


"""
Allows for primative generation at a selected vert. Accepts multiple vert selections.
Currently only creates polyCube. Will tweak to take a selection.

"""
#Tie the selection to a variable.
mySelection = cmds.ls(selection = True, fl = True)
print(mySelection)

for vertSelection in mySelection:
    vertSelection = cmds.xform(vertSelection, q=True, worldSpace=True, translation=True)
    print(vertSelection)
    testBuild = cmds.polyCube()
    cmds.move(vertSelection[0], vertSelection[1], vertSelection[2], testBuild) 

#cmds.move(selectionsPosition[0], selectionsPosition[1], selectionsPosition[2], testBuild)

