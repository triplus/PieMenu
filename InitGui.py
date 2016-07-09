#***************************************************************************
#*                                                                         *
#*   Copyright (c) 2015,2016 looo @ FreeCAD                                *
#*   Copyright (c) 2015 microelly <microelly2@freecadbuch.de>              * 
#*                                                                         *
#*   This program is free software; you can redistribute it and/or modify  *
#*   it under the terms of the GNU Lesser General Public License (LGPL)    *
#*   as published by the Free Software Foundation; either version 2 of     *
#*   the License, or (at your option) any later version.                   *
#*   for detail see the LICENCE text file.                                 *
#*                                                                         *
#*   This program is distributed in the hope that it will be useful,       *
#*   but WITHOUT ANY WARRANTY; without even the implied warranty of        *
#*   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the         *
#*   GNU Library General Public License for more details.                  *
#*                                                                         *
#*   You should have received a copy of the GNU Library General Public     *
#*   License along with this program; if not, write to the Free Software   *
#*   Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  *
#*   USA                                                                   *
#*                                                                         *
#***************************************************************************

# Attribution:
# http://forum.freecadweb.org/
# http://www.freecadweb.org/wiki/index.php?title=Code_snippets

# -*- coding: utf-8 -*-
# causes an action to the mouse click on an object
# This function remains resident (in memory) with the function "addObserver(s)"
# "removeObserver(s) # Uninstalls the resident function
#class SelObserver:
#    def addSelection(self,doc,obj,sub,pnt):               # Selection object
    #def setPreselection(self,doc,obj,sub):                # Preselection object
#        App.Console.PrintMessage("addSelection"+ "\n")
#        App.Console.PrintMessage(str(doc)+ "\n")          # Name of the document
#        App.Console.PrintMessage(str(obj)+ "\n")          # Name of the object
#        App.Console.PrintMessage(str(sub)+ "\n")          # The part of the object name
#        App.Console.PrintMessage(str(pnt)+ "\n")          # Coordinates of the object
#        App.Console.PrintMessage("______"+ "\n")

#    def removeSelection(self,doc,obj,sub):                # Delete the selected object
#        App.Console.PrintMessage("removeSelection"+ "\n")
#    def setSelection(self,doc):                           # Selection in ComboView
#        App.Console.PrintMessage("setSelection"+ "\n")
#    def clearSelection(self,doc):                         # If click on the screen, clear the selection
#        App.Console.PrintMessage("clearSelection"+ "\n")  # If click on another object, clear the previous object
#s =SelObserver()
#FreeCADGui.Selection.addObserver(s)                       # install the function mode resident
#FreeCADGui.Selection.removeObserver(s)                   # Uninstall the resident function

#from __future__ import division
#import FreeCADGui as Gui
#from PySide import QtCore, QtGui, QtSvg
#import numpy as np
#import time


#class PieButton(QtGui.QGraphicsEllipseItem):
#    def __init__(self, pos=(0, 0), angle_range=(0, 1), size=[50, 50], view=None, parent=None, command=None):
#        super(PieButton, self).__init__(None, scene=parent)
#        self.command = command
#        self.view = view
#        self._size = size
#        self._pos = pos
#        self.angle_range = angle_range
#        self.setRect(- size[0] / 2, - size[1] / 2, size[0], size[1])
#        self.draw_icon()
#        self.setPos(pos[0], pos[1])
#        self.setPen(QtGui.QPen(QtCore.Qt.gray, 0))
#        self.hover = False


#    def draw_icon(self):
#        self.setBrush(QtGui.QBrush(QtCore.Qt.gray))
#        if self.command[2]:
#            boarder_factor = -4
#            h = self._size[0] + boarder_factor
#            w = self._size[1] + boarder_factor
#            self.renderer = QtSvg.QSvgRenderer(self.command[2])
#            self.pixmap = QtGui.QPixmap(w, h)
#            self.pixmap.fill(QtCore.Qt.gray)
#            self.painter = QtGui.QPainter(self.pixmap)
#            self.renderer.render(self.painter)
#            brush = QtGui.QBrush()
#            brush.setTexture(self.pixmap)
#            brush.setStyle(QtCore.Qt.RadialGradientPattern)
#            brush.setTransform(QtGui.QTransform.fromTranslate(w / 2, h / 2))
#            self.setBrush(brush)

#    def setHover(self, value):
#        if not self.hover == value:
#            self.hover = value
#            if value:
#                self.setPen(QtGui.QPen(QtCore.Qt.blue, 3))
#                self.view.setText(self.command[0])
#            else:
#                self.setPen(QtGui.QPen(QtCore.Qt.gray, 0))

#    def paint(self, painter, options, widget):
#        painter.setRenderHints(painter.renderHints() | QtGui.QPainter.Antialiasing);
#        super(PieButton, self).paint(painter, options, widget)


#class PieDialog(QtGui.QGraphicsView):
#    def __init__(self, key, commands, parent=None):
#        super(PieDialog, self).__init__(parent)
#        self.key = key
#        self.setMouseTracking(True)
#        self.setWindowFlags(
#            QtCore.Qt.FramelessWindowHint |
#            QtCore.Qt.MSWindowsFixedSizeDialogHint)
#        self.setWindowModality(QtCore.Qt.ApplicationModal)
#        self.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
#        self.setDragMode(QtGui.QGraphicsView.NoDrag)
#        self.blockSignals(True)
#        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
#        self.setStyleSheet("QGraphicsView {border-style: none; background: transparent;}" )
#        self.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
#        self.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
#        self.setScene(QtGui.QGraphicsScene(self))
#        self.scene().setSceneRect(-200, -200, 400, 400)
#        self.center = [0, 0]
#        self.buttons = []
#        self.label = QtGui.QGraphicsSimpleTextItem("")
#        self.scene().addItem(self.label)
#        self.add_commands(commands)
#        self.is_on = False
#        self.is_hover = False

#    def setText(self, text):
#        self.label.setText(text)
#        self.label.setPos(-self.label.sceneBoundingRect().width() / 2, 0)
#        self.label.update()

#    def add_commands(self, commands):
#        num = len(commands)
#        r = 100
#        a = 70
#        pie_phi = np.linspace(0, np.pi * 2, num + 1)
#        phi = [(p + pie_phi[i + 1]) / 2 for i, p in enumerate(pie_phi[:-1])]
#        for i, command in enumerate(commands):
#            button = PieButton(
#                [r * np.cos(phi[i]), r * np.sin(phi[i])],
#                [pie_phi[i], pie_phi[i + 1]],
#                [a, a], self, self.scene(),
#                command=command)
#            self.buttons.append(button)

#    def mouseMoveEvent(self, event=None):
#        if self.is_on:
#            r2, angle = self.polarCoordinates
#            self.is_hover = False
#            for item in self.buttons:
#                if (item.angle_range[0] < angle and
#                    angle < item.angle_range[1] and
#                    r2 > 3000):
#                    item.setHover(True)
#                    self.is_hover = True
#                else:
#                    item.setHover(False)
#            if not self.is_hover:
#                self.setText("")

#    def resizeEvent(self, event):
#        pass

#    @property
#    def polarCoordinates(self):
#        pos = QtGui.QCursor.pos() - self.center
#        r2 = pos.x() ** 2 + pos.y() ** 2
#        angle = np.arctan2(pos.y(), pos.x())
#        return r2, angle + (angle < 0) * 2 * np.pi

#    def showAtMouse(self):
#        if not self.is_on:
#            self.setVisible(True)
#            self.center = QtGui.QCursor.pos()
#            self.move(self.center.x()-(self.width()/2), self.center.y()-(self.height()/2))
#            self.is_on = True

#    def keyPressEvent(self, event):
#        if event.key() == self.key:
#            if not event.isAutoRepeat():
#                print("not autorepeat")
#                self.hide_menu()

#    def keyReleaseEvent(self, event):
#        if event.key() == self.key:
#            self.mouseMoveEvent()
#            if self.is_hover and not event.isAutoRepeat():
#                self.hide_menu()

#    def mousePressEvent(self, event):
#        self.hide_menu()


#    def hide_menu(self):
#        self.is_on = False
#        self.hide()
#        for item in self.buttons:
#            if item.hover:
#                item.setHover(False)
#                item.command[1]()

#if __name__ == "__main__":
#    def part_design(): Gui.activateWorkbench("PartDesignWorkbench")
#    def part(): Gui.activateWorkbench("PartWorkbench")
#    def draft(): Gui.activateWorkbench("DraftWorkbench")
#    def arch(): Gui.activateWorkbench("ArchWorkbench")
#    def fem(): Gui.activateWorkbench("FemWorkbench")
#    def sketch(): Gui.activateWorkbench("SketcherWorkbench")
#    def draw(): Gui.activateWorkbench("DrawingWorkbench")
#    def mesh(): Gui.activateWorkbench("MeshWorkbench")

#    command_list = [
#        ["PartDesign", part_design, None],
#        ["Part", part, None],
#        ["Draft", draft, None],
#        ["Arch", arch, None],
#        ["Fem", fem, None],
#        ["sketch", sketch, None],
#        ["draw", draw, None],
#        ["mesh", mesh, None]]

#    a = PieDialog(QtGui.QKeySequence("TAB"), command_list)
#    action = QtGui.QAction(None)
#    action.setShortcut(a.key)
#    action.triggered.connect(a.showAtMouse)
#    Gui.getMainWindow().addAction(action)


#import FreeCAD,FreeCADGui
#import datetime

#global selpairs
#global signatur

#signatur='.v'
#selpairs=[]

#def scan_selection():
#	global signatur
#	global selpairs
#	seltab={}
#	selex=Gui.Selection.getSelectionEx()
#	for s in selex:
#		Msg(s.ObjectName)
#		suobjs=s.SubObjects
#		seltab[s]=suobjs
#	#	Msg(s)
#		Msg("\n")
#		
#		seltab[s.Object]=suobjs
#		seltab[s.Object].reverse()
#		for suob in suobjs:
#			Msg(suob)
#			Msg(suob.ShapeType)
#			Msg("\n")
#			if suob.ShapeType =="Edge":
#				Msg( suob.Vertexes[0].Point) ;Msg ("---");
#				Msg( suob.Vertexes[1].Point)
#			Msg("\n")
#		Msg("\n")


#	Msg(seltab)
#	print(seltab)

#	selpairs=[]
#	sel=Gui.Selection.getSelection()
#	for ss in sel:
#		Msg(ss.Label)
#		Msg("\n")
#		p=seltab[ss].pop()
#		print(p)
#		print(seltab[ss])
#		selpairs.append([ss,p])
#		

#	Msg("------------------\n")

#	signatur=""
#	for [a,b] in selpairs:
#		print a.Label,b
#		if b.ShapeType == "Edge":
#			print b.Vertexes[0].Point
#			print b.Vertexes[1].Point
#			signatur += ".e"
#		elif b.ShapeType == "Vertex":
#			print b.Vertexes[0].Point
#			signatur += ".v"
#		elif b.ShapeType == "Face":
#			print b.CenterOfMass
#			signatur += ".f"
#		else:
#			raise Exception

#----------------------
#print selpairs
#print signatur
#######################

#stream='''
#conf:
#  t1:
#    sig: .v.v
#    exec: Msg("signatur vertex vertex")
#    icon: /usr/lib/freecad/Mod/plugins/icons/rectellipse.png
#    info: This is the tooltipp
#  t2:
#    sig: .v.e
#    exec: Msg("signatur vertex edge")
#    icon: /usr/lib/freecad/Mod/plugins/icons/mars.png
#    info: create a well sized mars view

#  t3:
#    sig: .v.e
#    exec: Msg("signatur vertex edge")
#    icon: /usr/lib/freecad/Mod/plugins/icons/sun.png
#    info: create a well sized Sunview
#  t3a:
#    sig: .e.v
#    exec: Msg("signatur edge vertex")
#    icon: /usr/lib/freecad/Mod/plugins/icons/mars.png
#    info: create a well sized Marsview redirect!
#  
#  t4:
#    sig: .f.f
#    exec: Msg("two faces")
#    icon: /usr/lib/freecad/Mod/plugins/icons/master.png
#    info: two faces

#  t5:
#    sig: .f
#    exec: Msg("one faces")
#    icon: /usr/lib/freecad/Mod/plugins/icons/fem.png
#    info: one face tool
#  t6:
#    sig: .v.v.v
#    exec: Msg("signatur vertex vertex vertex")
#    icon: /usr/lib/freecad/Mod/plugins/icons/circle-3points.png
#    info: This three point tool
#  t7:
#    sig: .v
#    exec: Msg("signatur vertex ")
#    icon: /usr/lib/freecad/Mod/plugins/icons/help.png
#    info: This one point tool

#  t8:
#    sig: .e
#    exec: Msg("signatur vertex vertex")
#    icon: /usr/lib/freecad/Mod/plugins/icons/freecad.png
#    info: This edge tool

#  t9:
#    sig: .e
#    exec: Msg("signatur edge")
#    icon: /usr/lib/freecad/Mod/plugins/icons/ship.png
#    info: This is the other edge tool

#  ta:
#    sig: .e.e
#    exec: Msg("signatur edge edge")
#    icon: /usr/lib/freecad/Mod/plugins/icons/bolts.png
#    info: This two edge tool

#  tb:
#    sig: .e.e
#    exec: Msg("signatur edge edge")
#    icon: /usr/lib/freecad/Mod/plugins/icons/camera-photo.png
#    info: This is an other 2-edge tool
#'''


#import yaml
#global config3
#config3 = yaml.load(stream)

#def nn():
#	FreeCAD.Console.PrintMessage("nn")
#	fn="/usr/lib/freecad/Mod/plugins/selectiontoolbar.py";exec open(fn).read()
#	FreeCAD.Console.PrintMessage("nn")

#def starter(show=True):
#	show=False
#	global signatur
#	global selpairs
#	global config3
#	FreeCAD.Console.PrintMessage("\nStarter ....\n")
#	FreeCAD.Console.PrintMessage("\nsignatur=" + signatur +"\n")
#	mw=FreeCAD.Gui.getMainWindow()
#	mw.toolbar=None
#	toolbars = mw.findChildren(QtGui.QToolBar)
#	print toolbars
#	for t in toolbars:
#	#	print t.windowTitle()
#		wt=str(t.windowTitle())
#		if wt == 'www Y':
#			mw.toolbar=t
#			Msg("gefunden")
#	if not mw.toolbar:
#		Msg("erzeugnt")
#		mw.toolbar = mw.addToolBar("www")
#		mw.toolbar.setWindowTitle("www Y" )
#		mw.toolbar.hide()
#	mw.toolbar.hide()
#	mw.toolbar.setStyleSheet("\
#				QWidget { background-color: transparent;}\
#				QToolBar {border:1px solid white;padding:0px;}\
#				QToolBar:hover { background-color: yellow;}\
#				")
#	mw.toolbar.setAttribute(QtCore.Qt.WA_TranslucentBackground)
#	twas=mw.toolbar.actions()
#	for a in twas:
#		FreeCAD.Console.PrintMessage(str(a) +" Starter loesche aktion....")
#		mw.toolbar.removeAction(a)

#	import pprint
#	pprint.pprint(config3)
#	cf=config3['conf']
#	show=False
#	for k in cf.keys():
#		
#		print k
#		print cf[k]['sig']
#		if cf[k]['sig'] == signatur:
#			show=True
#			FreeCAD.Console.PrintMessage(k + "setze aktion\n")
#			myAction2=QtGui.QAction(QtGui.QIcon(cf[k]['icon']),k ,mw)
#			myAction2.setToolTip(cf[k]['info'])
#		#					try:
#		#						cmd=yy['exec']
#		#					except:
#		#						cmd="say('"+str(yy)+"')"
#		#					yy=MyAction2(cmd)
#		#					myAction2.yy=yy
#		#					myAction2.triggered.connect(yy.run) 
#			print myAction2
#			mw.toolbar.addAction(myAction2)
#	l=len(mw.toolbar.actions())
#	mw.toolbar.resize(40*l,10)
#	
#	if show:
#		FreeCAD.Console.PrintError("show  aktion\n")
#		mw.toolbar.show()
#	else: 
#		FreeCAD.Console.PrintError("hide  aktion\n")
#		mw.toolbar.hide()


#	if False:
#		eAction = QtGui.QAction(QtGui.QIcon('/usr/lib/freecad/Mod/plugins/icons/web-refresh.png'),'reload menu', mw)
#		# eAction = QtGui.QAction('reload menu', mw)
#		eAction.setShortcut('#')
#		eAction.triggered.connect(nn)
#		mw.toolbar.addAction(eAction)
#	FreeCAD.Console.PrintMessage("\nStarter  fertig\n")



#class SelObserver:

#	def __init__(self,method):
#		self.cmd=method

#	def run(self,show=True):
#		FreeCAD.Console.PrintWarning("\nRun SelObserver\n")
#		ts = datetime.datetime.now()
#		scan_selection()
#		self.cmd(show)
#		tf = datetime.datetime.now()
#		te = tf - ts
#		Msg(te)


#	def setSelection(self, doc):
#		Msg("Selection changed on " + doc + "\n")
#		self.run(True)


#	def addSelection(self, doc, obj, sub, pnt):
#		Msg("Add selection on " + doc + "\n")
#		# Msg(str(obj) +"!"+str(sub)+"!"+ str(pnt))
#		self.run(True)

#	def removeSelection(self, doc, obj, sub):
#		Msg("Remove selection on " + doc + "\n")
#		self.run(True)

#	def clearSelection(self, doc):
#		Msg("Remove selection on " + doc + "\n")
#		self.run(False)


#s=SelObserver(starter)
#Gui.Selection.addObserver(s)
