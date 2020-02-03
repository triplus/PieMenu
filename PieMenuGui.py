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

"""Pie menu for FreeCAD - Gui."""


from PySide import QtGui
from PySide import QtCore
import FreeCAD as App
import FreeCADGui as Gui
import PieMenuCommon as pmc
import PieMenuPreferences as pmp


p = pmc.p
mw = Gui.getMainWindow()


def onWorkbench():
    """Temp"""
    pass


def accessoriesMenu():
    """Add pie menu preferences to accessories menu."""
    pref = QtGui.QAction(mw)
    pref.setText("Pie menu")
    pref.setObjectName("PieMenu")
    pref.triggered.connect(onPreferences)
    try:
        import AccessoriesMenu
        AccessoriesMenu.addItem("PieMenu")
    except ImportError:
        a = mw.findChild(QtGui.QAction, "AccessoriesMenu")
        if a:
            a.menu().addAction(pref)
        else:
            mb = mw.menuBar()
            action = QtGui.QAction(mw)
            action.setObjectName("AccessoriesMenu")
            action.setIconText("Accessories")
            menu = QtGui.QMenu()
            action.setMenu(menu)
            menu.addAction(pref)

            def addMenu():
                """Add accessories menu to the menu bar."""
                mb.addAction(action)
                action.setVisible(True)

            addMenu()
            mw.workbenchActivated.connect(addMenu)


def onPreferences():
    """Open the preferences dialog."""
    pmp.createWidgets()
    dialog = pmp.dialog()
    dialog.show()


def onStart():
    """Start pie menu."""
    start = False
    try:
        mw.mainWindowClosed
        mw.workbenchActivated
        start = True
    except AttributeError:
        pass
    if start:
        t.stop()
        t.deleteLater()
        onWorkbench()
        accessoriesMenu()
        mw.mainWindowClosed.connect(onClose)
        mw.workbenchActivated.connect(onWorkbench)
        # a = QtGui.QAction(mw)
        # mw.addAction(a)
        # a.setText("Invoke pie menu")
        # a.setObjectName("InvokePieMenu")
        # a.setShortcut(QtGui.QKeySequence("Q"))
        # a.triggered.connect(onInvoke)


def onClose():
    """Remove system presets and groups without index on FreeCAD close."""
    p.RemGroup("System")

    for wb in Gui.listWorkbenches():
        base = p.GetGroup("User").GetGroup(wb)
        if not pmc.splitIndex(base):
            p.GetGroup("User").RemGroup(wb)


def onPreStart():
    """Improve start reliability and maintain FreeCAD 0.16 support."""
    if App.Version()[1] < "17":
        onStart()
    else:
        if mw.property("eventLoop"):
            onStart()


t = QtCore.QTimer()
t.timeout.connect(onPreStart)
t.start(500)
