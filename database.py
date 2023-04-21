import sqlite3

class Database:
    def __init__(self):
        self.con = sqlite3.connect('porter_track_db.db')
        self.cursor = self.con.cursor()
        self.create_task_table()
        self.create_porter_table()
    def create_porter_table(self):
        self.cursor.execute("""CREATE TABLE if not exists porters(
        porter_id integer PRIMARY KEY AUTOINCREMENT,
        porter_firstname varchar(50) NOT NULL,
        porter_surname varchar(50) NOT NULL,
        start_time varchar(50) NOT NULL,
        tasks_completed integer NOT NULL,
        available BOOLEAN NOT NULL CHECK (available IN(0, 1)),
        supervisor BOOLEAN NOT NULL CHECK (supervisor IN(0, 1)) 
        )""")

    def add_porter(self, porter_firstname, porter_surname, start_time):
        self.cursor.execute("INSERT INTO porters(porter_firstname, porter_surname, start_time, tasks_completed, available, supervisor) VALUES(?, ?, ?, ?, ?, ?)",
                            (porter_firstname, porter_surname, start_time, 0, 1, 0))
        self.con.commit()

        # Getting the last entered item to add in the list
        new_porter = self.cursor.execute("SELECT porter_id, porter_firstname, porter_surname, start_time FROM porters WHERE porter_firstname = ? and available = 1",
                                         (porter_firstname,)).fetchall()
        return new_porter[-1]

    def get_porters(self):
        # Getting all available and unavailable porters
        available_porters = self.cursor.execute("SELECT porter_id, porter_firstname, porter_surname, start_time, tasks_completed, available FROM porters WHERE available = 1").fetchall()

        unavailable_porters = self.cursor.execute("SELECT porter_id, porter_firstname, porter_surname, start_time, tasks_completed, available FROM porters WHERE available = 0").fetchall()

        return unavailable_porters, available_porters

    def mark_porter_available(self, p_id):
        self.cursor.execute("UPDATE porters SET available=1 WHERE porter_id=?", (p_id,))
        self.con.commit()

    def mark_porter_unavailable(self, p_id):
        self.cursor.execute("UPDATE porters SET available=0 WHERE porter_id=?", (p_id,))
        self.con.commit()

    def mark_supervisor(self, p_id):
        self.cursor.execute("UPDATE porters SET supervisor=1 WHERE porter_id=?", (p_id,))
        self.con.commit()

    def remove_porter(self, p_id):
        self.cursor.execute("DELETE FROM porters WHERE porter_id=?", (p_id,))
        self.con.commit()


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
        completed BOOLEAN NOT NULL CHECK (completed IN(0, 1)),
        assigned_porter integer NULL,
        FOREIGN KEY(assigned_porter) REFERENCES porters(porter_id)
        )""")


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

    def get_task_info(self):
        task_info = self.cursor.execute("SELECT id, origin, destination, equipment, jobtype, pname, day_month_yr, hour_min, priority FROM tasks")
        return task_info


    '''UPDATING the tasks status'''
    def mark_task_as_complete(self, taskid):
        self.cursor.execute("UPDATE tasks SET completed=1 WHERE id=?", (taskid,))
        self.con.commit()

    def mark_task_as_incomplete(self, taskid):
        self.cursor.execute("UPDATE tasks SET completed=0 WHERE id=?", (taskid,))
        self.con.commit()

        #task_text = self.cursor.execute("SELECT task FROM tasks WHERE id=?", (taskid,)).fetchall()
        #return task_text[0][0][0][0][0][0][0][0][0]

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
