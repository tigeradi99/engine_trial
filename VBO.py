from OpenGL.GL import *
import numpy as np 
class VBO:
    def __init__(self, vertices):
        self.VBO = glGenBuffers(1)
        self.vertices =  np.array(vertices, dtype=np.float32)
        glBufferData(GL_ARRAY_BUFFER, self.vertices.nbytes, self.vertices, GL_STATIC_DRAW)


    def Bind(self):
        glBindBuffer(GL_ARRAY_BUFFER, self.VBO)

    def Unbind(self):
        glBindBuffer(GL_ARRAY_BUFFER, 0)