from datetime import datetime
from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.core.window import Window
from kivymd.uix.dialog import MDDialog
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.pickers import MDDatePicker, MDTimePicker
from kivymd.uix.list import TwoLineAvatarIconListItem, ILeftBodyTouch
from kivymd.uix.selectioncontrol import MDCheckbox

Window.size = (400, 600)

from database import Database
# Instantiates DB class by creating db object
db = Database()




class DialogContent(MDBoxLayout):

    # init function for class constructor
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        #self.ids.date_text.text = str(datetime.now().strftime('%A %d %B %Y'))


    def on_save(self, instance, value, time_range):
        date = value.strftime('%A %d %B %Y')
        self.ids.date_text.text = str(date)

    def show_date_picker(self):
        date_dialog = MDDatePicker()
        date_dialog.bind(on_save = self.get_date)
        date_dialog.open()

    # Shows time picker
    def show_time_picker(self):
        time_dialog = MDTimePicker()
        time_dialog.bind(time = self.get_time)
        time_dialog.open()

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

# Class for marking / deleting list item
class ListItemWithCheckbox(TwoLineAvatarIconListItem):

    def __init__(self, pk=None, **kwargs):
        super().__init__(**kwargs)
        self.pk = pk

    # Marks item as complete
    def mark(self, check, the_list_item):
        if check.active == False:
            #the_list_item.text = '[s]' + the_list_item.text + ['/s']
            db.mark_task_as_complete(the_list_item.pk)
        else:
            the_list_item.text = str(db.mark_task_as_incomplete(the_list_item.pk))

    # Deletes a list item
    def delete_item(self, the_list_item):
        self.parent.remove_widget(the_list_item)
        db.delete_task(the_list_item.pk)

class LeftCheckbox(ILeftBodyTouch, MDCheckbox):
    '''custom left container'''

class MainApp(MDApp):
    task_list_dialog = None

    # Build function for theme
    def build(self):
        self.theme_cls.primary_palette = "Blue"
        self.theme_cls.theme_style = "Light"
        #self.theme_cls.icon_color = "Blue"

    # Show task function
    def show_task_dialog(self):
        if not self.task_list_dialog:
            self.task_list_dialog = MDDialog(
                title = "Create Task",
                type = "custom",
                content_cls = DialogContent()
            )

        self.task_list_dialog.open()


    def on_start(self):
        '''This is to load the saved tasks and add them to list widget'''
        try:
            completed_tasks, incompleted_tasks = db.get_tasks()

            if incompleted_tasks != []:
                for task in incompleted_tasks:
                    add_task = ListItemWithCheckbox(pk = task[0], text=task[1], secondary_text = task[2])
                    self.root.ids.container.add_widget(add_task)

            if completed_tasks != []:
                for task in completed_tasks:
                    add_task = ListItemWithCheckbox(pk = task[0], text = task[1], secondary_text = task[2])
                    add_task.ids.check.active = True
                    self.root.ids.container.add_widget(add_task)

        except Exception as e:
            print(e)
            pass


    # Closes dialog
    def close_dialog(self, *args):
        self.task_list_dialog.dismiss()


    # Adds task to system
    def add_task(self, task, task_time):
        print(task.text, task_time)
        created_task = db.create_task(task.text, task_time)

        self.root.ids['container'].add_widget(ListItemWithCheckbox(pk=created_task[0],
                                                                   text=created_task[1],
                                                                   secondary_text=created_task[2]))
        task.text = ''




#if __name__ == "main":
app = MainApp()
app.run()
