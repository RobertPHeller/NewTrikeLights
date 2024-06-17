#*****************************************************************************
#
#  System        : 
#  Module        : 
#  Object Name   : $RCSfile$
#  Revision      : $Revision$
#  Date          : $Date$
#  Author        : $Author$
#  Created By    : Robert Heller
#  Created       : Mon Jun 17 12:18:18 2024
#  Last Modified : <240617.1401>
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


import sys
import os
sys.path.append("/home/heller/kicad-footprint-generator/")

from math import *

from KicadModTree import *
from KicadModTree.nodes.specialized.PadArray import PadArray

if __name__ == '__main__':
    footprint_name = "MRJE3404"
    
    # init kicad footprint
    kicad_mod = Footprint(footprint_name, FootprintType.THT)
    kicad_mod.setDescription("MRJE 3P4T rotatary switch, PC pins")
    
    # set general values
    kicad_mod.append(Property(name=Property.REFERENCE, text='REF**', at=[0,-3], layer='F.SilkS'))
    kicad_mod.append(Property(name=Property.VALUE, text=footprint_name, at=[1.5,3], layer='F.Fab'))

    # create silscreen
    kicad_mod.append(Circle(center=[0,0], radius=6.1845, layer='F.SilkS', width=0.15))

    # create courtyard
    kicad_mod.append(Circle(center=[0,0], radius=6.5, layer='F.CrtYd', width=0.15, offset=2))

    # C1 = 13  Angle=-180
    #  1 = 1   Angle=-(180+15)
    #  2 = 2   Angle=-(180+30)
    #  3 = 3   Angle=-(180+45)
    #  4 = 4   Angle=-270
    # C2 = 14  Angle=-(270+15)
    #  1 = 5   Angle=-(270+30)
    #  2 = 6   Angle=-(270+45)
    #  3 = 7   Angle=0
    #  4 = 8   Angle=-30
    # C3 = 15  Angle=-(30+15)
    #  1 = 9   Angle=-90
    #  2 = 10  Angle=-(90+15)
    #  3 = 11  Angle=-(90+30)
    #  4 = 12  Angle=-(90+45)
    pads = [(13,-180), (1,-(180+15)), (2,-(180+30)), (3,-(180+45)), (4,-270), \
            (14,-(270+15)), (5,-(270+30)), (6,-(270+45)), (7,0), (8,-30), \
            (15,-(30+15)), (9,-90), (10,-(90+15)), (11,-(90+30)), (12,-(90+45))]
    # pads: thru_hole, circle, size 1.524 1.524 drill 0.762, layers *.Cu *.Mask    
    # Arranged on a circle centered at 0,0, with radius of 5.99440 mm
    # kicad_mod.append(Pad(number=22, type=Pad.TYPE_THT, shape=Pad.SHAPE_CIRCLE, at=[X,Y], size=[1.524,1.524], drill=.762, layers=['*.Cu', '*.Mask', 'F.SilkS']))
    CenterX=0
    CenterY=0
    Radius=5.99440
    for (number,angle) in pads:
        posangle = 360-angle
        rads = pi*(posangle/180.0)
        X = Radius*cos(rads)
        Y = Radius*sin(rads)
        kicad_mod.append(Pad(number=number, type=Pad.TYPE_THT, shape=Pad.SHAPE_CIRCLE, at=[X,Y], size=[1.524,1.524], drill=.762, layers=['*.Cu', '*.Mask']))
    # write file
    file_handler = KicadFileHandler(kicad_mod)
    file_handler.writeFile('MRJE3404.kicad_modXX')
