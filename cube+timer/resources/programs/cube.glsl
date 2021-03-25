#version 330

#if defined VERTEX_SHADER

in vec3 in_position;
in vec2 in_texcoord_0;

uniform mat3 rotation;

out vec2 uv;

void main() {
    gl_Position = vec4(rotation * in_position, 1.0);
    uv = in_texcoord_0;
}

#elif defined FRAGMENT_SHADER

in vec2 uv;

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
