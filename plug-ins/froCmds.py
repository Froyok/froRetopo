import maya.OpenMaya as om
import maya.OpenMayaMPx as mpx
import maya.OpenMayaUI as omUI
import math
import sys


# Plugin Settings
pluginCmdVertex = 'froVertexFinder'
pluginCmdName = 'froRayTrace'
vendor = 'Passerby & Froyok'
pluginVer = '1.1'
apiVersion = 'Any'

# Flags
kFroIndexF = '-fid'
kFroIndexLF = '-froIndex'
kFroRangeF = '-frg'
kFroRangeLF = '-froRange'
      
kDragPointF = '-dp'
kDragPointLF = '-dragPoint'
            
            

class froVertexFinder(mpx.MPxCommand):
    def __init__(self):
        mpx.MPxCommand.__init__(self)
  
    # Invoked when the command is run.
    def doIt(self, args):        
        # arguments
        argData = om.MArgParser(self.syntax(), args)
        index = argData.flagArgumentInt(kFroIndexF, 0) #currently selected vertex (index)
        range = argData.flagArgumentDouble(kFroRangeF, 0) #max distance to find a vertex
        
        # get the active selection
        sel = om.MSelectionList()
        om.MGlobal.getActiveSelectionList( sel )
        list = om.MItSelectionList(sel, om.MFn.kMesh)
        
        # get mesh
        mesh = None
        dagPath = om.MDagPath()
        list.getDagPath( dagPath )
        mesh = om.MFnMesh( dagPath )
        
        #define variables to find the vertex
        nb = mesh.numVertices()
        point = om.MPoint() #target point

        foundVtx = 0
        closestVert = 0
        minLength = None
        pos = om.MPoint()
        mesh.getPoint(index, pos, om.MSpace.kWorld)

        
        # search for the nearest vertex
        count = 0
        while count < nb :
            # ignore vertex already selected by user
            if count != index :
                #get point by its index
                mesh.getPoint(count, point, om.MSpace.kWorld)
                dist = pos.distanceTo( point )
                
                #if the vtx is the closest, save it (only if we are under the user range)
                if dist <= range :
                    if minLength is None or dist < minLength:
                        foundVtx = 1
                        minLength = dist
                        closestVert = count
                    
            count += 1

        #send the closest vertex to the user
        resultArray = om.MDoubleArray()
        resultArray.append( foundVtx )
        resultArray.append( closestVert )
        
        self.clearResult()
        self.setResult( resultArray )


    @classmethod
    def cmdCreator(cls):
        return mpx.asMPxPtr(cls())

    @staticmethod
    def syntaxCreator():
        syntax = om.MSyntax()
        syntax.addFlag(kFroIndexF, kFroIndexLF, om.MSyntax.kLong)
        syntax.addFlag(kFroRangeF, kFroRangeLF, om.MSyntax.kDouble)
        return syntax

        
class froRayTrace(mpx.MPxCommand):
    def __init__(self):
        mpx.MPxCommand.__init__(self)

    def doIt(self, args):
        self.parseArguments(args)
        self.live = liveMesh(self.obj)

        result = self.live.rayCast(self.flagValue)

        resultArray = om.MDoubleArray()
        if result:
            # resultArray.append(True)
            resultArray.append(float(1))
            resultArray.append(float(result[0]))
            resultArray.append(float(result[1]))
            resultArray.append(float(result[2]))
            self.clearResult()
            self.setResult(resultArray)
        else:
            # resultArray.append(False)
            resultArray.append(float(0))
            resultArray.append(float(0))
            resultArray.append(float(0))
            resultArray.append(float(0))
            self.clearResult()
            self.setResult(resultArray)

    def parseArguments(self, args):
        argData = om.MArgParser(self.syntax(), args)

        # Drag point
        self.flagValue = []
        self.flagValue.append(argData.flagArgumentDouble(kDragPointF, 0))
        self.flagValue.append(argData.flagArgumentDouble(kDragPointF, 1))
        self.flagValue.append(argData.flagArgumentDouble(kDragPointF, 2))

        # Live Object
        self.obj = argData.commandArgumentString(0)

    @classmethod
    def cmdCreator(cls):
        return mpx.asMPxPtr(cls())

    @staticmethod
    def syntaxCreator():
        syntax = om.MSyntax()
        syntax.addArg(om.MSyntax.kString)
        syntax.addFlag(kDragPointF, kDragPointLF, om.MSyntax.kDouble, om.MSyntax.kDouble, om.MSyntax.kDouble)
        return syntax


class camera(object):
    '''
    Object to get Camera data
    '''
    def __init__(self):
        #get VP camera info
        self.activeView = omUI.M3dView.active3dView()
        self.cameraPath = om.MDagPath()
        self.activeView.getCamera(self.cameraPath)
        self.cameraFn = om.MFnCamera(self.cameraPath)
        self.cameraName = (self.cameraFn.fullPathName()).split('|')[-1]

    @property
    def dirVec(self):
        return self.cameraFn.viewDirection(om.MSpace.kWorld)

    @property
    def loc(self):
        return self.cameraFn.eyePoint(om.MSpace.kWorld)


class liveMesh(object):
    '''Live Mesh'''
    def __init__(self, obj):
        '''
        Get Live Mesh and add function set
        '''
        # Get orgnial Selection List
        oldSel = om.MSelectionList()
        om.MGlobal.getActiveSelectionList(oldSel)

        sel = om.MSelectionList()
        # Select mesh in parms
        om.MGlobal.selectByName(obj, om.MGlobal.kReplaceList)
        om.MGlobal.getActiveSelectionList(sel)

        # Restore old selection
        om.MGlobal.setActiveSelectionList(oldSel)

        dag = om.MDagPath()
        sel.getDagPath(0, dag)
        self.liveFn = om.MFnMesh(dag)

        # define camera object to project from
        self.cam = camera()

    def rayCast(self, dp):
        '''
        Ray Cast method of live mesh
        args:
            dp(list): dragPoint vector

        returns:
            result(list): hitPoint
        '''

        # source
        raySource = om.MFloatPoint()
        raySource.setCast(self.cam.loc)

        # rayDirection
        draggerValues = om.MFloatPoint(dp[0], dp[1], dp[2])
        rayDirection = draggerValues - raySource
        rayDirection.normalize()

        # Test data against camera vecotor and invert of needed.
        camVec = om.MFloatVector(self.cam.dirVec)
        vecTest = rayDirection * camVec
        if vecTest < 0:
            rebuild = rayDirection.x, rayDirection.y, rayDirection.z
            rebuild = -rebuild[0], -rebuild[1], -rebuild[2]
            rayDirection = om.MFloatVector(rebuild[0], rebuild[1], rebuild[2])

        # HitPoint
        hitPoint = om.MFloatPoint()

        idsSorted = False
        testBothDirections = False
        faceIds = None
        triIds = None
        accelParams = None
        hitRayParam = None
        hitTriangle = None
        hitFacePtr = None
        hitBary1 = None
        hitBary2 = None

        maxParam = 10000.0
        space = om.MSpace.kWorld

        # tolerance = 0.1

        hit = self.liveFn.closestIntersection(raySource,
                                              rayDirection,
                                              faceIds,
                                              triIds,
                                              idsSorted,
                                              space,
                                              maxParam,
                                              testBothDirections,
                                              accelParams,
                                              hitPoint,
                                              hitRayParam,
                                              hitFacePtr,
                                              hitTriangle,
                                              hitBary1,
                                              hitBary2)

        if hit:
            return hitPoint.x, hitPoint.y, hitPoint.z
        else:
            return False
        
        
        
        
        
        


# init plug-in
def initializePlugin(mobject):
    mplugin = mpx.MFnPlugin(mobject, vendor, pluginVer, apiVersion)
      
    try:
        mplugin.registerCommand(pluginCmdName, froRayTrace.cmdCreator, froRayTrace.syntaxCreator)
    except:
        sys.stderr.write('Failed to register command: %s\n' % pluginCmdName)
        raise
      
    try:
        mplugin.registerCommand(pluginCmdVertex, froVertexFinder.cmdCreator, froVertexFinder.syntaxCreator)
    except:
        sys.stderr.write('Failed to register command: %s\n' % pluginCmdVertex)
        raise

        
# Uninitialize the script plug-in
def uninitializePlugin(mobject):
    mplugin = mpx.MFnPlugin(mobject)
     
    try:
        mplugin.deregisterCommand(pluginCmdName)
    except:
        sys.stderr.write('Failed to unregister command: %s\n' % pluginCmdName)
     
    try:
        mplugin.deregisterCommand(pluginCmdVertex)
    except:
        sys.stderr.write('Failed to unregister command: %s\n' % pluginCmdVertex)
        
