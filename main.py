from kivy.lang import Builder
import sqlite3
from kivymd.app import MDApp
from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager, Screen, NoTransition
from kivymd.uix.navigationdrawer import MDNavigationDrawer
from create_task import TaskWindow
from kivymd.uix.pickers import MDDatePicker, MDTimePicker
from kivymd.uix.menu import MDDropdownMenu
from task_card import Card
from task_storage import GetData
import subprocess
from datetime import datetime
from kivymd.uix.snackbar import Snackbar
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton, MDRaisedButton, MDIconButton
from kivy.utils import get_color_from_hex
from random import randint
from kivymd.toast import toast


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
        #self.root.ids.day_month_yr.text = str(datetime.now().strftime('%A %d %B %Y'))
        self.screen = Builder.load_file('all_screens.kv')


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

    def on_save_time(self, instance, value, time_range):
        time = value.strftime("%H:%M:%S")
        self.root.ids.hour_min.text = str(time)


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

    def mark(self, check, Card):
        if check.active == False:
            db.mark_task_as_complete(Card.taskid)
        else:
            Card.text = str(db.mark_task_as_incomplete(Card.taskid))

    def delete_task(self, condition):
        if condition == 'complete':
            pass
        elif condition == 'delete':
            db.delete_task(Card.taskid)


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
        '''This is to load the saved tasks and add them to list widget'''
        try:
            completed_tasks, incompleted_tasks = db.get_tasks()

            if incompleted_tasks != []:
                for task in incompleted_tasks:
                    add_task = Card(
                        app,
                        taskid = task[0],
                        origin = task[1],
                        destination = task[2],
                        equipment = task[3],
                        jobtype = task[4],
                        pname = task[5],
                        time = task[6],
                        date = task[7],
                        priority = task[8]
                    )
                    self.root.ids.box.add_widget(add_task)

            if completed_tasks != []:
                for task in completed_tasks:
                    add_task = Card(
                        app,
                        taskid=task[0],
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
                    self.root.ids.box.add_widget(add_task)

        except Exception as e:
            print(e)
            pass

    def callback(self, slider_value):
        self.priority = int(slider_value)

    def notification_show(self, condition):
        self.condition = condition


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
                taskid = created_task[0],
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
        #origin.text = ''
        #destination.text = ''
        #equipment.text = ''
        #jobtype.text = ''
        #pname.text = ''

    def delete_all(self):
        self.dialog = MDDialog(
            title = "Clear all tasks?",
            text = "This will remove all tasks and restart application.",
            buttons = [
                MDFlatButton(
                    text = "CANCEL",
                    on_release = lambda x: self.dialog.dismiss()
                ),
                MDRaisedButton(
                    text = "DELETE",
                    md_bg_color = get_color_from_hex('FF0000'),
                    on_press = lambda x: self.restart(),
                    on_release = lambda x: self.dialog.dismiss()
                ),
            ],
        )
        self.dialog.open()




    def delcompleted_dialog_box(self):
        self.delcompleted_dialog = MDDialog(
            title = "Clear all completed tasks?",
            text = "This will delete all tasks which have been completed.",
            buttons = [
                MDFlatButton(
                    text = "CANCEL",
                    on_release = lambda x: self.delcompleted_dialog.dismiss()
                ),
                MDRaisedButton(
                    text = "DELETE",
                    md_bg_color = get_color_from_hex('FF0000'),
                    on_press = lambda x: self.delete_completed(),
                    on_release = lambda x: self.delcompleted_dialog.dismiss()
                ),
            ],
        )
        self.delcompleted_dialog.open()

    def delete_completed(self):
        delete = open('db_files\\completed_tasks.txt', 'w')
        delete.write('COMPLETED TASKS: ')
        toast("Successfully deleted all completed tasks")




if __name__=='__main__':
    app = porter_track()
    app.run()
