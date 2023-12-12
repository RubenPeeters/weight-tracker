from kivy.app import App
from ui.camera import CameraClick


class MyApp(App):
    def build(self):
        self.title = "Weight tracker"
        return CameraClick()


if __name__ == "__main__":
    MyApp().run()
