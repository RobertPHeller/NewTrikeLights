#*****************************************************************************
#
#  System        : 
#  Module        : 
#  Object Name   : $RCSfile$
#  Revision      : $Revision$
#  Date          : $Date$
#  Author        : $Author$
#  Created By    : Robert Heller
#  Created       : Tue Jun 25 13:48:11 2024
#  Last Modified : <240625.1624>
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
import math

import datetime

class BiFlasherHousing(object):
    __BoardWidth    = 19.05
    __BoardLength   = 25.4
    __HousingWidth  = 19.05+(.125*25.4)
    __HousingLength = 25.4+(.125*25.4)
    __DepthAbove    = 3
    __DepthBelow    = 3
    __DepthBottom   = .125*25.4
    __NutWidth      = (1.0/4.0)*25.4
    __NutThick      = (3.0/32.0)*25.4
    __MHoles        = [(7.14375,7.14375), (7.14375,21.43125), \
                       (15.08125,21.43125), (15.08125,7.14375)] 
    __MHoleRadius   = (.1285*25.4)/2
    __30DegRadians  = (30.0/180.0)*math.pi
    __PoleRadius    = (.25*25.4)/2.0
    def __HexNut(self,origin):
        if not isinstance(origin,Base.Vector):
            raise RuntimeError("origin is not a Vector!")
        points = []
        nw2=self.__NutWidth/2.0
        h = math.tan(self.__30DegRadians)*nw2
        fw = math.sqrt((h*h)+(nw2*nw2))
        #print("*** BiFlasherHousing.__HexNut(): __30DegRadians is %g, __NutWidth is %g, nw2 is %g, h is %g, fw is %g"%(self.__30DegRadians,self.__NutWidth,nw2,h,fw));
        for i in range(6):
            angle = i * 2 * math.pi / 6
            angle += self.__30DegRadians
            x = math.cos(angle)*fw
            y = math.sin(angle)*fw
            points.append(origin.add(Base.Vector(x, y, 0)))
        angle = 0 * 2 * math.pi / 6
        angle += self.__30DegRadians
        x = math.cos(angle)*fw
        y = math.sin(angle)*fw
        points.append(origin.add(Base.Vector(x, y, 0)))
        return Part.Face(Part.makePolygon(points))\
                .extrude(Base.Vector(0,0,self.__NutThick))
    def __init__(self,name,origin):
        self.name = name
        if not isinstance(origin,Base.Vector):
            raise RuntimeError("origin is not a Vector!")
        self.origin = origin
        housing = Part.makePlane(self.__HousingWidth,self.__HousingLength,\
                                 origin)\
                      .extrude(Base.Vector(0,0,(self.__PoleRadius*.8)+\
                                               self.__DepthBottom+\
                                               self.__NutThick))
        poleCut = Part.Face(Part.Wire(Part.makeCircle(self.__PoleRadius,\
                                                      origin.add(Base.Vector(0,self.__HousingLength/2,-(self.__PoleRadius*.2))),\
                                                      Base.Vector(1,0,0))))\
                       .extrude(Base.Vector(self.__HousingWidth,0,0))
        housing = housing.cut(poleCut)
        #self.nuts = []
        for x,y in self.__MHoles:
            mhole = Part.Face(Part.Wire(Part.makeCircle(self.__MHoleRadius,\
                                                        origin.add(Base.Vector(x,y,0)))))\
                      .extrude(Base.Vector(0,0,(self.__PoleRadius*.8)+\
                                               self.__DepthBottom+\
                                               self.__NutThick))
            housing = housing.cut(mhole)
            nut = self.__HexNut(origin.add(Base.Vector(x,y,\
                                                       (self.__PoleRadius*.8)+\
                                                       self.__DepthBottom)))
            housing = housing.cut(nut)
            #self.nuts.append(nut)
        self.housing = housing
    def show(self,doc=None):
        if doc==None:
            doc = App.activeDocument()
        obj = doc.addObject("Part::Feature",self.name+"_housing")
        obj.Shape=self.housing
        obj.Label=self.name+"_housing"
        obj.ViewObject.ShapeColor=tuple([0.7,0.7,0.7])
        #i = 0
        #for n in self.nuts:
        #    nlab = ("_nut%d"%i)
        #    obj = doc.addObject("Part::Feature",self.name+nlab)
        #    obj.Shape=n
        #    obj.Label=self.name+nlab
        #    obj.ViewObject.ShapeColor=tuple([0.9,0.9,0.9])
        #    i += 1

if __name__ == '__main__':
    docs = App.listDocuments()
    for k in docs:
        App.closeDocument(k)
    App.ActiveDocument=App.newDocument("Temp")
    doc = App.activeDocument()
    x = BiFlasherHousing("Housing",Base.Vector(0,0,0))
    x.show(doc)
    Gui.SendMsgToActiveView("ViewFit")
    Gui.activeDocument().activeView().viewTop()
    
