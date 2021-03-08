from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
import random


class Random_generator(App):
    def build(self):
        main_layout = BoxLayout(orientation="vertical")
        self.min = TextInput(multiline=False, halign="right", font_size=22)
        self.max = TextInput(multiline=False, halign="right", font_size=22)
        label_min = Label(text='min', font_size=20)
        label_max = Label(text='max', font_size=20)

        n_layout = BoxLayout()
        n_layout.add_widget(label_min)
        n_layout.add_widget(self.min)
        main_layout.add_widget(n_layout)

        n_layout = BoxLayout()
        n_layout.add_widget(label_max)
        n_layout.add_widget(self.max)
        main_layout.add_widget(n_layout)

        n_layout = BoxLayout()
        generate_button = Button(text='Generate', background_color=[0, 1, 1], font_size=20)
        generate_button.bind(on_press=self.on_generate)
        self.res = TextInput(readonly=True, font_size=16)
        n_layout.add_widget(generate_button)
        n_layout.add_widget(self.res)
        main_layout.add_widget(n_layout)

        clear_button = Button(text='Clear', background_color=[1, 0, 1], font_size=20)
        clear_button.bind(on_press=self.on_clear)
        main_layout.add_widget(clear_button)

        return main_layout

    def on_generate(self, instance):
        current_min = self.min.text
        current_max = self.max.text
        if current_max.isdigit() and current_min.isdigit():
            if int(current_min) <= int(current_max):
                sol = random.randint(int(current_min), int(current_max))
                self.res.text += '\n' + str(sol)

    def on_clear(self, instance):
        self.res.text = ''


if __name__ == "__main__":
    app = Random_generator()
    app.run()