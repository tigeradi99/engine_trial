from OpenGL.GL import *
import numpy as np 
class EBO:
    def __init__(self, indices):
        self.EBO = glGenBuffers(1)
        self.indices =  np.array(indices, dtype=np.float32)
        glBufferData(GL_ELEMENT_ARRAY_BUFFER, self.indices.nbytes, self.indices, GL_STATIC_DRAW)


    def Bind(self):
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, self.EBO)

    def Unbind(self):
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, 0)