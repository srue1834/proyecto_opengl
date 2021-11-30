# los vertices se mandan a los shaders
vertex_shader = """
#version 460

layout (location = 0) in vec3 position;
layout (location = 1) in vec3 ccolor; //para aceptar color, despues podemos cambiar la variable
layout (location = 2) in vec3 normal;

uniform mat4 theMatrix; //se recibe la matriz completa
uniform vec3 light;
uniform mat4 nnormal;

out float intensity;
out vec4 normal_shader;
out vec3 mycolor; 

void main()
{
    intensity = dot(normal, normalize(light));
    normal_shader = normalize(nnormal * vec4(normal, 1.0));
    gl_Position = theMatrix * vec4(position.x, position.y, position.z, 1);
    mycolor = ccolor * light; //cada uno de los colores del vertice
}
"""
fragment_shader = """
#version 460

layout(location = 0) out vec4 fragColor;

uniform vec4 diffuse;
uniform vec4 ambient;

//color por pixel
in vec3 mycolor;
in vec4 normal_shader;


void main() 
{
    fragColor = diffuse + ambient * vec4(mycolor, 1.0f);
}
"""
