from kivy.app import App
from kivy.uix.slider import Slider
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.camera import Camera
import cv2
import numpy as np
import statistics


def coindetect(img, p1, p2):
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    img = cv2.GaussianBlur(img, (29, 29), cv2.BORDER_DEFAULT)

    circles = cv2.HoughCircles(img, cv2.HOUGH_GRADIENT, 1.45, 90, param1=p1, param2=p2, minRadius=10, maxRadius=400)
    circles_r = []
    if circles is not None:
        circles_r = np.uint16(np.around(circles))

    return circles_r


class CamApp(App):

    def build(self):
        main_layout = FloatLayout(size=(300, 300))

        self.camera = Camera(resolution=(640, 480), play=True, pos_hint={'x': 0, 'y': .25}, size_hint=(1, .65))
        main_layout.add_widget(self.camera)

        self.label = Label(text='0р', font_size=20, pos_hint={'x': .45, 'y': .9}, size_hint=(.1, .1), color=[1, 1, 1, 1])
        main_layout.add_widget(self.label)

        self.slider = Slider(min=45, max=60, value=46, pos_hint={'x': 0, 'y': .2}, size_hint=(1, .05))
        main_layout.add_widget(self.slider)
        self.slider_value = self.slider.value

        photo_button = Button(text='Photo', background_color=[0, 1, 1], font_size=20, pos_hint={'x': .15, 'y': 0}, size_hint=(.7, .2))
        photo_button.bind(on_press=self.photo)
        main_layout.add_widget(photo_button)

        return main_layout


    def photo(self, instance):
        self.camera.export_to_png("new.png")

        frame = cv2.imread("new.png")

        self.slider_value = round(self.slider.value)

        buf1 = cv2.flip(frame, 1)
        buf1 = cv2.flip(buf1, 0)
        self.fc = buf1.copy()

        self.circles = coindetect(buf1, 25, self.slider_value)


        summa = 0
        cnt = 0

        min_ten = 0
        min_ne_ten = 0

        spisok_radius_10 = []
        spisok_radius_ne10 = []

        kernel = np.array([[1, 1, 1, 1, 1],
                           [1, 1, 1, 1, 1],
                           [1, 1, 1, 1, 1],
                           [1, 1, 1, 1, 1],
                           [1, 1, 1, 1, 1]])
        kernel = kernel / sum(kernel)

        res = cv2.filter2D(self.fc, -1, kernel)

        ten = self.circles.copy()
        ne_ten = self.circles.copy()

        if len(self.circles) != 0:
            for i in self.circles[0, :]:
                kef = 1.05
                sr, sc = round(i[1] - kef * i[2]), round(i[0] - kef * i[2])

                er, ec = round(i[1] + kef * i[2]), round(i[0] + kef * i[2])

                imgm = res[sr:er, sc:ec]
                circle_ten = coindetect(imgm, 20, 40)
                if len(circle_ten) > 0:
                    ne_ten = np.delete(ne_ten, cnt - min_ne_ten, axis=1)
                    spisok_radius_10.append(i[2])
                    min_ne_ten += 1
                    summa += 10
                else:
                    ten = np.delete(ten, cnt - min_ten, axis=1)
                    min_ten += 1
                    spisok_radius_ne10.append(i[2])
                cnt += 1

            if len(spisok_radius_10) > 0:
                avg = statistics.mean(spisok_radius_10)
            else:
                avg = min(spisok_radius_ne10) / 0.93

            for i in ne_ten[0, :]:
                if i[2] > avg * 1.07:
                    summa += 5
                elif i[2] < avg * 0.93:
                    summa += 1
                else:
                    summa += 2

        self.label.text = (str(summa) + "р")


if __name__ == '__main__':
    CamApp().run()
