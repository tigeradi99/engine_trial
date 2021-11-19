from OpenGL.GL import GL_VERTEX_SHADER , GL_FRAGMENT_SHADER
from OpenGL.GL.shaders import compileShader, compileProgram

def getShaderProgram():
    try:
        vertexSrc = open("Resources/Shaders/vertexShader.glsl",'r+b')
        fragmentSrc = open("Resources/Shaders/fragmentShader.glsl",'r+b')
        vertexSrcCode = vertexSrc.read()
        fragmentSrcCode = fragmentSrc.read()
        shaderProgramID = compileProgram(compileShader(vertexSrcCode, GL_VERTEX_SHADER), compileShader(fragmentSrcCode, GL_FRAGMENT_SHADER))
    finally:
        vertexSrc.close()
        fragmentSrc.close()
        return shaderProgramID
