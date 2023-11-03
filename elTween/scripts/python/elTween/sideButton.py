from PySide2.QtCore import QSize, QEvent, QPoint, Qt, QPropertyAnimation
from PySide2.QtWidgets import QPushButton,  QWidget
from PySide2.QtGui import QCursor, QPixmap, QIcon

import os
class sideButton(QWidget):
    elGlobal =[]
    index = -1
    labels = ["Position", "Rotation", "Scale", "Skew"]
    widths = [70, 70, 55, 55]

    def __init__(self, parent):
        QWidget.__init__(self, parent) 

    def setup(self,elGlobal):
        self.elGlobal=elGlobal

        self.button = QPushButton('', self)
        self.button.setFixedSize(
        self.elGlobal["timelineHeightPX"], self.elGlobal["timelineHeightPX"])
        self.type = None
        self.button.clicked.connect(self.clicked)

    def addImage(self, numb, size):
        self.index = numb

        icon_path = os.path.join(os.path.dirname(
            __file__), "images/icon_"+str(numb+1)+".png")
        self.button.setStyleSheet("border: none;")
        self.button.setIcon(QIcon(icon_path))
        self.button.setIconSize(size)
        self.button.setFixedSize(size)
        self.setFixedSize(size)

    def event(self, event):
        if event.type() == QEvent.Enter:
            self.elGlobal["infoBG"].setVisible(True)
            self.elGlobal["infoBG"].setRect(0, 0, self.widths[self.index], 30)
            self.elGlobal["infoBG"].prepareGeometryChange()
            self.elGlobal["infoBG"].update()
            self.elGlobal["infoText"].setVisible(True)
            self.elGlobal["infoText"].setText(self.labels[self.index])
            newY = self.index * \
                self.elGlobal["timelineHeightPX"] + \
                self.elGlobal["timelineHeightPX"]*0.25
            self.elGlobal["infoBG"].setY(newY)
            self.elGlobal["infoText"].setY(
                newY + self.elGlobal["infoBG"].boundingRect().size().height()*0.2)
        elif event.type() == QEvent.Leave:
            self.elGlobal["infoBG"].setVisible(False)
            self.elGlobal["infoText"].setVisible(False)
        return super().event(event)

    def clicked(self):

        # set mode tonormal
        self.elGlobal["navigationMode"] = 0
        self.doAnim()
        box = self.elGlobal["elTweenLayout"].addTween(self.type)

    def doAnim(self):
        startX = self.pos().x()
        startY = self.pos().y()
        self.anim = QPropertyAnimation(self, b"pos")
        self.anim.setDuration(300)
        self.anim.setKeyValueAt(0.1, QPoint(startX, startY-10))
        self.anim.setKeyValueAt(0.4, QPoint(startX, startY))
        self.anim.start()
