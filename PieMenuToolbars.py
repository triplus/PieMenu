# Pie menu for FreeCAD.
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

"""Pie menu for FreeCAD - extract commands from toolbars."""


from PySide import QtGui
import FreeCADGui as Gui
import PieMenuCommon as pmc


mw = Gui.getMainWindow()


def getToolbars():
    "Workbench toolbars."

    exclude = [
        "File",
        "Workbench",
        "Macro",
        "View",
        "Structure"]

    toolbars = []
    for tb in mw.findChildren(QtGui.QToolBar):
        if (tb.toggleViewAction().isVisible() and
                tb.objectName() not in exclude):
            toolbars.append(tb)
    return toolbars


def menuCommands(menu, actions, commands):
    "Extract commands from button with menu."
    for a in menu.actions():
        name = a.objectName()
        if name and name in actions:
            commands.append(name)


def toolbarCommands(name=None):
    "Extract commands from toolbars."
    commands = []
    actions = pmc.actionList()
    if name:
        toolbars = [mw.findChild(QtGui.QToolBar, name)]
    else:
        toolbars = getToolbars()

    for tb in toolbars:
        for btn in tb.findChildren(QtGui.QToolButton):
            if btn.menu():
                menuCommands(btn.menu(), actions, commands)
            elif (btn.defaultAction() and
                  btn.defaultAction().objectName() in actions):
                commands.append(btn.defaultAction().objectName())
            else:
                pass
    return commands
