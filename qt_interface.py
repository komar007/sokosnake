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

class QtInterface(ActionReceiver):
	def __init__(self, filename):
		self.game = Sokosnake(filename)
		self.init_qt()
		self.i = 0;
		self.steps = open(sys.argv[2]).read()

		self.game.connect(events.Create('after'), self.action('create'))
		self.game.load()

	def action_create(self, event, params):
		GuiElement(event.element)
		self.scene.addItem(event.element.gui)
		event.element.gui.moveBy(SIZE * event.element.x, SIZE * event.element.y)
		self.game.connect(event.element.event('after', events.Move), event.element.gui.action('move'))

	supported_actions = {'create': action_create}

	def init_qt(self):
		self.app = QtGui.QApplication(sys.argv)
		self.scene = QtGui.QGraphicsScene()
		self.scene.setSceneRect(0,0,self.game.size_x * SIZE, self.game.size_y * SIZE)

		self.view = QtGui.QGraphicsView(self.scene)
		self.view.setRenderHint(QtGui.QPainter.Antialiasing)

		self.view.resize(self.game.size_x * SIZE, self.game.size_y * SIZE)

		for el in [Passage, Wall, Head, Body, Apple, Room, Rock, Diamond, Teleport, Teleend, Hole, Gate]:
			ELS[el] = QtSvg.QSvgRenderer('img/' + el.__name__.lower() + '.svg')

		self.view.show()
	
	def start(self):
		self.timer = QtCore.QTimer()
		QtCore.QObject.connect(self.timer, QtCore.SIGNAL('timeout()'), self.step)
		self.timer.start(300)
		return self.app.exec_()

	def step(self):
		self.game.step(DIR[self.steps[self.i]])
		self.i+=1

q = QtInterface(sys.argv[1])
q.start()
