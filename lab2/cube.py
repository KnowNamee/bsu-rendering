import moderngl
import moderngl_window as mglw

from moderngl_window import geometry
from pyrr import Matrix33

global_width = 800
global_height = 800


class Window(mglw.WindowConfig):
    gl_version = (3, 3)
    window_size = (global_width, global_height)
    title = "Colored cube"
    resource_dir = 'resources'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # do initialization here
        self.cube = geometry.cube()
        self.prog = self.load_program('programs/cube.glsl')
        self.texture = self.load_texture_array(
            'textures/pattern.jpg', layers=2, mipmap=True, anisotropy=8.0)
        self.prog['texture0'].value = 0
        self.prog['layers'].value = 10
        self.rotation = self.prog['rotation']

    def render(self, time: float, frametime: float):
        self.ctx.enable(moderngl.DEPTH_TEST | moderngl.CULL_FACE)
        self.ctx.clear(1.0, 1.0, 0.5, 1.0)
        self.rotation.value = tuple(
            Matrix33.from_eulers((time/2, time/2, time/2)).reshape(9).tolist())
        self.prog['time'].value = time
        self.texture.use(location=0)
        self.cube.render(self.prog)

    def resize(self, width: int, height: int):
        self.ctx.viewport = (0, 0, min(width, height), min(width, height))


def main():
    mglw.run_window_config(Window)


if __name__ == "__main__":
    main()
