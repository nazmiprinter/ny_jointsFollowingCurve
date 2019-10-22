from maya import cmds
import maya.OpenMaya as om

#AUTHOR = Nazmi Yazici
#EMAIL = nazmiprinter@gmail.com
#WEBSITE = vimeo.com/nazmiprinter
#DATE = 16/05/2019


#script for creating offset group by Josh Sobel
def grpEach():
    
    removeSuff = 1
    
    sel = cmds.ls (sl = True)
    for obj in sel:
        
        if removeSuff == 1:
            
            objShort = obj.replace ('_JNT', '')
            objShort = objShort.replace ('_Jnt', '')
            objShort = objShort.replace ('_Bnd', '')
            objShort = objShort.replace ('_BND', '')
            objShort = objShort.replace ('_Jt', '')
            objShort = objShort.replace ('_CON', '')
            objShort = objShort.replace ('_Con', '')
            objShort = objShort.replace ('_CTRL', '')
            objShort = objShort.replace ('_Ctrl', '')
            objShort = objShort.replace ('_LOC', '')
            objShort = objShort.replace ('_Loc', '')
            objShort = objShort.replace ('_GRP', '')
            objShort = objShort.replace ('_Grp', '')
            objShort = objShort.replace ('_CTRL*', '')
        
        else:
            objShort = obj
        
        par = cmds.listRelatives (obj, p = True)
        
        grp = cmds.group (em = True, w = True, n = '%s_offset' %objShort)
        
        if par != None:
            cmds.parent (grp, par)
        
        cnst = cmds.parentConstraint (obj, grp)
        cmds.delete (cnst)
        cmds.makeIdentity (grp, a = True, s = 1)
        
        cmds.parent (obj, grp)
        cmds.select(grp)
        
    
def jointsFollowingCurve(*arg):

    #INITIAL SETUP

    sel = cmds.ls(sl=True)
    if len(sel) == 0:
        cmds.warning('Please select your curve')
    elif len(sel) >= 2:
        cmds.warning('Please select only one curve')
    else:
        crv = sel[0]
        setupName = cmds.textField('setupName', q=True, tx=True)
        jntInput = cmds.intField('jointCount', q=True, value=True)
        radio1Var = cmds.radioCollection('radio1', q=True, sl=True)
        ctrlNormalVar = cmds.radioCollection('radio2', q=True, sl=True)
        locCB = cmds.checkBox('Offset_Locators', q=True, v=True)
        skinJntInput = cmds.intField('controlCount', q=True, value=True)
        scaleInput = cmds.intField('scaleFloat', q=True, value=True)
        if ctrlNormalVar == 'X':
            ctrlNormal = (1,0,0)
        if ctrlNormalVar == 'Y':
            ctrlNormal = (0,1,0)
        if ctrlNormalVar == 'Z':
            ctrlNormal = (0,0,1)
        jntList = []
        ctrlList = []
        skinJntList = []
        skinPntList = []
        skinCtrlList = []
        locList = []
        ctrlGrp = []


        #JOINT PLACEMENT

        jntCount = int(jntInput) - 1
        jntMinus = jntCount - 1
        param = 0
        paramDiv = 1.000 / float(jntCount)

        if setupName == '':
            cmds.warning('Please give a unique setup name')
        else:
            #FIRST JOINT FOR PARAMETER 0
            firstPnt = cmds.createNode('pointOnCurveInfo', n =setupName + '_POCI_01')
            cmds.setAttr(firstPnt + '.turnOnPercentage', 1)
            firstJnt = cmds.joint(n=setupName + '_JNT_01')
            jntList.append(firstJnt)
            cmds.connectAttr(crv + '.worldSpace[0]', firstPnt + '.inputCurve')
            cmds.connectAttr(firstPnt + '.position', firstJnt + '.translate')
            cmds.setAttr(firstPnt + '.parameter', 0)


            #INBETWEENS
            for x in range(int(jntMinus)):
                pnt = cmds.createNode('pointOnCurveInfo', n =setupName + '_POCI_01')
                cmds.setAttr(pnt + '.turnOnPercentage', 1)
                jnt = cmds.joint(n=setupName + '_JNT_01')
                jntList.append(jnt)
                cmds.connectAttr(crv + '.worldSpace[0]', pnt + '.inputCurve')
                cmds.connectAttr(pnt + '.position', jnt + '.translate')
                param = param + paramDiv 
                cmds.setAttr(pnt + '.parameter', param)
                
                
            #END JOINT FOR PARAMETER 1
            lastPnt = cmds.createNode('pointOnCurveInfo', n =setupName + '_POCI_01')
            cmds.setAttr(lastPnt + '.turnOnPercentage', 1)
            lastJnt = cmds.joint(n=setupName + '_JNT_01')
            jntList.append(lastJnt)
            cmds.connectAttr(crv + '.worldSpace[0]', lastPnt + '.inputCurve')
            cmds.connectAttr(lastPnt + '.position', lastJnt + '.translate')
            cmds.setAttr(lastPnt + '.parameter', 1)

            if locCB:
                #CREATE OFFSET LOCATORS FOR JOINTS
                for loc in jntList:
                    locator = cmds.spaceLocator(n=setupName + '_LOC_01')
                    locList.append(locator)
                    cmds.matchTransform(locator, loc)
                    cmds.parent(loc, locator)
                    tx = cmds.getAttr('{0}.tx'.format(locator[0]))
                    ty = cmds.getAttr('{0}.ty'.format(locator[0]))
                    tz = cmds.getAttr('{0}.tz'.format(locator[0]))
                    cmds.setAttr(locator[0] + '.lpx', tx)
                    cmds.setAttr(locator[0] + '.lpy', ty)
                    cmds.setAttr(locator[0] + '.lpz', tz)
                    cmds.setAttr(locator[0] + '.lsx', scaleInput)
                    cmds.setAttr(locator[0] + '.lsy', scaleInput)
                    cmds.setAttr(locator[0] + '.lsz', scaleInput)
                    cmds.setAttr(locator[0] + '.tx', 0)
                    cmds.setAttr(locator[0] + '.ty', 0)
                    cmds.setAttr(locator[0] + '.tz', 0)
                    cmds.xform(locator[0], cp=True)

            if locCB:   
                for locs in locList:
                    cmds.select(locs, add=True)
                cmds.group(n = setupName + '_LOC_GRP')
                cmds.parent(jntList[-1], locList[-1])
            else:
                cmds.select(jntList, add=True)
                cmds.group(n = setupName + '_JNT_GRP')
            
            cmds.select(cl=True)
            om.MGlobal.displayInfo('Job Done!')

            #CONTROL SETUP
            if radio1Var == 'For_Each_CV':
                #CREATION
                curveCVs = cmds.ls('{0}.cv[:] '.format(crv), fl=True)
                if curveCVs:
                    for cv in curveCVs:
                        clstr = cmds.cluster(cv, n =setupName + '_CLS_01')
                        cmds.setAttr(clstr[0] + 'Handle.v', 0)
                        for x in clstr[::2]:
                            circle = cmds.circle(c=(0,0,0), nr=ctrlNormal, r=scaleInput, ch=0, n =setupName + '_CTRL_01')
                            cmds.setAttr(circle[0] + '.sx', k=False, lock=True)
                            cmds.setAttr(circle[0] + '.sy', k=False, lock=True)
                            cmds.setAttr(circle[0] + '.sz', k=False, lock=True)
                            cmds.matchTransform(circle, clstr)
                            cmds.parent(clstr, circle)
                            cmds.select(circle)
                            selected = cmds.ls(sl=True)
                            ctrlList.append(selected)
                            
                            
                for off in ctrlList:
                    cmds.select(off)
                    grpEach()
                    grp = cmds.ls(sl=True)[0]
                    ctrlGrp.append(grp)

                cmds.select(ctrlGrp)
                cmds.group(n=setupName + '_CTRL_GRP')



                cmds.select(cl=True)
                om.MGlobal.displayInfo('Job Done!')

            elif skinJntInput == 0:
                pass
            elif skinJntInput == 1:
                onlyPnt = cmds.createNode('pointOnCurveInfo', n= setupName + 'onlyPOCI')
                onlyCtrl = cmds.circle(c=(0,0,0), nr=ctrlNormal, r=scaleInput, ch=0, n = setupName + '_CTRL')
                onlyJnt = cmds.joint(n = setupName + '_skin_JNT')
                cmds.setAttr(onlyPnt + '.turnOnPercentage', 1)
                cmds.connectAttr(crv + '.worldSpace[0]', onlyPnt + '.inputCurve')
                cmds.setAttr(onlyPnt + '.parameter', 0.5)
                cmds.connectAttr(onlyPnt + '.result.position', onlyJnt + '.translate')
                cmds.matchTransform(onlyCtrl, onlyJnt)
                cmds.select(onlyCtrl)
                grpEach()
                cmds.group(n = setupName + '_CTRL_GRP')
                cmds.delete(onlyPnt)
                cmds.setAttr(onlyJnt + '.v', 0)
                cmds.setAttr(onlyJnt + '.tx', 0)
                cmds.setAttr(onlyJnt + '.ty', 0)
                cmds.setAttr(onlyJnt + '.tz', 0)
                cmds.select(onlyJnt)
                cmds.select(crv, add=True)
                cmds.skinCluster()
                cmds.select(cl=True)
                
                om.MGlobal.displayInfo('Job Done!')
            else:
                skinJntCount = int(skinJntInput) - 1
                skinJntMinus = skinJntCount - 1
                skinParam = 0
                skinParamDiv = 1.000 / float(skinJntCount)
                
                

                #FIRST SKIN JOINT ON CURVE FOR PARAMETER 0
                skinFirstPnt = cmds.createNode('pointOnCurveInfo', n = setupName + '_skinPOCI_01')
                skinPntList.append(skinFirstPnt)
                cmds.setAttr(skinFirstPnt + '.turnOnPercentage', 1)
                skinFirstJnt = cmds.joint(n=setupName + '_skin_JNT_01')
                skinJntList.append(skinFirstJnt)
                cmds.connectAttr(crv + '.worldSpace[0]', skinFirstPnt + '.inputCurve')
                cmds.connectAttr(skinFirstPnt + '.position', skinFirstJnt + '.translate')
                cmds.setAttr(skinFirstPnt + '.parameter', 0)


                #INBETWEEN SKIN JOINTS
                for x in range(int(skinJntMinus)):
                    skinPnt = cmds.createNode('pointOnCurveInfo', n =setupName + '_skinPOCI_01')
                    skinPntList.append(skinPnt)
                    cmds.setAttr(skinPnt + '.turnOnPercentage', 1)
                    skinJnt = cmds.joint(n=setupName + '_skin_JNT_01')
                    skinJntList.append(skinJnt)
                    cmds.connectAttr(crv + '.worldSpace[0]', skinPnt + '.inputCurve')
                    cmds.connectAttr(skinPnt + '.position', skinJnt + '.translate')
                    skinParam = skinParam + skinParamDiv 
                    cmds.setAttr(skinPnt + '.parameter', skinParam)
                    
                    
                #END SKIN JOINT FOR PARAMETER 1
                skinLastPnt = cmds.createNode('pointOnCurveInfo', n =setupName + '_skinPOCI_01')
                skinPntList.append(skinLastPnt)
                cmds.setAttr(skinLastPnt + '.turnOnPercentage', 1)
                skinLastJnt = cmds.joint(n=setupName + '_skin_JNT_01')
                skinJntList.append(skinLastJnt)
                cmds.connectAttr(crv + '.worldSpace[0]', skinLastPnt + '.inputCurve')
                cmds.connectAttr(skinLastPnt + '.position', skinLastJnt + '.translate')
                cmds.setAttr(skinLastPnt + '.parameter', 1)


                #DELETE POINT ON CURVE INFO NODES AND HIDE SKIN JOINTS
                for clean in range(len(skinJntList)):
                    cmds.disconnectAttr(skinPntList[clean] + '.result.position', skinJntList[clean] + '.translate')
                    cmds.delete(skinPntList[clean])
                    
                for hideJt in skinJntList:
                    cmds.select(hideJt)
                    cmds.setAttr(hideJt + '.v', 0)

                cmds.select(skinJntList)
                cmds.select(crv, add=True)
                cmds.skinCluster()

                
                for ct in skinJntList:
                    skinCtrl = cmds.circle(c=(0,0,0), nr=ctrlNormal, r=scaleInput, ch=0, n = setupName + '_CTRL_01')
                    skinCtrlList.append(skinCtrl)
                    cmds.matchTransform(skinCtrl, ct)
                    cmds.parent(ct, skinCtrl)

                for y in skinCtrlList:
                    cmds.select(y)
                    grpEach()
                    grp = cmds.ls(sl=True)[0]
                    ctrlGrp.append(grp)

                cmds.select(ctrlGrp)
                cmds.group(n=setupName + '_CTRL_GRP')


                cmds.select(cl=True)
                om.MGlobal.displayInfo('Job Done!')

def ny_jFC_UI():

    if(cmds.window('ny_jointsFollowingCurve',q=1,ex=1)):cmds.deleteUI('ny_jointsFollowingCurve')
    cmds.window('ny_jointsFollowingCurve',ret=1,s=0,h=220,w=400,mb=1)
    cmds.gridLayout('gridLayout2',cw=98,w=220,nc=4,h=79,ch=35)
    cmds.text('Setup Name:')
    cmds.textField('setupName')
    cmds.text('Joint Number:',al='center')
    cmds.intField('jointCount', v=2, min=2)
    cmds.text('Control Setup:',al='center')
    cmds.radioCollection('radio1')
    cmds.radioButton('For Each CV')
    cmds.radioButton('Ctrl Number:', en=1, w=100)
    cmds.intField('controlCount', min=0)
    cmds.text('Control Normal:')
    cmds.radioCollection('radio2')
    cmds.radioButton('X', sl=True)
    cmds.radioButton('Y')
    cmds.radioButton('Z')
    cmds.checkBox('Offset Locators')
    cmds.text('Ctrl/Loc Scale:')
    cmds.intField('scaleFloat',v=1.0, min=1)
    cmds.button('BUILD!',w=70, command=jointsFollowingCurve)
    cmds.showWindow('ny_jointsFollowingCurve')
    
ny_jFC_UI()
