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

# returns a list of lines, each line split by white space into a list
def parseGLIB(glibFile):
    # read our glib file
    with open(glibFile) as f:
        glibContents = f.readlines()
    # trim whitespace off the ends of strings
    glibContents = [x.strip() for x in glibContents]
    # split each argument by whitespace
    glibContents = [x.split() for x in glibContents]
    # remove all empty lines
    glibContents = [x for x in glibContents if x != []]
    return glibContents

def parseUniformVariables(glibContents):
    # a list of all our programs
    programs = []
    # the current program number we are on
    programNumber = 0
    # a flag to let us know if we are currently in a program scope (aka. between brackets)
    inProgram = False

    for line in glibContents:
        # if we find an open bracket at the begining of a line, throw an error
        if line[0] == "{":
            print("""
                Error: Unexpected open bracket.
                Please place your opening brackets at the end of your program line""")
            exit(1)

        # if we got to a program
        if line[0] == "Program":
            programs.append({})
            # get our program name
            programs[programNumber]["name"] = line[1]
            programs[programNumber]["variables"] = []
            # if the user opened up a scope, that means they are going to have
            # uniform variables that we are going to use in our program
            if line[2] == "{":
                inProgram = True
                # move on to the next line
                continue

        if line[0] == "}":
            inProgram = False
            programNumber += 1

        if inProgram:
            # store the name, min default and max values
            programs[programNumber]["variables"].append({
                "name": line[0],
                # remove the opening <
                "min": float(line[1][1:]),
                "default": float(line[2]),
                # remove the closing >
                "max": float(line[3][:-1])
            })
    return programs


class Window(QWidget):

    def __init__(self):
        super(Window, self).__init__()

        self.glWidget = MakeGLWidget()

        # create our main layout
        self.mainLayout = QHBoxLayout()
        self.mainLayout.addWidget(self.glWidget)

        # expand the glWidget to fill all available space
        self.glWidget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        self.controlBar = self.makeControlBar()

        # add the vertical layout
        self.mainLayout.addLayout(self.controlBar)

        # set our main layout for the window
        self.setLayout(self.mainLayout)

        self.setWindowTitle("glman")

    def makeControlBar(self):
        # create each slider
        self.xSlider = self.createSlider(0, 360 * 16)
        self.ySlider = self.createSlider(0, 360 * 16)
        self.zSlider = self.createSlider(0, 360 * 16)

        # the connect function takes in a single value, which is the new value
        # of the slider when it is changed.
        # use a lambda function to connect set the rotation on the axis and
        # send in the new value to be used for that element
        self.xSlider.valueChanged.connect( lambda newValue: self.glWidget.setRotation('x', newValue))
        self.glWidget.xRotationChanged.connect(self.xSlider.setValue)
        self.ySlider.valueChanged.connect( lambda newValue: self.glWidget.setRotation('y', newValue))
        self.glWidget.yRotationChanged.connect(self.ySlider.setValue)
        self.zSlider.valueChanged.connect( lambda newValue: self.glWidget.setRotation('z', newValue))
        self.glWidget.zRotationChanged.connect(self.zSlider.setValue)

        # set the value of the slider now that they are linked
        self.xSlider.setValue(23  * 16)
        self.ySlider.setValue(315 * 16)
        self.zSlider.setValue(1   * 16)

        # add in a vertical layout for all our controls
        controlBar = QVBoxLayout()

        # a horizontal layout for some check boxes
        checkBoxes = QHBoxLayout()

        # create an axis box and connect a state changed listener to the glWidget
        self.axisCheckbox = self.makeCheckBox("Axes")
        self.axisCheckbox.setCheckState(Qt.Checked)
        self.axisCheckbox.stateChanged.connect(self.glWidget.toggleAxes)

        checkBoxes.addWidget(self.makeCheckBox("Orthographic"))
        checkBoxes.addWidget(self.axisCheckbox)
        controlBar.addLayout(checkBoxes)

        loadGlibButton = QPushButton("Load GLIB File")
        loadGlibButton.clicked.connect(self.getGLIB)

        reloadGlibButton = QPushButton("Reload GLIB File")
        reloadGlibButton.clicked.connect(self.glWidget.loadGLIB)

        controlBar.addWidget(loadGlibButton)
        controlBar.addWidget(reloadGlibButton)
        controlBar.addWidget(self.xSlider)
        controlBar.addWidget(self.ySlider)
        controlBar.addWidget(self.zSlider)
        return controlBar

    def addSliders(self, programs):
        variableSliders = []
        sliderLabels = []

        # for every program we have
        for program in programs:
            for key, value in program.items():
                # if we see variables
                if key == "variables":
                    for variable in value:
                        # make a slider with a min and max value
                        slider = self.createSlider(variable["min"], variable["max"])
                        # set the slider to the default variable
                        slider.setValue(variable["default"])
                        # make a label for our slider
                        label = QLabel()
                        # set our label name
                        label.setText(variable["name"])
                        # make the text white and center it on the menu
                        label.setStyleSheet("QLabel { color : white; qproperty-alignment: AlignCenter; }")

                        # add the label and slider to their respective arrays
                        sliderLabels.append(label)
                        variableSliders.append(slider)

        # just in case we have an uneven number of sliders and labels
        if len(variableSliders) != len(sliderLabels):
            print("Error: the number of sliders and labels do not match")
            exit(1)

        # for every slider and label
        for x in range(0,len(variableSliders)):
            self.controlBar.addWidget(sliderLabels[x])
            self.controlBar.addWidget(variableSliders[x])

    def makeCheckBox(self, label):
        checkBox = QCheckBox(label)
        # make the text white
        checkBox.setStyleSheet("""
            QCheckBox {
               border: none;
               color: white;
            }""")
        return checkBox

    def createSlider(self, start, end):
        slider = QSlider(Qt.Horizontal)
        slider.setRange(start, end)
        return slider

    def getGLIB(self):
        # prompt the user for the file location
        dialog = QFileDialog()
        # it returns a tuple with the path and the filter type
        self.glibFile = dialog.getOpenFileName()[0]
        self.glibContents = parseGLIB(self.glibFile)
        self.addSliders(parseUniformVariables(self.glibContents))

        # now that we have the glib location, load it in
        self.glWidget.loadGLIB(self.glibFile)

class MakeGLWidget(QOpenGLWidget):
    # these are signals that are emitted to make connections
    xRotationChanged = pyqtSignal(int)
    yRotationChanged = pyqtSignal(int)
    zRotationChanged = pyqtSignal(int)

    def __init__(self, parent=None):
        super(MakeGLWidget, self).__init__(parent)

        self.axis = 0

        self.rotation = {
            "x": 0,
            "y": 0,
            "z": 0
        }

        self.axisOn = 2

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
        self.axisOn = value
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

    def loadGLIB(self, glibFile):
        self.glibFile = glibFile
        self.glibContents = parseGLIB(glibFile)

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


    def setRotation(self, axis, angle):
        angle = self.normalizeAngle(angle)
        if angle != self.rotation[axis]:
            self.rotation[axis] = angle
            if axis == 'x':
                self.xRotationChanged.emit(angle)
            elif axis == 'y':
                self.yRotationChanged.emit(angle)
            elif axis == 'z':
                self.zRotationChanged.emit(angle)
            self.update()

    def initializeGL(self):
        print(self.getOpenglInfo())

        self.setClearColor(self.backgroundColor.darker())
        # create an arrows object (call list)
        self.axis = self.Arrow()
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
            gl.glRotated(self.rotation['x'] / 16.0, 1.0, 0.0, 0.0)
            gl.glRotated(self.rotation['y'] / 16.0, 0.0, 1.0, 0.0)
            gl.glRotated(self.rotation['z'] / 16.0, 0.0, 0.0, 1.0)
            # if the box is checked
            if (self.axisOn == 2):
                gl.glCallList(self.axis)
        else:
            # http://doc.qt.io/qt-5/qopenglshaderprogram.html
            self.shaderProgram = QOpenGLShaderProgram()
            self.shaderProgram.addShaderFromSourceFile(QOpenGLShader.Vertex, self.vertexFile)
            self.shaderProgram.addShaderFromSourceFile(QOpenGLShader.Fragment, self.fragmentFile)
            # don't bind the shader just yet. We need to draw the axis first
            self.shaderProgram.release()

            gl.glTranslated(0.0, 0.0, -10.0)
            gl.glRotated(self.rotation['x'] / 16.0, 1.0, 0.0, 0.0)
            gl.glRotated(self.rotation['y'] / 16.0, 0.0, 1.0, 0.0)
            gl.glRotated(self.rotation['z'] / 16.0, 0.0, 0.0, 1.0)

            # if the box is checked for axis on
            if (self.axisOn == 2):
                gl.glCallList(self.axis)

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
            self.setRotation('x', self.rotation['x'] + 8 * dy)
            self.setRotation('y', self.rotation['y'] + 8 * dx)
        elif event.buttons() & Qt.RightButton:
            self.setRotation('x', self.rotation['x'] + 8 * dy)
            self.setRotation('z', self.rotation['z'] + 8 * dx)

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
