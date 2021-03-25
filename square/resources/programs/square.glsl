#version 330

#if defined VERTEX_SHADER

in vec3 in_coord;
in vec3 in_color;
out vec4 color;

void main() {
    gl_Position = vec4(in_coord, 1.0);
    color = vec4(in_color, 1.0);
}

#elif defined FRAGMENT_SHADER

in vec4 color;
out vec4 f_color;

void main() {
    f_color = color;
}

#endif
