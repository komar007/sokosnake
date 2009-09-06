import sys
from PyQt4 import QtCore, QtGui, QtSvg
from sokosnakewindow import Ui_SokosnakeWindow

class SokosnakeWindow(QtGui.QMainWindow):
	def __init__(self, parent=None):
		QtGui.QWidget.__init__(self, parent)
		self.ui = Ui_SokosnakeWindow()
		self.ui.setupUi(self)
	
	def load_level(self):
		self.filename = QtGui.QFileDialog.getOpenFileName(self, "Choose a level...", "levels", "All Files (*.*)")

if __name__ == "__main__":
	app = QtGui.QApplication(sys.argv)
	win = SokosnakeWindow()
	win.show()
	sys.exit(app.exec_())

