from kivy.lang import Builder
import sqlite3
from kivymd.app import MDApp
from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager, Screen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.card import MDCard
from kivymd.uix.dialog import MDDialog
from kivymd.uix.label import MDLabel
from kivymd.uix.list import TwoLineAvatarIconListItem, ThreeLineAvatarIconListItem, ILeftBodyTouch, \
    ThreeLineRightIconListItem
from kivymd.uix.selectioncontrol import MDCheckbox
from create_task import TaskWindow
from add_porter import PorterWindow
from kivymd.uix.pickers import MDDatePicker, MDTimePicker
from datetime import datetime
from kivymd.uix.snackbar import Snackbar


Window.size = (400, 600)

# Instantiates DB class by creating db object
from database import Database
db = Database()

class WindowManager(ScreenManager):
    pass

class MainScreen(Screen):
    pass

class LoginScreen(Screen):
    pass

# Class for the task entity
class ListItemWithCheckbox(ThreeLineAvatarIconListItem):
    task_info_dialog = None
    def __init__(self, pk=None, **kwargs):
        super().__init__(**kwargs)
        self.pk = pk

    # Marks an item as complete
    def mark_complete(self, check, the_list_item):
        if check.active == True:
            db.mark_task_as_complete(the_list_item.pk)
        else:
            the_list_item.text = str(db.mark_task_as_incomplete(the_list_item.pk))
        self.parent.remove_widget(the_list_item)
        print("Task Completed")
        Snackbar(text="Task completed.").open()

    # Deletes task from the system
    def delete_task(self, the_list_item):
        self.parent.remove_widget(the_list_item)
        db.delete_task(the_list_item.pk)
        print("Task deleted")
        Snackbar(text="Task deleted.").open()

    def clear_list(self, MDList):
        self.root.clear_widgets(MDList)
        db.delete_all()
        print("All tasks deleted")

    def show_task_info_dialog(self):
        if not self.task_info_dialog:
            self.task_info_dialog = MDDialog(
                type = "custom",
                content_cls = DialogContent(),
            )
        self.task_info_dialog.open()


class LeftCheckbox(ILeftBodyTouch, MDCheckbox):
    '''custom left container'''

class DialogContent(MDBoxLayout):
    '''Dialog box for task_info'''

# Class for the porter entity
class ThreeLineListItem1(TwoLineAvatarIconListItem):
        '''Porter List item'''
        def __init__(self, pk=None, **kwargs):
            super().__init__(**kwargs)
            self.pk = pk

        def remove_porter(self, porter_list_item):
            self.parent.remove_widget(porter_list_item)
            db.remove_porter(porter_list_item.pk)
            print("Porter removed")
            Snackbar(text="Porter logged out.").open()


# Main App class for running PorterTrack
class porter_track(MDApp):
    condition=''
    check_date=''
    check_time=''
    task_info_dialog = None

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.screen = Builder.load_file('../kv/all_screens.kv')
        #self.screen = Builder.load_file('kv/login.kv')

    # Holds the styling for the file
    def build(self):
        self.theme_cls.primary_palette = "Blue"
        self.theme_cls.theme_style = "Light"
        return self.screen

    # Changes the screen to the target screen
    def change_screen(self, screen_name):
        print (self.root.ids)
        screen_manager = self.root.ids['screen_manager']
        screen_manager.current = screen_name

    def close_dialog(self, *args):
        self.task_info_dialog.dismiss()

    # Shows date picker
    def show_date_picker(self):
        date_dialog = MDDatePicker()
        date_dialog.bind(on_save = self.get_date)
        date_dialog.open()

    # Shows time picker
    def show_time_picker(self):
        time_dialog = MDTimePicker()
        time_dialog.bind(time = self.get_time)
        time_dialog.open()

    # Shows start time picker
    def show_start_time_picker(self):
        time_dialog = MDTimePicker()
        time_dialog.bind(time=self.get_start_time)
        time_dialog.open()

    # Function that calls when the date picker is interacted with
    def on_save(self, instance, value, date_range):
        date = value.strftime('%A %d %B %Y')
        self.root.ids.day_month_yr.text = str(date)

    # Opens the navigation drawer for the user to select a screen
    def open_nav_drawer(self, *args):
        nav_drawer = self.root.ids.nav_drawer
        nav_drawer.set_state("open")

    # Closes the navigation drawer
    def close_nav_drawer(self, *args):
        nav_drawer = self.root.ids.nav_drawer
        nav_drawer.set_state("close")

    # Function to check all fields of the task window have been entered
    def check_all_fields(self):
        if self.check_time == 'ok' and self.check_date == 'ok':
            return True
        else:
            return False

    # If the user has not entered any fields of the task window, display warning
    def warning(self):
        Snackbar(text="Please enter all fields.").open()

    # Opens the task window
    def open_task_window(self):
        pop_screen = TaskWindow(app)
        pop_screen.open()

    # Closes the task window
    def close_task_window(self, *args):
        pop_screen = TaskWindow(app)
        pop_screen.dismiss()

    # Opens the porter creation window
    def open_porter_window(self):
        pop_screen = PorterWindow(app)
        pop_screen.open()

    # Closes the porter creation window
    def close_porter_window(self, *args):
        pop_screen = PorterWindow(app)
        pop_screen.dismiss()

    # Checks the entered fields of the login page against the credentials
    def check_login_details(self):
        if self.root.ids.user.text == "Bailey" and self.root.ids.password.text == "1234":
            self.change_screen('main')
            Snackbar(text="Successfully logged in as "+ self.root.ids.user.text).open()
        else:
            Snackbar(text="Invalid login credentials.").open()
            self.clear()

    # Clears the entered text from the login fields
    def clear(self):
        self.root.ids.user.text = ""
        self.root.ids.password.text = ""

    # Gets the value from the priority slider
    def callback(self, slider_value):
        self.priority = int(slider_value)

    # Function to store date in variables
    def get_date(self, instance, value, date_range):
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

    # Function to store time in variables
    def get_time(self, instance, time):
        self.hour = str(time.hour)
        self.min = str(time.minute)
        # adding 0 to single digit numbers in time
        if int(self.hour) < 10:
            self.hour = "0" + str(self.hour)

        if int(self.min) < 10:
            self.min = "0" + str(self.min)

        self.hour_min = self.hour + ":" + self.min
        self.check_time = 'ok'

    # Gets and saves the porter's start time
    def get_start_time(self, instance, time):
        self.hour = str(time.hour)
        self.min = str(time.minute)
        # adding 0 to single digit numbers in time
        if int(self.hour) < 10:
            self.hour = "0" + str(self.hour)

        if int(self.min) < 10:
            self.min = "0" + str(self.min)

        self.start_time = self.hour + ":" + self.min

    def empty_comp_tasks(self, empty_comp):
        incompleted_tasks = db.get_tasks()
        if incompleted_tasks == []:
            self.root.ids.notask.text = 'No tasks to show.'

    # On system start, loads up task lists
    def on_start(self):
        try:
            completed_tasks, incompleted_tasks = db.get_tasks()

            if completed_tasks != []:
                for task in incompleted_tasks:
                    add_task = ListItemWithCheckbox(
                        pk=task[0],
                        text='[b]' + task[5] + '[/b]',
                        secondary_text='From: ' + task[1],
                        tertiary_text= 'To: ' + task[2]
                    )
                    add_task.ids.check.active = True
                    self.root.ids.container2.add_widget(add_task)

            if incompleted_tasks != []:
                for task in completed_tasks:
                    add_task = ListItemWithCheckbox(
                        pk=task[0],
                        text='[b]' + task[5] + '[/b]',
                        secondary_text='From: ' + task[1],
                        tertiary_text='To: ' + task[2]
                    )
                    add_task.ids.check.active = False
                    self.root.ids.container1.add_widget(add_task)


            available_porters, unavailable_porters = db.get_porters()

            if available_porters != []:
                for porter in available_porters:
                    add_new_porter = ThreeLineListItem1(
                        pk=porter[0],
                        text ='[b]'+porter[1]+' '+ porter[2]+'[/b]',
                        secondary_text = 'Start time: ' + porter[3],
                    )
                    self.root.ids.p_container.add_widget(add_new_porter)

            if unavailable_porters != []:
                for porter in unavailable_porters:
                    add_new_porter = ThreeLineListItem1(
                        pk=porter[0],
                        text ='[b]'+porter[1]+' '+ porter[2]+'[/b]',
                        secondary_text = 'Start time: ' + porter[3],
                    )
                    self.root.ids.p_container.add_widget(add_new_porter)

        except Exception as e:
            print(e)
            pass


    # Function for adding task to the system
    def add_task(self, origin, destination, equipment, jobtype, pname, day_month_yr, hour_min, priority):
        created_task = db.create_task(origin, destination, equipment, jobtype, pname, day_month_yr, hour_min, priority)

        self.root.ids['container1'].add_widget(ListItemWithCheckbox(
            pk=created_task[0],
            text ='[b]'+created_task[5]+'[/b]',
            secondary_text = 'From: ' + created_task[1],
            tertiary_text = 'To: ' + created_task[2]
        )
        )


    # Function for adding a porter to the system
    def add_new_porter(self, porter_firstname, porter_surname, start_time):
        new_porter = db.add_porter(porter_firstname, porter_surname, start_time)

        self.root.ids['p_container'].add_widget(ThreeLineListItem1(
            pk=new_porter[0],
            text ='[b]'+new_porter[1]+' '+ new_porter[2]+'[/b]',
            secondary_text = 'Start time: ' + new_porter[3],
        )
        )


if __name__=='__main__':
    app = porter_track()
    app.run()
