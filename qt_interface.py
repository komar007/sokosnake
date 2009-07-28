#!/usr/bin/env python

from PyQt4 import QtCore, QtGui, QtSvg
import sys

from sokolib.action import *
import sokolib.events
from sokosnake import *

SIZE=16
DIR = {'r': Right, 'l': Left, 'u': Up, 'd': Down}
ELS = {}

class GuiElement(QtGui.QGraphicsItem, ActionReceiver):
	def __init__(self, element):
		self.element = element
		self.element.gui = self
		QtGui.QGraphicsItem.__init__(self)
		self.setZValue(self.element.game.map[self.element.x, self.element.y].index(self.element))

	def paint(self, painter, option, widget):
		ELS[type(self.element)].render(painter, QtCore.QRectF(0,0, SIZE, SIZE))
	
	def boundingRect(self):
		return QtCore.QRectF(0,0,SIZE, SIZE)

	def action_move(self, event, params):
		self.setPos(SIZE * event.to_field[0], SIZE * event.to_field[1])
		self.setZValue(self.element.game.map[event.to_field].index(self.element))

	supported_actions = {'move': action_move}

class MyView(QtGui.QGraphicsView):
	def keyPressEvent(self, event):
		if event.type() == QtCore.QEvent.KeyPress:
			if event.key() == QtCore.Qt.Key_Down:
				self.interface.step(Down)
			elif event.key() == QtCore.Qt.Key_Up:
				self.interface.step(Up)
			elif event.key() == QtCore.Qt.Key_Left:
				self.interface.step(Left)
			elif event.key() == QtCore.Qt.Key_Right:
				self.interface.step(Right)
				

class QtInterface(ActionReceiver):
	def __init__(self, filename):
		self.init_qt(not filename)
		self.game = Sokosnake(filename or self.filename)
		self.set_sizes()

		self.game.connect(events.Create('after'), self.action('create'))
		self.game.connect(events.Remove(None, 'before'), self.action('destroy'))
		self.game.load()

	def action_create(self, event, params):
		GuiElement(event.element)
		self.scene.addItem(event.element.gui)
		event.element.gui.moveBy(SIZE * event.element.x, SIZE * event.element.y)
		self.game.connect(event.element.event('after', events.Move), event.element.gui.action('move'))

	def action_destroy(self, event, params):
		self.scene.removeItem(event.element.gui)
		del(event.element.gui)

	supported_actions = {'create': action_create, 'destroy': action_destroy}

	def init_qt(self, choose):
		self.app = QtGui.QApplication(sys.argv)
		self.scene = QtGui.QGraphicsScene()

		self.view = MyView(self.scene)
		if choose:
			self.filename = QtGui.QFileDialog.getOpenFileName(self.view, "Choose a level...", "./levels", "All Files (*.*)")
		self.view.interface = self
		self.view.setRenderHint(QtGui.QPainter.Antialiasing)
		self.view.setBackgroundBrush(QtGui.QBrush(QtGui.QColor(0,0,0)))

		self.view.resize(self.game.size_x * SIZE + 50, self.game.size_y * SIZE + 50)
		for el in [Passage, Wall, Head, Body, Apple, Room, Rock, Diamond, Teleport, Teleend, Hole, Gate]:
			ELS[el] = QtSvg.QSvgRenderer('img/' + el.__name__.lower() + '.svg')

		self.view.show()

	def set_sizes(self):
		self.scene.setSceneRect(0,0,self.game.size_x * SIZE, self.game.size_y * SIZE)
		self.view.resize(self.game.size_x * SIZE + 64, self.game.size_y * SIZE + 64)
	
	def start(self):
		self.timer = QtCore.QTimer()
		#QtCore.QObject.connect(self.timer, QtCore.SIGNAL('timeout()'), self.step)
		QtCore.QObject.connect(self.view, QtCore.SIGNAL('clicked'), self.step)
		self.timer.start(300)
		return self.app.exec_()

	def step(self, dir):
		try:
			self.game.step(dir)
		except sokolib.game.Conflict:
			print "Game over"

if len(sys.argv) == 2:
	filename = sys.argv[1]
else:
	filename = None
q = QtInterface(filename)
q.start()
