class GetData:
    def __init__(self, app, origin, destination, equipment, jobtype, pname, date, time, priority):
        self.app = app
        self.origin = origin
        self.destination = destination
        self.equipment = equipment
        self.jobtype = jobtype
        self.pname = pname
        self.date = date
        self.time = time
        self.priority = priority

    def get_data(self):
        with open('db_files\\tasks_db.txt', 'r') as data_file:
            self.data_lines = data_file.readlines()
        with open('db_files\\tasks_db.txt', 'r') as file:
            self.content = file.read()
        self.store_data()

    def store_data(self):
        self.decision=[]

        with open('db_files\\tasks_db.txt', 'a') as db1:

            if self.content == '':
                self.idd = '1'
            else:
                self.idd = str(self.data_lines[-1][8])

            if len(self.data_lines) != 0:
                for line in self.data_lines:
                    line = str(line[9:].strip())
                    if line == f'{self.origin};{self.destination};{self.jobtype};{self.equipment};{self.pname};{self.hour_min};{self.day_month_yr};{self.priority}':
                        self.decision.append(1)
                    elif line != f'{self.origin};{self.destination};{self.jobtype};{self.equipment};{self.pname};{self.hour_min};{self.day_month_yr};{self.priority}':
                        pass
                if len(self.decision) == 0:
                    db1.write(
                        f'ID:{self.idd}>{self.origin};{self.destination};{self.jobtype};{self.equipment};{self.pname};{self.hour_min};{self.day_month_yr};{self.priority}\n')
                else:
                    pass
            if len(self.data_lines) == 0:
                db1.write(f'ID:{self.idd}>{self.origin};{self.destination};{self.jobtype};{self.equipment};{self.pname};{self.hour_min};{self.day_month_yr};{self.priority}\n')

    def send_data(self):
        with open('db_files\\tasks_db.txt', 'r') as file:
            self.data_lines = file.readlines()
            if len(self.data_lines) == 0:
                return 'database is empty'
            else:
                self.data_lines = [line.strip() for line in self.data_lines]
                return self.data_lines

    def delete_data(self, origin, destination, equipment, jobtype, pname, hour_min, day_month_yr, priority):
        self.origin = origin
        self.destination = destination
        self.equipment = equipment
        self.jobtype = jobtype
        self.pname = pname
        self.hour_min = hour_min
        self.day_month_yr = day_month_yr
        self.priority = priority
        self.target = str(self.origin) + ';' + str(self.destination) + ';' + str(self.equipment) + ';' + str(self.jobtype) + ';' + str(self.pname) + ';' + str(self.hour_min) + ';' + str(self.day_month_yr) + ';' + str(self.priority)
        self.the_lines = []

        with open('db_files\\tasks_db.txt', 'r') as file:
            self.list = file.readlines()
        for one in self.list:
            self.the_lines.append(one[8:].strip())

        for line in self.the_lines:
            if line == self.target:
                self.the_lines.remove(line)
            elif line != self.target:
                pass

        with open('db_files\\tasks_db.txt', 'w') as file_2:
            file_2.write('')

        with open('db_files\\tasks_db.txt', 'w+') as file_3:
            for num, the_line in enumerate(self.the_lines):
                file_3.write('ID:' + str(num+1) + '>' + the_line + '\n')

