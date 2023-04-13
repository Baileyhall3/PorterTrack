from kivymd.uix.list import TwoLineAvatarIconListItem

from kivymd.app import MDApp
from kivymd.uix.dialog import MDDialog
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.pickers import MDDatePicker

from kivymd.uix.list import TwoLineAvatarIconListItem, ILeftBodyTouch
from kivymd.uix.selectioncontrol import MDCheckbox

from datetime import datetime

# To be added after creating the database
from database import Database
# Initialize db instance
db = Database()


class ListItemWithCheckbox(TwoLineAvatarIconListItem):
    '''Custom list item'''

    def __init__(self, taskid=None, **kwargs):
        super().__init__(**kwargs)
        # state a pk which we shall use link the list items with the database primary keys
        self.taskid = taskid

    def mark(self, check, the_list_item):
        '''mark the task as complete or incomplete'''
        if check.active == True:
            #the_list_item.text = the_list_item.text
            db.mark_task_as_complete(the_list_item.taskid)
        else:
            the_list_item.text = str(db.mark_task_as_incomplete(the_list_item.taskid))

    def delete_item(self, the_list_item):
        '''Delete the task'''
        self.parent.remove_widget(the_list_item)
        db.delete_task(the_list_item.taskid)# Here

class LeftCheckbox(ILeftBodyTouch, MDCheckbox):
    '''Custom left container'''
