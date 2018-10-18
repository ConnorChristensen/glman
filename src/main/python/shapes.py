import OpenGL.GL as gl

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
