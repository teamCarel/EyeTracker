import sys
from Ui_MainWindow import Ui_MainWindow
from Ui_RunWindow import Ui_RunWindow
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication
from random import randint
import time
class MyWindow(Ui_MainWindow):
    def __init__(self, dialog):
        Ui_MainWindow.__init__(self)

def run_Run(self):
    global RunWindow
    global run_ui
    resolution = (ui.comboBox.currentText()).partition('x')
    row = int(resolution[0])
    column = int(resolution[2])

    i=0
    pictures =[]

    for i in range(len(ui.fieldChecks)):
       if ui.fieldChecks[i].isChecked():
            pictures.append(len(ui.fieldChecks))
            pictures[len(pictures)-1]=i
    if((row*column) == len(pictures)):
        RunWindow = QtWidgets.QMainWindow()

        run_ui = Ui_RunWindow()
        run_ui.setupUi(RunWindow, row, column, pictures) ##rows, cols, field
        run_ui.Exit.clicked.connect(run_ui_run_Exit)
        run_ui.ExitAll.clicked.connect(run_ui_run_ExitAll)
        RunWindow.showFullScreen()
    else:
        print((row*column))
        
def run_ui_run_Exit(self):
    x = randint(0,2)
    y = randint(0,2)
    run_ui.highlightPic(x, y)
    print("barvim")
    RunWindow.repaint()
    time.sleep(10)
    run_ui.unHighlightPic(x, y)
    print("vracim")
    # RunWindow.close()
    
def run_ui_run_ExitAll(self):
    RunWindow.close()
    MainWindow.close()

if __name__ == '__main__':
    global MainWindow
    global ui
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    run = ui.Run.clicked.connect(run_Run)   
    MainWindow.show()
    sys.exit(app.exec_())

