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

"""Pie menu for FreeCAD - Preferences."""


import os
import FreeCADGui as Gui
from PySide import QtGui
from PySide import QtCore
import PieMenuGui as pmg
import PieMenuCommon as pmc
import PieMenuToolbars as pmt


p = pmc.p
mw = Gui.getMainWindow()
path = os.path.dirname(__file__) + "/Resources/icons/"

cBoxWb = None
cBoxMenu = None
enabled = None
copyDomain = None
editContext = None


def createWidgets():
    """Create widgets on preferences dialog start."""
    global cBoxWb
    cBoxWb = QtGui.QComboBox()
    cBoxWb.setSizePolicy(QtGui.QSizePolicy.Expanding,
                         QtGui.QSizePolicy.Preferred)
    global cBoxMenu
    cBoxMenu = QtGui.QComboBox()
    cBoxMenu.setSizePolicy(QtGui.QSizePolicy.Expanding,
                           QtGui.QSizePolicy.Preferred)
    global enabled
    enabled = QtGui.QListWidget()


def baseGroup():
    """Current workbench base group."""
    wb = cBoxWb.itemData(cBoxWb.currentIndex(), QtCore.Qt.UserRole)
    g = p.GetGroup("User").GetGroup(wb)
    return g


def saveEnabled():
    """Save enabled on change."""
    items = []
    for index in range(enabled.count()):
        items.append(enabled.item(index).data(QtCore.Qt.UserRole))
    domain = cBoxMenu.itemData(cBoxMenu.currentIndex())
    if domain:
        g = pmc.findGroup(domain)
        if g:
            g.SetString("commands", ",".join(items))
            pmg.onWorkbench()


def dialog():
    """Pie menu preferences dialog."""

    def onAccepted():
        """Close dialog on button close."""
        dia.done(1)

    def onFinished():
        """ Delete dialog on close."""
        dia.deleteLater()

    # Dialog
    dia = QtGui.QDialog(mw)
    dia.setModal(True)
    dia.resize(900, 500)
    dia.setWindowTitle("Pie menu preferences")
    dia.finished.connect(onFinished)

    # Stack
    stack = QtGui.QStackedWidget()
    layout = QtGui.QVBoxLayout()
    layout.setContentsMargins(0, 0, 0, 0)
    dia.setLayout(layout)
    layout.addWidget(stack)

    # Button settings
    btnSettings = QtGui.QPushButton("Settings")
    btnSettings.setToolTip("Open settings")

    def onSettings():
        """Stack widget index change."""
        stack.setCurrentIndex(2)

    btnSettings.clicked.connect(onSettings)

    # Button settings done
    btnSettingsDone = QtGui.QPushButton("Done")
    btnSettingsDone.setToolTip("Return to general preferences")

    def onBtnSettingsDone():
        """Return to general preferences."""
        btnSettings.clearFocus()
        stack.setCurrentIndex(0)
        if p.GetBool("Global", 0):
            cBoxWb.setCurrentIndex(cBoxWb.findData("GlobalPanel"))
        else:
            activeWb = Gui.activeWorkbench().__class__.__name__
            cBoxWb.setCurrentIndex(cBoxWb.findData(activeWb))

    btnSettingsDone.clicked.connect(onBtnSettingsDone)

    # Button close
    btnClose = QtGui.QPushButton("Close")
    btnClose.setToolTip("Close the preferences dialog")
    btnClose.clicked.connect(onAccepted)

    stack.insertWidget(0, general(dia, stack, btnClose, btnSettings))
    stack.insertWidget(1, edit(stack))
    stack.insertWidget(2, settings(stack, btnSettingsDone))

    btnClose.setDefault(True)
    btnClose.setFocus()

    return dia


def general(dia, stack, btnClose, btnSettings):
    """General pie menu preferences."""

    # Widgets
    lo = QtGui.QVBoxLayout()
    w = QtGui.QWidget(mw)
    w.setLayout(lo)

    # Search
    search = QtGui.QLineEdit()

    # Available commands
    commands = QtGui.QListWidget()
    commands.setSortingEnabled(True)
    commands.sortItems(QtCore.Qt.AscendingOrder)

    # Reset workbench
    btnResetWb = QtGui.QPushButton()
    btnResetWb.setToolTip("Reset workbench to defaults")
    btnResetWb.setIcon(QtGui.QIcon(path + "PieMenuReset.svg"))

    # Checkbox default menu
    ckDefault = QtGui.QCheckBox()
    ckDefault.setToolTip("Set menu as default workbench menu")

    # Button add workbench menu
    btnAddWbMenu = QtGui.QPushButton()
    btnAddWbMenu.setToolTip("Add new workbench menu")
    btnAddWbMenu.setIcon(QtGui.QIcon(path + "PieMenuAdd.svg"))

    # Button remove workbench menu
    btnRemoveWbMenu = QtGui.QPushButton()
    btnRemoveWbMenu.setToolTip("Remove selected workbench menu")
    btnRemoveWbMenu.setIcon(QtGui.QIcon(path + "PieMenuRemove.svg"))

    # Button copy workbench menu
    btnCopyWbMenu = QtGui.QPushButton()
    btnCopyWbMenu.setToolTip("Copy existing workbench menu")
    btnCopyWbMenu.setIcon(QtGui.QIcon(path + "PieMenuCopy.svg"))

    # Button rename workbench menu
    btnRenameWbMenu = QtGui.QPushButton()
    btnRenameWbMenu.setToolTip("Rename selected workbench menu")
    btnRenameWbMenu.setIcon(QtGui.QIcon(path + "PieMenuRename.svg"))

    # Button add command
    btnAddCommand = QtGui.QPushButton()
    btnAddCommand.setToolTip("Add selected command")
    btnAddCommand.setIcon(QtGui.QIcon(path + "PieMenuAddCommand.svg"))

    # Button remove command
    btnRemoveCommand = QtGui.QPushButton()
    btnRemoveCommand.setToolTip("Remove selected command")
    btnRemoveCommand.setIcon(QtGui.QIcon(path +
                                         "PieMenuRemoveCommand.svg"))

    # Button move up
    btnMoveUp = QtGui.QPushButton()
    btnMoveUp.setToolTip("Move selected command up")
    btnMoveUp.setIcon(QtGui.QIcon(path + "PieMenuUp.svg"))

    # Button move down
    btnMoveDown = QtGui.QPushButton()
    btnMoveDown.setToolTip("Move selected command down")
    btnMoveDown.setIcon(QtGui.QIcon(path + "PieMenuDown.svg"))

    # Button add separator
    btnAddSeparator = QtGui.QPushButton()
    btnAddSeparator.setToolTip("Add separator")
    btnAddSeparator.setIcon(QtGui.QIcon(path +
                                        "PieMenuAddSeparator.svg"))

    # Button add menu
    btnAddMenu = QtGui.QPushButton()
    btnAddMenu.setToolTip("Add menu")
    btnAddMenu.setIcon(QtGui.QIcon(path + "PieMenuAddMenu.svg"))

    # Button edit menu
    btnEditMenu = QtGui.QPushButton()
    btnEditMenu.setEnabled(False)
    btnEditMenu.setToolTip("Edit menu")
    btnEditMenu.setIcon(QtGui.QIcon(path + "PieMenuEditMenu.svg"))

    # Layout
    loPanels = QtGui.QHBoxLayout()
    loLeft = QtGui.QVBoxLayout()
    loRight = QtGui.QVBoxLayout()
    loPanels.insertLayout(0, loLeft)
    loPanels.insertLayout(1, loRight)

    loLeft.addWidget(search)
    loLeft.addWidget(commands)

    loCBoxWb = QtGui.QHBoxLayout()
    loCBoxWb.addWidget(cBoxWb)
    loCBoxWb.addWidget(btnResetWb)

    loCBoxMenu = QtGui.QHBoxLayout()
    loCBoxMenu.addWidget(ckDefault)
    loCBoxMenu.addWidget(cBoxMenu)
    loCBoxMenu.addWidget(btnAddWbMenu)
    loCBoxMenu.addWidget(btnRemoveWbMenu)
    loCBoxMenu.addWidget(btnRenameWbMenu)
    loCBoxMenu.addWidget(btnCopyWbMenu)

    loControls = QtGui.QHBoxLayout()
    loControls.addStretch()
    loControls.addWidget(btnAddCommand)
    loControls.addWidget(btnRemoveCommand)
    loControls.addWidget(btnMoveUp)
    loControls.addWidget(btnMoveDown)
    loControls.addWidget(btnAddSeparator)
    loControls.addWidget(btnAddMenu)
    loControls.addWidget(btnEditMenu)

    loRight.insertLayout(0, loCBoxWb)
    loRight.insertLayout(1, loCBoxMenu)
    loRight.addWidget(enabled)
    loRight.insertLayout(3, loControls)

    loBottom = QtGui.QHBoxLayout()
    loBottom.addWidget(btnSettings)
    loBottom.addStretch()
    loBottom.addWidget(btnClose)

    lo.insertLayout(0, loPanels)
    lo.insertLayout(1, loBottom)

    # Functions and connections

    def onSearch(text):
        """Show or hide commands on search."""
        for index in range(commands.count()):
            if text.lower() in commands.item(index).text().lower():
                commands.item(index).setHidden(False)
            else:
                commands.item(index).setHidden(True)

    search.textEdited.connect(onSearch)

    def populateCommands():
        """Populate available commands panel."""
        actions = pmc.actionList()
        commands.blockSignals(True)
        commands.clear()
        for i in actions:
            item = QtGui.QListWidgetItem(commands)
            item.setText(actions[i].text().replace("&", ""))
            item.setToolTip(actions[i].toolTip())
            icon = actions[i].icon()
            if icon.isNull():
                item.setIcon(QtGui.QIcon(":/icons/freecad"))
            else:
                item.setIcon(icon)
            item.setData(QtCore.Qt.UserRole, actions[i].objectName())
        commands.setCurrentRow(0)
        commands.blockSignals(False)

    def populateCBoxWb():
        """Workbench selector combo box."""
        wb = Gui.listWorkbenches()
        wbSort = list(wb)
        wbSort.sort()
        wbSort.reverse()
        cBoxWb.blockSignals(True)
        cBoxWb.clear()
        for i in wbSort:
            try:
                icon = pmc.wbIcon(wb[i].Icon)
            except AttributeError:
                icon = QtGui.QIcon(":/icons/freecad")
            mt = wb[i].MenuText
            cn = wb[i].__class__.__name__
            cBoxWb.insertItem(0, icon, mt, cn)
        cBoxWb.insertSeparator(0)
        cBoxWb.insertItem(0,
                          QtGui.QIcon(":/icons/freecad"),
                          "Global pie menu",
                          "GlobalPanel")
        if p.GetBool("Global", 0):
            cBoxWb.setCurrentIndex(cBoxWb.findData("GlobalPanel"))
        else:
            activeWb = Gui.activeWorkbench().__class__.__name__
            cBoxWb.setCurrentIndex(cBoxWb.findData(activeWb))
        cBoxWb.blockSignals(False)

    def onCBoxWb():
        """Activate workbench on selection."""
        base = baseGroup()
        wb = Gui.listWorkbenches()
        current = cBoxWb.itemData(cBoxWb.currentIndex(),
                                  QtCore.Qt.UserRole)
        for i in wb:
            if wb[i].__class__.__name__ == current:
                Gui.activateWorkbench(i)
        pmc.defaultGroup(base)
        populateCommands()
        populateCBoxMenu()
        domain = cBoxMenu.itemData(cBoxMenu.currentIndex())
        if domain:
            populateEnabled(pmc.findGroup(domain))
        btnClose.setFocus()

    cBoxWb.currentIndexChanged.connect(onCBoxWb)

    def populateCBoxMenu():
        """Workbench menu combo box."""
        base = baseGroup()
        index = pmc.splitIndex(base)
        ckDefault.blockSignals(True)
        cBoxMenu.blockSignals(True)
        cBoxMenu.clear()
        for i in index:
            name = base.GetGroup(i).GetString("name")
            uid = base.GetGroup(i).GetString("uuid")
            wb = cBoxWb.itemData(cBoxWb.currentIndex(), QtCore.Qt.UserRole)
            domain = "PMMenu" + "." + "User" + "." + wb + "." + uid
            try:
                cBoxMenu.insertItem(0, name.decode("UTF-8"), domain)
            except AttributeError:
                cBoxMenu.insertItem(0, name, domain)
        default = base.GetString("default")
        data = cBoxMenu.findData(default)
        cBoxMenu.setCurrentIndex(data)
        if isDefaultMenu():
            ckDefault.setChecked(True)
        else:
            cBoxMenu.setCurrentIndex(0)
            ckDefault.setChecked(False)
        ckDefault.blockSignals(False)
        cBoxMenu.blockSignals(False)

    def onCBoxMenu():
        """Load workbench menu data."""
        domain = cBoxMenu.itemData(cBoxMenu.currentIndex())

        ckDefault.blockSignals(True)
        if isDefaultMenu():
            ckDefault.setChecked(True)
        else:
            ckDefault.setChecked(False)
        ckDefault.blockSignals(False)
        populateEnabled(pmc.findGroup(domain))
        btnClose.setFocus()

    cBoxMenu.currentIndexChanged.connect(onCBoxMenu)

    def onBtnResetWb():
        """Reset workbench to defaults."""
        base = baseGroup()
        base.Clear()
        pmc.defaultGroup(base)
        populateCBoxMenu()
        domain = cBoxMenu.itemData(cBoxMenu.currentIndex())
        if domain:
            populateEnabled(pmc.findGroup(domain))
        btnClose.setFocus()

    btnResetWb.clicked.connect(onBtnResetWb)

    def onBtnAddWbMenu():
        """Add new workbench menu."""
        d = QtGui.QInputDialog(dia)
        d.setModal(True)
        d.setInputMode(QtGui.QInputDialog.InputMode.TextInput)
        text, ok = QtGui.QInputDialog.getText(dia,
                                              "New menu",
                                              "Please insert menu name.")
        if ok:
            wb = cBoxWb.itemData(cBoxWb.currentIndex())
            domain = "PMMenu" + "." + "User" + "." + wb
            g = pmc.newGroup(domain)
            if g:
                uid = g.GetString("uuid")
                domain = domain + "." + uid
                try:
                    g.SetString("name", text.encode("UTF-8"))
                except TypeError:
                    g.SetString("name", text)
                populateCBoxMenu()
                cBoxMenu.setCurrentIndex(cBoxMenu.findData(domain))
                populateEnabled(g)
        d.deleteLater()
        btnClose.setFocus()

    btnAddWbMenu.clicked.connect(onBtnAddWbMenu)

    def onBtnRemoveWbMenu():
        """Remove selected workbench menu."""
        base = baseGroup()
        domain = cBoxMenu.itemData(cBoxMenu.currentIndex())
        if domain:
            pmc.deleteGroup(domain)
        pmc.defaultGroup(base)
        populateCBoxMenu()
        domain = cBoxMenu.itemData(cBoxMenu.currentIndex())
        populateEnabled(pmc.findGroup(domain))
        btnClose.setFocus()

    btnRemoveWbMenu.clicked.connect(onBtnRemoveWbMenu)

    def onBtnRenameWbMenu():
        """Rename existing workbench menu."""
        d = QtGui.QInputDialog(dia)
        d.setModal(True)
        d.setInputMode(QtGui.QInputDialog.InputMode.TextInput)
        text, ok = QtGui.QInputDialog.getText(dia,
                                              "Rename menu",
                                              "Please insert new menu name.")
        if ok:
            domain = cBoxMenu.itemData(cBoxMenu.currentIndex())
            g = pmc.findGroup(domain)
            if g:
                try:
                    g.SetString("name", text.encode("UTF-8"))
                except TypeError:
                    g.SetString("name", text)
                populateCBoxMenu()
                cBoxMenu.setCurrentIndex(cBoxMenu.findData(domain))
                populateEnabled(g)

        d.deleteLater()
        btnClose.setFocus()

    btnRenameWbMenu.clicked.connect(onBtnRenameWbMenu)

    def onCKDefault(checked):
        """Set the checkbox state."""
        base = baseGroup()
        domain = cBoxMenu.itemData(cBoxMenu.currentIndex())
        if checked:
            base.SetString("default", domain)
        else:
            base.RemString("default")
        pmg.onWorkbench()

    ckDefault.stateChanged.connect(onCKDefault)

    def isDefaultMenu():
        """Check if current menu is the default menu."""
        default = False
        base = baseGroup()
        domain = cBoxMenu.itemData(cBoxMenu.currentIndex())
        if domain and base.GetString("default") == domain:
            default = True
        return default

    def populateEnabled(group):
        """Populate enabled commands panel."""
        if group:
            items = group.GetString("commands")
        else:
            items = []
        if items:
            items = items.split(",")
        else:
            items = []
        actions = pmc.actionList()
        enabled.blockSignals(True)
        enabled.clear()
        for i in items:
            item = QtGui.QListWidgetItem(enabled)
            if i == "PMSeparator":
                item.setText("Separator")
                item.setData(QtCore.Qt.UserRole, i)
                item.setIcon(QtGui.QIcon(path +
                                         "PieMenuAddSeparator.svg"))
            elif i.startswith("PMMenu"):
                g = pmc.findGroup(i)
                if g:
                    try:
                        text = g.GetString("name").decode("UTF-8")
                    except AttributeError:
                        text = g.GetString("name")
                    item.setText("Menu: " + text)
                else:
                    item.setText("Menu")
                item.setData(QtCore.Qt.UserRole, i)
                item.setIcon(QtGui.QIcon(path + "PieMenuAddMenu.svg"))
            elif i in actions:
                item.setText(actions[i].text().replace("&", ""))
                item.setToolTip(actions[i].toolTip())
                icon = actions[i].icon()
                if icon.isNull():
                    item.setIcon(QtGui.QIcon(":/icons/freecad"))
                else:
                    item.setIcon(icon)
                item.setData(QtCore.Qt.UserRole, i)
            else:
                item.setText(i)
                item.setToolTip("Command " + i + " is not currently available")
                icon = QtGui.QIcon()
                icon.addPixmap(QtGui.QPixmap(":/icons/freecad"))
                item.setIcon(QtGui.QIcon(icon.pixmap(256,
                                                     QtGui.QIcon.Disabled)))
                item.setData(QtCore.Qt.UserRole, i)
        enabled.setCurrentRow(0)
        enabled.blockSignals(False)
        pmg.onWorkbench()
        onSelectionChanged()

    def onBtnAddCommand():
        """Add the selected command."""
        row = enabled.currentRow()
        data = commands.currentItem().data(QtCore.Qt.UserRole)
        item = QtGui.QListWidgetItem()
        enabled.insertItem(row + 1, item)
        enabled.setCurrentRow(row + 1)
        item.setText(commands.currentItem().text().replace("&", ""))
        item.setToolTip(commands.currentItem().toolTip())
        item.setIcon(commands.currentItem().icon())
        item.setData(QtCore.Qt.UserRole, data)
        saveEnabled()

    btnAddCommand.clicked.connect(onBtnAddCommand)
    commands.itemDoubleClicked.connect(onBtnAddCommand)

    def onBtnRemoveCommand():
        """Remove the selected command."""
        row = enabled.currentRow()
        item = enabled.takeItem(row)
        if item:
            del item
            if row == enabled.count():
                enabled.setCurrentRow(row - 1)
            else:
                enabled.setCurrentRow(row)
            saveEnabled()

    btnRemoveCommand.clicked.connect(onBtnRemoveCommand)

    def onBtnMoveUp():
        """Move selected command up."""
        row = enabled.currentRow()
        if row != 0:
            item = enabled.takeItem(row)
            enabled.insertItem(row - 1, item)
            enabled.setCurrentRow(row - 1)
            saveEnabled()

    btnMoveUp.clicked.connect(onBtnMoveUp)

    def onBtnMoveDown():
        """Move selected command down."""
        row = enabled.currentRow()
        if row != enabled.count() - 1 and row != -1:
            item = enabled.takeItem(row)
            enabled.insertItem(row + 1, item)
            enabled.setCurrentRow(row + 1)
            saveEnabled()

    btnMoveDown.clicked.connect(onBtnMoveDown)

    def onBtnAddSeparator():
        """Add separator."""
        row = enabled.currentRow()
        item = QtGui.QListWidgetItem()
        enabled.insertItem(row + 1, item)
        enabled.setCurrentRow(row + 1)
        item.setText("Separator")
        item.setData(QtCore.Qt.UserRole, "PMSeparator")
        item.setIcon(QtGui.QIcon(path + "PieMenuAddSeparator.svg"))
        saveEnabled()

    btnAddSeparator.clicked.connect(onBtnAddSeparator)

    def onBtnAddMenu():
        """Add menu."""
        row = enabled.currentRow()
        item = QtGui.QListWidgetItem()
        enabled.insertItem(row + 1, item)
        enabled.setCurrentRow(row + 1)
        item.setText("Menu")
        item.setData(QtCore.Qt.UserRole, "PMMenu")
        item.setIcon(QtGui.QIcon(path + "PieMenuAddMenu.svg"))
        saveEnabled()
        onSelectionChanged()

    btnAddMenu.clicked.connect(onBtnAddMenu)

    def onSelectionChanged():
        """Set enabled state for widgets on selection changed."""
        current = enabled.currentItem()
        if current:
            data = current.data(QtCore.Qt.UserRole)
        if current and data and data.startswith("PMMenu"):
            btnEditMenu.setEnabled(True)
            btnEditMenu.setFocus()
        else:
            btnEditMenu.setEnabled(False)

    enabled.itemSelectionChanged.connect(onSelectionChanged)

    def onEditMenu():
        """Open edit dialog for selected menu ."""
        current = enabled.currentItem()
        if current and current.data(QtCore.Qt.UserRole).startswith("PMMenu"):
            global editContext
            editContext = "Set"
            stack.setCurrentIndex(1)

    btnEditMenu.clicked.connect(onEditMenu)
    enabled.itemDoubleClicked.connect(onEditMenu)

    def onCopyWbMenu():
        """Open copy menu dialog."""
        global editContext
        editContext = "Copy"
        stack.setCurrentIndex(1)

    btnCopyWbMenu.clicked.connect(onCopyWbMenu)

    def onStack(n):
        """Stack widget index change."""
        global copyDomain
        if n == 0:
            row = enabled.currentRow()
            domain = cBoxMenu.itemData(cBoxMenu.currentIndex())
            if domain:
                populateEnabled(pmc.findGroup(domain))
            enabled.setCurrentRow(row)
            btnClose.setDefault(True)
            if copyDomain:
                populateCBoxMenu()
                cBoxMenu.setCurrentIndex(cBoxMenu.findData(copyDomain))
                domain = cBoxMenu.itemData(cBoxMenu.currentIndex())
                populateEnabled(pmc.findGroup(domain))
                copyDomain = None
        onSelectionChanged()

    stack.currentChanged.connect(onStack)

    # Available workbenches
    populateCBoxWb()
    # Default menu
    pmc.defaultGroup(baseGroup())
    # Available menus
    populateCBoxMenu()
    # Available commands
    populateCommands()
    # Enabled commands
    populateEnabled(pmc.findGroup(cBoxMenu.itemData(cBoxMenu.currentIndex())))

    return w


def edit(stack):
    """Preferences for editable commands."""

    items = []

    # Widgets
    widget = QtGui.QWidget()
    layout = QtGui.QVBoxLayout()
    widget.setLayout(layout)

    tree = QtGui.QTreeWidget()
    if editContext == "Copy":
        tree.setHeaderLabel("Copy menu: None")
    else:
        tree.setHeaderLabel("Set menu: None")

    # Button edit done
    btnEditDone = QtGui.QPushButton()
    btnEditDone.setText("Done")
    btnEditDone.setToolTip("Return to general preferences")

    # Layout button edit done
    loBtnEditDone = QtGui.QHBoxLayout()
    loBtnEditDone.addStretch()
    loBtnEditDone.addWidget(btnEditDone)

    layout.addWidget(tree)
    layout.insertLayout(1, loBtnEditDone)

    # Functions and connections

    def updateTree():
        """Update tree widget and add available menus."""
        tree.blockSignals = True
        wb = Gui.listWorkbenches()
        currentWb = cBoxWb.itemData(cBoxWb.currentIndex())

        wbSort = list(wb)
        wbSort.sort()
        if currentWb in wbSort:
            wbSort.remove(currentWb)

        def treeItems(currentWb=None,
                      mt=None,
                      cn=None,
                      expanded=False,
                      itemTop=None):
            """Create tree widget items."""
            if currentWb:
                try:
                    icon = pmc.wbIcon(wb[currentWb].Icon)
                except AttributeError:
                    icon = QtGui.QIcon(":/icons/freecad")
            else:
                icon = QtGui.QIcon(":/icons/freecad")

            if not mt:
                mt = wb[currentWb].MenuText
            if not cn:
                cn = wb[currentWb].__class__.__name__

            if itemTop:
                item = QtGui.QTreeWidgetItem(itemTop)
            else:
                item = QtGui.QTreeWidgetItem(tree)

            if cn != "GlobalPanel":
                item.setIcon(0, icon)

            try:
                item.setText(0, mt.decode("UTF-8"))
            except AttributeError:
                item.setText(0, mt)

            item.setExpanded(expanded)

            source = ["User", "System"]
            for s in source:
                itemSource = QtGui.QTreeWidgetItem(item)
                itemSource.setText(0, s)
                itemSource.setExpanded(expanded)

                base = p.GetGroup(s).GetGroup(cn)
                index = pmc.splitIndex(base)
                for i in index:
                    g = base.GetGroup(i)
                    uid = g.GetString("uuid")
                    domain = "PMMenu" + "." + s + "." + cn + "." + uid
                    itemMenu = QtGui.QTreeWidgetItem(itemSource)
                    name = g.GetString("name")
                    try:
                        itemMenu.setText(0, name.decode("UTF-8"))
                    except AttributeError:
                        itemMenu.setText(0, name)
                    itemMenu.setCheckState(0, QtCore.Qt.Unchecked)
                    itemMenu.setData(0, QtCore.Qt.UserRole, domain)
                    items.append(itemMenu)

                if itemSource.childCount() == 0:
                    item.removeChild(itemSource)

        # Current workbench
        if currentWb != "GlobalPanel":
            treeItems(currentWb, None, None, True, None)
        else:
            treeItems(None, "Global", "GlobalPanel", True, None)

        # Other workbenches
        item = QtGui.QTreeWidgetItem(tree)
        item.setText(0, "Workbenches")
        for i in wbSort:
            treeItems(i, None, None, False, item)

        # Remove empty
        for i in reversed(range(item.childCount())):
            if item.child(i).childCount() == 0:
                item.removeChild(item.child(i))

        # Global menus
        if currentWb != "GlobalPanel":
            treeItems(None, "Global", "GlobalPanel", False, None)

        # Toolbars (for copy mode only)
        if editContext == "Copy":
            tree.setHeaderLabel("Copy: None")
            itemsToolbar = QtGui.QTreeWidgetItem(tree)
            itemsToolbar.setText(0, "Toolbars")
            tb = []
            for i in mw.findChildren(QtGui.QToolBar):
                if i.objectName():
                    tb.append(i.objectName())
            tb.sort()
            for name in tb:
                domain = "PMMenu" + "." + "Toolbar" + "." + name
                itemTb = QtGui.QTreeWidgetItem(itemsToolbar)
                itemTb.setText(0, name)
                itemTb.setCheckState(0, QtCore.Qt.Unchecked)
                itemTb.setData(0, QtCore.Qt.UserRole, domain)
                items.append(itemTb)

        # Current (for set mode only)
        if editContext == "Set":
            current = enabled.currentItem()
            if current and (current.data(QtCore.Qt.UserRole)
                            .startswith("PMMenu")):
                data = current.data(QtCore.Qt.UserRole)
                for i in items:
                    if i.data(0, QtCore.Qt.UserRole) == data:
                        i.setCheckState(0, QtCore.Qt.Checked)
                        text = i.text(0)
                        tree.setHeaderLabel("Set menu: " + text)

                        parent = i.parent()
                        while parent:
                            parent.setExpanded(True)
                            parent = parent.parent()

        tree.blockSignals = False

    def onChecked(item):
        """Copy or set menu."""
        global copyDomain
        tree.blockSignals = True
        if item.checkState(0) == QtCore.Qt.Checked:
            for i in items:
                if i.checkState(0) == QtCore.Qt.Checked and i is not item:
                    i.setCheckState(0, QtCore.Qt.Unchecked)
            data = item.data(0, QtCore.Qt.UserRole)
        else:
            data = None

        text = item.text(0)

        if editContext == "Set" and data:
            tree.setHeaderLabel("Set menu: " + text)
            enabled.currentItem().setData(QtCore.Qt.UserRole,
                                          item.data(0, QtCore.Qt.UserRole))
            saveEnabled()
        elif editContext == "Set" and not data:
            tree.setHeaderLabel("Set menu: None")
            enabled.currentItem().setData(QtCore.Qt.UserRole, "PMMenu")
            saveEnabled()
        elif editContext == "Copy" and data:
            tree.setHeaderLabel("Copy: " + text)
            copyDomain = data
        elif editContext == "Copy" and not data:
            tree.setHeaderLabel("Copy: None")
            copyDomain = None
        else:
            pass
        tree.blockSignals = False

    def onEditDone():
        """Switch to general preferences."""
        global copyDomain
        tree.itemChanged.disconnect(onChecked)
        del items[:]
        tree.clear()

        if copyDomain:
            wb = cBoxWb.itemData(cBoxWb.currentIndex())
            domain = "PMMenu" + "." + "User" + "." + wb
            if copyDomain.startswith("PMMenu.Toolbar"):
                name = copyDomain.split(".")[2]
                grpCopy = pmc.newGroup(domain)
                uid = grpCopy.GetString("uuid")
                copyDomain = domain + "." + uid
                grpCopy.SetString("name", name)
                grpCopy.SetString("commands",
                                  ",".join(pmt.toolbarCommands(name)))
            else:
                grpOrigin = pmc.findGroup(copyDomain)
                grpCopy = pmc.newGroup(domain)
                uid = grpCopy.GetString("uuid")
                domain = domain + "." + uid
                if grpOrigin and grpCopy:
                    grpCopy.SetString("name", grpOrigin.GetString("name"))
                    grpCopy.SetString("commands",
                                      grpOrigin.GetString("commands"))
                    copyDomain = domain
                else:
                    copyDomain = None

        stack.setCurrentIndex(0)

    btnEditDone.clicked.connect(onEditDone)

    def onStack(n):
        """Stack widget index change."""
        if n == 1:
            btnEditDone.setDefault(True)
            btnEditDone.setFocus()
            updateTree()
            tree.itemChanged.connect(onChecked)

    stack.currentChanged.connect(onStack)

    return widget


def settings(stack, btnSettingsDone):
    """Settings widget for preferences."""

    # Widgets
    widgetSettings = QtGui.QWidget()
    layoutMain = QtGui.QVBoxLayout()
    widgetSettings.setLayout(layoutMain)
    widget = QtGui.QWidget()
    layout = QtGui.QVBoxLayout()
    widget.setLayout(layout)
    scroll = QtGui.QScrollArea()
    scroll.setWidgetResizable(True)
    scroll.setWidget(widget)
    layoutMain.addWidget(scroll)

    # Mode
    grpBoxMode = QtGui.QGroupBox("Mode:")
    loMode = QtGui.QVBoxLayout()
    grpBoxMode.setLayout(loMode)

    # Global pie menu mode
    loGlobal = QtGui.QHBoxLayout()
    lblGlobal = QtGui.QLabel("Global pie menu")
    ckBoxGlobal = QtGui.QCheckBox()
    ckBoxGlobal.setToolTip("Enable global pie menu mode")

    loGlobal.addWidget(lblGlobal)
    loGlobal.addStretch()
    loGlobal.addWidget(ckBoxGlobal)
    loMode.insertLayout(0, loGlobal)

    if p.GetBool("Global", 0):
        ckBoxGlobal.setChecked(True)

    def onCkBoxGlobal(checked):
        """Set global pie menu mode."""
        if checked:
            p.SetBool("Global", 1)
        else:
            p.SetBool("Global", 0)

        pmg.onWorkbench()

    ckBoxGlobal.stateChanged.connect(onCkBoxGlobal)

    loBtnSettings = QtGui.QHBoxLayout()
    loBtnSettings.addStretch()
    loBtnSettings.addWidget(btnSettingsDone)

    # Layout
    layout.addWidget(grpBoxMode)
    layout.addStretch()
    layoutMain.insertLayout(1, loBtnSettings)

    def onStack(n):
        """Stack widget index change."""
        if n == 2:
            btnSettingsDone.setDefault(True)
            btnSettingsDone.setFocus()

    stack.currentChanged.connect(onStack)

    return widgetSettings
