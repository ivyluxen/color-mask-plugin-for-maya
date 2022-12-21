import sys
import random

from maya import cmds
from maya import OpenMayaMPx
from maya.api import OpenMaya

kPluginCmdName = "colorID"

# Command
class colorIDCommand(OpenMayaMPx.MPxCommand):

    def __init__(self):
        super(colorIDCommand, self).__init__()

    # Invoked when the command is run.
    def doIt(self, argList):
        # select faces
        selection = cmds.ls(sl=True, o=True)[0]
        faces = cmds.ls(sl=True)
        x = 0

        # assign shader
        sha = cmds.shadingNode(
            'lambert', asShader=True,
            name="{}_{}_lambert".format(selection, x))

        sg = cmds.sets(
            empty=True, renderable=True, noSurfaceShader=True,
            name="{}_{}_sg".format(selection, x))
        cmds.connectAttr(
            sha + ".outColor", sg + ".surfaceShader", force=True)
        cmds.sets(faces, edit=True, forceElement=sg)

        # assign random colors
        cmds.setAttr(
            sha + '.color',
            random.randint(0, 1),
            random.randint(0, 1),
            random.randint(0, 1))


# Creator
def cmdCreator():
    return OpenMayaMPx.asMPxPtr(colorIDCommand())


# Initialize the script plug-in
def initializePlugin(mobject):
    mplugin = OpenMayaMPx.MFnPlugin(mobject)
    try:
        mplugin.registerCommand(kPluginCmdName, cmdCreator)
    except Exception:
        sys.stderr.write("Failed to register command: %s\n" % kPluginCmdName)
        raise


# Uninitialize the script plug-in
def uninitializePlugin(mobject):
    mplugin = OpenMayaMPx.MFnPlugin(mobject)
    try:
        mplugin.deregisterCommand(kPluginCmdName)
    except Exception:
        sys.stderr.write("Failed to unregister command: %s\n" % kPluginCmdName)
