from kivy.lang import Builder
import sqlite3
from kivymd.app import MDApp
from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager, Screen, NoTransition
from kivymd.uix.list import TwoLineAvatarIconListItem
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
                    add_task = Card(
                        app,
                        pk = task[0],
                        origin = task[1],
                        destination = task[2],
                        equipment = task[3],
                        jobtype = task[4],
                        pname = task[5],
                        time = task[6],
                        date = task[7],
                        priority = task[8]
                    )
                    self.root.ids.tasklist.add_widget(add_task)

            if completed_tasks != []:
                for task in completed_tasks:
                    add_task = Card(
                        app,
                        pk=task[0],
                        origin=task[1],
                        destination=task[2],
                        equipment=task[3],
                        jobtype=task[4],
                        pname=task[5],
                        time=task[6],
                        date=task[7],
                        priority=task[8]
                    )
                    add_task.ids.check.active = True
                    self.root.ids.tasklist.add_widget(add_task)

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

        def mark_complete(self, Card):
            db.mark_task_as_complete(Card.taskid)
            self.card.remove_widget(Card)
            print("Task Completed")

        def delete_task(self, card_info):
            db.delete_task(card_info.pk)
            print("Task deleted")
            self.card = self.root.ids.card_info
            self.card.remove_widget(card_info)


if __name__=='__main__':
    app = porter_track()
    app.run()
