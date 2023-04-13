from kivy.config import value
from kivy.uix.popup import Popup
from kivymd.uix.floatlayout import MDFloatLayout
from kivymd.uix.slider import MDSlider
from kivymd.uix.textfield import MDTextField
from kivy.lang import Builder
from kivymd.uix.button import MDFloatingActionButton, MDIconButton, MDRaisedButton, MDFlatButton, MDFillRoundFlatIconButton
from kivy.utils import get_color_from_hex
from kivymd.uix.tooltip import MDTooltip
#from kivymd.uix.chip import MDChip

class TooltipMDIconButton(MDIconButton, MDTooltip):
    pass

class TaskWindow(Popup):
    def __init__(self, app, **kwargs):
        super(TaskWindow, self).__init__(**kwargs)
        self.app = app
        self.title = "Create New Task"
        self.title_size = "20dp"
        self.size_hint = (0.82, 0.82)
        self.title_align = 'center'
        self.title_color = get_color_from_hex('#4472C4')
        self.background = 'White'
        self.container = MDFloatLayout()
        self.mode = "fill"

        self.origin = MDTextField(
            hint_text = "From...",
            size_hint = (0.4, 1),
            font_size = '15sp',
            pos_hint = {
                'center_x': 0.8,
                'y': 0.85
            },
            helper_text_mode = "on_focus",
            #mode = "fill",
            #text_color = get_color_from_hex('#000000')

        )
        #self.origin.focus = True
        self.container.add_widget(self.origin)


        self.destination = MDTextField(
            hint_text="To...",
            size_hint=(0.4, 1),
            font_size='15sp',
            pos_hint={
                'center_x': 0.2,
                'y': 0.85
            },
            helper_text_mode="on_focus",
        )
        self.container.add_widget(self.destination)


        self.equipment = MDTextField(
            hint_text="Using...",
            size_hint=(0.4, 1),
            font_size='15sp',
            pos_hint={
                'center_x': 0.2,
                'y': 0.7
            },
            helper_text_mode="on_focus",
        )
        self.container.add_widget(self.equipment)

        self.jobtype = MDTextField(
            hint_text="Job Type...",
            size_hint=(0.4, 1),
            font_size='15sp',
            pos_hint={
                'center_x': 0.8,
                'y': 0.7
            },
            helper_text_mode="on_focus",

        )
        self.container.add_widget(self.jobtype)


        self.pname = MDTextField(
            hint_text="Patient Name...",
            size_hint=(0.98, 1),
            font_size='15sp',
            pos_hint={
                'center_x': 0.5,
                'y': 0.56
            },
            helper_text_mode="on_focus",
        )
        self.container.add_widget(self.pname)


        self.save_button = MDFloatingActionButton(
            icon = "content-save",
            md_bg_color=get_color_from_hex('#4472C4'),
            pos_hint = {
                'x': 0.75,
                'y': 0.01
            },
        )
        self.save_button.bind(
            on_press = lambda x: self.app.add_task1(
                self.origin.text,
                self.destination.text,
                self.equipment.text,
                self.jobtype.text,
                self.pname.text,
                self.app.day_month_yr,
                self.app.hour_min,
                self.app.priority
            ) if self.origin.text != '' and self.destination.text != '' and self.equipment.text != '' and self.jobtype.text != '' and self.pname.text != '' and app.check_all_fields() == True else app.warning()
        )
        self.save_button.bind(
            on_release = lambda x: self.dismiss() if self.origin.text != '' and self.destination.text != '' and self.equipment.text != '' and self.jobtype.text != '' and self.pname.text != '' and app.check_all_fields() == True else self.dismiss == False
        )
        self.container.add_widget(self.save_button)


        self.cancel_button = MDFloatingActionButton(  # to go back to previous screen
            icon="arrow-left-circle-outline",
            #tooltip_text='back',
            font_size="40sp",
            md_bg_color=get_color_from_hex('#4472C4'),
            pos_hint={
                'x': 0.001,
                'y': 0.001
            },
        )
        self.cancel_button.bind(
            on_release = lambda x: self.dismiss()
        )
        self.container.add_widget(self.cancel_button)

        self.kv_file=Builder.load_file('kv/task_window.kv')
        self.container.add_widget(self.kv_file)
        self.add_widget(self.container)
