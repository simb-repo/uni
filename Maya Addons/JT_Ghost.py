#Pose ghoster
"""
Developed by Professor JT
Ver 2.0
"""
import maya.cmds as mc
windowID = "JTGhost20193182330"
if mc.window(windowID,q=True, exists = True):
    mc.deleteUI(windowID)
    
mc.window(windowID, t="Pose Ghoster",w=500)
masterLayout = mc.columnLayout()
fieldLayout = mc.rowColumnLayout(nc = 3)
mc.text("Geo to ghost: ")
geoToGhostTF = mc.textField(w=400, ed = False)
mc.button(l="Add Geo", c = "potSelectionIntoField(geoToGhostTF)", bgc = [0,128,0])
mc.text("OPACITY: ")
opacitySlider = mc.floatSlider( min=0, max=10, value=5, step=1, cc="updateTrans()")
mc.setParent(masterLayout)
btnLayout = mc.rowColumnLayout(nc=2)
mc.button(l="Make Ghost Pose", w=240, c = "MakeGhostPose()", bgc = [0,128,0])
mc.button(l="Update Ghost Pose", w=240, c= "UpdateGhostPose()", bgc = [124,252,0])
mc.button(l="<<< Go To Previous Ghost", c="GoToPreviousGhost()")
mc.button(l="Go To Next Ghost >>>", c="GoToNextGhost()")
mc.button(l="Delete Current Ghost", w = 240, c= "deleteCurrentGhost()", bgc = [255,0,0])
mc.button(l="Delete all Ghost", w=240, c= "deleteAllGhosts()", bgc = [0,0,0])
mc.showWindow()

def deleteCurrentGhost():
    if not mc.objExists(getGhostGrpName()):
        return
    objectGhosted = getListFromTF(geoToGhostTF)
    Ghosts = mc.listRelatives(getGhostGrpName(),c=True)
    if objectGhosted==None or Ghosts==None:
        return
    for obj in objectGhosted:
        for item in Ghosts:
            if not mc.objExists(item):
                continue
            item_Frame,itemID_Name = GetGhostIdentification(item)  
            if item_Frame == getCurrentFrame() and itemID_Name == obj:
                mc.delete(item)

def deleteAllGhosts(): 
    mc.delete(getGhostGrpName())

def updateTrans():
    sliderVal = mc.floatSlider(opacitySlider, q=True, v= True)
    trans = 1-sliderVal/10.0
    shader = getGhostShaderName()
    if mc.objExists(shader):
        mc.setAttr(shader + ".transparency",trans,trans,trans,type = "double3" )
        
def getAllGhostedFrames():
    Frames = []
    if mc.objExists(getGhostGrpName()):
        Ghosts = mc.listRelatives(getGhostGrpName(), c=True)
        if Ghosts!=None:
            for Ghost in Ghosts:
                frame, name = GetGhostIdentification(Ghost)
                if frame not in Frames:
                    Frames.append(frame)
    Frames.sort()
    return Frames
        
def GoToPreviousGhost():
    frames = getAllGhostedFrames()
    if frames == None:
        return 
    currentFrame = getCurrentFrame()
    
    #check 2 ends
    if frames[0] > currentFrame:
        return
    if frames[-1] < currentFrame:
        SetCurrentFrame(frames[-1])
        return
    
    #check one by one
    for i in range(1, len(frames)):
        if frames[i] >= currentFrame:
            SetCurrentFrame(frames[i-1])
            break

def SetCurrentFrame(frame):
    mc.currentTime(frame,edit=True)    
        
def GoToNextGhost():
    frames = getAllGhostedFrames()
    if frames == None:
        return 
    currentFrame = getCurrentFrame()
    
    #check 2 ends
    if frames[-1] < currentFrame:
        return
    if frames[0] > currentFrame:
        SetCurrentFrame(frames[0])
        return
    #hceck one by one
    for i in range(1, len(frames)):
        if frames[i] > currentFrame:
            SetCurrentFrame(frames[i])
            break
            
       
#Static Functions to get variable name
def getGhostShaderName():
    return "GhostMat"
def getGhostGrpName():
    return "GhostGrp"
def getFrameAttrName():
    return "frame"  
def getObjAttrName():
    return "objName"
def potSelectionIntoField(field):
    selection = mc.ls(sl=True,l=True)
    selectionText = ",".join(selection)
    mc.textField(field, e=True, tx=selectionText)
    
def getListFromTF(field):
    TFText = mc.textField(field, q=True, tx=True)
    list = TFText.split(",")
    return list
	
def getCurrentFrame():
    currentFrame = mc.currentTime(q=True)
    currentFrameInInt = int(currentFrame)
    return currentFrameInInt
#this funcion is not used
def duplicateShader(obj):
    objShape = mc.listRelatives(obj, s=True)
    materialSG = mc.listConnections(objShape,type = "shadingEngine")[0]
    material = mc.listConnections(materialSG+".surfaceShader")[0]
    GhostMatName = "ghost_" + material
    if not mc.objExists(GhostMatName):
        mc.duplicate(material, n = GhostMatName)
        mc.setAttr(GhostMatName + ".transparency",0.5,0.5,0.5,type = "double3" )
    return GhostMatName
    
def checkAndMakeGhostMat(name):
    if not mc.objExists(name):
        mc.shadingNode('lambert', asShader=True, n=name)
        mc.sets(renderable=True, nss=True, empty=True, name = name+"SG")
        mc.connectAttr(name + ".outColor", name+"SG.surfaceShader",f=True)
        
        mc.setAttr(name + ".transparency",0.5,0.5,0.5,type = "double3" )

def checkAndMakeGhostGrp(name):
    if not mc.objExists(name):
        mc.group(em=True, n=name)
    return name
	
def GenerateGhostName(nameBase):
    GhostName = nameBase + "_" + str(getCurrentFrame())
    return GhostName
	
def AddGhostIdentification(obj, nameAttrValue):
    #Add Currnet Frame Attr
    mc.addAttr(obj, ln = getFrameAttrName(), at = 'long')
    mc.setAttr(obj + "." + getFrameAttrName(), e=True, keyable = True)
    mc.setAttr(obj + "." + getFrameAttrName(), getCurrentFrame())
    
    #Add Object Name Attr
    mc.addAttr(obj, ln = getObjAttrName(), dt = 'string')
    mc.setAttr(obj + "." + getObjAttrName(), e=True, keyable = True)
    mc.setAttr(obj + "." + getObjAttrName(), nameAttrValue,type = "string")
    
def GetGhostIdentification(ghost):
    frame = mc.getAttr(ghost + "." + getFrameAttrName())
    name = mc.getAttr(ghost + "." + getObjAttrName())   
    return frame, name
def UpdateGhostPose():
    deleteCurrentGhost()
    MakeGhostPose()
    
def MakeGhostPose():
    selection = mc.ls(sl=True, l = True)
    objectToGhost = getListFromTF(geoToGhostTF)
    ghostGrp = checkAndMakeGhostGrp(getGhostGrpName())
    
    for item in objectToGhost:
        dupGhost = mc.duplicate(item, name = GenerateGhostName(item))[0]
        AddGhostIdentification(dupGhost, item)	
        GhostMatName = getGhostShaderName()
        checkAndMakeGhostMat(GhostMatName)
        mc.select(dupGhost, r=True)
        mc.sets( e=True, forceElement= GhostMatName + 'SG')
        
        mc.parent(dupGhost, getGhostGrpName())
    mc.select(selection, r=True)