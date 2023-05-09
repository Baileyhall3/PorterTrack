import sqlite3

# [1] Class for the project's DB
class Database:

    # Initialises the DB
    def __init__(self):
        self.con = sqlite3.connect('portertrack.db')
        self.cursor = self.con.cursor()
        self.create_task_table()
        self.create_porter_table()

    # Adds the porters table to the DB
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

    # Function for adding a porter to the system
    def add_porter(self, porter_firstname, porter_surname, start_time):
        self.cursor.execute("INSERT INTO porters(porter_firstname, porter_surname, start_time, tasks_completed, available, supervisor) VALUES(?, ?, ?, ?, ?, ?)",
                            (porter_firstname, porter_surname, start_time, 0, 1, 0))
        self.con.commit()

        # Getting the last entered item to add in the list
        new_porter = self.cursor.execute("SELECT porter_id, porter_firstname, porter_surname, start_time FROM porters WHERE porter_firstname = ? and available = 1",
                                         (porter_firstname,)).fetchall()
        return new_porter[-1]

    # Gets all available and unavailable porters to display
    def get_porters(self):
        # Getting all available and unavailable porters
        available_porters = self.cursor.execute("SELECT porter_id, porter_firstname, porter_surname, start_time, tasks_completed, available FROM porters WHERE available = 1 ORDER BY start_time").fetchall()

        unavailable_porters = self.cursor.execute("SELECT porter_id, porter_firstname, porter_surname, start_time, tasks_completed, available FROM porters WHERE available = 0").fetchall()

        return unavailable_porters, available_porters

    # Marks a porter as available (sets the value to 1)
    def mark_porter_available(self, p_id):
        self.cursor.execute("UPDATE porters SET available=1 WHERE porter_id=?", (p_id,))
        self.con.commit()

    # Marks a porter as unavailable (sets the value to 0)
    def mark_porter_unavailable(self, p_id):
        self.cursor.execute("UPDATE porters SET available=0 WHERE porter_id=?", (p_id,))
        self.con.commit()

    # Marks the porter as a supervisor (sets the value to 1)
    def mark_supervisor(self, p_id):
        self.cursor.execute("UPDATE porters SET supervisor=1 WHERE porter_id=?", (p_id,))
        self.con.commit()

    # Removes a porter from the system
    def remove_porter(self, p_id):
        self.cursor.execute("DELETE FROM porters WHERE porter_id=?", (p_id,))
        self.con.commit()


    # Creates the tasks table and adds it to DB
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


    # Function for adding a task to the system
    def create_task(self, origin, destination, equipment, jobtype, pname, day_month_yr, hour_min, priority):
        self.cursor.execute("INSERT INTO tasks(origin, destination, equipment, jobtype, pname, day_month_yr, hour_min, priority, completed) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?)",
                            (origin, destination, equipment, jobtype, pname, day_month_yr, hour_min, priority, 0))
        self.con.commit()

        # Getting the last entered item to add in the list
        created_task = self.cursor.execute("SELECT id, origin, destination, equipment, jobtype, pname, day_month_yr, hour_min, priority FROM tasks WHERE origin = ? and completed = 0",
                                           (origin,)).fetchall()
        return created_task[-1]

    # Gets all completed and incompleted tasks
    def get_tasks(self):

        completed_tasks = self.cursor.execute("SELECT id, origin, destination, equipment, jobtype, pname, day_month_yr, hour_min, priority FROM tasks WHERE completed = 1 ORDER BY hour_min").fetchall()

        incompleted_tasks = self.cursor.execute("SELECT id, origin, destination, equipment, jobtype, pname, day_month_yr, hour_min, priority FROM tasks WHERE completed = 0 ORDER BY hour_min").fetchall()

        return incompleted_tasks, completed_tasks

    # Gets the information of a particular task
    def get_task_info(self):
        task_info = self.cursor.execute("SELECT id, origin, destination, equipment, jobtype, pname, day_month_yr, hour_min, priority FROM tasks")
        return task_info


    # Marks a task as complete (sets the value to 1)
    def mark_task_as_complete(self, taskid):
        self.cursor.execute("UPDATE tasks SET completed=1 WHERE id=?", (taskid,))
        self.con.commit()

    # Marks a task as incomplete (sets the value to 0)
    def mark_task_as_incomplete(self, taskid):
        self.cursor.execute("UPDATE tasks SET completed=0 WHERE id=?", (taskid,))
        self.con.commit()

    # Deletes a task from the system
    def delete_task(self, taskid):
        self.cursor.execute("DELETE FROM tasks WHERE id=?", (taskid,))
        self.con.commit()

    # Deletes all tasks from the system
    def delete_all(self):
        self.cursor.execute("DELETE FROM tasks WHERE completed = 1")
        self.con.commit()

    # Closes the connection to the DB
    def close_db_connection(self):
        self.con.close()
