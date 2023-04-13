from kivy.lang import Builder
import sqlite3
from kivymd.app import MDApp
from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager, Screen, NoTransition
from kivymd.uix.list import TwoLineAvatarIconListItem, ThreeLineAvatarIconListItem, ILeftBodyTouch
from kivymd.uix.selectioncontrol import MDCheckbox

from create_task import TaskWindow
from kivymd.uix.pickers import MDDatePicker, MDTimePicker
from task_card import Card
from datetime import datetime
from kivymd.uix.snackbar import Snackbar


Window.size = (400, 600)


from database import Database
# Instantiates DB class by creating db object
db = Database()


class HomeScreen(Screen):
    pass

class BookedTasks(Screen):
    pass

class WindowManager(ScreenManager):
    sm = ScreenManager(transition=NoTransition())
    pass

class ListItemWithCheckbox(ThreeLineAvatarIconListItem):
    def __init__(self, pk=None, **kwargs):
        super().__init__(**kwargs)
        self.pk = pk

    def mark_complete(self, check, the_list_item):
        self.parent.remove_widget(the_list_item)
        if check.active == True:
            db.mark_task_as_complete(the_list_item.pk)
        print("Task Completed")
        Snackbar(text="Task completed.").open()

    def delete_task(self, the_list_item):
        self.parent.remove_widget(the_list_item)
        db.delete_task(the_list_item.pk)
        print("Task deleted")
        Snackbar(text="Task deleted.").open()

    def clear_list(self, MDList):
        self.root.clear_widgets(MDList)
        db.delete_all()
        print("All tasks deleted")

class LeftCheckbox(ILeftBodyTouch, MDCheckbox):
    '''custom left container'''


class porter_track(MDApp):
    condition=''
    check_date=''
    check_time=''
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.screen = Builder.load_file('kv/all_screens.kv')


    def build(self):
        self.theme_cls.primary_palette = "Blue"
        self.theme_cls.theme_style = "Light"
        return self.screen

    def change_screen(self, screen_name):
        print (self.root.ids)
        screen_manager = self.root.ids['screen_manager']
        screen_manager.current = screen_name
        #screen_manager.transition = transition
        #sm = ScreenManager.transition = NoTransition

    # Gets and saves date
    def show_date_picker(self):
        date_dialog = MDDatePicker()
        date_dialog.bind(on_save = self.get_date)
        date_dialog.open()

    # Shows time picker
    def show_time_picker(self):
        time_dialog = MDTimePicker()
        time_dialog.bind(time = self.get_time)
        time_dialog.open()

    def on_save(self, instance, value, date_range):
        date = value.strftime('%A %d %B %Y')
        self.root.ids.day_month_yr.text = str(date)

    def open_nav_drawer(self, *args):
        nav_drawer = self.root.ids.nav_drawer
        nav_drawer.set_state("open")

    def close_nav_drawer(self, *args):
        nav_drawer = self.root.ids.nav_drawer
        nav_drawer.set_state("close")

    def check_all_fields(self):
        if self.check_time == 'ok' and self.check_date == 'ok':
            return True
        else:
            return False

    def warning(self):
        Snackbar(text="Please enter all fields.").open()

    def open_task_window(self):
        pop_screen = TaskWindow(app)
        pop_screen.open()

    def close_task_window(self, *args):
        pop_screen = TaskWindow(app)
        pop_screen.dismiss()

    def get_date(self, instance, value, date_range):  # to store the date in variables
        self.year = str(value.year)
        self.month = str(value.month)
        self.day = str(value.day)
        # adding 0 to single digit numbers in date
        if int(self.day) < 10:
            self.day = "0" + str(self.day)

        if int(self.month) < 10:
            self.month = "0" + str(self.month)

        self.day_month_yr = self.day + '/' + self.month + '/' + self.year
        self.check_date = 'ok'

    def get_time(self, instance, time):  # to store time in variables
        self.hour = str(time.hour)
        self.min = str(time.minute)
        # adding 0 to single digit numbers in time
        if int(self.hour) < 10:
            self.hour = "0" + str(self.hour)

        if int(self.min) < 10:
            self.min = "0" + str(self.min)

        self.hour_min = self.hour + ":" + self.min
        self.check_time = 'ok'

    def on_start(self):
        try:
            completed_tasks, incompleted_tasks = db.get_tasks()

            if incompleted_tasks != []:
                for task in incompleted_tasks:
                    add_task1 = ListItemWithCheckbox(
                        pk=task[0],
                        text='[b]' + task[5] + '[/b]',
                        secondary_text=task[1],
                        tertiary_text=task[2]
                    )
                    self.root.ids.container1.add_widget(add_task1)

            if completed_tasks != []:
                for task in completed_tasks:
                    add_task1 = ListItemWithCheckbox(
                        pk=task[0],
                        text='[b]' + task[5] + '[/b]',
                        secondary_text=task[1],
                        tertiary_text=task[2]
                    )
                    add_task1.ids.check.active = True
                    self.root.ids.container1.add_widget(add_task1)

        except Exception as e:
            print(e)
            pass

    def callback(self, slider_value):
        self.priority = int(slider_value)


    # Function for adding a task to the system
    def add_task(self, origin, destination, equipment, jobtype, pname, hour_min, day_month_yr, priority):
        self.origin = origin
        self.destination = destination
        self.equipment = equipment
        self.jobtype = jobtype
        self.pname = pname
        self.hour_min = hour_min
        self.day_month_yr = day_month_yr
        self.priority = priority
        #self.task_content('user')

        print(origin, destination, equipment, jobtype, pname, day_month_yr, hour_min, priority)
        created_task = db.create_task(origin, destination, equipment, jobtype, pname, day_month_yr, hour_min, priority)

        self.card = self.root.ids.box
        self.card.add_widget(
            Card(
                app,
                pk = created_task[0],
                origin = created_task[1],
                destination = created_task[2],
                equipment = created_task[3],
                jobtype = created_task[4],
                pname = created_task[5],
                time = created_task[6],
                date = created_task[7],
                priority = created_task[8]
            )
        )



    def add_task1(self, origin, destination, equipment, jobtype, pname, hour_min, day_month_yr, priority):
        created_task = db.create_task(origin, destination, equipment, jobtype, pname, day_month_yr, hour_min, priority)

        self.root.ids['container1'].add_widget(ListItemWithCheckbox(
            pk=created_task[0],
            text='[b]'+created_task[5]+'[/b]',
            secondary_text=created_task[1],
            tertiary_text=created_task[2]
        )
        )

if __name__=='__main__':
    app = porter_track()
    app.run()
