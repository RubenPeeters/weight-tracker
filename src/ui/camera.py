# from kivy.logger import Logger
# import logging

# Logger.setLevel(logging.TRACE)

from pathlib import Path
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
import time

from analyze.read_image import read_image
from analyze.matches import analyze_cloud_vision, analyze_and_write_to_csv, analyze_mock

Builder.load_string(
    """
<CameraClick>:
    orientation: 'vertical'
    Camera:
        id: camera
        resolution: (640, 480)
        play: False
    ToggleButton:
        text: 'Camera on/off'
        on_press: camera.play = not camera.play
        size_hint_y: None
        height: '48dp'
    Button:
        text: 'Capture'
        size_hint_y: None
        height: '48dp'
        on_press: root.capture()
    Button:
        text: 'Analyze'
        size_hint_y: None
        height: '48dp'
        on_press: root.analyze()
"""
)


class CameraClick(BoxLayout):
    def capture(self):
        """
        Function to capture the images and give them the names
        according to their captured time and date.
        """
        camera = self.ids["camera"]
        timestr = time.strftime("%Y%m%d_%H%M%S")
        output_path = f"output/images/IMG_{timestr}.png"
        self.image_path = output_path
        camera.export_to_png(output_path)

    def analyze(self):
        cwd = Path.cwd()
        img = read_image(cwd / self.image_path)
        analyze_and_write_to_csv(analyze_mock, img, cwd / "output" / "output.csv")
