#***************************************************************************
#*                                                                         *
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
