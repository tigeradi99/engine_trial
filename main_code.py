import glfw
import numpy as np
from OpenGL.GL import *
#from OpenGL.GL.shaders import compileShader, compileProgram
import shaderProgram
import pyrr

vertex_src = """
# version 330

layout(location = 0) in vec3 a_position;
layout(location = 1) in vec3 a_color;

out vec3 v_color;

uniform mat4 rotation; 

void main()
{
    gl_Position = rotation * vec4(a_position, 1.0);
    v_color = a_color;
}
"""

fragment_src = """
# version 330
in vec3 v_color;
out vec4 out_color;
void main()
{
    out_color = vec4(v_color, 1.0);
}
"""
def window_resize(window, width, height):
    glViewport(0, 0, width, height)

#initialize GLFW library
if not glfw.init():
    raise Exception("Unable to initialize GLFW!")

width = 1280
height = 720
#make a new window
window = glfw.create_window(width, height, "TestWindow", None, None)

#Check window creation
if not window:
    glfw.terminate()
    raise Exception("Unable to create a window!")

#Set window position
glfw.set_window_pos(window, 400, 200)

glfw.set_window_size_callback(window, window_resize)

#make window the current context
glfw.make_context_current(window)

vertices = [-0.5, -0.5, 0.5, 1.0, 0.0, 0.0,
             0.5, -0.5, 0.5, 0.0, 1.0, 0.0,
             0.5,  0.5, 0.5, 0.0, 0.0, 1.0,
            -0.5,  0.5, 0.5, 1.0, 1.0, 1.0,

            -0.5, -0.5, -0.5, 1.0, 0.0, 0.0,
             0.5, -0.5, -0.5, 0.0, 1.0, 0.0,
             0.5,  0.5, -0.5, 0.0, 0.0, 1.0,
            -0.5,  0.5, -0.5, 1.0, 1.0, 1.0]

indices = [0, 1, 2, 2, 3, 0,
           4, 5, 6, 6, 7, 4,
           4, 5, 1, 1, 0, 4,
           6, 7, 3, 3, 2, 6,
           5, 6, 2, 2, 1, 5,
           7, 4, 0, 0, 3, 7]

vertices = np.array(vertices, dtype=np.float32)
indices = np.array(indices, dtype=np.uint32)

#create a shaderProgram
#shaderProgram = compileProgram(compileShader(vertex_src, GL_VERTEX_SHADER), compileShader(fragment_src, GL_FRAGMENT_SHADER))
shaderProgramID = shaderProgram.getShaderProgram()

#Create a Vertex Buffer, VBO will store the reference to the buffer. C++ eqv: GLuint VBO; glGenBuffers(1, &VBO)
VBO = glGenBuffers(1)
glBindBuffer(GL_ARRAY_BUFFER, VBO)
glBufferData(GL_ARRAY_BUFFER, vertices.nbytes, vertices, GL_STATIC_DRAW)

EBO = glGenBuffers(1)
glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, EBO)
glBufferData(GL_ELEMENT_ARRAY_BUFFER, indices.nbytes, indices, GL_STATIC_DRAW)

#Get reference to vec3 a_position from shader, pass to glEnableVertexAttribArray
glEnableVertexAttribArray(0)
glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 24, ctypes.c_void_p(0))

#Do the same for color attributes
glEnableVertexAttribArray(1)
glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, 24, ctypes.c_void_p(12))


glUseProgram(shaderProgramID)
#set color
glClearColor(0, 0.1, 0.1, 1)
glEnable(GL_DEPTH_TEST)

rot_loc = glGetUniformLocation(shaderProgramID, "rotation")

#Main loop
while not glfw.window_should_close(window):
    glfw.poll_events()

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    rot_x = pyrr.Matrix44.from_x_rotation(0.5 * glfw.get_time())
    rot_y = pyrr.Matrix44.from_y_rotation(0.8 * glfw.get_time())

    glUniformMatrix4fv(rot_loc, 1, GL_FALSE, pyrr.matrix44.multiply(rot_x, rot_y))

    glDrawElements(GL_TRIANGLES, len(indices), GL_UNSIGNED_INT, None)

    glfw.swap_buffers(window)

#Program finished
glfw.terminate()