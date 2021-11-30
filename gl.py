from OpenGL.GL import *
import glm

class Renderer(object):
    def __init__(self, screen):
        self.screen = screen
        _, _, self.width, self.height = screen.get_rect()
        self.view_translate = glm.vec3(0, 2, 7)
        self.view_rotate = glm.vec3(0, 0, 0)

        self.i = glm.mat4(1) # identidad
        self.projection = glm.perspective(glm.radians(45), self.width/self.height, 0.1, 1000.0)

        glEnable(GL_DEPTH_TEST)
        glViewport(0, 0, self.width, self.height)

    def view(self):
        # se simula la vista de una camara
        cam_translate = glm.translate(self.i, self.view_translate)

        cam_rotate_x = glm.rotate(self.i, glm.radians( self.view_rotate.x ), glm.vec3(1,0,0))
        cam_rotate_y = glm.rotate(self.i, glm.radians( self.view_rotate.y ), glm.vec3(0,1,0))
        cam_rotate_z = glm.rotate(self.i, glm.radians( self.view_rotate.z ), glm.vec3(0,0,1))
        cam_rotate = cam_rotate_x * cam_rotate_y * cam_rotate_z

        return glm.inverse(cam_translate * cam_rotate)
    
    def model(self):
        model_translate = glm.translate(self.i, glm.vec3(0,0,0)) #matriz de translacion
        model_rotate = glm.rotate(self.i, glm.radians(0), glm.vec3(0, 1, 0))
        model_scale = glm.scale(self.i, glm.vec3(2, 2, 2))

        return model_translate * model_rotate * model_scale

