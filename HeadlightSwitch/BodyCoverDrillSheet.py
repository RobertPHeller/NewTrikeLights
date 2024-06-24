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
#  Last Modified : <240624.0006>
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
        switchhole = Part.Face(Part.Wire(Part.makeCircle(self.__SwitchHoleR,origin.add(Base.Vector(self.__SwitchHoleX,self.__SwitchHoleY,0)))))\
                .extrude(Base.Vector(0,0,self.__CoverThick))
        cover = cover.cut(switchhole)
        mounthole = Part.Face(Part.Wire(Part.makeCircle(self.__MountHoleR,origin.add(Base.Vector(self.__MountHoleX1,self.__MountHoleY,0)))))\
                .extrude(Base.Vector(0,0,self.__CoverThick))
        cover = cover.cut(mounthole)
        mounthole = Part.Face(Part.Wire(Part.makeCircle(self.__MountHoleR,origin.add(Base.Vector(self.__MountHoleX2,self.__MountHoleY,0)))))\
                .extrude(Base.Vector(0,0,self.__CoverThick))
        cover = cover.cut(mounthole)
        LEDHole = Part.Face(Part.Wire(Part.makeCircle(self.__LEDsR,origin.add(Base.Vector(self.__LEDHiBeamX,self.__LEDsY,0)))))\
                .extrude(Base.Vector(0,0,self.__CoverThick))
        cover = cover.cut(LEDHole)
        LEDHole = Part.Face(Part.Wire(Part.makeCircle(self.__LEDsR,origin.add(Base.Vector(self.__LEDLoBeamX,self.__LEDsY,0)))))\
                .extrude(Base.Vector(0,0,self.__CoverThick))
        cover = cover.cut(LEDHole)
        LEDHole = Part.Face(Part.Wire(Part.makeCircle(self.__LEDsR,origin.add(Base.Vector(self.__LEDMarkerX,self.__LEDsY,0)))))\
                .extrude(Base.Vector(0,0,self.__CoverThick))
        cover = cover.cut(LEDHole)
        self.cover = cover
        self.rodHiBeam = Part.Face(Part.Wire(Part.makeCircle(self.__LEDsR,origin.add(Base.Vector(self.__LEDHiBeamX,self.__LEDsY,self.__CoverThick)))))\
                .extrude(Base.Vector(0,0,-self.__LEDRodLength))
        self.rodLoBeam = Part.Face(Part.Wire(Part.makeCircle(self.__LEDsR,origin.add(Base.Vector(self.__LEDLoBeamX,self.__LEDsY,self.__CoverThick)))))\
                .extrude(Base.Vector(0,0,-self.__LEDRodLength))
        self.rodMarker = Part.Face(Part.Wire(Part.makeCircle(self.__LEDsR,origin.add(Base.Vector(self.__LEDMarkerX,self.__LEDsY,self.__CoverThick)))))\
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

if __name__ == '__main__':
    App.ActiveDocument=App.newDocument("Temp")
    doc = App.activeDocument()
    cover = HeadlightSwitchBodyCoverDrillSheet("cover",Base.Vector(0,0,0))
    cover.show()
    Gui.SendMsgToActiveView("ViewFit")
    Gui.activeDocument().activeView().viewTop()
    
