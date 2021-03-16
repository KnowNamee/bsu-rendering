import moderngl_window as mglw
import moderngl
import numpy as np

vbo_coords = np.array([
    [-0.5,  0.5, 0.5],
    [0.5,   0.5, 0.5],
    [0.5,  -0.5, 0.5],
    [-0.5, -0.5, 0.5],
    [-0.5,  0.5, -0.5],
    [0.5,   0.5, -0.5],
    [0.5,  -0.5, -0.5],
    [-0.5, -0.5, -0.5]
], dtype='f4')
vbo_colors = np.array([
    [0.0, 0.0, 1.0],
    [0.0, 0.0, 1.0],
    [0.0, 0.0, 1.0],
    [1.0, 0.0, 1.0],
    [1.0, 0.0, 1.0],
    [0.0, 0.0, 1.0],
    [0.0, 0.0, 1.0],
    [0.0, 0.0, 1.0]
], dtype='f4')
indexes = np.array([
    0, 1, 2,
    0, 2, 3,
    4, 5, 6,
    4, 6, 7,
    0, 3, 7,
    0, 7, 4,
    0, 1, 5,
    0, 4, 5,
    3, 7, 6,
    3, 2, 6,
    1, 2, 6,
    1, 6, 5
], dtype='u4')

vertex_shader = """
#version 330

in vec3 in_coord;
in vec3 in_color;

out vec3 color;

uniform float rxc;
uniform float ryc;
uniform float rzc;

void main() {
    mat3 rx = mat3(
        1.0, 0.0, 0.0,
        0.0, cos(rxc), -sin(rxc),
        0.0, sin(rxc), cos(rxc)
    );
    mat3 ry = mat3(
        cos(ryc), 0.0, -sin(ryc),
        0.0, 1.0, 0.0,
        sin(ryc), 0.0, cos(ryc)
    );
    mat3 rz = mat3(
        cos(rzc), -sin(rzc), 0.0, 
        sin(rzc), cos(rzc), 0.0, 
        0.0, 0.0, 0.1
    );
    
    gl_Position = vec4(rz * ry * rx * in_coord, 1.0);
    color = in_color;
}
"""

fragment_shader = """
#version 330

in vec3 color;
out vec4 f_color;

void main() {
    f_color = vec4(color, 1.0);
}
"""

global_width = 800
global_height = 800


class Window(mglw.WindowConfig):
    gl_version = (3, 3)
    window_size = (global_width, global_height)
    title = "Colored cube"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # do initialization here
        self.prog = self.ctx.program(vertex_shader=vertex_shader, fragment_shader=fragment_shader)
        self.vao = self.ctx.vertex_array(
            self.prog,
            [
                (self.ctx.buffer(vbo_coords.tobytes()), "3f", "in_coord"),
                (self.ctx.buffer(vbo_colors.tobytes()), "3f", "in_color")
            ],
            self.ctx.buffer(indexes.tobytes())
        )
        self.rotation_x = self.prog['rxc']
        self.rotation_y = self.prog['ryc']
        self.rotation_z = self.prog['rzc']


    def render(self, time, frametime):
        self.ctx.enable(moderngl.DEPTH_TEST)
        self.ctx.clear(1.0, 1.0, 0.5, 1.0)
        self.rotation_x.value = float(time) / 2
        self.rotation_y.value = float(time) / 2
        self.rotation_z.value = float(time) / 2
        self.vao.render(mode=self.ctx.TRIANGLES)

    def resize(self, width: int, height: int):
        self.ctx.viewport = (0, 0, min(width, height), min(width, height))


def main():
    mglw.run_window_config(Window)


if __name__ == "__main__":
    main()