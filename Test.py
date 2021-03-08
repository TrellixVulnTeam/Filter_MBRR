from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from kivy.clock import Clock
from kivy.graphics.texture import Texture
import cv2
import numpy as np


class CamApp(App):

    def build(self):
        self.img1 = Image()
        main_layout = BoxLayout(orientation="vertical")
        main_layout.add_widget(self.img1)
        self.capture = cv2.VideoCapture(0)

        Clock.schedule_interval(self.update, 1.0/33.0)
        return main_layout

    def update(self, dt):
        ret, frame = self.capture.read()
        fc = frame.copy()

        kernel = np.array([[1, 1, 1, 1, 1],
                           [1, 1, 1, 1, 1],
                           [1, 1, 1, 1, 1],
                           [1, 1, 1, 1, 1],
                           [1, 1, 1, 1, 1]])
        kernel = kernel / sum(kernel)

        # filter the source image
        fc = cv2.filter2D(fc, -1, kernel)


        buf1 = cv2.flip(fc, 0)
        buf = buf1.tostring()

        texture1 = Texture.create(size=(frame.shape[1], frame.shape[0]), colorfmt='bgr')
        texture1.blit_buffer(buf, colorfmt='bgr', bufferfmt='ubyte')

        self.img1.texture = texture1


if __name__ == '__main__':
    CamApp().run()
    cv2.destroyAllWindows()