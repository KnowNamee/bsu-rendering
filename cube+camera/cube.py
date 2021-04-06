import moderngl
import moderngl_window as mglw

from moderngl_window.scene.camera import KeyboardCamera
from moderngl_window import geometry
from pyrr import Matrix44

global_width = 800
global_height = 800


class Window(mglw.WindowConfig):
    gl_version = (3, 3)
    window_size = (global_width, global_height)
    title = "Colored cube with camera"
    resource_dir = 'resources'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.camera = KeyboardCamera(self.wnd.keys, aspect_ratio=self.wnd.aspect_ratio)
        self.camera.set_position(4.0, 4.0, 4.0)
        self.lookat = self.camera.look_at(pos=(1.0, 1.0, 1.0))
        self.camera_enabled = True
        self.cube = geometry.cube()
        self.prog = self.load_program('programs/cube.glsl')
        self.texture = self.load_texture_array(
            'textures/pattern.jpg', layers=2, mipmap=True, anisotropy=8.0)
        self.prog['texture0'].value = 0
        self.prog['layers'].value = 10

    def key_event(self, key, action, modifiers):
        keys = self.wnd.keys

        if self.camera_enabled:
            self.camera.key_input(key, action, modifiers)

        if action == keys.ACTION_PRESS:
            if key == keys.C:
                self.camera_enabled = not self.camera_enabled
                self.wnd.mouse_exclusivity = self.camera_enabled
                self.wnd.cursor = not self.camera_enabled
            if key == keys.SPACE:
                self.timer.toggle_pause()

    def mouse_position_event(self, x: int, y: int, dx, dy):
        if self.camera_enabled:
            self.camera.rot_state(-dx // 3, -dy // 3)

    def resize(self, width: int, height: int):
        self.camera.projection.update(aspect_ratio=self.wnd.aspect_ratio)

    def render(self, time: float, frametime: float):
        self.ctx.enable(moderngl.CULL_FACE | moderngl.DEPTH_TEST)

        rotation = Matrix44.from_eulers((time, time, time), dtype='f4')
        translation = self.lookat * Matrix44.from_translation((1.0, -1.0, 1.2), dtype='f4')
        modelview = translation * rotation

        self.prog['m_proj'].write(self.camera.projection.matrix)
        self.prog['m_model'].write(modelview)
        self.prog['m_view'].write(self.camera.matrix)
        self.prog['time'].value = time

        self.texture.use(location=0)
        self.cube.render(self.prog)


def main():
    mglw.run_window_config(Window)


if __name__ == "__main__":
    main()
