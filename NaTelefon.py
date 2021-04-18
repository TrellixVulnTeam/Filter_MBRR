from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.slider import Slider
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.image import Image
from kivy.clock import Clock
from kivy.graphics.texture import Texture
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.filechooser import FileChooserIconView
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


class MyApp(App):

    def build(self):
        main_layout = FloatLayout(size=(300, 300))

        self.label = Label(text='0р', font_size=20, pos_hint={'x': .45, 'y': .9}, size_hint=(.1, .1), color=[1, 1, 1, 1])
        main_layout.add_widget(self.label)

        self.file = FileChooserIconView(pos_hint={'x': 0, 'y': .25}, size_hint=(0.15, .65))
        main_layout.add_widget(self.file)

        self.img1 = Image(color=[1, 1, 1, 1], pos_hint={'x': 0.15, 'y': .25}, size_hint=(0.85, .65))
        main_layout.add_widget(self.img1)


        self.slider = Slider(min=40, max=90, value=70, pos_hint={'x': 0, 'y': .2}, size_hint=(1, .05))
        main_layout.add_widget(self.slider)
        self.slider_value = self.slider.value

        photo_button = Button(text='Photo', background_color=[0, 1, 1], font_size=20, pos_hint={'x': .15, 'y': 0}, size_hint=(.7, .2))
        photo_button.bind(on_press=self.photo)
        main_layout.add_widget(photo_button)

        self.past_frame = ''
        self.past_slider_value = 45

        Clock.schedule_interval(self.update, 1.0/60.0)
        return main_layout

    def update(self, dt):
        self.slider_value = round(self.slider.value)

        if len(self.file.selection) != 0:
            if self.file.selection[0] != self.past_frame or self.slider_value != self.past_slider_value:
                frame = cv2.imread(self.file.selection[0])
                self.past_frame = self.file.selection[0]
                self.past_slider_value = self.slider_value

                buf1 = cv2.flip(frame, 1)
                buf1 = cv2.flip(buf1, 0)
                self.fc = buf1.copy()
                self.circles = coindetect(buf1, 25, self.slider_value)

                self.hsv = cv2.cvtColor(buf1, cv2.COLOR_BGR2HSV)

                r = []
                m = []
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
                imgm = cv2.cvtColor(imgm, cv2.COLOR_RGB2BGR)
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


        print("summa = {0}".format(summa))


if __name__ == '__main__':
    MyApp().run()