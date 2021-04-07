from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.slider import Slider
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.image import Image
from kivy.clock import Clock
from kivy.graphics.texture import Texture
from kivy.uix.button import Button
from kivy.uix.label import Label
import cv2
import numpy as np
import statistics
from CoinDetector1 import coindetect


class CamApp(App):

    def build(self):
        self.label = Label(text='0', font_size=20, pos_hint={'x': .45, 'y': .95}, size_hint=(.1, .05))

        self.img1 = Image(color=[1, 1, 1, 1], pos_hint={'x': .15, 'y': .25}, size_hint=(.7, .7))
        main_layout = FloatLayout(size=(300, 300))
        main_layout.add_widget(self.img1)
        self.capture = cv2.VideoCapture(0)

        self.slider = Slider(min=45, max=90, value=70, orientation='vertical', pos_hint={'x': 0, 'y': 0}, size_hint=(.15, 1))
        main_layout.add_widget(self.slider)
        self.slider_value = self.slider.value

        photo_button = Button(text='Photo', background_color=[0, 1, 1], font_size=20, pos_hint={'x': .15, 'y': 0}, size_hint=(.7, .25))
        photo_button.bind(on_press=self.photo)
        main_layout.add_widget(photo_button)

        Clock.schedule_interval(self.update, 1.0/60.0)
        return main_layout

    def update(self, dt):

        ret, frame = self.capture.read()

        self.slider_value = round(self.slider.value)

        buf1 = cv2.flip(frame, 1)
        buf1 = cv2.flip(buf1, 0)
        self.fc = buf1.copy()
        self.circles = coindetect(buf1, 25, self.slider_value)

        self.hsv = cv2.cvtColor(buf1, cv2.COLOR_BGR2HSV)

        r = []
        m = []
        cnt = []
        if len(self.circles) != 0:
            for i in self.circles[0, :]:
                cv2.circle(buf1, (i[0], i[1]), i[2], (0, 255, 0), 4)
                cv2.circle(buf1, (i[0], i[1]), 2, (255, 0, 0), 7)
                r.append(int(i[2]))
                m.append((i[0], i[1]))
            r.sort()


        buf = buf1.tostring()
        texture1 = Texture.create(size=(frame.shape[1], frame.shape[0]), colorfmt='bgr')
        texture1.blit_buffer(buf, colorfmt='bgr', bufferfmt='ubyte')

        self.img1.texture = texture1

    def photo(self, instance):
        lo = (20, 90, 15)
        do = (35, 255, 255)

        summa = 0
        cnt = 0

        min_ten = 0
        min_ne_ten = 0

        spisok_radius = []

        mask = cv2.inRange(self.hsv, lo, do)
        res = cv2.bitwise_and(self.fc, self.fc, mask=mask)
        izobr = self.fc

        ten = self.circles.copy()
        ne_ten = self.circles.copy()

        for i in self.circles[0, :]:
            kef = 1.05
            sr, sc = round(i[1] - kef * i[2]), round(i[0] - kef * i[2])

            er, ec = round(i[1] + kef * i[2]), round(i[0] + kef * i[2])

            imgm = res[sr:er, sc:ec]
            circle_ten = coindetect(imgm, 20, 40)
            if len(circle_ten) > 0:
                ne_ten = np.delete(ne_ten, cnt - min_ne_ten, axis=1)
                spisok_radius.append(i[2])
                min_ne_ten += 1
                summa += 10
            else:
                ten = np.delete(ten, cnt - min_ten, axis=1)
                min_ten += 1
            cnt += 1

        print('ten:' + str(ten))
        print()
        print('neten:' + str(ne_ten))
        print()

        avg = statistics.mean(spisok_radius)

        print(avg)

        for i in ne_ten[0, :]:
            if i[2] > avg * 1.07:
                summa += 5
            elif i[2] < avg * 0.93:
                summa += 1
            else:
                summa += 2
        self.label.text = str(summa)


        print("summa = {0}".format(summa))
        cv2.imshow('orange', res)
        cv2.imwrite("izobr.png", izobr)


if __name__ == '__main__':
    CamApp().run()
    cv2.destroyAllWindows()