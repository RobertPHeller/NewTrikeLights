#*****************************************************************************
#
#  System        : 
#  Module        : 
#  Object Name   : $RCSfile$
#  Revision      : $Revision$
#  Date          : $Date$
#  Author        : $Author$
#  Created By    : Robert Heller
#  Created       : Sun Jun 23 19:39:24 2024
#  Last Modified : <240624.1503>
#
#  Description	
#
#  Notes
#
#  History
#	
#*****************************************************************************
#
#    Copyright (C) 2024  Robert Heller D/B/A Deepwoods Software
#			51 Locke Hill Road
#			Wendell, MA 01379-9728
#
#    This program is free software; you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation; either version 2 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program; if not, write to the Free Software
#    Foundation, Inc., 675 Mass Ave, Cambridge, MA 02139, USA.
#
# 
#
#*****************************************************************************

import Part, TechDraw, Spreadsheet, TechDrawGui
import FreeCADGui
from FreeCAD import Console
from FreeCAD import Base
import FreeCAD as App
import os
import sys
sys.path.append(os.path.dirname(__file__))

import datetime

class HeadlightSwitchBodyCoverDrillSheet(object):
    __BoardWidth  = 88.35
    __BoardHeight = 25.4
    __SwitchHoleX = 41.445
    __SwitchHoleY = 12.954
    __SwitchHoleR = (.25*25.4)/2.0
    __MountHoleX1 = 2.45
    __MountHoleX2 = 88.35-2.45
    __MountHoleY  = 12.7
    __MountHoleR  = (2.2)/2.0
    __MountStandR = (.1875*25.4)/2.0
    __LEDsY       = 6.604
    __LEDHiBeamX  = 8.382
    __LEDLoBeamX  = 8.382+2.54
    __LEDMarkerX  = 8.382+2.54+2.54
    __LEDsR       = (.0625*25.4)/2.0
    __SwitchDepth = .3*25.4
    __LEDRodLength = ((.125*25.4)+(.3*25.4))-.7
    __CoverThick = .125*25.4
    def __init__(self,name,origin):
        self.name = name
        if not isinstance(origin,Base.Vector):
            raise RuntimeError("origin is not a Vector!")
        self.origin = origin
        cover = Part.makePlane(self.__BoardWidth,self.__BoardHeight,origin)\
                .extrude(Base.Vector(0,0,self.__CoverThick))
        switchhole = Part.Face(Part.Wire(Part.makeCircle(self.__SwitchHoleR,origin.add(Base.Vector(self.__SwitchHoleX,self.__BoardHeight-self.__SwitchHoleY,0)))))\
                .extrude(Base.Vector(0,0,self.__CoverThick))
        cover = cover.cut(switchhole)
        mounthole = Part.Face(Part.Wire(Part.makeCircle(self.__MountHoleR,origin.add(Base.Vector(self.__MountHoleX1,self.__MountHoleY,0)))))\
                .extrude(Base.Vector(0,0,self.__CoverThick))
        cover = cover.cut(mounthole)
        mounthole = Part.Face(Part.Wire(Part.makeCircle(self.__MountHoleR,origin.add(Base.Vector(self.__MountHoleX2,self.__MountHoleY,0)))))\
                .extrude(Base.Vector(0,0,self.__CoverThick))
        cover = cover.cut(mounthole)
        LEDHole = Part.Face(Part.Wire(Part.makeCircle(self.__LEDsR,origin.add(Base.Vector(self.__LEDHiBeamX,self.__BoardHeight-self.__LEDsY,0)))))\
                .extrude(Base.Vector(0,0,self.__CoverThick))
        cover = cover.cut(LEDHole)
        LEDHole = Part.Face(Part.Wire(Part.makeCircle(self.__LEDsR,origin.add(Base.Vector(self.__LEDLoBeamX,self.__BoardHeight-self.__LEDsY,0)))))\
                .extrude(Base.Vector(0,0,self.__CoverThick))
        cover = cover.cut(LEDHole)
        LEDHole = Part.Face(Part.Wire(Part.makeCircle(self.__LEDsR,origin.add(Base.Vector(self.__LEDMarkerX,self.__BoardHeight-self.__LEDsY,0)))))\
                .extrude(Base.Vector(0,0,self.__CoverThick))
        cover = cover.cut(LEDHole)
        self.cover = cover
        self.rodHiBeam = Part.Face(Part.Wire(Part.makeCircle(self.__LEDsR,origin.add(Base.Vector(self.__LEDHiBeamX,self.__BoardHeight-self.__LEDsY,self.__CoverThick)))))\
                .extrude(Base.Vector(0,0,-self.__LEDRodLength))
        self.rodLoBeam = Part.Face(Part.Wire(Part.makeCircle(self.__LEDsR,origin.add(Base.Vector(self.__LEDLoBeamX,self.__BoardHeight-self.__LEDsY,self.__CoverThick)))))\
                .extrude(Base.Vector(0,0,-self.__LEDRodLength))
        self.rodMarker = Part.Face(Part.Wire(Part.makeCircle(self.__LEDsR,origin.add(Base.Vector(self.__LEDMarkerX,self.__BoardHeight-self.__LEDsY,self.__CoverThick)))))\
                .extrude(Base.Vector(0,0,-self.__LEDRodLength))
        standOff = Part.Face(Part.Wire(Part.makeCircle(self.__MountStandR,origin.add(Base.Vector(self.__MountHoleX1,self.__MountHoleY,0)))))\
                .extrude(Base.Vector(0,0,-self.__SwitchDepth))
        self.standOff1 = standOff.cut(Part.Face(Part.Wire(Part.makeCircle(self.__MountHoleR,origin.add(Base.Vector(self.__MountHoleX1,self.__MountHoleY,0)))))\
                .extrude(Base.Vector(0,0,-self.__SwitchDepth)))
        standOff = Part.Face(Part.Wire(Part.makeCircle(self.__MountStandR,origin.add(Base.Vector(self.__MountHoleX2,self.__MountHoleY,0)))))\
                .extrude(Base.Vector(0,0,-self.__SwitchDepth))
        self.standOff2 = standOff.cut(Part.Face(Part.Wire(Part.makeCircle(self.__MountHoleR,origin.add(Base.Vector(self.__MountHoleX2,self.__MountHoleY,0)))))\
                .extrude(Base.Vector(0,0,-self.__SwitchDepth)))
    def show(self,doc=None):
        if doc==None:
            doc = App.activeDocument()
        obj = doc.addObject("Part::Feature",self.name+"_cover")
        obj.Shape=self.cover
        obj.Label=self.name+"_cover"
        obj.ViewObject.ShapeColor=tuple([0.7,0.7,0.7])
        self.coverObj = obj
        obj = doc.addObject("Part::Feature",self.name+"_HiBeam")
        obj.Shape=self.rodHiBeam
        obj.Label=self.name+"_HiBeam"
        obj.ViewObject.ShapeColor=tuple([1.0,1.0,1.0])
        obj.ViewObject.Transparency=90
        obj = doc.addObject("Part::Feature",self.name+"_LoBeam")
        obj.Shape=self.rodLoBeam
        obj.Label=self.name+"_LoBeam"
        obj.ViewObject.ShapeColor=tuple([0.0,0.0,1.0])
        obj.ViewObject.Transparency=90
        obj = doc.addObject("Part::Feature",self.name+"_Marker")
        obj.Shape=self.rodMarker
        obj.Label=self.name+"_Marker"
        obj.ViewObject.ShapeColor=tuple([0.0,1.0,0.0])
        obj.ViewObject.Transparency=90
        obj = doc.addObject("Part::Feature",self.name+"_standOff1")
        obj.Shape=self.standOff1
        obj.Label=self.name+"_standOff1"
        obj.ViewObject.ShapeColor=tuple([0.7,0.7,0.7])
        obj.ViewObject.Transparency=50
        obj = doc.addObject("Part::Feature",self.name+"_standOff2")
        obj.Shape=self.standOff2
        obj.Label=self.name+"_standOff2"
        obj.ViewObject.ShapeColor=tuple([0.7,0.7,0.7])
        obj.ViewObject.Transparency=50
    def TechPage(self,doc=None):
        if doc==None:
            doc = App.activeDocument()
        for g in doc.findObjects('TechDraw::DrawSVGTemplate'):
            doc.removeObject(g.Name)
        for g in doc.findObjects('TechDraw::DrawPage'):
            doc.removeObject(g.Name)
        for g in doc.findObjects('Spreadsheet::Sheet'):
            doc.removeObject(g.Name)
        for g in doc.findObjects('TechDraw::DrawViewPart'):
            doc.removeObject(g.Name)
        for g in doc.findObjects('TechDraw::DrawViewDimension'):
            doc.removeObject(g.Name)
        doc.addObject('TechDraw::DrawSVGTemplate','USLetterTemplate')
        doc.USLetterTemplate.Template = App.getResourceDir()+"Mod/TechDraw/Templates/USLetter_Landscape.svg"
        edt = doc.USLetterTemplate.EditableTexts
        doc.addObject('TechDraw::DrawSVGTemplate','USLetterTemplate')
        doc.USLetterTemplate.Template = App.getResourceDir()+"Mod/TechDraw/Templates/USLetter_Landscape.svg"
        edt = doc.USLetterTemplate.EditableTexts
        edt['CompanyName'] = "Deepwoods Software"
        edt['CompanyAddress'] = '51 Locke Hill Road, Wendell, MA 01379 USA'    
        edt['DrawingTitle1']= 'Headlight Switch Body Cover'
        edt['DrawingTitle3']= ""
        edt['DrawnBy'] = "Robert Heller"
        edt['CheckedBy'] = ""
        edt['Approved1'] = ""
        edt['Approved2'] = ""
        edt['Code'] = ""
        edt['Weight'] = ''
        edt['DrawingNumber'] = datetime.datetime.now().ctime()
        edt['Revision'] = "A"
        doc.USLetterTemplate.EditableTexts = edt
        doc.addObject('TechDraw::DrawPage','BodyCoverDrillSheet')        
        doc.BodyCoverDrillSheet.Template = doc.USLetterTemplate
        edt = doc.BodyCoverDrillSheet.Template.EditableTexts
        edt['DrawingTitle2']= "Drill Template"
        edt['Scale'] = '1.0'
        edt['Sheet'] = "Sheet 1 of 1"
        doc.BodyCoverDrillSheet.Template.EditableTexts = edt
        doc.BodyCoverDrillSheet.ViewObject.show() 
        drillsheet = doc.addObject('Spreadsheet::Sheet','DrillTemplateDimensionTable')
        drillsheet.set("A1",'%-11.11s'%"Dim")
        drillsheet.set("B1",'%10.10s'%"inch")
        drillsheet.set("C1",'%10.10s'%"mm") 
        ir = 2
        doc.addObject('TechDraw::DrawViewPart','CoverTopView')
        doc.BodyCoverDrillSheet.addView(doc.CoverTopView)
        doc.CoverTopView.Source = self.coverObj
        doc.CoverTopView.Direction=(0.0,0.0,1.0)
        doc.CoverTopView.Scale = 1
        doc.CoverTopView.X =  90
        doc.CoverTopView.Y = 130
        #**************
        #minX = 999999999
        #minY = 999999999
        #maxX = 0
        #maxY = 0
        #i = 0
        #for v in self.cover.Vertexes:
        #   if v.X < minX:
        #       minX = v.X
        #   if v.X > maxX:
        #       maxX = v.X    
        #   if v.Y < minY:
        #       minY = v.Y
        #   if v.Y > maxY:
        #       maxY = v.Y
        #   print ('*** TechPage(): Vertexes[%d] at (%g,%g,%g)'%(i,v.X,v.Y,v.Z))
        #   i += 1
        #length = maxX - minX
        #height = maxY - minY
        #print ('*** TechPage(): origin (%g,%g), length = %g, height = %g'%(minX,minY,length,height))    
        #i = 0
        #for e in self.cover.Edges:
        #    if isinstance(e.Curve,Part.Circle):
        #        #print('*** TechPage(): Edges[%d].Curve is a %s'%(i,type(e.Curve)))
        #        circ = e.Curve
        #        print('*** TechPage(): Edges[%d].Curve %g at (%g,%g,%g)'%\
        #              (i,circ.Radius*2,circ.Location.x,circ.Location.y,circ.Location.z))
        #    i += 1
        #*********
        doc.addObject('TechDraw::DrawViewDimension','SwitchShaftHDia')
        doc.SwitchShaftHDia.Type = 'Diameter'
        doc.SwitchShaftHDia.References2D=[(doc.CoverTopView,'Edge5')]
        doc.SwitchShaftHDia.FormatSpec='SWHDia'
        doc.SwitchShaftHDia.Arbitrary = True
        doc.SwitchShaftHDia.X = -5
        doc.SwitchShaftHDia.Y = 41
        doc.BodyCoverDrillSheet.addView(doc.SwitchShaftHDia)
        drillsheet.set("A%d"%ir,'%-11.11s'%"SWHDia")
        drillsheet.set("B%d"%ir,'%10.6f'%((self.__SwitchHoleR*2)/25.4))
        drillsheet.set("C%d"%ir,'%10.6f'%(self.__SwitchHoleR*2))
        ir += 1
        doc.addObject('TechDraw::DrawViewDimension','MountHoleHDia')
        doc.MountHoleHDia.Type = 'Diameter'
        doc.MountHoleHDia.References2D=[(doc.CoverTopView,'Edge4')]
        doc.MountHoleHDia.FormatSpec='MHDia (2x)'
        doc.MountHoleHDia.Arbitrary = True
        doc.MountHoleHDia.X = -38
        doc.MountHoleHDia.Y = -25
        doc.BodyCoverDrillSheet.addView(doc.MountHoleHDia)
        drillsheet.set("A%d"%ir,'%-11.11s'%"MHDia")
        drillsheet.set("B%d"%ir,'%10.6f'%((self.__MountHoleR*2)/25.4))
        drillsheet.set("C%d"%ir,'%10.6f'%(self.__MountHoleR*2))
        ir += 1
        doc.addObject('TechDraw::DrawViewDimension','LEDHoleHDia')
        doc.LEDHoleHDia.Type = 'Diameter'
        doc.LEDHoleHDia.References2D=[(doc.CoverTopView,'Edge9')]
        doc.LEDHoleHDia.FormatSpec='LEDHDia (3x)'
        doc.LEDHoleHDia.Arbitrary = True
        doc.LEDHoleHDia.X = -30.5
        doc.LEDHoleHDia.Y = 33.5
        doc.BodyCoverDrillSheet.addView(doc.LEDHoleHDia)
        drillsheet.set("A%d"%ir,'%-11.11s'%"MHDia")
        drillsheet.set("B%d"%ir,'%10.6f'%((self.__LEDsR*2)/25.4))
        drillsheet.set("C%d"%ir,'%10.6f'%(self.__LEDsR*2))
        ir += 1
        doc.addObject('TechDraw::DrawViewSpreadsheet','HeadlightSwitchDrillDimBlock')
        doc.BodyCoverDrillSheet.addView(doc.HeadlightSwitchDrillDimBlock)
        doc.HeadlightSwitchDrillDimBlock.Source = drillsheet
        doc.HeadlightSwitchDrillDimBlock.TextSize = 8
        doc.HeadlightSwitchDrillDimBlock.CellEnd = "C%d"%(ir-1)
        doc.HeadlightSwitchDrillDimBlock.recompute()
        doc.HeadlightSwitchDrillDimBlock.X = 195
        doc.HeadlightSwitchDrillDimBlock.Y = 130
        doc.BodyCoverDrillSheet.recompute()
        doc.recompute()
        
if __name__ == '__main__':
    docs = App.listDocuments()
    for k in docs:
        App.closeDocument(k)
    App.ActiveDocument=App.newDocument("Temp")
    doc = App.activeDocument()
    cover = HeadlightSwitchBodyCoverDrillSheet("cover",Base.Vector(0,0,0))
    cover.show()
    Gui.SendMsgToActiveView("ViewFit")
    Gui.activeDocument().activeView().viewTop()
    cover.TechPage()
