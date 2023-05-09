from kivy.config import value
from kivy.uix.popup import Popup
from kivymd.uix.floatlayout import MDFloatLayout
from kivymd.uix.textfield import MDTextField
from kivy.lang import Builder
from kivymd.uix.button import MDRaisedButton
from kivy.utils import get_color_from_hex

# Class for the porter creation window
class PorterWindow(Popup):
    def __init__(self, app, **kwargs):
        super(PorterWindow, self).__init__(**kwargs)
        self.app = app
        self.title = "Add Porter"
        self.title_size = "20dp"
        self.size_hint = (0.72, 0.62)
        self.title_align = 'center'
        self.title_color = get_color_from_hex('#4472C4')
        self.background = 'White'
        self.container = MDFloatLayout()
        self.mode = "fill"

        self.porter_surname = MDTextField(
            hint_text = "Surname...",
            size_hint = (0.4, 0.7),
            font_size = '15sp',
            pos_hint = {
                'center_x': 0.8,
                'y': 0.75
            },
            helper_text_mode = "on_focus",

        )
        self.container.add_widget(self.porter_surname)

        self.porter_firstname = MDTextField(
            hint_text="First Name...",
            size_hint=(0.4, 0.7),
            font_size='15sp',
            pos_hint={
                'center_x': 0.2,
                'y': 0.75
            },
            helper_text_mode="on_focus",
        )
        self.container.add_widget(self.porter_firstname)

        self.save_button = MDRaisedButton(
            icon = "content-save",
            text = "SAVE",
            elevation = 0,
            size_hint=(0.4, 0.01),
            pos_hint = {
                'center_x': 0.5,
                'y': 0.05
            },
        )
        self.save_button.bind(
            on_press = lambda x: self.app.add_new_porter(
                self.porter_firstname.text,
                self.porter_surname.text,
                self.app.start_time,
            ) if self.porter_firstname.text != '' and self.porter_surname.text != '' else app.warning()
        )
        self.save_button.bind(
            on_release = lambda x: self.dismiss() if self.porter_firstname.text != '' and self.porter_surname.text != ''  else self.dismiss == False
        )
        self.container.add_widget(self.save_button)

        self.kv_file=Builder.load_file('../kv/add_porter.kv')
        self.container.add_widget(self.kv_file)
        self.add_widget(self.container)
