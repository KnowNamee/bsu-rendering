import moderngl_window as mglw
import numpy as np

vbo_coords = np.array([
    [-0.5,  0.5, 0.0],
    [0.5,   0.5, 0.0],
    [0.5,  -0.5, 0.0],
    [-0.5, -0.5, 0.0]
], dtype='f4')
vbo_colors = np.array([
    [1.0, 0.0, 0.0],
    [1.0, 1.0, 1.0],
    [0.1, 0.0, 1.0]
], dtype='f4')
indexes = np.array([0, 2, 1, 0, 2, 3], dtype='u4')

global_width = 800
global_height = 800


class Window(mglw.WindowConfig):
    gl_version = (3, 3)
    window_size = (global_width, global_height)
    title = "Colored square"
    resource_dir = "resources"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # do initialization here
        self.prog = self.load_program("programs/square.glsl")
        self.vao = self.ctx.vertex_array(
            self.prog,
            [
                (self.ctx.buffer(vbo_coords.tobytes()), "3f", "in_coord"),
                (self.ctx.buffer(vbo_colors.tobytes()), "3f", "in_color")
            ],
            self.ctx.buffer(indexes.tobytes())
        )

    def render(self, time, frametime):
        self.vao.render(mode=self.ctx.TRIANGLES)

    def resize(self, width: int, height: int):
        self.ctx.viewport = (0, 0, min(width, height), min(width, height))


def main():
    mglw.run_window_config(Window)


if __name__ == "__main__":
    main()
