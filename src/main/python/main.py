#!/usr/bin/env python

import sys
import math

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

# the following should not be happening and is some kind of scoping issue
# TODO: only import the shapes library once
# this is so we can call the functions
from shapes import *
# this is so we can scan the functions
import shapes

# an inspecting function that will allow us to get all functions in a file
# as a list
import inspect

import OpenGL.GL as gl


class Window(QWidget):

    def __init__(self):
        super(Window, self).__init__()

        self.glWidget = MakeGLWidget()

        # create each slider
        self.xSlider = self.createSlider()
        self.ySlider = self.createSlider()
        self.zSlider = self.createSlider()

        # connect a value changed listener to the sliders
        self.xSlider.valueChanged.connect(self.glWidget.setXRotation)
        self.glWidget.xRotationChanged.connect(self.xSlider.setValue)
        self.ySlider.valueChanged.connect(self.glWidget.setYRotation)
        self.glWidget.yRotationChanged.connect(self.ySlider.setValue)
        self.zSlider.valueChanged.connect(self.glWidget.setZRotation)
        self.glWidget.zRotationChanged.connect(self.zSlider.setValue)

        # create our main layout
        mainLayout = QHBoxLayout()
        mainLayout.addWidget(self.glWidget)

        # expand the glWidget to fill all available space
        self.glWidget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        # add in a vertical layout for all our controls
        controlBar = QVBoxLayout()

        # a horizontal layout for some check boxes
        checkBoxes = QHBoxLayout()

        # create an axes box and connect a state changed listener to the
        # glWidget
        self.axesCheckbox = self.makeCheckBox("Axes")
        self.axesCheckbox.setCheckState(Qt.Checked)
        self.axesCheckbox.stateChanged.connect(self.glWidget.toggleAxes)

        checkBoxes.addWidget(self.axesCheckbox)
        checkBoxes.addWidget(self.makeCheckBox("Orthographic"))
        controlBar.addLayout(checkBoxes)

        loadGlibButton = QPushButton("Load GLIB File")
        loadGlibButton.clicked.connect(self.glWidget.getGLIB)

        reloadGlibButton = QPushButton("Reload GLIB File")
        reloadGlibButton.clicked.connect(self.glWidget.loadGLIB)

        controlBar.addWidget(loadGlibButton)
        controlBar.addWidget(reloadGlibButton)
        controlBar.addWidget(self.xSlider)
        controlBar.addWidget(self.ySlider)
        controlBar.addWidget(self.zSlider)

        # add the vertical layout
        mainLayout.addLayout(controlBar)

        # set our main layout for the window
        self.setLayout(mainLayout)

        # set the starting values of the slider
        self.xSlider.setValue(292 * 16)
        self.ySlider.setValue(179 * 16)
        self.zSlider.setValue(44  * 16)

        self.setWindowTitle("glman")

    def makeCheckBox(self, label):
        checkBox = QCheckBox(label)
        # make the text white
        checkBox.setStyleSheet("""
            QCheckBox {
               border: none;
               color: white;
            }""")
        return checkBox

    def createSlider(self):
        slider = QSlider(Qt.Horizontal)

        slider.setRange(0, 360 * 16)
        slider.setSingleStep(16)
        slider.setPageStep(15 * 16)

        return slider


class MakeGLWidget(QOpenGLWidget):
    # these are signals that are emitted to make connections
    xRotationChanged = pyqtSignal(int)
    yRotationChanged = pyqtSignal(int)
    zRotationChanged = pyqtSignal(int)

    def __init__(self, parent=None):
        super(MakeGLWidget, self).__init__(parent)

        self.axes = 0
        self.xRot = 0
        self.yRot = 0
        self.zRot = 0
        self.axesOn = 2

        self.programOn = False

        self.lastPos = QPoint()

        self.glibFile = ""
        self.glibContents = ""

        # get all functions in the shapes module
        self.availableShapes = inspect.getmembers(shapes, inspect.isfunction)
        self.availableShapes = [i[0] for i in self.availableShapes]

        self.backgroundColor = QColor.fromCmykF(0.0, 0.0, 0.0, 1.0)

    def getOpenglInfo(self):
        info = """
            Vendor: {0}
            Renderer: {1}
            OpenGL Version: {2}
            Shader Version: {3}
        """.format(
            gl.glGetString(gl.GL_VENDOR),
            gl.glGetString(gl.GL_RENDERER),
            gl.glGetString(gl.GL_VERSION),
            gl.glGetString(gl.GL_SHADING_LANGUAGE_VERSION)
        )

        return info

    def minimumSizeHint(self):
        return QSize(150, 150)

    def sizeHint(self):
        return QSize(4000, 4000)

    def toggleAxes(self, value):
        self.axesOn = value
        self.update()

    def glibCommandToFunction(self, command):
        # get the function name
        function = command[0] + "("
        # start at the first argument and add in all the arguments that
        # have a comma after them
        for x in range(1,len(command) - 1):
            function += command[x]
            function += ","
        # add in the last argument with a closing parenthisis
        function += command[-1] + ")"
        return function

    def getGLIB(self):
        # prompt the user for the file location
        dialog = QFileDialog()
        # it returns a tuple with the path and the filter type
        self.glibFile = dialog.getOpenFileName()[0]
        # now that we have the glib location, load it in
        self.loadGLIB()

    def loadGLIB(self):
        # read our glib file
        with open(self.glibFile) as f:
            self.glibContents = f.readlines()
        # trim whitespace off the ends of strings
        self.glibContents = [x.strip() for x in self.glibContents]
        # split each argument by whitespace
        self.glibContents = [x.split() for x in self.glibContents]

        for line in self.glibContents:
            if line[0] == 'Vertex':
                self.vertexFile = line[1] + '.vert'
                print("Loaded ", self.vertexFile)
                self.vertOn = True
            if line[0] == 'Fragment':
                self.fragmentFile = line[1] + '.frag'
                print("Loaded ", self.fragmentFile)
                self.fragOn = True

        self.programOn = True
        self.update()

    def setXRotation(self, angle):
        angle = self.normalizeAngle(angle)
        if angle != self.xRot:
            self.xRot = angle
            self.xRotationChanged.emit(angle)
            self.update()

    def setYRotation(self, angle):
        angle = self.normalizeAngle(angle)
        if angle != self.yRot:
            self.yRot = angle
            self.yRotationChanged.emit(angle)
            self.update()

    def setZRotation(self, angle):
        angle = self.normalizeAngle(angle)
        if angle != self.zRot:
            self.zRot = angle
            self.zRotationChanged.emit(angle)
            self.update()

    def initializeGL(self):
        print(self.getOpenglInfo())

        self.setClearColor(self.backgroundColor.darker())
        # create an arrows object (call list)
        self.axes = self.Arrow()
        gl.glShadeModel(gl.GL_SMOOTH)
        gl.glEnable(gl.GL_DEPTH_TEST)
        gl.glEnable(gl.GL_CULL_FACE)

    def evaluateShape(self, command):
        function = self.glibCommandToFunction(command)
        gl.glCallList(eval(function))

    def evaluateCommand(self, command):
        # if it is a shape
        if command[0] in self.availableShapes:
            self.evaluateShape(command)

    # every time the screen reloads
    def paintGL(self):
        gl.glClear(gl.GL_COLOR_BUFFER_BIT | gl.GL_DEPTH_BUFFER_BIT)
        gl.glLoadIdentity()

        # if we never loaded in a glib file
        if self.glibFile == "":
            gl.glTranslated(0.0, 0.0, -10.0)
            gl.glRotated(self.xRot / 16.0, 1.0, 0.0, 0.0)
            gl.glRotated(self.yRot / 16.0, 0.0, 1.0, 0.0)
            gl.glRotated(self.zRot / 16.0, 0.0, 0.0, 1.0)
            # if the box is checked
            if (self.axesOn == 2):
                gl.glCallList(self.axes)
        else:
            # http://doc.qt.io/qt-5/qopenglshaderprogram.html
            self.shaderProgram = QOpenGLShaderProgram()
            self.shaderProgram.addShaderFromSourceFile(QOpenGLShader.Vertex, self.vertexFile)
            self.shaderProgram.addShaderFromSourceFile(QOpenGLShader.Fragment, self.fragmentFile)
            # don't bind the shader just yet. We need to draw the axes first
            self.shaderProgram.release()

            gl.glTranslated(0.0, 0.0, -10.0)
            gl.glRotated(self.xRot / 16.0, 1.0, 0.0, 0.0)
            gl.glRotated(self.yRot / 16.0, 0.0, 1.0, 0.0)
            gl.glRotated(self.zRot / 16.0, 0.0, 0.0, 1.0)

            # if the box is checked for axes on
            if (self.axesOn == 2):
                gl.glCallList(self.axes)

            # bind the shader program
            self.shaderProgram.bind()

            for command in self.glibContents:
                self.evaluateCommand(command)

    def resizeGL(self, width, height):
        # get the smallest edge
        minSide = min(width, height)
        # the default x and y spans -.5 to .5
        xRange = yRange = 0.5

        # distort the Orthographic view so that it maintains the same aspect
        # ratio for the elements in the screen
        if width > height:
            xRange = (width / height) * yRange
        else:
            yRange = (height / width) * xRange

        gl.glMatrixMode(gl.GL_PROJECTION)
        gl.glLoadIdentity()
        gl.glOrtho(-xRange, xRange, -yRange, yRange, 0.01, 1000.)
        gl.glMatrixMode(gl.GL_MODELVIEW)

    def mousePressEvent(self, event):
        self.lastPos = event.pos()

    def mouseMoveEvent(self, event):
        dx = event.x() - self.lastPos.x()
        dy = event.y() - self.lastPos.y()

        if event.buttons() & Qt.LeftButton:
            self.setXRotation(self.xRot + 8 * dy)
            self.setYRotation(self.yRot + 8 * dx)
        elif event.buttons() & Qt.RightButton:
            self.setXRotation(self.xRot + 8 * dy)
            self.setZRotation(self.zRot + 8 * dx)

        self.lastPos = event.pos()

    def Arrow(self):
        genList = gl.glGenLists(1)
        gl.glNewList(genList, gl.GL_COMPILE)

        dx = .5
        dy = .5
        dz = .5

        gl.glBegin(gl.GL_LINES)

        # red +x
        gl.glColor(1, 0, 0)
        gl.glVertex3f(0, 0, 0)
        gl.glVertex3f(dx, 0, 0)

        # dark red -x
        gl.glColor(.2, 0, 0)
        gl.glVertex3f(0, 0, 0)
        gl.glVertex3f(-dx, 0, 0)

        # green +y
        gl.glColor(0, 1, 0)
        gl.glVertex3f(0, 0, 0)
        gl.glVertex3f(0, dy, 0)

        # dark red -y
        gl.glColor(0, .2, 0)
        gl.glVertex3f(0, 0, 0)
        gl.glVertex3f(0, -dy, 0)

        # blue z
        gl.glColor(0, 0, 1)
        gl.glVertex3f(0, 0, 0)
        gl.glVertex3f(0, 0, dz)

        # dark blue -z
        gl.glColor(0, 0, .2)
        gl.glVertex3f(0, 0, 0)
        gl.glVertex3f(0, 0, -dz)

        gl.glEnd()
        gl.glEndList()

        return genList

    def normalizeAngle(self, angle):
        while angle < 0:
            angle += 360 * 16
        while angle > 360 * 16:
            angle -= 360 * 16
        return angle

    def setClearColor(self, c):
        gl.glClearColor(c.redF(), c.greenF(), c.blueF(), c.alphaF())

    def setColor(self, c):
        gl.glColor4f(c.redF(), c.greenF(), c.blueF(), c.alphaF())


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec_())
