from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import sys
import skica
from skica import ICA
import numpy as np
import matplotlib.pyplot as plt
import argparse

class widget(QWidget):

    def __init__(self, file_names, parent = None):
        super(widget, self).__init__(parent)
        
        self.file_names = file_names
        
        self.vlay = QVBoxLayout()
        self.setLayout(self.vlay)
        
        self.ICA = ICA()
        self.runICA()
        self.createButtons()
        
    def createButtons(self):
        self.buttons = []
        
        self.vlay.addWidget( QLabel("Inverse color map:", self) )
        self.qlay = QGridLayout()
        self.vlay.addLayout(self.qlay)
        
        for i in range(self.ICA.npics):
            button = QPushButton('Picture '+str(i+1), self)
            button.clicked.connect(self.inverseFig)
            self.qlay.addWidget(button, i, 0)
            self.buttons.append(button)
        
        button = QPushButton('Exit', self)
        button.clicked.connect(self.exitActivated)
        self.vlay.addWidget(button)
        
    def runICA(self):
        QApplication.setOverrideCursor(Qt.WaitCursor)
        self.ICA.read_sources(self.file_names)
        self.ICA.run()
        self.ICA.plot()
        QApplication.restoreOverrideCursor()
    
    def closeEvent(self, event):
        self.exitActivated()

    def exitActivated(self):
        plt.close('all')
        self.close()
        
    def inverseFig(self):
        QApplication.setOverrideCursor(Qt.WaitCursor)
        for i in range(self.ICA.npics):
            if self.buttons[i] == self.sender():
                self.ICA.inverseFig(i)
                break
        QApplication.restoreOverrideCursor()

def runGUI(file_name, argv):
    app = QApplication(argv)
    ex = widget(file_name)
    ex.show()
    return app.exec_()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog="python skica", \
        description='compute the independent components of linearly mixed images')
    parser.add_argument('--seed', \
        type=int, \
        default=1, \
        help="seed for the normal random generator (default is 1)")
    parser.add_argument("--file", \
        default=["./city.jpg", "./bumper.jpg", "./raisin.jpg", "./flats.jpg"], \
        help="pictures", \
        nargs="+")
    args = parser.parse_args()
    
    # setting seed
    print("setting seed for normal number generator to {}".format(args.seed))
    np.random.seed(seed=args.seed)
    
    # run
    runGUI(args.file, sys.argv)
