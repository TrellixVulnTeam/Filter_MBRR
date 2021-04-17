from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.slider import Slider
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.image import Image
from kivy.clock import Clock
from kivy.graphics.texture import Texture
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.camera import Camera
from kivy.lang import Builder
import cv2
import numpy as np
import statistics
import time
from CoinDetector1 import coindetect


class CamApp(App):

    def build(self):
        main_layout = FloatLayout(size=(300, 300))

        self.camera = Camera(resolution=(640, 480), play=True, pos_hint={'x': 0, 'y': .25}, size_hint=(1, .65))

        photo_button = Button(text='Photo', background_color=[0, 1, 1], font_size=20, pos_hint={'x': .15, 'y': 0}, size_hint=(.7, .2))
        photo_button.bind(on_press=self.photo)
        main_layout.add_widget(photo_button)

        return main_layout
    def photo(self, instance):
        print(self.camera.export_to_png())



if __name__ == '__main__':
    CamApp().run()
    cv2.destroyAllWindows()