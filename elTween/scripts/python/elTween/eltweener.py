import hou
import os
import math
import json
import inspect
import webbrowser
import numpy as np
import logging
from PySide2 import QtCore, QtWidgets
from PySide2.QtWidgets import QHBoxLayout, QComboBox, QSizePolicy, QAbstractSpinBox,  QSpinBox, QPushButton,  QCheckBox, QGraphicsView, QWidget, QDoubleSpinBox, QLabel, QVBoxLayout,  QGraphicsScene,  QGraphicsItem, QGraphicsRectItem
from PySide2.QtGui import QColor, QFont, QTransform, QCursor, QPixmap, QPainter, QPen, QIcon, QBrush, QPainterPath
from PySide2.QtCore import QEvent, QTimer, QSize,  QPointF, QLineF,  QPoint, Qt, QRect, QRectF, QPropertyAnimation

#(.)thing is relative importing from same directory
from .sideButton import *
import importlib

#FOR DEBUGGING
mainDirPath = os.path.dirname(os.path.realpath(__file__))

"""
Debug Notes:
After completion search for
#DEBUG to see what to commend back out

 To hot refresh a script: exec(open(os.path.join(mainDirPath,  "sideButton.py")).read(), globals())

"""
logger = logging.getLogger(__name__)
FORMAT = "[%(filename)s:%(lineno)s - %(funcName)20s() ] %(message)s"
logging.basicConfig(format=FORMAT)
logger.setLevel(logging.DEBUG)  # LUCKY, REMOVE LOGGING ON FINAL
gen_object = type('object', (object,), {})  # generic object maker
# #UTILITY

#will be used for referencing
#properties panel
parameter_props = {}
parameter_prop_objects = {}
#CSS

##GLOBALS
paneTab = None
#SET


######## ##          ######## ##      ## ######## ######## ##    ##
##       ##             ##    ##  ##  ## ##       ##       ###   ##
##       ##             ##    ##  ##  ## ##       ##       ####  ##
######   ##             ##    ##  ##  ## ######   ######   ## ## ##
##       ##             ##    ##  ##  ## ##       ##       ##  ####
##       ##             ##    ##  ##  ## ##       ##       ##   ###
######## ########       ##     ###  ###  ######## ######## ##    ##

## BY LUCKY DEE
## WWW.THISGOODBOY.COM
class eltween(QtWidgets.QFrame):
    global paneTab
    __paneSize = None

    ##TWEEN PROPERTIES
    __tweenExportables = dict(
        x=dict(value=0, type=QDoubleSpinBox, row=1),
        y=dict(value=0, type=QDoubleSpinBox, row=2),
        z=dict(value=0, type=QDoubleSpinBox, row=3),
        relative=dict(value=0, type=QCheckBox, row=4),
        duration=dict(value=0, type=QDoubleSpinBox, row=5),
        delay=dict(value=0, type=QDoubleSpinBox, row=6),
        easeType=dict(value="Linear", type=QComboBox, row=1),
        inOut=dict(value="Out", type=QComboBox, row=2),
        atprops_0=dict(value=0.4, type=QDoubleSpinBox, row=3),
        atprops_1=dict(value=0.6, type=QDoubleSpinBox, row=4),
        loops=dict(value=0, type=QSpinBox, row=5),
        loop_delay=dict(value=0, type=QDoubleSpinBox, row=6),
        stagger_x=dict(value=0, type=QDoubleSpinBox, row=1),
        stagger_y=dict(value=0, type=QDoubleSpinBox, row=2),
        stagger_z=dict(value=0, type=QDoubleSpinBox, row=3),
        pointStagger=dict(value=0, type=QDoubleSpinBox, row=4),
        _spacer1=dict(value="", type=QLabel, row=5),
        _spacer2=dict(value="", type=QLabel, row=6),
        pivot_x=dict(value=0, type=QDoubleSpinBox, row=1),
        pivot_y=dict(value=0, type=QDoubleSpinBox, row=2),
        pivot_z=dict(value=0, type=QDoubleSpinBox, row=3),
        _spacer3=dict(value="", type=QLabel, row=4),
        _spacer4=dict(value="", type=QLabel, row=5),
        track=dict(value=0, type=QLabel, row=6),
        subTrack=dict(value=-1, type=QSpinBox, row=4),
    )
    __easeTypes = ["Linear", "Power1", "Power2", "Power3",
                   "Power4", "Elastic", "Bounce", "Back", "Expo"]
    __easeInOut = ["Out", "In", "InOut"]

    def _setupGlobals(self):
        self.elGlobal = dict(
            CSS=dict(
                draggableBox=dict(
                    colorStroke=["#ab0681", "#750583", "#ffb98e", "#fff397"],
                    colorFill=["#fff397",  "#ffb98e", "#ab0681", "#750583"]
                ),
                tabButtonFont="Helvetica [Adobe]",
                tabButtonFontSize=hou.ui.scaledSize(13),
                tabButtonFontWeight=QFont.Light,
                tabButtonOff=[
                    """
                    background-color: #ffffff;
                    color:#232323;
                    border-bottom-left-radius : 18px;
                    """,
                    """
                    background-color: #e1e1e1;
                    color:#232323;
                    border: none;
                    """,
                    """
                    background-color: #ffffff;
                    color:#232323;
                    border: none;
                    """,
                    """
                    background-color: #e1e1e1;
                    color:#232323;
                    border-bottom-right-radius : 18px;
                    """

                ],
                tabButtonOn=[
                    """
                    background-color: #e30573;
                    color:#ffffff;
                    border-bottom-left-radius : 18px;
                    """,
                    """
                    background-color: #e30573;
                    color:#ffffff;
                    border: none;
                    """,
                    """
                    background-color: #e30573;
                    color:#ffffff;
                    border: none;
                    """,
                    """
                    background-color: #e30573;
                    color:#ffffff;
                    border-bottom-right-radius : 18px;
                    """

                ],
                subTweenColors=[
                    "ffea93", "ffdd8f", "ffcc8d", "faa281", "f48a78", "e56773",
                    "e56773", "b11e7c", "9d0981", "750583", "553191", "3e3e95"
                ],
                subTweenOn="""
                    border-top: solid; border-bottom: solid;  color:#ffffff;
                     background-color: #101010;
                    """,
                subTweenOff="""color:rgba(0,0,0,0); border: none; """,
                scrubbingLine=QPen(QColor("#750583"), 6)
            ),
            node=None,
            size=None,
            view=None,
            scene=None,
            midFrame=None,
            tabsBar=None,
            elTweenLayout=None,
            shadowBox=None,
            layoutRatios=dict(  # x out of 10, height ratios
                topLayout=0.67,
                drawingSceneLayout=3.67,
                TabsBar=5.67,
            ),
            #TAB BUTTONS LEFT RIGHT TOP BOT
            tabButtons=[],
            buttonSizes=dict(
                leftSideButtons=QSize(50, 60),
                rightSideButtons=QSize(50, 60),
                TopButtons=QSize(35, 40)
            ),
            #TIMELINE INFORMATION
            tweenStartValues=dict(self.__tweenExportables),
            timeline_width=None,
            tracks=4,  # position, rotation, scale ,skew
            currentZoomLevel=1,  # ACTUALLY USED
            currentOffetX=1,  # ACTUALLY USED

            boxZoomFactor=1,
            viewPanOffsetX=0,
            navigationMode=0,  # 0 normal, 1 zoom in 2 zoom out 3 pan
            minimumFrames=2,  # minimum frames for a tween to be not deleted
            optimal_timeline_length=3,  # seconds
            default_tween_length=8,  # frames
            default_tween_pixels=None,  # will be autofilled later
            dragging=True,  # tracks current drag state
            timelineHeightPX=60,  # should be drawingSceneLayout*ratio/10*stageheight
            #object_tracking
            elBoxes=[],
            #this == a 2d array for each track has all the sub objects
            timeline_items=[],
            #this == like the items array but it tracks in terms of numbers
            #e.g. -1-1-1-1-1 1 2 3 4 means the first 5 frames has an object

            # 2d array, top 4 (prssh), inside 3(xyz)
            subTimelines=[
                [[], [], []],
                [[], [], []],
                [[], [], []],
                [[], [], []]
            ],
            objectsOnStage=gen_object(),
            currentBoxSelected=None,
            infoText=None,
            infoBG=None,

            #Houdini info
            startFrame=hou.playbar.frameRange()[0]-1,
            endFrame=hou.playbar.frameRange()[1],
            fps=hou.fps(),
            #Properties Panel

            Tabs=["Animate", "Stagger", "Pivot", "Adjust"],
            TabFrames=[],  # will store all the popup menus
            subTweenMenus=[],  # will store all sub tween buttons
            TabProps=[
                ["x", "y", "z", "easeType", "inOut", "atprops_0", "atprops_1"],
                ["stagger_x", "stagger_y", "stagger_z", "pointStagger"],
                ["pivot_x", "pivot_y", "pivot_z"],
                ["delay", "duration", "loop_delay", "loops", "relative"],
            ],
            TabPositions=[  # 2d representation of where everything goes
                [[0, 0], [0, 1], [0, 2], [1, 0], [1, 1], [2, 0], [2, 1]],
                [[0, 0], [0, 1], [0, 2], [1, 0]],
                [[0, 0], [0, 1], [0, 2]],
                [[0, 0], [0, 1], [0, 5], [1, 0], [1, 1]],
            ],
            propertiesWidgets={},  # to be filled with inputs,
            propertiesHeadings={},  # to be filled with headings,
            trashBtn=None,
            trashBtnFiller=None,  # used for spacing

            )
        self.elGlobal["frames"] = self.elGlobal["endFrame"] - \
            self.elGlobal["startFrame"]
        self.elGlobal["midFrame"] = QtWidgets.QFrame()
        self.elGlobal["scene"] = QtWidgets.QGraphicsScene(
            self.elGlobal["midFrame"])  # Graphics Scene
        #this fixes the delete bug where it crashes
        # see https://doc.qt.io/qt-5/qgraphicsscene.html#itemIndexMethod-prop

        self.elGlobal["scene"].setItemIndexMethod(QGraphicsScene.NoIndex)

        #EL TWEEN PROPERTIES
        self.parameters = {}  # Will be filled up by the properties

    def __init__(self, parent=None):

        super(eltween, self).__init__(parent)

    ##INIT CLASS INSTANCE
    def setCurrentNode(self, node):
        if node != None and node.type().name().startswith("elTween"):
            self.elGlobal["node"] = node
            self.elGlobal["shadowBox"].hide()

            self.importTool()
            exportTool(self)  # save the import as the export
            boxLen = len(self.elGlobal["elBoxes"])
            for b in range(boxLen):
                if self.elGlobal["elBoxes"][b].highlighted:
                    newSize = QRectF(
                        self.elGlobal["elBoxes"][b].boundingRect())
                    self.elGlobal["elBoxes"][b].attachShadow(newSize)
                    self.elGlobal["currentBoxSelected"] = self.elGlobal["elBoxes"][b]

    def setCurrentPaneTab(self, panetab):
        if panetab != None:
            self.__paneSize = panetab.size()

    ##CSS
    def CSS(self):
        this = {}
        this["generic_info"] = "red"

        def layoutCSS():
            layoutCSS = {}
            layoutCSS["roundedButtonHighlighted"] = """
            background-color: #3a7b06;
            border-style: solid;
            border-width: 4px;
            border-radius: 10px;
            border-color: #3a7b06;
            """

            layoutCSS["roundedButton"] = """
            background-color: black;
            border-style: solid;
            border-width: 4px;
            border-radius: 10px;
            """

            return layoutCSS

        this["layout"] = layoutCSS()
        return this

    ##          ###    ##    ##  #######  ##     ## ########
    ##         ## ##    ##  ##  ##     ## ##     ##    ##
    ##        ##   ##    ####   ##     ## ##     ##    ##
    ##       ##     ##    ##    ##     ## ##     ##    ##
    ##       #########    ##    ##     ## ##     ##    ##
    ##       ##     ##    ##    ##     ## ##     ##    ##
    ######## ##     ##    ##     #######   #######     ##

      ########  #######  ########     ##          ###    ##    ##  #######  ##     ## ########
        ##    ##     ## ##     ##    ##         ## ##    ##  ##  ##     ## ##     ##    ##
        ##    ##     ## ##     ##    ##        ##   ##    ####   ##     ## ##     ##    ##
        ##    ##     ## ########     ##       ##     ##    ##    ##     ## ##     ##    ##
        ##    ##     ## ##           ##       #########    ##    ##     ## ##     ##    ##
        ##    ##     ## ##           ##       ##     ##    ##    ##     ## ##     ##    ##
        ##     #######  ##           ######## ##     ##    ##     #######   #######     ##
    def topLayout(self):
        TopNavLayout = QHBoxLayout()
        TopNavLayout.setSpacing(0)
        TopNavLayout.setContentsMargins(0, 0, 0, 0)
        rightButttonCount = 4
        #add left side buttons
        for i in range(rightButttonCount):
            button = addFunctionButton(self)
            if i == 1:
                button.setMode(1)  # zoom in
            if i == 2:
                button.setMode(2)  # zoom out
            if i == 3:
                button.setMode(3)  # pan
            button.addImage(i, self.elGlobal["buttonSizes"]["TopButtons"])
            button.type = i
            # button.setFixedHeight(
            # self.elGlobal["timelineHeightPX"])
            TopNavLayout.addWidget(button)

        #attach left side
        spacer = QLabel()
        spacer.setFixedWidth(
            self.elGlobal["buttonSizes"]["leftSideButtons"].width())
        TopNavLayout.addWidget(spacer)
        TopNavLayout.setAlignment(Qt.AlignRight)
        # scroll bar

        return TopNavLayout
    ######## ##      ## ######## ######## ##    ##    ########  ##     ## ######## ########  #######  ##    ##
       ##    ##  ##  ## ##       ##       ###   ##    ##     ## ##     ##    ##       ##    ##     ## ###   ##
       ##    ##  ##  ## ##       ##       ####  ##    ##     ## ##     ##    ##       ##    ##     ## ####  ##
       ##    ##  ##  ## ######   ######   ## ## ##    ########  ##     ##    ##       ##    ##     ## ## ## ##
       ##    ##  ##  ## ##       ##       ##  ####    ##     ## ##     ##    ##       ##    ##     ## ##  ####
       ##    ##  ##  ## ##       ##       ##   ###    ##     ## ##     ##    ##       ##    ##     ## ##   ###
       ##     ###  ###  ######## ######## ##    ##    ########   #######     ##       ##     #######  ##    ##

    def midLeftLayout(self):
        midLeftLayout = QVBoxLayout()
        midLeftLayout.setSpacing(0)
        midLeftLayout.setContentsMargins(0, 0, 0, 0)
        addButtons = []
        leftButtonCount = 4
        #add left side buttons
        exec(open(os.path.join(mainDirPath,  "sideButton.py")).read(), globals())  #DEBUG - DELETE LATER, THIS RELOADS THE FILE
        for i in range(leftButtonCount):
            button = sideButton(self)
            button.setup(self.elGlobal)

            button.addImage(i, self.elGlobal["buttonSizes"]["leftSideButtons"])
            button.type = i
            midLeftLayout.addWidget(button)

        midLeftLayout.setAlignment(Qt.AlignTop)
        return midLeftLayout
    #>>RIGHT SCROLLBAR WIDGET

    def midRightButtons(self):
        mirDightLayout = QVBoxLayout()
        mirDightLayout.setSpacing(0)
        mirDightLayout.setContentsMargins(0, 0, 0, 0)
        rightButtonCount = self.elGlobal["tracks"]*3
        for i in range(rightButtonCount):
            button = addSubTweenButton(self)

            button.setup(self.elGlobal, i)

            button.type = i
            self.elGlobal["subTweenMenus"].append(button)
            mirDightLayout.addWidget(button)
        return mirDightLayout

    def addDrawingSceneGrid(self):
        height = self.elGlobal["timelineHeightPX"]
        w = 3000
        shade1 = QColor("#ffffff")
        shade2 = QColor("#e1e1e1")
        BG = QtWidgets.QGraphicsRectItem(
            QRect(0, 0, w, height*self.elGlobal["tracks"]))
        BG.setBrush(shade1)
        self.elGlobal["scene"].addItem(BG)
        BG.setPen(Qt.NoPen)
        for i in range(2):
            row_odd = QtWidgets.QGraphicsRectItem(
                QRect(0, height*(1*i+i)+height, w, height))
            row_odd.setBrush(shade2)
            row_odd.setPen(Qt.NoPen)
            self.elGlobal["scene"].addItem(row_odd)

    def addTrackGuide(self):
        textBackground = QtWidgets.QGraphicsRectItem()
        textBackground.setBrush(QColor("#202020"))
        textBackground.setPen(Qt.NoPen)
        textBackground.setZValue(150)
        onCSS = "border: 15px solid #"

        textFontSize = hou.ui.scaledSize(11)
        textFontWeight = QFont.Light
        text = self.elGlobal["scene"].addSimpleText("Position")
        text.setZValue(151)
        text.setBrush(QColor("#fff"))
        text.setFont(QFont("Helvetica [Adobe]",
                     textFontSize, weight=textFontWeight))
        text.setX(8)
        self.elGlobal["infoBG"] = textBackground
        self.elGlobal["infoText"] = text
        self.elGlobal["scene"].addItem(textBackground)
        self.elGlobal["infoBG"].setVisible(False)
        self.elGlobal["infoText"].setVisible(False)

    def addEdgeLine(self):
        h = self.elGlobal["scene"].height()
        lineWidth = 2
        vertical_bar = QPen(QColor("#000"), lineWidth)

        self.elGlobal["objectsOnStage"].edgeLine = self.elGlobal["scene"].addLine(
            0, 0, 0, h, vertical_bar)
        self.elGlobal["objectsOnStage"].edgeLine.setZValue(21)
    #>> TOP MID DRAWING SCENE LAYOUT

    def drawingSceneLayout(self):

        layout = QHBoxLayout()
        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 0)
        #create drawing view
        self.elGlobal["view"] = elTimeline(self.elGlobal["midFrame"])
        self.elGlobal["view"].addGlobals(self)
        #self.elGlobal["view"] = QGraphicsView(self.elGlobal["midFrame"])
        self.elGlobal["view"].setScene(self.elGlobal["scene"])
        viewWidth = self.__paneSize[0]*86.7/100
        viewHeight = self.__paneSize[1] * \
            self.elGlobal["layoutRatios"]["drawingSceneLayout"]/10

        self.elGlobal["view"].setFixedSize(
            viewWidth, self.elGlobal["timelineHeightPX"])
        self.elGlobal["view"].setHorizontalScrollBarPolicy(
            Qt.ScrollBarAlwaysOff)
        self.elGlobal["view"].setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        #link drawing view to the main Widget
        updatedSettings = gen_object()
        self.elGlobal["size"] = [self.__paneSize[0], self.__paneSize[1]]
        self.elGlobal["initSize"] = self.elGlobal["size"]
        #updatedSettings.size.setHeight(panetab.size.width()
        self.elGlobal["elTweenLayout"].updateSettings()

        self.elGlobal["scene"].setBackgroundBrush(QColor("#ff00ff"))

        self.elGlobal["view"].setAlignment(Qt.AlignLeft | Qt.AlignTop)

        #NOW WE CAN ADD ITEMS TO STAGE
        self.addDrawingSceneGrid()
        self.addTrackGuide()
        self.addEdgeLine()
        #shadowBox
        shadow = QtWidgets.QGraphicsRectItem(QtCore.QRectF(0, 0, 100, 100))
        shadow.setBrush(QColor("#3a3a3a"))
        shadow.setPen(Qt.NoPen)
        shadow.setZValue(51)
        self.elGlobal["shadowBox"] = shadow
        self.elGlobal["scene"].addItem(shadow)
        shadow.hide()

        self.elGlobal["objectsOnStage"].verticalLine = self.elGlobal["scene"].addLine(
            0, 0, 0, self.elGlobal["scene"].height(), self.elGlobal["CSS"]["scrubbingLine"])

        self.elGlobal["view"].setup(1)  # passing innitial scale
        self.elGlobal["objectsOnStage"].verticalLine.setZValue(60)
        self.elGlobal["view"].setFrameStyle(QtWidgets.QFrame.NoFrame)

        #setup horisontal layout
        #attach left side
        layout.addLayout(self.midLeftLayout())

        #make a center frame, add the stage, and align it to top
        mainFrameLayout = QVBoxLayout()
        mainFrameLayout.setSpacing(0)
        mainFrameLayout.setContentsMargins(0, 0, 0, 0)
        mainFrameLayout.addWidget(self.elGlobal["midFrame"])
        mainFrameLayout.setAlignment(Qt.AlignTop)
        layout.addLayout(mainFrameLayout)
        #attach right side
        layout.addLayout(self.midRightButtons())
       # layout.setVerticalPolicy(QSizePolicy.Maximum)
        self.elGlobal["midFrame"].setFixedHeight(
            self.elGlobal["timelineHeightPX"]*self.elGlobal["tracks"])

        return layout
    ########    ###    ########   ######
       ##      ## ##   ##     ## ##    ##
       ##     ##   ##  ##     ## ##
       ##    ##     ## ########   ######
       ##    ######### ##     ##       ##
       ##    ##     ## ##     ## ##    ##
       ##    ##     ## ########   ######

    def TabsBar(self):
        layout = QHBoxLayout()
        layout.setAlignment(Qt.AlignTop | Qt.AlignTop)
        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 0)

        #TRASH BUTTON
        trashButton = QPushButton('', self)
        trashButton.setFixedWidth(
            self.elGlobal["buttonSizes"]["leftSideButtons"].width())
        trash_icon_path = os.path.join(os.path.dirname(
            __file__), "images/icon_trash.png")
        trashButton.setStyleSheet("border: none;")
        trashButton.clicked.connect(self.deleteBox)
        trashButton.setIcon(QIcon(trash_icon_path))
        trashButton.setIconSize(QSize(35, 35))
        trashButtonSpacer = QLabel('')
        trashButtonSpacer.setFixedSize(trashButton.width(), 0)
        trashButton.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        trashButtonSpacer.setSizePolicy(
            QSizePolicy.Expanding, QSizePolicy.Expanding)
        layout.addWidget(trashButtonSpacer, 6.65)
        layout.addWidget(trashButton, 6.65)
        layout.setAlignment(trashButton, Qt.AlignTop)
        trashButton.hide()
        #trashButtonSpacer.hide()
        self.elGlobal["trashBtn"] = trashButton
        self.elGlobal["trashBtnFiller"] = trashButtonSpacer

        #MIDDLE SECTION , TABS
        #VERTICAL LAYOUT GOING DOWN
        midFrame = QtWidgets.QFrame()
        midVerticalLayout = QVBoxLayout()
        midVerticalLayout.setSpacing(0)
        midVerticalLayout.setContentsMargins(0, 0, 0, 0)
        midVerticalLayout.setAlignment(Qt.AlignTop | Qt.AlignTop)

        #TABS LAYOUT GOING LEFT TO RIGHT
        tabFrame = QtWidgets.QFrame()

        TabHorisontalLayout = QHBoxLayout()
        TabHorisontalLayout.setAlignment(Qt.AlignTop | Qt.AlignTop)
        TabHorisontalLayout.setSpacing(0)
        TabHorisontalLayout.setContentsMargins(0, 0, 0, 0)
        Tabs = self.elGlobal["Tabs"]
        tabCount = len(Tabs)
        css = self.elGlobal["CSS"]
        for t in range(tabCount):
            TabButton = addTabButton(Tabs[t], self)
            TabButton.setup(self.elGlobal, t)
            TabButton.setFixedHeight(40)
            TabButton.setFont(
                QFont(css["tabButtonFont"], css["tabButtonFontSize"], weight=css["tabButtonFontWeight"]))
            TabButton.setStyleSheet(css["tabButtonOff"][t])
            TabHorisontalLayout.addWidget(TabButton)
            self.elGlobal["tabButtons"].append(TabButton)
        #highlight the first menu
        self.elGlobal["tabButtons"][0].setStyleSheet(
            self.elGlobal["CSS"]["tabButtonOn"][0])

        tabFrame.setLayout(TabHorisontalLayout)

        #ADD THE FIRST ROW( the tabs) to the vertical mid layout
        midVerticalLayout.addWidget(tabFrame)
        midFrame.setLayout(midVerticalLayout)

        #Cheatily add the vertical frame to the middle
        layout.addWidget(midFrame)
        spacer = QLabel()
        spacer.setFixedWidth(
            self.elGlobal["buttonSizes"]["leftSideButtons"].width())
        layout.addWidget(spacer)

        tabProps = self.elGlobal["TabProps"]
        TabPositions = self.elGlobal["TabPositions"]
        #run trough the tab count

        not_resizeTF = tabFrame.sizePolicy()
        not_resizeTF.setRetainSizeWhenHidden(True)
        tabFrame.setSizePolicy(not_resizeTF)
        self.elGlobal["tabFrame"] = tabFrame

        self.elGlobal["subTabsFrames"] = []
        self.elGlobal["Tab1Frames"] = []
        for t in range(tabCount):

            ##Create Frame for each
            subTabsFrame = QtWidgets.QFrame()
            self.elGlobal["subTabsFrames"].append(subTabsFrame)

            ly = QtWidgets.QGridLayout(self)
            ly.setAlignment(Qt.AlignTop)
            subTabsFrame.setLayout(ly)
            tempTabArray = []  # used for Tabs
            #add stuff to it
            for key in tabProps[t]:
                prop = self.__tweenExportables[key]
                value = prop["value"]
                type = prop["type"]
                if key == "easeType":
                    self.parameters[key] = self.createProperty(
                        type, key, self.__easeTypes)
                elif key == "inOut":
                    self.parameters[key] = self.createProperty(
                        type, key, self.__easeInOut)
                else:
                    self.parameters[key] = self.createProperty(type, key)
                indx = tabProps[t].index(key)
                positions = TabPositions[t][indx]
                ly.addLayout(self.parameters[key], positions[0], positions[1])
                tempTabArray.append(self.parameters[key].itemAt(1).widget())

                #used to setup navigating with Tab
                if indx != 0:
                    me = tempTabArray[len(tempTabArray)-1]
                    last_me = tempTabArray[len(tempTabArray)-2]
                    self.setTabOrder(last_me, me)
                if indx == len(tabProps) and t == tabCount-1:
                    self.elGlobal["dragging"] = False
            #add it to list

            not_resize = subTabsFrame.sizePolicy()
            not_resize.setRetainSizeWhenHidden(True)
           # subTabsFrame.setSizePolicy(not_resize)
            self.elGlobal["TabFrames"].append(subTabsFrame)
            midVerticalLayout.addWidget(subTabsFrame)
            if t != 0:
                subTabsFrame.hide()  # only show the first tab
            else:  # prevent menu collapsing if we hide them later on

                self.elGlobal["Tab1Frames"].append(subTabsFrame)

        return layout
    #>> PROPERTIES PANEL

    def createProperty(self, type, id, optionalArray=None):
        layout = QHBoxLayout()
        name = id.replace("_", " ")
        heading = QLabel(name.capitalize())
        heading.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        heading.setAlignment(Qt.AlignCenter | Qt.AlignRight)
        heading.setMaximumHeight(28)

        input = type()
        # setting geometry to spin box
        input.setMaximumHeight(42)
        input.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        input.setStyleSheet(self.CSS()["layout"]["roundedButton"])
        if type == QDoubleSpinBox:
            input.setRange(-1000000, 1000000)
            if id == "duration":
                input.setRange(8,  self.elGlobal["endFrame"])

            if id == "delay":
                input.setRange(0,  self.elGlobal["endFrame"])
            else:
                input.setRange(-1000000, 1000000)

        if type == QDoubleSpinBox or type == QSpinBox:
            input.setButtonSymbols(QAbstractSpinBox.NoButtons)
            input.setAlignment(Qt.AlignCenter)
            input.valueChanged.connect(lambda e: self.updateProperty(e, id))

        if type == QCheckBox:  # RELATIVE CHECKBOX
            input.setChecked(False)
            input.stateChanged.connect(
                lambda x:  self.updateProperty(True if x == 2 else False, id))

        if optionalArray:  # theres an array so lets use it
            input.addItems(optionalArray)
            if id == "easeType":
                input.currentIndexChanged.connect(
                    (lambda e: self.updateProperty(self.__easeTypes[e], id)))

            if id == "inOut":
                input.currentIndexChanged.connect(
                    (lambda e: self.updateProperty(self.__easeInOut[e], id)))
        if type == QLabel:  # SPACER
            heading.setText('')
            input.setMinimumHeight(26)
        input.setDisabled(True)  # disable on launch

        if id == "loops" or id == "loop_delay" or id == "relative":  # LUCKY  , WILL MAKE WORK IN FUTURE
            heading.hide()
            input.hide()
        #input.setMaximumWidth(83)
        if id == "atprops_0":
            heading.setText("Overshoot")
        if id == "atprops_1":
            heading.setText("Amplitute")
       # self.setTabOrder(input, b)
        layout.addWidget(heading, 2)
        layout.addWidget(input, 8)

        self.elGlobal["propertiesWidgets"][id] = input

        return layout

    def updateProperty(self, event, id):
        bArr = self.elGlobal["elBoxes"]
        for b in bArr:
            if b.highlighted == True:
                if event != b.exportables[id]:  # new info
                    """
                    if duration or delay
                    1: reset frames for the current position to clean
                    2: update property
                    3: fill the new frames that location will take
                    4: visually update
                    """
                    if id == "duration" or id == "delay":
                        # makes a function out of id
                        self.elGlobal["elTweenLayout"].addFrames(
                            b, b.track, b.subTrack)
                        if id == "duration":
                            b.duration(event)
                        if id == "delay":
                            b.delay(event)

                        self.elGlobal["elTweenLayout"].removeFrames(
                            b, b.track, b.subTrack)
                        b.prepareGeometryChange()
                        b.update()
                    else:

                        b.updateExportable(id, event)

                break
        if not self.elGlobal["dragging"]:
            exportTool(self.elGlobal["elTweenLayout"])

        #Add visual guide something == different
        startValue = (self.elGlobal["tweenStartValues"][id]["value"])
       # print(self)
        bar = self.parameters[id].itemAt(1).widget()
        isSame = None
        if hasattr(bar, 'currentText'):
           isSame = startValue == str(bar.currentText())
        else:
            value = None
            if type(bar) == QCheckBox:
                value = bar.isChecked()
            else:
                value = bar.value()
            isSame = abs(startValue - value)  # accurate way to compare
        if isSame:
            bar.setStyleSheet(self.CSS()["layout"]["roundedButtonHighlighted"])
        else:
            bar.setStyleSheet(self.CSS()["layout"]["roundedButton"])

 ######  ########    ###    ########  ########
##    ##    ##      ## ##   ##     ##    ##
##          ##     ##   ##  ##     ##    ##
 ######     ##    ##     ## ########     ##
      ##    ##    ######### ##   ##      ##
##    ##    ##    ##     ## ##    ##     ##
 ######     ##    ##     ## ##     ##    ##

    def mainResize(self, event, ):
        pass

    def createLayout(self):
        self._setupGlobals()
        #create the main layout
        mainLayout = QVBoxLayout()
        mainLayout.setMargin(0)
        r = self.elGlobal["layoutRatios"]
        mainLayout.addLayout(self.topLayout())

        self.elGlobal["elTweenLayout"] = elTweenLayoutidget(self)
        self.elGlobal["elTweenLayout"].size.setHeight(
            self.elGlobal["timelineHeightPX"])

        self.elGlobal["elTweenLayout"].setLayout(mainLayout)
        self.elGlobal["elTweenLayout"].setSizePolicy(
            QSizePolicy.Preferred, QSizePolicy.Preferred)
        mainLayout.addLayout(self.drawingSceneLayout(),
                             r["drawingSceneLayout"])

        mainLayout.addLayout(self.TabsBar())
        mainLayout.addLayout(self.About())

       # self.sortPropertiesTabbing()
        #add scrubber listner
        hou.playbar.addEventCallback(self.elGlobal["elTweenLayout"].scrubEvent)
        #import prev node data
        #self.importTool()
        return self.elGlobal["elTweenLayout"]

    def About(self):
        selfLayout = QHBoxLayout()
        thisgoodBoyText = QLabel(
            '<a href="https://thisgoodboy.com/" style="color:white">By Lucky Dee</a>')
        thisgoodBoyText.setOpenExternalLinks(True)

        trashButton = QPushButton('', self)
        trashButton.setFixedSize(50, 50)
        logoImagePath = os.path.join(os.path.dirname(
            __file__), "images/logo.png")

        trashButton.setIcon(QIcon(logoImagePath))
        trashButton.setIconSize(QSize(50, 50))
        trashButton.setStyleSheet("border: none;")
        trashButton.clicked.connect(self.AboutSite)
        selfLayout.addWidget(thisgoodBoyText, 0)
        selfLayout.addWidget(trashButton, 0)
        selfLayout.setAlignment(Qt.AlignRight)
        return selfLayout

    def AboutSite(self):
        webbrowser.open('https://thisgoodboy.com/')
    ##MOUSE EVENTS - LAYOUT

    def updatePanOffsetX(self, newPanOffset):
        self.elGlobal['viewPanOffsetX'] = newPanOffset


#### ##     ## ########   #######  ########  ########
 ##  ###   ### ##     ## ##     ## ##     ##    ##
 ##  #### #### ##     ## ##     ## ##     ##    ##
 ##  ## ### ## ########  ##     ## ########     ##
 ##  ##     ## ##        ##     ## ##   ##      ##
 ##  ##     ## ##        ##     ## ##    ##     ##
#### ##     ## ##         #######  ##     ##    ##


    def highlightLastBox(self):
        boxes = self.elGlobal["elBoxes"]
        if len(boxes) > 0:  # there are other boxes to delete still! point at it next
            lastBox = boxes[len(boxes)-1]
            lastBox.setHighlight(True)
            self.elGlobal["currentBoxSelected"] = lastBox
            self.elGlobal["trashBtn"].show()
            self.elGlobal["trashBtnFiller"].hide()
            self.elGlobal["shadowBox"].show()
            lastBox.attachShadow()

        else:  # no boxes left, hide trash icon
            self.elGlobal["shadowBox"].hide()
            self.elGlobal["trashBtn"].hide()
            self.elGlobal["trashBtnFiller"].show()

    def deleteBox(self):
        #performs a hell of a lot better when its not constantly playing too
        if hou.playbar.isPlaying():
            hou.playbar.stop()

        self.elGlobal["shadowBox"].hide()
        box = self.elGlobal["currentBoxSelected"]
        if box:  # why make new function when we can reuse the built in one : )
            box.delete(self.elGlobal["elTweenLayout"])
            exportTool(self)
            self.highlightLastBox()

    def deleteAll(self):
        for item in self.elGlobal["scene"].items():
            if item in self.elGlobal["elBoxes"]:
                self.elGlobal["scene"].removeItem(item)
        #clear objects
        self.elGlobal["elBoxes"] = []

        #reset timelines
        self.elGlobal["subTimelines"] = [[], [], []],  [
            [], [], []],  [[], [], []],  [[], [], []]

        for t in range(self.elGlobal["tracks"]):
            for i in range(self.elGlobal["frames"]):
                #create overal list for each prop
                #create xyz list for each prop
                self.elGlobal["subTimelines"][t][0].append(i)
                self.elGlobal["subTimelines"][t][1].append(i)
                self.elGlobal["subTimelines"][t][2].append(i)
        #delete all nodes

    def importTool(self):
        #delete all living child nodes
        self.deleteAll()

        str_data = self.elGlobal["node"].userData("boxExportables")
        if str_data != None:
            rawJSON = json.loads(
                self.elGlobal["node"].userData("boxExportables"))
            #populate new data
            for tween in rawJSON:
                track = rawJSON[tween]["track"]
                subTrack = rawJSON[tween]["subTrack"]
                #visuallly import tweens
                box = self.elGlobal["elTweenLayout"].addTweenVisual(
                    track, subTrack)  # import mode
                for key in rawJSON[tween]:
                    value = rawJSON[tween][key]
                    box.exportables[key] = value
                box.delay(box.exportables["delay"]*hou.fps())
                box.duration(box.exportables["duration"]*hou.fps())

                #fill their respected timelines
                self.elGlobal["elTweenLayout"].removeFrames(
                    box, track, subTrack)
            #     box.setHighlight(False)

    ##EXPORT DATA

    ##TEMP LANDING PAGE

    def _serve_temp_landing_page(self):
        widget = QtWidgets.QLabel('Hello World!')
        return widget

    def getTimelineScale(self):

        bestLenght = self.elGlobal["optimal_timeline_length"] * hou.fps()
        currentLength = hou.playbar.frameRange(
        )[1] - hou.playbar.frameRange()[0]-1
        boxZoomFactor = self.elGlobal["boxZoomFactor"]
        lenScale = bestLenght/currentLength * (boxZoomFactor)
        return lenScale


######## ##          ##          ###    ##    ##  #######  ##     ## ########
   ##    ##          ##         ## ##    ##  ##  ##     ## ##     ##    ##
   ##    ##          ##        ##   ##    ####   ##     ## ##     ##    ##
   ##    ##          ##       ##     ##    ##    ##     ## ##     ##    ##
   ##    ##          ##       #########    ##    ##     ## ##     ##    ##
   ##    ##          ##       ##     ##    ##    ##     ## ##     ##    ##
   ##    ########    ######## ##     ##    ##     #######   #######     ##
class elTweenLayoutidget(QWidget):
    size = QSize(600, 600)
    settings = gen_object()
    settings.startFrame = 0
    node = None

    def __init__(self, eltween):
        self.mainResize = eltween.mainResize
        self.elGlobal = eltween.elGlobal
        self.parameters = eltween.parameters
        tracks = self.elGlobal["tracks"]
        #generate object tracker from N tracks
        self.elGlobal["subTimelines"] = [[], [], []], [
            [], [], []], [[], [], []], [[], [], []]
        self.elGlobal["startFrame"] = hou.playbar.frameRange()[0]-1
        self.elGlobal["endFrame"] = hou.playbar.frameRange()[1]
        #we should get this made asap
        self.elGlobal["frames"] = int(
            self.elGlobal["endFrame"] - self.elGlobal["startFrame"])
        for t in range(tracks):
            for i in range(self.elGlobal["frames"]):
                self.elGlobal["subTimelines"][t][0].append(i)
                self.elGlobal["subTimelines"][t][1].append(i)
                self.elGlobal["subTimelines"][t][2].append(i)
        super(elTweenLayoutidget, self).__init__()

    def resizeEvent(self, event):

        if not self.size:
            self.size = event.size()

            self.updateSettings()

        self.size = event.size()
        if self.elGlobal["view"]:  # if youve hooked the graphics view in resize it
            self.mainResize(event)
            buttonSizeWidth = self.elGlobal["buttonSizes"]["leftSideButtons"].width(
            )
            #resize stage, view and definitions
            height = self.elGlobal["timelineHeightPX"]*self.elGlobal["tracks"]
            self.elGlobal["view"].setFixedSize(
                self.size.width() - (buttonSizeWidth*2), height)
            self.elGlobal["size"][0] = (
                self.size.width() - (buttonSizeWidth*2))
            self.elGlobal["scene"].sceneRect().setWidth(
                self.size.width() - (buttonSizeWidth*2))
            self.updateSettings()

            #we all the frames are still accurate but the widths changed so we run a updater once
            #to update the physical look
        self.checkSettings()
        #move and resize the shadow to the last selected box
        for b in self.elGlobal["elBoxes"]:
            if b.highlighted:
                newSize = QRectF(b.boundingRect())
                b.attachShadow(newSize)
     ######   ######  ########  ##     ## ########
    ##    ## ##    ## ##     ## ##     ## ##     ##
    ##       ##       ##     ## ##     ## ##     ##
     ######  ##       ########  ##     ## ########
        ## ##       ##   ##   ##     ## ##     ##
    ##    ## ##    ## ##    ##  ##     ## ##     ##
     ######   ######  ##     ##  #######  ########

    def scrubEvent(self, event, currentFrame):
       length = (self.elGlobal["frames"]-1) / self.elGlobal["fps"]
       newPos = self.elGlobal["timeline_width"] * hou.time()/length
       self.elGlobal["objectsOnStage"].verticalLine.setX(int(newPos))
       self.elGlobal["objectsOnStage"].edgeLine.setZValue(21)
       self.checkSettings()

    def addTween(self, track, importMode=False, subTrack=-1):
        trackX = self.elGlobal["subTimelines"][track][0]
        trackY = self.elGlobal["subTimelines"][track][1]
        trackZ = self.elGlobal["subTimelines"][track][2]
        framecount = self.elGlobal["frames"]
        if subTrack > -1:  # its a sub tween so check against sub timelines isntead
            tl_track = self.elGlobal["subTimelines"][track][subTrack]
        box = None
        freeI = 0
        minFreeFrames = self.elGlobal["default_tween_length"]-1
        for i in range(framecount):
            if freeI == minFreeFrames:
                #available frame
                box = self.addTweenVisual(track, subTrack)
                box.delay(i-minFreeFrames)
                # remove from available spaces list
                self.removeFrames(box, track, subTrack)
                self.elGlobal["currentBoxSelected"] = box
                box.attachShadow()
                break
            #SUB TRACK CHECK
            if subTrack != -1:
                #check only the current subtrack
                if tl_track[i] != -1:  # start checking for space
                    freeI += 1
            #MAIN TRACK CHECK
            elif subTrack == -1 and trackX[i] != -1 and trackY[i] != -1 and trackZ[i] != -1:
                #this == a main track so check if any of the 3 subtracks have something in them
                freeI += 1
            else:  # if something shows up reset the counter
                freeI = 0
            if(i == framecount-1):
                #if we got to end of array then theres no empty space
                hou.ui.displayMessage(
                    "No space available", help="Try clearing some tweens on this track!")
        if importMode == False:
            exportTool(self)

        #print(tl_track, track ,subTrack)
        if box:
            self.elGlobal["currentBoxSelected"] = box
            return box

    ########  ##     ## ######## ########  #######  ##    ##    ######## ##      ## ######## ######## ##    ##
    ##     ## ##     ##    ##       ##    ##     ## ###   ##       ##    ##  ##  ## ##       ##       ###   ##
    ##     ## ##     ##    ##       ##    ##     ## ####  ##       ##    ##  ##  ## ##       ##       ####  ##
    ########  ##     ##    ##       ##    ##     ## ## ## ##       ##    ##  ##  ## ######   ######   ## ## ##
    ##     ## ##     ##    ##       ##    ##     ## ##  ####       ##    ##  ##  ## ##       ##       ##  ####
    ##     ## ##     ##    ##       ##    ##     ## ##   ###       ##    ##  ##  ## ##       ##       ##   ###
    ########   #######     ##       ##     #######  ##    ##       ##     ###  ###  ######## ######## ##    ##
    def addTweenVisual(self, track, subTrack):

        box = draggableBox(None)
        box.exportables["track"] = track
        box.exportables["subTrack"] = subTrack
        box.exportables["duration"] = self.elGlobal["startFrame"] + \
            self.elGlobal["default_tween_length"]

        # delay doesnt matter its gonna get changed in addTween
        box.exportables["delay"] = 0
        box.addGlobals(self)
        box.info()

        self.elGlobal["scene"].addItem(box)

        self.elGlobal["elBoxes"].append(box)
        #highlights current box and links it to properties panel
        for b in self.elGlobal["elBoxes"]:
            if b == box:
                b.setHighlight(True)
                #b.update()

            else:
                pass
                b.setHighlight(False)
        return box

    def checkSettings(self):
        firstFrameChange = self.elGlobal["startFrame"] != hou.playbar.frameRange()[
                                                                                 0]-1
        lastFrameChange = self.elGlobal["endFrame"] != hou.playbar.frameRange()[
                                                                              1]
        fpsChange = self.elGlobal["fps"] != hou.fps()

        if firstFrameChange or lastFrameChange or fpsChange:
            self.updateSettings()
            self.elGlobal["view"].resize(self.size)

    def addFrames(self, box, track, subTrack):
        #subtrack should be 0, 1, 2 (xyz)
        delay = int(box.exportables["delay"])
        for i in range(int(box.exportables["duration"])):
            if subTrack > -1:  # its a sub track so fill just that
                self.elGlobal["subTimelines"][track][subTrack][delay+i] = delay+i
            else:  # its a main track so fill all sub tracks
                self.elGlobal["subTimelines"][track][0][delay+i] = delay+i
                self.elGlobal["subTimelines"][track][1][delay+i] = delay+i
                self.elGlobal["subTimelines"][track][2][delay+i] = delay+i

        #print('adding frames', self.elGlobal["subTimelines"][track][1])
            #print('adding frames', self.elGlobal["subTimelines"][track][1])
            #print('adding frames', self.elGlobal["subTimelines"][track][2])
    def removeFrames(self, box, track, subTrack):
       # print("call from", inspect.stack()[1][3])

        delay = int(box.exportables["delay"])
        duration = int(box.exportables["duration"])
        for i in range(int(box.exportables["duration"])):
            if subTrack > -1:  # its a sub track so fill just that
                self.elGlobal["subTimelines"][track][subTrack][delay+i] = -1

            else:  # its a main track so fill all sub tracks
                self.elGlobal["subTimelines"][track][0][delay+i] = -1
                self.elGlobal["subTimelines"][track][1][delay+i] = -1
                self.elGlobal["subTimelines"][track][2][delay+i] = -1

           #print('remving frames', self.elGlobal["subTimelines"][track][1])
           #print('remving frames', self.elGlobal["subTimelines"][track][2])

    def updateSettings(self):
        self.elGlobal["startFrame"] = hou.playbar.frameRange()[0]-1
        self.elGlobal["endFrame"] = hou.playbar.frameRange()[1]
        lastFrames = self.elGlobal["frames"]

        currentFrames = int(hou.playbar.frameRange()[
                            1]-hou.playbar.frameRange()[0]+1)

        currentTLLenght = len(self.elGlobal["subTimelines"][0][0])
        newFrames = currentFrames-currentTLLenght

       # newFrames = self.elGlobal["frames"]

        #only add if there are more frames now, dont wanna lose any info
        if newFrames > 0:
            #loop over only the new frames
            for t in range(newFrames):
                for track in range(4):
                    self.elGlobal["subTimelines"][track][0].append(
                        currentTLLenght+t)
                    self.elGlobal["subTimelines"][track][1].append(
                        currentTLLenght+t)
                    self.elGlobal["subTimelines"][track][2].append(
                        currentTLLenght+t)

        self.elGlobal["frames"] = currentFrames

        self.elGlobal["fps"] = hou.fps()
        self.elGlobal["scene_len"] = self.elGlobal["frames"] / \
            self.elGlobal["fps"]

        self.elGlobal["timeline_width"] = self.elGlobal["size"][0]

        self.elGlobal["default_tween_pixels"] = self.elGlobal["timeline_width"] / \
            self.elGlobal["scene_len"] * \
            self.elGlobal["default_tween_length"] / \
            hou.fps()  # TEMP , DELETE THS /2
        self.elGlobal["scene"].setSceneRect(
            0, 0, self.elGlobal["timeline_width"], self.elGlobal["timeline_width"])
        self.elGlobal["timeline_height"] = self.size.height() / \
            self.elGlobal["tracks"]

        #we all the frames are still accurate but the widths changed so we run a updater once
        #to update the physical look
        for bar in self.elGlobal["elBoxes"]:
            bar.setX(bar.exportables["delay"])
            bar.duration(bar.exportables["duration"])
            if bar.highlighted:
                newSize = QRectF(bar.boundingRect())
                bar.attachShadow(newSize)
            #Justification for geo update:
            #timeline == being rescaled so we have to somehow update the bounding box of each box
            bar.prepareGeometryChange()
            bar.update()


######## #### ##     ## ######## ##       #### ##    ## ########
   ##     ##  ###   ### ##       ##        ##  ###   ## ##
   ##     ##  #### #### ##       ##        ##  ####  ## ##
   ##     ##  ## ### ## ######   ##        ##  ## ## ## ######
   ##     ##  ##     ## ##       ##        ##  ##  #### ##
   ##     ##  ##     ## ##       ##        ##  ##   ### ##
   ##    #### ##     ## ######## ######## #### ##    ## ########
class elTimeline(QGraphicsView):
    __leftClickDown = False
    __boxSelected = False
    __mode = 0  # navigation mode
    DragXStartPos = None

    def __init__(self, parent=None):
        QGraphicsView.__init__(self, parent)

        #used for zoom in and out buttons
        self.zoomInFactor = 1.25
        self.zoomOutFactor = 1 / self.zoomInFactor
        self.oldPos = None
        self.setOptimizationFlags(QGraphicsView.DontAdjustForAntialiasing
                                  or QGraphicsView.DontClipPainter
                                  or QGraphicsView.DontSavePainterState)

    def addGlobals(self, eltween):
        self.elGlobal = eltween.elGlobal
        self.__mode = self.elGlobal["navigationMode"]

    def setup(self, size):
        self.resetMatrix()

    def hideAllProps(self):
        self.elGlobal["shadowBox"].hide()
        self.elGlobal["tabFrame"].hide()
        for frame in self.elGlobal["Tab1Frames"]:
            not_resize = frame.sizePolicy()
            not_resize.setRetainSizeWhenHidden(True)
            frame.setSizePolicy(not_resize)
        for frame in self.elGlobal["TabFrames"]:
            frame.hide()

    def showAllProps(self):
        self.elGlobal["tabFrame"].show()
        for frame in self.elGlobal["Tab1Frames"]:
            not_resize = frame.sizePolicy()
            not_resize.setRetainSizeWhenHidden(False)
            frame.setSizePolicy(not_resize)
            frame.show()

        for t in range(3):
            self.elGlobal["tabButtons"][t].setStyleSheet(
                self.elGlobal["CSS"]["tabButtonOff"][t])

        self.elGlobal["tabButtons"][0].setStyleSheet(
            self.elGlobal["CSS"]["tabButtonOn"][0])

    def mousePressEvent(self, event):

        self.__mode = self.elGlobal["navigationMode"]
        self.setTransformationAnchor(QGraphicsView.NoAnchor)
        self.setResizeAnchor(QGraphicsView.NoAnchor)
        super(QGraphicsView, self).mousePressEvent(event)

        if event.button() == Qt.LeftButton:
            self.startPos = self.mapToScene(event.pos())
            pos = (event.pos())
            item = self.itemAt(pos.x(), pos.y())
            isBox = isinstance(item, draggableBox)
            if not isBox:
                self.hideAllProps()
            else:
                self.showAllProps()

            self.__leftClickDown = True
            if self.__mode == 0:
                self.boxPress(event)
            elif self.__mode == 1 or self.__mode == 2:  # ZOOM
                self.zoomStage(event)

    def mouseMoveEvent(self, event):
        #self.translate(event.pos().x(), event.pos().y())
        if self.__leftClickDown:
            if self.__mode == 0:
                self.boxMove(event)
            elif self.__mode == 3:  # PAN
                self.panStage(event)

    def mouseReleaseEvent(self, event):
        self.startPos = None
        if self.__mode == 0:
            self.boxRelease(event)

        #EXECUTE LAST
        self.__leftClickDown = False

    def boxPress(self, event):

        pos = (event.pos())
        item = self.itemAt(pos.x(), pos.y())
        if item in self.elGlobal["elBoxes"]:  # clicked on a box
            self.__boxSelected = item
            self.elGlobal["currentBoxSelected"] = item
            self.__boxSelected.press(
                event, 1, self.elGlobal["elTweenLayout"])
        #set highlights
        for box in self.elGlobal["elBoxes"]:
            if box == self.__boxSelected:

                box.setHighlight(True)
            else:
                box.setHighlight(False)
               # parameter_props[prop].setDisabled(True)

    def boxMove(self, event):  # moving a box

        if self.__boxSelected:
            self.__boxSelected.move(event, 1, self.elGlobal["elTweenLayout"])

    def boxRelease(self, event):  # letting go of a box
        if self.__boxSelected:
            self.__boxSelected.release(
                event, 1, self.elGlobal["elTweenLayout"])
        #EXECUTE LAST
        self.__boxSelected = None

    def zoomStage(self, event):

        if self.__mode == 1:
            self.zoomFactor = self.zoomInFactor
        elif self.__mode == 2:
            self.zoomFactor = self.zoomOutFactor
        self.scale(self.zoomFactor, 1)
        self.elGlobal["currentZoomLevel"] *= self.zoomFactor
        newPos = self.mapToScene(event.pos())
        delta = newPos - self.startPos
        self.translate(delta.x(), 0)
        sceneX = self.mapToScene(self.rect()).boundingRect().x()
        self.elGlobal["currentOffetX"] = sceneX

    def panStage(self, event):
        delta = self.startPos - event.pos()
        transform = self.transform()*self.elGlobal["currentZoomLevel"]
        deltaX = delta.x() * self.elGlobal["currentZoomLevel"]/3
        self.translate(deltaX, 0)
        sceneX = self.mapToScene(self.rect()).boundingRect().x()
        self.elGlobal["currentOffetX"] = sceneX
        self.startPos = event.pos()


########  ##     ## ######## ########  #######  ##    ##  ######
##     ## ##     ##    ##       ##    ##     ## ###   ## ##    ##
##     ## ##     ##    ##       ##    ##     ## ####  ## ##
########  ##     ##    ##       ##    ##     ## ## ## ##  ######
##     ## ##     ##    ##       ##    ##     ## ##  ####       ##
##     ## ##     ##    ##       ##    ##     ## ##   ### ##    ##
########   #######     ##       ##     #######  ##    ##  ######
class addFunctionButton(QWidget):
    mode = 0

    def __init__(self, eltween):
        QWidget.__init__(self, eltween)
        self.elGlobal = eltween.elGlobal

        self.button = QPushButton('', self)
        self.button.setStyleSheet("border: none;")
        self.button.setFixedSize(
            self.elGlobal["timelineHeightPX"], self.elGlobal["timelineHeightPX"])
      #  self.button.setFixedHeight(self.elGlobal["timelineHeightPX"])
        self.type = None
        self.button.clicked.connect(self.clicked)

    def setMode(self, mode):
        self.mode = mode

    def addImage(self, numb, size):

        icon_path = os.path.join(os.path.dirname(
            __file__), "images/right_icon_"+str(numb+1)+".png")
        self.button.setIcon(QIcon(icon_path))
        self.button.setIconSize(size)
        self.button.setFixedSize(size)
        self.setFixedSize(size)

    def mouseMoveEvent(self, event):
       # if event.pos().x() > self.width()-10 or event.pos().y() > self.height()-10\
        #  or event.pos().x() < 10 or event.pos().y() < 10:
        pass

    def clicked(self):

        self.elGlobal["navigationMode"] = self.mode
        self.setCursor(self.mode)
        self.doAnim()

    def setCursor(self, mode):
        if mode == 0:
            self.elGlobal["view"].setCursor(
                QCursor(Qt.ArrowCursor))
        else:
            curosr_path = os.path.join(os.path.dirname(
                __file__), "images/mode_"+str(mode)+".png")
            pixmap = QPixmap(curosr_path)
            pixmapScaled = pixmap.scaled(QSize(30, 30), Qt.KeepAspectRatio)

            cursor = QCursor(pixmapScaled, -1, -1)
            self.elGlobal["view"].setCursor(cursor)

    def doAnim(self):
        startX = self.pos().x()
        startY = self.pos().y()
        self.anim = QPropertyAnimation(self, b"pos")
        self.anim.setDuration(300)
        self.anim.setKeyValueAt(0.1, QPoint(startX, startY-10))
        self.anim.setKeyValueAt(0.4, QPoint(startX, startY))
        self.anim.start()


class addTabButton(QPushButton):
    id = -1

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.clicked.connect(self.tap)

    def setup(self, elGlobal, id):
        self.id = id
        self.elGlobal = elGlobal

    def tap(self):
        tabMenus = self.elGlobal["TabFrames"]
        for t in range(len(tabMenus)):
            self.elGlobal["tabButtons"][t].setStyleSheet(
                self.elGlobal["CSS"]["tabButtonOff"][t])
            tabMenus[t].hide()
            tabMenus[self.id].show()
        self.setStyleSheet(self.elGlobal["CSS"]["tabButtonOn"][self.id])


class addSubTweenButton(QPushButton):
    id = -1
    prop = -1
    cssOFF = None
    cssON = None
    BorderColor = None
    xyz = -1
    index = -1

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.clicked.connect(self.tap)

    def setup(self, elGlobal, id):
        self.id = id

        self.elGlobal = elGlobal
        if self.id < 3:
            self.prop = 0
        elif self.id < 6:
            self.prop = 1
        elif self.id < 9:
            self.prop = 2
        else:
            self.prop = 3  # im too dumb to think of a modulo for this
        onCSS = "border: 15px solid #"
        offCSS = "background-color: #"
        self.BorderColor = elGlobal["CSS"]["subTweenColors"][self.id]
        self.cssON = onCSS+self.BorderColor+";" + elGlobal["CSS"]["subTweenOn"]
        self.cssOFF = offCSS+self.BorderColor + \
            ";" + elGlobal["CSS"]["subTweenOff"]
        self.setStyleSheet(self.cssOFF)
        self.xyz = ["X", "Y", "Z"][self.id % 3]
        self.index = [0, 1, 2][self.id % 3]
        self.setText(self.xyz)
        self.setIconSize(elGlobal["buttonSizes"]["rightSideButtons"])
        self.setFixedSize(elGlobal["buttonSizes"]["rightSideButtons"])
        self.setFixedHeight(self.height()/3)

    def enterEvent(self, event):
        self.setStyleSheet(self.cssON)

    def leaveEvent(self, event):
        self.setStyleSheet(self.cssOFF)

    def tap(self):
        self.elGlobal["navigationMode"] = 0
        self.elGlobal["elTweenLayout"].addTween(self.prop, False, self.index)


########  ########     ###     ######      ########   #######  ##     ##
##     ## ##     ##   ## ##   ##    ##     ##     ## ##     ##  ##   ##
##     ## ##     ##  ##   ##  ##           ##     ## ##     ##   ## ##
##     ## ########  ##     ## ##   ####    ########  ##     ##    ###
##     ## ##   ##   ######### ##    ##     ##     ## ##     ##   ## ##
##     ## ##    ##  ##     ## ##    ##     ##     ## ##     ##  ##   ##
########  ##     ## ##     ##  ######      ########   #######  ##     ##
class draggableBox(QGraphicsItem):
    __mousePosStart = QPoint(0, 0)
    __minWidth = 40  # probably should be a hard number just gotta see which
    __mouseDownOffsetFromCenter = None
    __edgeSide = 0
    __colorBorderNormal = QColor(0, 0, 0, 90)
    __colorBorder = QColor(0, 0, 0, 90)
    __neighbours = []
    __totalFrames = 0
    __track = -1
    highlighted = False
    __innerColor = None
    exportables = None
    main = None
    __subTrack = None  # start seeing myself as the full sized track
    subTrack = None  # exposed version of __subTrack

    def info(self):
        self.__width = self.exportables["duration"] / \
            self.elGlobal["frames"] * self.elGlobal["timeline_width"]
        self.setCacheMode(QGraphicsItem.DeviceCoordinateCache)

        #colors
        css = self.elGlobal["CSS"]["draggableBox"]
        self.__innerColor = QColor(css["colorFill"][self.exportables["track"]])
        self.__outerColor = QColor(
            css["colorStroke"][self.exportables["track"]])
        self.__nibColor = self.__outerColor

        self.__boundScalePercent = 0  # used for clipping so the bounds have a bit of space
        self.__edgeRadius = 16  # how close to the edge before youre reshaping the node
        self.__defaultZ = 10
        self.__dragZ = 50
        self.__posX = None
        self.__drag = False
        #from take 3
        self.__track = self.exportables["track"]
        self.__subTrack = self.exportables["subTrack"]
        self.subTrack = self.exportables["subTrack"]

        self.curHeight = self.elGlobal["timelineHeightPX"]
        ySubOffset = 0
        if self.subTrack > -1:
            self.curHeight /= 3
            ySubOffset = self.curHeight*self.subTrack

        #y based out of what track youre in plus an offset if its a subtrack
        self.__pos = QPoint(0, 0)
        self.__pos.setY(
            self.elGlobal["timelineHeightPX"]*self.exportables["track"]+ySubOffset)

        self.__colorBorderNormal = self.__outerColor
        self.__colorBorder = self.__colorBorderNormal
        #scale should start at 1, everything else 0
        self.exportables["x"] = 0 if self.__track != 2 else 1
        self.exportables["y"] = 0 if self.__track != 2 else 1
        self.exportables["z"] = 0 if self.__track != 2 else 1
        self.exportables["relative"] = False
        self.exportables["easeType"] = "Linear"
        self.exportables["inOut"] = "Out"
        self.exportables["atprops_0"] = 0.7
        self.exportables["atprops_1"] = 0.4
        self.exportables["loops"] = 0
        self.exportables["loop_delay"] = 0
        self.exportables["stagger_x"] = 0
        self.exportables["stagger_y"] = 0
        self.exportables["stagger_z"] = 0
        self.exportables["pointStagger"] = 0
        self.exportables["pivot_x"] = 0
        self.exportables["pivot_y"] = 0
        self.exportables["pivot_z"] = 0

        self.setZValue(self.__defaultZ)

        self.hideNonRelativeProps()

    def __init__(self, parent, *args, **kwargs):
        self.highlighted = True
        self.exportables = {}  # unique for each object
        self.track = self.__track
        super(draggableBox, self).__init__()
        self.setAcceptHoverEvents(True)

    def addGlobals(self, eltween):
        self.elGlobal = eltween.elGlobal
        self.parameters = eltween.parameters
        self.panOffset = self.elGlobal['viewPanOffsetX']
        #self.setSubTrack()

    def setHighlight(self, on):

        #self.elGlobal["trashBtn"].hide()
        #self.elGlobal["trashBtnFiller"].show()
        if not on:

            self.highlighted = False
        else:
            self.highlighted = True
            # swaps focus of properties to currently selected box
            self.enablePropertiesPanel()

        self.prepareGeometryChange()
        self.update()

    def attachShadow(self, newSize=None):
        shadowYScale = 0.2
        self.elGlobal["shadowBox"].show()
        size = QRectF(self.boundingRect().x(), self.boundingRect().y(
        )+self.boundingRect().height(), self.boundingRect().width(), self.boundingRect().height())
        if newSize:
            size = newSize
        size.setY(self.boundingRect().y(
        )+self.boundingRect().height())
        size.setHeight(self.boundingRect().height()*shadowYScale)
        if self.__subTrack > -1:  # its a subtrack, dif height
            size.setHeight(self.boundingRect().height()*shadowYScale*2)
        self.elGlobal["shadowBox"].setRect(size)
        #self.setZValue(self.__dragZ)

    def boundingRect(self, newSize=None):

        #width =  self.__width if self.__startWidth == None else self.__startWidth
        return QRectF(self.__pos.x() - self.__width*self.__boundScalePercent*0.5, self.__pos.y(),
                      self.__width*(1+self.__boundScalePercent),
                      self.curHeight)

    def delay(self, amount=None):
        if amount != None:
            self.exportables["delay"] = amount
            if self.exportables["duration"]+self.exportables["delay"] > (float(self.elGlobal["frames"])):
                self.exportables["delay"] = float(
                    self.elGlobal["frames"]) - self.exportables["duration"]
            self.setX(self.exportables["delay"])
            self.prepareGeometryChange()
            self.update()

        return int(self.exportables["delay"])

    def setX(self, amount=None):
        if amount != None:
            frames = float(self.elGlobal["frames"])
            self.__pos.setX(float(amount)/(frames)
                            * self.elGlobal["scene"].width())
            self.exportables["delay"] = amount
        return int(self.exportables["delay"])
        self.update()

    def duration(self, amount=None):

        if amount != None:
            self.exportables["duration"] = amount
            if self.exportables["duration"]+self.exportables["delay"] > (float(self.elGlobal["frames"])):
                self.exportables["duration"] = float(
                    self.elGlobal["frames"]) - self.exportables["delay"]
            self.__width = (self.exportables["duration"]) / \
                (float(self.elGlobal["frames"])) * \
                self.elGlobal["scene"].width()

            #self.prepareGeometryChange()
            #self.update()
        return int(self.exportables["duration"])

    def delete(self, main):
        main.addFrames(self,  self.__track, self.__subTrack)
        #self.elGlobal["timeline_items"][self.__track].remove(self)
        self.elGlobal["elBoxes"].remove(self)
        self.elGlobal["scene"].removeItem(self)

    def updateFrames(self, main):
        main.updateFrames()

    def isBoxType(self):
        return True

    def paint(self, painter, option, widget):
        x = self.__pos.x()
        y = self.__pos.y()

        w = self.__width
        h = self.curHeight

        currentZoomLevel = self.elGlobal["currentZoomLevel"]
        bo = h*0.125  # box offset inner
        #Main Box
        painter.fillRect(x, y, w, h, QBrush(self.__colorBorder))
        offset = 6/currentZoomLevel
        #sub Box
        bX = x+offset
        bY = y+bo
        bW = w-offset*2
        bH = h - bo*2
        if self.__subTrack > -1:
            scaledOffset = 0.5
            bX = x+offset*scaledOffset
            bY = y+bo*scaledOffset
            bW = w-offset*scaledOffset*2
            bH = h - bo*2*scaledOffset
            sTColors = self.elGlobal["CSS"]["subTweenColors"]
            colorIndex = self.__track*3 + self.__subTrack
            self.__innerColor = QColor("#"+sTColors[colorIndex])
        painter.fillRect(bX, bY, bW, bH, QBrush(self.__innerColor))

        #nibs
        ho = h*0.15  # height offset
        o = offset*1.5
        s = 2.4  # scale
        if self.__subTrack > -1:  # tweaks in position for sub tweens
            o *= 0.75  # closeness to center
            ho *= 2.2  # height
        lNib_tl = QPoint(x+o, y+ho)
        lNib_tr = QPoint(x+o*s, y+ho)
        lNib_bl = QPoint(x+o, y+ho*s)

        rNib_tr = QPoint(x+w-offset*0.3-o, y+ho)
        rNib_tl = QPoint(x+w-offset*0.3-o*s, y+ho)
        rNib_br = QPoint(x+w-offset*0.3-(+o), y+ho*s)

        nibDistance = (rNib_tl-lNib_tr).x()

        if nibDistance < 0:  # only show nibs if its not too small
            rNib_tl.setX(rNib_tl.x()-nibDistance)
            lNib_tr.setX(lNib_tr.x()+nibDistance)
            if rNib_tl.x() > rNib_tr.x():
                rNib_tl = rNib_tr
            if lNib_tr.x() < lNib_tl.x():
                lNib_tr = lNib_tl

        path = QPainterPath()
        path.moveTo(lNib_tl)  # top left
        path.lineTo(lNib_tr)  # top right
        path.lineTo(lNib_bl)  # bot left
        painter.fillPath(path, QBrush(self.__nibColor))
        path = QPainterPath()
        path.moveTo(rNib_tr)
        path.lineTo(rNib_tl)
        path.lineTo(rNib_br)
        painter.fillPath(path, QBrush(self.__nibColor))
       # painter.drawText( QPointF(self.__pos.x(), self.__pos.y()+10), "Hssssssdfsdfssfdsssssiya" )

    def alignToTL(self, event, zoomFactor, main, movingX):
        #TIMELINE INFO
        frames = float(self.elGlobal["frames"])
        stageW = self.elGlobal["timeline_width"]

        #SNAP X AND WIDTH TO NEAREST PPOSITION
        x = movingX
        boxW = self.boundingRect().width()
        closestFrame = int((x*(frames-1)) / stageW)  # get closest frame to x
        # get closest frame to the width
        Width = int(((boxW)*(frames)) / stageW)
        #keep in bounds
        if closestFrame < 0:
            closestFrame = 0
        if closestFrame > frames-Width:
            closestFrame = int(frames-Width)
            #if closestFrame > frames-Width and frames-closestFrame < minSizeToFrames:
        snapX = (closestFrame/frames) * stageW  # update so it SNAPs to it
        self.__pos.setX(snapX)  # snap to nearest frame
        self.prepareGeometryChange()
        self.update()
        boxW = self.boundingRect().width()   # update width
        XFrame = int((snapX*frames) / stageW)  # debug checking, not needed
        self.delay(XFrame)
        self.duration(Width)

    def enablePropertiesPanel(self):
        self.elGlobal["trashBtn"].show()
        self.elGlobal["trashBtnFiller"].hide()
        for p in self.parameters:
            if "spacer" not in p:
                widget = self.parameters[p].itemAt(1).widget()
                value = self.exportables[p]
                if type(widget) == QDoubleSpinBox:
                    widget.setValue(value)
                if type(widget) == QCheckBox:
                    widget.setChecked(value)
                if type(widget) == QComboBox:
                    index = widget.findText(value)
                    widget.setCurrentIndex(index)
                   # widget.setValue(value)
                widget.setEnabled(True)

    def updateExportable(self, exportable, value):
        self.exportables[str(exportable)] = value

    def hideNonRelativeProps(self):
        propXYZ = ["x", "y", "z"]
        for p in range(3):
            #first enable everything so it resets
            paramXYZ = self.parameters[propXYZ[p]]
            for i in range(paramXYZ.count()):
                paramXYZ.itemAt(i).widget().setHidden(False)

            if self.__subTrack > -1:  # Sub Track selected, #hide non active props
                if p != self.__subTrack:
                    for i in range(paramXYZ.count()):
                        paramXYZ.itemAt(i).widget().setHidden(True)

    def press(self, event, zoomFactor, main):

        self.elGlobal["dragging"] = True
        #DRAGGING INFO
        self.__drag = True
        #set neighbours to default z, push sected and shadow to front
        for n in self.elGlobal["elBoxes"]:
            n.setZValue(self.__defaultZ)

        self.setZValue(self.__dragZ)
        self.attachShadow()

        #creation of reference sizes
        self.__mousePosStart = self.mapToScene(event.pos())

        sf = (self.elGlobal["currentZoomLevel"])
        oX = self.elGlobal["currentOffetX"]
        self.__mousePos = self.__mousePosStart
        self.__mousePos.setX(self.__mousePos.x()/sf)
        self.__mouseDownOffset = (self.__mousePos.x()-(self.__pos.x()))

        #centering
        ##the difference between mouse and center

        tw = self.boundingRect().width()
        tx = self.boundingRect().x()
        c = tx + tw/2
        dfc = (self.__mousePos.x() - (c-oX))/tw*100
        sideSelectPercent = 30
        self.__edgeSide = 0
        if abs(dfc) > sideSelectPercent:
            if dfc > sideSelectPercent:
                self.__edgeSide = 1
            elif dfc < sideSelectPercent:
                self.__edgeSide = -1

        #used for dragging and for dragging only
        self.init_duration = self.duration()
        self.init_x = self.setX()
        self.init_x_PX = self.__mousePos.x()
        #clear out info for current frames so its 1,2,3, instead of -1(indicating taken)
        main.addFrames(self,  self.__track, self.__subTrack)
        #visual
        #fade out a bit for dragging
        #if sub track, hide other props
        self.hideNonRelativeProps()

    def move(self, event, zoomFactor, main):
        sf = (self.elGlobal["currentZoomLevel"])
        self.__mousePos = (self.mapToScene(event.pos()).x())/sf
        if self.__drag == True:
            self.__posX = self.__mousePos-self.__mouseDownOffset
            #DRAG

            if self.__edgeSide == 0:  # drag mode
                self.alignToTL(event, zoomFactor, main, self.__posX)

            else:
                dragFrame = int(math.floor(
                    (self.__mousePos-self.init_x_PX) / self.elGlobal["scene"].width()*float(self.elGlobal["frames"])))

                if self.__edgeSide == 1:  # Right side selected
                    # if self.init_x+self.duration()+dragFrame < float(self.elGlobal["frames"]):
                    self.duration(self.init_duration+dragFrame)
                    self.elGlobal["objectsOnStage"].edgeLine.setX(
                        self.__pos.x()+self.boundingRect().width())
                    self.elGlobal["objectsOnStage"].edgeLine.setZValue(21)
                    # RIGHT EDGE CAP
                    if self.init_duration+dragFrame + self.init_x > float(self.elGlobal["frames"]):
                        self.duration(
                            float(self.elGlobal["frames"]) - self.init_x)
                if self.__edgeSide == -1:  # left side selected
                    if self.init_duration-dragFrame > self.elGlobal["minimumFrames"]:
                        if(self.__posX < 0):
                            self.setX(0)
                        else:
                            self.setX(self.init_x+dragFrame)
                            self.duration(self.init_duration-dragFrame)

                            self.elGlobal["objectsOnStage"].edgeLine.setX(
                                self.__pos.x())
                            self.elGlobal["objectsOnStage"].edgeLine.setZValue(
                                21)
                # cap drag to min
                if self.duration() < self.elGlobal["minimumFrames"]:
                   self.duration(self.elGlobal["minimumFrames"])

            #     #VISUAL

            self.prepareGeometryChange()
            self.update()
            self.attachShadow()

    def release(self, event, zoomFactor, main):
        #mark frames on release as taken
        main.removeFrames(self,  self.__track, self.__subTrack)
        neighbours = self.elGlobal["elBoxes"]

        for n in neighbours:
            me = self.boundingRect()
            neighbour = n.boundingRect()
            collision = me.intersects(neighbour)

            if collision and self != n:  # take out self and check if collision
                #COLLISION STATE
                #OVERLAP
                overlap = me.intersected(neighbour)
                if overlap.width() >= self.__width:  # full overlap
                    #print('full overlap')
                    n.delete(main)
                else:  # partial overlap
                    sDel = self.exportables["delay"]
                    sDur = self.exportables["duration"]

                    nDel = n.exportables["delay"]
                    nDur = n.exportables["duration"]

                    ovarlapFrames = nDel+nDur-sDel
                    newDuration = nDur-ovarlapFrames

                    if sDel+sDur < nDel+nDur:  # Left side, adjust n pos
                        n.setX(sDel+sDur)
                        ovarlapFrames = int((sDel+sDur)-nDel)
                        newDuration = nDur-ovarlapFrames

                    # width adjust for left and right
                    n.duration(newDuration)
                    #justification: neighbour has to physically get smaller
                    # if too skiny blast it
                    n.prepareGeometryChange()
                    n.update()
                    if n.exportables["duration"] < self.elGlobal["minimumFrames"]:
                        #print("too small ,remove")
                        n.delete(main)

        #visual
       # self.setZValue(self.__defaultZ)
        #self.elGlobal["shadowBox"].setZValue(self.__defaultZ-1)
        self.prepareGeometryChange()
        self.update()
        self.elGlobal["objectsOnStage"].edgeLine.setX(0)

        #Properties Panel

        self.exportables["duration"] = self.duration()
        self.exportables["delay"] = self.setX()
        # re enable properties panel so duratin and delay can be updated
        self.enablePropertiesPanel()

        #Export
        exportTool(main)
        self.elGlobal["dragging"] = False

######## ##     ## ########   #######  ########  ########
##        ##   ##  ##     ## ##     ## ##     ##    ##
##         ## ##   ##     ## ##     ## ##     ##    ##
######      ###    ########  ##     ## ########     ##
##         ## ##   ##        ##     ## ##   ##      ##
##        ##   ##  ##        ##     ## ##    ##     ##
######## ##     ## ##         #######  ##     ##    ##


def exportTool(context):
    node = context.elGlobal["node"]
    #JSON
    JSON_elTweenSettings = {}
    boxes = context.elGlobal["elBoxes"]
    boxCount = len(boxes)
    timelineSnippet = []
    #HOUDINI
    #CLEAR OLD KIDS AND FIND START AND EXIT
    path = node.path()
    kids = node.children()
    subnet = node.node("addTweens")

    pOffset = hou.Vector2(0, 1)
    entryNode = None
    exitNode = None
    currentNodes = []
    leftOverNodes = []
    for k in subnet.children():
        if k.name() == "ENTRY":
            entryNode = k
        if k.name() == "EXIT":
            exitNode = k
        if "DYNA_" in k.name():
           leftOverNodes.append(k)
          # k.destroy()
    setupCode = []  # for use in merging vex
    for t in range(context.elGlobal["tracks"]):
        setupCode.append(
            hou.node(subnet.path()+'/el_tween_setup_CODE_'+str(t)))

    #HOUDINI PLUS JSON
    for i in range(boxCount):
        #For Json
        JSON_elTweenSettings["tween"+str(i)] = {}  # JSON
        mainString = ""

        #For Houdini

        #check if kid exists before adding it
        track = boxes[i].exportables["track"]
        newKidName = "DYNA_eltween_"+"track_"+str(track)+"_"+str(i)
        newKid = None
        for k in leftOverNodes:
            if newKidName in k.name():
                newKid = k
                leftOverNodes.remove(k)
                break

        if newKid == None:
            newKid = subnet.createNode("attribwrangle")
            newKid.setName(newKidName)

            position = hou.Vector2(0, -i)
            newKid.setPosition(position)
        LastNodeToTrack = entryNode
        if len(currentNodes) > 0:  # not the first thing on the chain
            LastNodeToTrack = currentNodes[len(currentNodes)-1]
        newKid.setInput(0, LastNodeToTrack, 0)
        if i == boxCount-1:  # lastNode
            exitNode.setInput(0, newKid)

        currentNodes.append(newKid)
        for e in boxes[i].exportables:
            prop = e
            value = boxes[i].exportables[e]

            if prop == "relative":
                if value == False:
                    value = 0
                if value == True:
                    value = 1
            if prop == "easeType" or prop == "inOut":
                value = '"'+value+'"'
            if prop == "delay" or prop == "duration":
                value /= hou.fps()

            snippet = prop+" = " + str(value)+";\n"
            mainString += snippet
            #JSON, delete the quotes so they dont show up in teh json

            if type(value) == str:
                value = value.replace('"', "")
            JSON_elTweenSettings["tween"
                                 + str(i)][prop] = value

        ##setup Vex , thanks ToadStorm for the script extractor!
        snippet = setupCode[track].evalParm(
            'snippet').split('/* SNIPPET */')
        newSnippet = "\n".join(
            [snippet[0], mainString, snippet[1]])
        newKid.parm("snippet").set(newSnippet)

        #FOR JSOn
        timelineSnippet.append(mainString)
    #JSON SAVING
    node.setUserData("boxExportables", json.dumps(JSON_elTweenSettings))
    #print("user data boxExportables")
    #print(node.userData("boxExportables"))
    #delete leftovers
    for k in leftOverNodes:
        k.destroy()
