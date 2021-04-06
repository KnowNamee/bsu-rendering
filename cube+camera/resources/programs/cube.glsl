#version 330

#if defined VERTEX_SHADER

in vec2 in_texcoord_0;
in vec3 in_position;
in vec3 in_normal;

uniform mat4 m_model;
uniform mat4 m_proj;
uniform mat4 m_view;

out vec2 uv;
out vec3 normal;

void main() {
    gl_Position = m_proj * m_view * m_model * vec4(in_position, 1.0);
    uv = in_texcoord_0;
}

#elif defined FRAGMENT_SHADER

in vec2 uv;
in vec3 normal;

uniform sampler2DArray texture0;
uniform float layers;
uniform float time;

out vec4 f_color;

void main() {
    float layer = floor(time);
    vec4 c1 = texture(texture0, vec3(uv, mod(layer+0, layers)));
    vec4 c2 = texture(texture0, vec3(uv, mod(layer+1, layers)));

    float t = mod(time, 1.0);
    f_color = (c1 * (1.0 - t) + c2 * t) + vec4(0.25);
}

#endif
