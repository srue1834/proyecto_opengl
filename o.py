from OpenGL.GL import shaders
import pygame
import numpy
from OpenGL.GL import *
from OpenGL.GL.shaders import compileProgram, compileShader
from obj import *
import glm
import shaders
from gl import Renderer


pygame.init()
screen = pygame.display.set_mode((1200, 720), pygame.OPENGL | pygame.DOUBLEBUF)

glClearColor(0.2, 0.3, 0.3, 1)
# reloj interno de pygame
clock = pygame.time.Clock()


r = Renderer(screen)




# compilar shaders

cvs = compileShader(shaders.vertex_shader, GL_VERTEX_SHADER)
cfs = compileShader(shaders.fragment_shader, GL_FRAGMENT_SHADER)

shader =  compileProgram(cvs, cfs) 

mesh = Obj('./models/zombie.obj')

vertex_data = numpy.hstack((
    numpy.array(mesh.vertex, dtype=numpy.float32),
    numpy.array(mesh.nvertex, dtype=numpy.float32),
)).flatten() # para saber cuantos bytes ocupa cada valor

index_data = numpy.array([
    [vertex[0] - 1 for vertex in face] for face in mesh.faces
], dtype=numpy.uint32).flatten()

vertex_buffer_object = glGenBuffers(1)    # aparta un bloque de memoria
glBindBuffer(GL_ARRAY_BUFFER, vertex_buffer_object)    # las siguientes instrucciones ocurriran en ese bloque de memoria
glBufferData(GL_ARRAY_BUFFER, vertex_data.nbytes, vertex_data, GL_STATIC_DRAW)   # ahora se mete al bloque de memoria


 # describir data
vertex_array_object = glGenVertexArrays(1)
glBindVertexArray(vertex_array_object)


glVertexAttribPointer(
    0, # location
    3, # size
    GL_FLOAT, # tipo
    GL_FALSE, # normalizados
    24, # stride 
    ctypes.c_void_p(0) # puntero
)
# se activa el vertex_array

glEnableVertexAttribArray(0)


element_buffer_object = glGenBuffers(1)    # aparta un bloque de memoria
glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, element_buffer_object)    # las siguientes instrucciones ocurriran en ese bloque de memoria
glBufferData(GL_ELEMENT_ARRAY_BUFFER, index_data.nbytes, index_data, GL_STATIC_DRAW)   # ahora se mete al bloque de memoria


# CREO QUE ES PARA CAMBIAR DE COLOR IDK
glVertexAttribPointer(
    1, # location
    3, # size
    GL_FLOAT, # tipo
    GL_FALSE, # normalizados
    24, # stride 
    ctypes.c_void_p(12) # puntero ahora empieza en 12 para cambiar de color
)
# se activa el vertex_array en 1

glEnableVertexAttribArray(1)

glUseProgram(shader)

def render():
    
    # matriz de tranformacion
    theMatrix = r.projection * r.view() * r.model()

    glUniformMatrix4fv(
        glGetUniformLocation(shader, 'theMatrix'), # ubicacion en memoria
        1, # tamano de puntero
        GL_FALSE, # ya esta transpuesta por glm :p
        glm.value_ptr(theMatrix) # puntero
    ) 
    glUniformMatrix4fv(
        glGetUniformLocation(shader, 'nnormal'), 
        1,
        GL_FALSE,
        glm.value_ptr(theMatrix) # puntero
    ) 

    glUniform3f(
      glGetUniformLocation(shader, 'light'),
      1, 1, 0 )

    glUniform4f(
      glGetUniformLocation(shader, "diffuse"),
      0.5, 1, 1, 1 )

    glUniform4f(
      glGetUniformLocation(shader, "ambient"),
      0.5, 0.5, 1, 1 )


running = True
while running:
    glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
    render()

    glDrawElements(GL_TRIANGLES, len(index_data), GL_UNSIGNED_INT, None)

    pygame.display.flip()
    clock.tick(15)
    deltaTime = clock.get_time() / 500

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                r.view_translate.x -= 1 * deltaTime
            if event.key == pygame.K_d:
                r.view_translate.x += 1 * deltaTime
                
            if event.key == pygame.K_w:
                r.view_translate.y += 1 * deltaTime
                
            if event.key == pygame.K_s:
                r.view_translate.y -= 1 * deltaTime

            if event.key == pygame.K_j:
                r.view_translate.z -= 1 * deltaTime
            if event.key == pygame.K_k:
                r.view_translate.z += 1 * deltaTime




         
            
