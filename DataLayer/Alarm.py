import os

alarm_list = []   ## List of all alarm objects
alarm_dir = "./alarmas/"


def add_alarm(alarm_id):
    alarm_list.append(alarm_id)


def rm_alarm(alarm_id):
    if os.path.exists(alarm_dir+alarm_id.get_name()+".alarm"):
        os.remove(alarm_dir+alarm_id.get_name()+".alarm")
    alarm_list.remove(alarm_id)


def load_alarm_list():
    if not os.path.exists(alarm_dir):
        os.makedirs(alarm_dir)
    files = os.listdir(alarm_dir)
    for i in sorted(files):
        my_alarms = Alarm()
        my_alarms.load(str(i[:-6]))
        alarm_list.append(my_alarms)


def get_alarm_by_name(name):
    for i in alarm_list:
        if i.get_name() == name:
            return i
    return False


def rm_alarm_by_name(name):
    for i in alarm_list:
        if i.get_name() == name:
            rm_alarm(i)


def get_alarm_bibrary_use(name):
    a = 0
    for i in alarm_list:
        if i.get_library() == name:
            a = a +1
    return a

def get_alarm_list():
    return alarm_list

class Alarm():
    def __init__(self):
        self.name = ""
        self.lib_dir =  "./biblioteca/"
        self.myfile = ""
        self.active = False
        self.days = False
        self.monday = False
        self.tuesday = False
        self.wednesday = False
        self.thursday = False
        self.friday = False
        self.saturday = False
        self.sunday = False
        self.hours = 0
        self.minutes = 0
        self.library = ""
        self.snooze = False
        self.min_snooze = 5

    def set_name(self, name):
        self.name = name

    def set_myfile(self):
        if not os.path.exists(alarm_dir):
            os.makedirs(alarm_dir)
        self.myfile = alarm_dir+str(self.name) + ".alarm"

    def load(self, name):
        self.set_name(name)
        self.set_myfile()
        self.load_params()

    def load_params(self):
        if os.path.isfile(self.myfile):
            file = open(self.myfile, "r")
            for line in file:
                if line.split(":")[0] == 'active':
                    if (line.split(":")[1]) == "True\n":
                        self.active = True
                    else:
                        self.active = False

                elif line.split(":")[0] == "days":
                    if (line.split(":")[1]) == "True\n":
                        self.days = True
                    else:
                        self.days = False

                elif line.split(":")[0] == "monday":
                    if (line.split(":")[1]) == "True\n":
                        self.monday = True
                    else:
                        self.monday = False

                elif line.split(":")[0] == "tuesday":
                    if (line.split(":")[1]) == "True\n":
                        self.tuesday = True
                    else:
                        self.tuesday = False

                elif line.split(":")[0] == "wednesday":
                    if (line.split(":")[1]) == "True\n":
                        self.wednesday = True
                    else:
                        self.wednesday = False

                elif line.split(":")[0] == "thursday":
                    if (line.split(":")[1]) == "True\n":
                        self.thursday = True
                    else:
                        self.thursday = False

                elif line.split(":")[0] == "friday":
                    if (line.split(":")[1]) == "True\n":
                        self.friday = True
                    else:
                        self.friday = False

                elif line.split(":")[0] == "saturday":
                    if (line.split(":")[1]) == "True\n":
                        self.saturday = True
                    else:
                        self.saturday = False

                elif line.split(":")[0] == "sunday":
                    if (line.split(":")[1]) == "True\n":
                        self.sunday = True
                    else:
                        self.sunday = False

                elif line.split(":")[0] == "hour":
                    self.hours= int(line.split(":")[1])

                elif line.split(":")[0] == "minutes":
                    self.minutes = int(line.split(":")[1])

                elif line.split(":")[0] == "library":
                    self.library = str(line.split(":")[1])[:-1]

                elif line.split(":")[0] == "snooze":
                    if line.split(":")[1] == "True\n":
                        self.snooze = True
                    else:
                        self.snooze = False

                elif (line.split(":")[0] == "min_snooze"):
                    self.min_snooze = int(line.split(":")[1])

        file.close()

    def save_params(self):
        fichero = open(alarm_dir + self.name + ".alarm", "w")
        fichero.write("active:" + str(self.active) + "\n")
        fichero.write("days:" + str(self.days) + "\n")
        fichero.write("monday:" + str(self.monday) + "\n")
        fichero.write("tuesday:" + str(self.tuesday) + "\n")
        fichero.write("wednesday:" + str(self.wednesday) + "\n")
        fichero.write("thursday:" + str(self.thursday) + "\n")
        fichero.write("friday:" + str(self.friday) + "\n")
        fichero.write("saturday:" + str(self.saturday) + "\n")
        fichero.write("sunday:" + str(self.sunday) + "\n")
        fichero.write("hora:" + str(self.hours) + "\n")
        fichero.write("minutes:" + str(self.minutes) + "\n")
        fichero.write("library:" + str(self.library) + "\n")
        fichero.write("snooze:"+str(self.snooze)+"\n")
        fichero.write("min_snooze:"+str(self.min_snooze)+"\n")
        fichero.close()

    def get_name(self):
        return self.name

    def set_name(self, name):
        self.name = name

    def get_my_file(self):
        return self.my_file

    def set_my_file(self, file):
        self.my_file = file

    def get_active(self):
        return self.active

    def set_active(self, activa):
        self.active = activa

    def get_days(self):
        return self.days

    def set_days(self, days):
        self.days= days

    def get_monday(self):
        return self.monday

    def set_monday(self, monday):
        self.monday = monday

    def get_tuesday(self):
        return self.tuesday

    def set_tuesday(self, tuesday):
        self.tuesday = tuesday

    def get_wednesday(self):
        return self.wednesday

    def set_wednesday(self, wednesday):
        self.wednesday = wednesday

    def get_thursday(self):
        return self.thursday

    def set_thursday(self, thursday):
        self.thursday = thursday

    def get_friday(self):
        return self.friday

    def set_friday(self, friday):
        self.friday = friday

    def get_saturday(self):
        return self.saturday

    def set_saturday(self, saturday):
        self.saturday = saturday

    def get_sunday(self):
        return self.sunday

    def set_sunday(self, sunday):
        self.sunday = sunday

    def get_hours(self):
        return self.hours

    def set_hours(self, hours):
        self.hours = hours

    def get_minutes(self):
        return self.minutes

    def set_minutes(self, minutes):
        self.minutes = minutes

    def get_library(self):
        return self.library

    def set_library(self, library):
        self.library = library

    def get_snooze(self):
        return self.snooze

    def set_snooze(self, snooze):
        self.snooze = snooze

    def get_min_snooze(self):
        return self.min_snooze

    def set_min_snooze(self, minutes):
        self.min_snooze = minutes
