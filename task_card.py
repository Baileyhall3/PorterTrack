from kivymd.uix.card import MDCard
from kivymd.uix.floatlayout import MDFloatLayout
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDFillRoundFlatIconButton, MDFloatingActionButton, MDFlatButton, MDRaisedButton
from kivymd.uix.expansionpanel import MDExpansionPanel, MDExpansionPanelOneLine, MDExpansionPanelThreeLine
from kivymd.uix.list import TwoLineListItem, ThreeLineListItem
from task_storage import GetData
from kivymd.uix.chip import MDChip
from kivy.utils import get_color_from_hex
from kivymd.uix.label import MDLabel


class Content(MDBoxLayout):
    '''Custom content'''
class Card(MDCard):
    def __init__(self, app, origin, destination, equipment, jobtype, pname, day_month_yr, hour_min, priority, taskid, **kwargs):
        super(Card, self).__init__(**kwargs)
        self.app = app
        self.taskid = taskid
        self.origin = origin
        self.destination = destination
        self.equipment = equipment
        self.jobtype = jobtype
        self.pname = pname
        self.day_month_yr = day_month_yr
        self.hour_min = hour_min
        self.priority = priority
        self.orientation = 'vertical'
        self.size_hint_y = None
        self.height = 150
        self.float = MDFloatLayout()

        self.data = GetData(
            self.priority,
            self.origin,
            self.destination,
            self.equipment,
            self.jobtype,
            self.pname,
            self.day_month_yr,
            self.hour_min,
            self.priority
        )
        self.data.get_data()


        self.box = MDBoxLayout(
            orientation = 'horizontal',
            size_hint = (0.4, 0.2),
            pos_hint = {
                "y": 0.9,
                "x": 0.75
            },
            spacing = 7,
            #background = 'White',
            padding = 8
        )

        self.task_info = MDExpansionPanel(
            content = TwoLineListItem(
                text = self.jobtype,
                secondary_text = "Using: " + self.equipment
            ),
            panel_cls = MDExpansionPanelThreeLine(
                text = self.pname,
                secondary_text = "From: " + self.origin,
                tertiary_text = "To: " + self.destination
            ),
            pos_hint = {
                "center_x": 0.5,
                "center_y": 0.56
            },
            size_hint = (0.96, 1)
        )
        self.float.add_widget(self.task_info)


        self.complete = MDFillRoundFlatIconButton(
            icon = 'calendar-check',
            text = "Save",
            size_hint = (None, None),
            size = (35, 35),
            #elevation=10,
            theme_text_color = 'Custom',
            text_color = [1, 1, 1, 1]
        )
        self.complete.bind(
            on_press = lambda x: self.app.mark(app.check, Card)
        )
        self.box.add_widget(self.complete)


        self.delete = MDFillRoundFlatIconButton(
            icon = 'delete',
            text = "Delete",
            size_hint = (None, None),
            size = (35, 35),
            #elevation=10,
            theme_text_color = 'Custom',
            text_color = [1, 1, 1, 1],
            md_bg_color = get_color_from_hex('#E3242B')
        )
        self.delete.bind(
            on_press = lambda x: self.app.delete_task(Card, 'delete')
        )
        self.box.add_widget(self.delete)


        self.imp = MDChip(
            text="Imp",
            #icon = '',
            pos_hint = {
                "x": 0.8,
                "y": 0.1
            },
            #color = get_color_from_hex('#3944BC')
        )
        if int(self.priority) == 2 or int(self.priority) == 3 or int(self.priority) == 4:
            self.float.add_widget(self.imp)

        self.float.add_widget(self.box)
        self.add_widget(self.float)


