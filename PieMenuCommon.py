# Pie menu for FreeCAD
# Copyright (C) 2015, 2016 (as part of TabBar) triplus @ FreeCAD
# Copyright (C) 2017, 2018, 2019 (as part of CommandPanel) triplus @ FreeCAD
# Copyright (C) 2020 triplus @ FreeCAD
#
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this library; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301 USA

"""Pie menu for FreeCAD - Common."""


import uuid
import FreeCADGui as Gui
import FreeCAD as App
from PySide import QtGui


mw = Gui.getMainWindow()
p = App.ParamGet("User parameter:BaseApp/PieMenuDev")


def actionList():
    """Create a dictionary of unique actions. Exclude command names
       containing . to prevent domain name system clash. Exclude
       command names containing , to prevent possible join and split
       related issues. Exclude actions with no text, as that can
       result in ambiguity, when selecting the command."""
    actions = {}
    duplicates = []
    for i in mw.findChildren(QtGui.QAction):
        name = i.objectName()
        if (name and
                i.text() and
                "." not in name and
                "," not in name):
            if name in actions:
                if name not in duplicates:
                    duplicates.append(name)
            else:
                actions[name] = i
    for d in duplicates:
        del actions[d]
    return actions


def wbIcon(i):
    """Create workbench icon."""
    if str(i.find("XPM")) != "-1":
        icon = []
        for a in ((((i
                     .split('{', 1)[1])
                    .rsplit('}', 1)[0])
                   .strip())
                  .split("\n")):
            icon.append((a
                         .split('"', 1)[1])
                        .rsplit('"', 1)[0])
        icon = QtGui.QIcon(QtGui.QPixmap(icon))
    else:
        icon = QtGui.QIcon(QtGui.QPixmap(i))
    if icon.isNull():
        icon = QtGui.QIcon(":/icons/freecad")
    return icon


def defaultGroup(base):
    """Create default group if no group exist."""
    g = None
    index = base.GetString("index")
    if not index:
        base.SetString("index", "1")
        g = base.GetGroup("1")
        g.SetString("uuid", str(uuid.uuid4()))
        g.SetString("name", "Default")
        cmd = ["Std_ViewFront",
               "Std_ViewTop",
               "Std_ViewRight"]
        g.SetString("commands", ",".join(cmd))
    return g


def splitIndex(base, string="index"):
    """Convenience function to create and return the index."""
    index = base.GetString(string)
    if index:
        index = index.split(",")
    else:
        index = []
    return index


def splitDomain(domain=None):
    """Split the domain name."""
    if domain:
        try:
            d = domain.split(".")
        except:
            d = []
    else:
        d = []
    # CPMenu
    try:
        prefix = d[0]
    except IndexError:
        prefix = None
    # Source (User or System)
    try:
        source = d[1]
    except IndexError:
        source = None
    # Workbench
    try:
        workbench = d[2]
    except IndexError:
        workbench = None
    # UUID
    try:
        uid = d[3]
    except IndexError:
        uid = str(uuid.uuid4())
    return [prefix, source, workbench, uid]


def findGroup(domain):
    """Find group matching the domain name."""
    g = None
    d = splitDomain(domain)
    if all(d):
        prefix, source, workbench, uid = d
        base = p.GetGroup(source).GetGroup(workbench)
        index = splitIndex(base)
        for i in index:
            if base.GetGroup(i).GetString("uuid") == uid:
                g = base.GetGroup(i)
    return g


def newGroup(domain):
    """Create a new group."""
    g = None
    d = splitDomain(domain)
    if all(d):
        prefix, source, workbench, uid = d
        base = p.GetGroup(source).GetGroup(workbench)
        index = splitIndex(base)
        x = 1
        while str(x) in index and x < 1000:
            x += 1
        index.append(str(x))
        base.SetString("index", ",".join(index))
        g = base.GetGroup(str(x))
        g.SetString("uuid", uid)
    return g


def deleteGroup(domain):
    """Delete group matching the domain name."""
    d = splitDomain(domain)
    if all(d):
        temp = []
        prefix, source, workbench, uid = d
        base = p.GetGroup(source).GetGroup(workbench)
        index = splitIndex(base)
        for i in index:
            if base.GetGroup(i).GetString("uuid") == uid:
                base.RemGroup(i)
            else:
                temp.append(i)
        base.SetString("index", ",".join(temp))
        defaultGroup(base)
        return True
    return False
