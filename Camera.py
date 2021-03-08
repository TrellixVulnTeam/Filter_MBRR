from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from kivy.clock import Clock
from kivy.graphics.texture import Texture
from kivy.uix.button import Button
import cv2
import numpy as np


class CamApp(App):

    def build(self):
        self.img1 = Image(color=[1, 1, 1, 1])
        main_layout = BoxLayout(orientation="vertical")
        main_layout.add_widget(self.img1)
        self.capture = cv2.VideoCapture(0)

        photo_button = Button(text='Photo', background_color=[0, 1, 1], font_size=20)
        photo_button.bind(on_press=self.photo)
        main_layout.add_widget(photo_button)

        Clock.schedule_interval(self.update, 1.0/60.0)
        return main_layout

    def update(self, dt):
        ret, frame = self.capture.read()
        self.fc = frame.copy()

        buf1 = cv2.flip(self.fc, 1)
        buf1 = cv2.flip(buf1, 0)
        buf = buf1.tostring()

        texture1 = Texture.create(size=(frame.shape[1], frame.shape[0]), colorfmt='bgr')
        texture1.blit_buffer(buf, colorfmt='bgr', bufferfmt='ubyte')

        self.img1.texture = texture1

    def photo(self, instance):
        izobr = self.fc
        cv2.imwrite("izobr.png", izobr)


if __name__ == '__main__':
    CamApp().run()
    cv2.destroyAllWindows()