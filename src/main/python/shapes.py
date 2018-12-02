import OpenGL.GL as gl
import math
import copy

def cube(dx, dy, dz):
    genList = gl.glGenLists(1)
    gl.glNewList(genList, gl.GL_COMPILE)

    dx /= 2.0
    dy /= 2.0
    dz /= 2.0

    gl.glBegin(gl.GL_QUADS)

    gl.glNormal3f(0.0, 0.0, 1.0)
    gl.glTexCoord2f(0.0, 0.0)
    gl.glVertex3f(-dx, -dy, dz)
    gl.glTexCoord2f(1.0, 0.0)
    gl.glVertex3f(dx, -dy, dz)
    gl.glTexCoord2f(1.0, 1.0)
    gl.glVertex3f(dx, dy, dz)
    gl.glTexCoord2f(0.0, 1.0)
    gl.glVertex3f(-dx, dy, dz)

    gl.glNormal3f(0.0, 0.0, -1.0)
    gl.glTexCoord2f(0.0, 0.0)
    gl.glVertex3f(-dx, -dy, -dz)
    gl.glTexCoord2f(0.0, 1.0)
    gl.glVertex3f(-dx, dy, -dz)
    gl.glTexCoord2f(1.0, 1.0)
    gl.glVertex3f(dx, dy, -dz)
    gl.glTexCoord2f(1.0, 0.0)
    gl.glVertex3f(dx, -dy, -dz)

    gl.glNormal3f(1.0, 0.0, 0.0)
    gl.glTexCoord2f(0.0, 0.0)
    gl.glVertex3f(dx, -dy, dz)
    gl.glTexCoord2f(1.0, 0.0)
    gl.glVertex3f(dx, -dy, -dz)
    gl.glTexCoord2f(1.0, 1.0)
    gl.glVertex3f(dx, dy, -dz)
    gl.glTexCoord2f(0.0, 1.0)
    gl.glVertex3f(dx, dy, dz)

    gl.glNormal3f(-1.0, 0.0, 0.0)
    gl.glTexCoord2f(0.0, 0.0)
    gl.glVertex3f(-dx, -dy, dz)
    gl.glTexCoord2f(0.0, 1.0)
    gl.glVertex3f(-dx, dy, dz)
    gl.glTexCoord2f(1.0, 1.0)
    gl.glVertex3f(-dx, dy, -dz)
    gl.glTexCoord2f(1.0, 0.0)
    gl.glVertex3f(-dx, -dy, -dz)

    gl.glNormal3f(0.0, 1.0, 0.0)
    gl.glTexCoord2f(0.0, 0.0)
    gl.glVertex3f(-dx, dy, dz)
    gl.glTexCoord2f(1.0, 0.0)
    gl.glVertex3f(dx, dy, dz)
    gl.glTexCoord2f(1.0, 1.0)
    gl.glVertex3f(dx, dy, -dz)
    gl.glTexCoord2f(0.0, 1.0)
    gl.glVertex3f(-dx, dy, -dz)

    gl.glNormal3f(0.0, -1.0, 0.0)
    gl.glTexCoord2f(0.0, 0.0)
    gl.glVertex3f(-dx, -dy, dz)
    gl.glTexCoord2f(0.0, 1.0)
    gl.glVertex3f(-dx, -dy, -dz)
    gl.glTexCoord2f(1.0, 1.0)
    gl.glVertex3f(dx, -dy, -dz)
    gl.glTexCoord2f(1.0, 0.0)
    gl.glVertex3f(dx, -dy, dz)

    gl.glEnd()
    gl.glEndList()
    return genList

class Point(object):
    def __init__(self):
        super(Point, self).__init__()

    # coordinants
    def setCoordinants(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def setSurfaceNormals(self, nx, ny, nz):
        self.nx = nx
        self.ny = ny
        self.nz = nz

    def setTextureCoordinants(self, s, t):
        self.s = s
        self.t = t

    def setTangentVector(self, tx, ty, tz):
        self.tx = tx
        self.ty = ty
        self.tz = tz

    def getCoordinants(self):
        return (self.x, self.y, self.z)

def drawPoint(p):
    gl.glNormal3f(p.nx, p.ny, p.nz)
    gl.glTexCoord2f(p.s, p.t)
    gl.glVertex3f(p.x, p.y, p.z)

def getPoint(points, lat, lng, NumLats, NumLngs):
    if lat < 0: lat += NumLats - 1
    if lng < 0: lng += NumLngs - 1
    if lat > NumLats - 1: lat -= NumLats - 1
    if lng > NumLngs - 1: lng -= NumLngs - 1
    return points[NumLngs * lat + lng]

def sphere(radius, slices, stacks):
    p = Point() # a single point class
    points = [] # the rest of the points

    # set the globals:
    NumLngs = 3 if slices < 3 else slices
    NumLats = 3 if stacks < 3 else stacks

    # fill the Pts structure:
    for ilat in range(0, NumLats):
        lat = (-math.pi / 2.0) + ((math.pi * float(ilat)) / (float(NumLats) - 1))
        xz = math.cos(lat)
        y = math.sin(lat)
        for ilng in range(0, NumLngs):
            lng = -math.pi + ((2.0 * math.pi * float(ilng)) / (float(NumLngs) - 1))
            x = xz * math.cos(lng)
            z = -xz * math.sin(lng)
            p.setCoordinants(radius * x, radius * y, radius * z)
            p.setSurfaceNormals(x, y, z)
            p.setTextureCoordinants((lng + math.pi) / (2.0 * math.pi), (lat + math.pi / 2.0) / math.pi)
            tx = -y * math.cos(lng)
            ty = xz
            tz = y * math.sin(lng)
            denom = math.sqrt(tx * tx + ty * ty + tz * tz)
            tx = tx / denom
            ty = ty / denom
            tz = tz / denom
            p.setTangentVector(tx, ty, tz)
            points.append(copy.copy(p))

    genList = gl.glGenLists(1)
    gl.glNewList(genList, gl.GL_COMPILE)

    # connect the north pole to the latitude NumLats-2:
    gl.glBegin(gl.GL_QUADS)
    for ilng in range(0, NumLngs - 1):
        drawPoint(getPoint(points, NumLats - 1, ilng, NumLats, NumLngs))
        drawPoint(getPoint(points, NumLats - 2, ilng, NumLats, NumLngs))
        drawPoint(getPoint(points, NumLats - 2, ilng + 1, NumLats, NumLngs))
        drawPoint(getPoint(points, NumLats - 1, ilng + 1, NumLats, NumLngs))
    gl.glEnd()

    # connect the south pole to the latitude 1:
    gl.glBegin(gl.GL_QUADS)
    for ilng in range(0, NumLngs - 1):
        drawPoint(getPoint(points, 0, ilng, NumLats, NumLngs))
        drawPoint(getPoint(points, 0, ilng + 1, NumLats, NumLngs))
        drawPoint(getPoint(points, 1, ilng + 1, NumLats, NumLngs))
        drawPoint(getPoint(points, 1, ilng, NumLats, NumLngs))
    gl.glEnd()

    # connect the other 4-sided polygons:
    gl.glBegin(gl.GL_QUADS)
    for ilat in range(2, NumLats - 1):
        for ilng in range(0, NumLngs - 1):
          drawPoint(getPoint(points, ilat - 1, ilng, NumLats, NumLngs))
          drawPoint(getPoint(points, ilat - 1, ilng + 1, NumLats, NumLngs))
          drawPoint(getPoint(points, ilat, ilng + 1, NumLats, NumLngs))
          drawPoint(getPoint(points, ilat, ilng, NumLats, NumLngs))
    gl.glEnd()

    gl.glEndList()
    return genList
