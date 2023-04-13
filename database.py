import sqlite3




class Database:
    def __init__(self):
        self.con = sqlite3.connect('pt_task_db.db')
        self.cursor = self.con.cursor()
        self.create_task_table()

    def create_task_table(self):
        self.cursor.execute("""CREATE TABLE if not exists tasks(
        id integer PRIMARY KEY AUTOINCREMENT,
        origin varchar(50) NOT NULL,
        destination varchar(50) NOT NULL,
        equipment varchar(50) NOT NULL,
        jobtype varchar(50) NOT NULL,
        pname varchar(50) NOT NULL,
        day_month_yr varchar(50) NOT NULL,
        hour_min varchar(50) NOT NULL,
        priority integer NOT NULL,
        completed BOOLEAN NOT NULL CHECK (completed IN(0, 1)))
        """)


    def create_task(self, origin, destination, equipment, jobtype, pname, day_month_yr, hour_min, priority):
        self.cursor.execute("INSERT INTO tasks(origin, destination, equipment, jobtype, pname, day_month_yr, hour_min, priority, completed) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?)",
                            (origin, destination, equipment, jobtype, pname, day_month_yr, hour_min, priority, 0))
        self.con.commit()

        # Getting the last entered item to add in the list
        created_task = self.cursor.execute("SELECT id, origin, destination, equipment, jobtype, pname, day_month_yr, hour_min, priority FROM tasks WHERE origin = ? and completed = 0",
                                           (origin,)).fetchall()
        return created_task[-1]

    '''READ / GET the tasks'''

    def get_tasks(self):
        # Getting all complete and incomplete tasks

        completed_tasks = self.cursor.execute("SELECT id, origin, destination, equipment, jobtype, pname, day_month_yr, hour_min, priority FROM tasks WHERE completed = 1").fetchall()

        incompleted_tasks = self.cursor.execute("SELECT id, origin, destination, equipment, jobtype, pname, day_month_yr, hour_min, priority FROM tasks WHERE completed = 0").fetchall()

        return incompleted_tasks, completed_tasks

    '''UPDATING the tasks status'''

    def mark_task_as_complete(self, taskid):
        self.cursor.execute("UPDATE tasks SET completed=1 WHERE id=?", (taskid,))
        self.con.commit()

    def mark_task_as_incomplete(self, taskid):
        self.cursor.execute("UPDATE tasks SET completed=0 WHERE id=?", (taskid,))
        self.con.commit()

        # returning the task text
        task_text = self.cursor.execute("SELECT task FROM tasks WHERE id=?", (taskid,)).fetchall()
        return task_text[0][0][0][0][0][0][0][0][0]

    '''Deleting the task'''
    def delete_task(self, taskid):
        self.cursor.execute("DELETE FROM tasks WHERE id=?", (taskid,))
        self.con.commit()

    def delete_all(self):
        self.cursor.execute("DELETE FROM tasks")
        self.con.commit()

    '''Closing the connection '''

    def close_db_connection(self):
        self.con.close()
