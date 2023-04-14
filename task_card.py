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

    def __init__(self, app, origin, destination, equipment, jobtype, pname, date, time, priority, pk=None, **kwargs):
        super(Card, self).__init__(**kwargs)
        self.app = app
        self.pk = pk
        self.origin = origin
        self.destination = destination
        self.equipment = equipment
        self.jobtype = jobtype
        self.pname = pname
        self.date = date
        self.time = time
        self.priority = priority
        self.orientation = 'vertical'
        self.size_hint_y = None
        self.height = 150
        self.float = MDFloatLayout()


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


        # Container for the task
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


        # Button for completing a task
        self.complete = MDFillRoundFlatIconButton(
            icon = 'calendar-check',
            text = "Complete",
            size_hint = (None, None),
            size = (35, 35),
            #elevation=10,
            theme_text_color = 'Custom',
            text_color = [1, 1, 1, 1]
        )
        self.complete.bind(
            on_press = lambda x: self.app.mark_complete(Card)
        )
        self.box.add_widget(self.complete)


        # Button for cancelling/deleting a task
        self.delete = MDFillRoundFlatIconButton(
            icon = 'delete',
            text = "Cancel",
            size_hint = (None, None),
            size = (35, 35),
            #elevation=10,
            theme_text_color = 'Custom',
            text_color = [1, 1, 1, 1],
            md_bg_color = get_color_from_hex('#E3242B')
        )
        self.delete.bind(
            on_press = lambda x: self.app.delete_task()
        )
        self.box.add_widget(self.delete)

        # Adds the box widget to the screen
        self.float.add_widget(self.box)
        self.add_widget(self.float)





