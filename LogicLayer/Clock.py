from datetime import datetime
import EventDispatcher.EventDispatcher


class Clock():
    def __init__(self):
        # make it private

        self.update()
        # clock hands
        # self._update_id = GObject.timeout_add(200, self.update)

    def update(self):
        # update the time
        self._time = datetime.now()
        return True # keep running this event
    # public access to the time member

    def _get_time(self):
        return self._time

    def _set_time(self, datetime):
        self._time = datetime

    def get_time_formated(self):
        time = self._time.now().strftime("%H:%M:%S")
        return time

    def get_seconds(self):
        return self._time.now().second

    def get_minutes(self):
        return self._time.now().minute

    def get_horurs(self):
        return self._time.now().hour

    def get_week_day(self):
        return self._time.now().weekday()  #0 Monday 6 Sunday

    def get_date_formated(self):
        data = self._time.now().strftime("%A, %d-%m-%Y")
        return data


class Cronometer():
    def __init__(self):
        # make it private
        self.state = 1
        self.start_time = datetime.now()
        self.update()

    def update(self):
        # update the time
        self._time = datetime.now()

        if self.state is 1:
            return True  # keep running this event
        else:
            return False
    # public access to the time member

    def stop(self):
        self.state = 0

    def _get_time(self):
        time = self._time - self.start_time
        return time

    def get_time_now(self):
        return self._time

    def _set_time(self, datetime):
        self.start_time = datetime

    def _get_time_formated(self):
        time = self._time - self.start_time
        return time


class Alarm:
    def __init__(self, logic_controller, clock, event_dispatcher):
        self.event_dispatcher = event_dispatcher
        self.my_logic_controller = logic_controller
        self.clock = clock
        self.event_dispatcher.add_event_listener(
                EventDispatcher.EventDispatcher.MyAlarmEvent.SET_ALARM_LIST, self.reload_alarm_items)
        self.alarm_actives = 0
        self.message = ""
        self.message_new = ""
        self.set_alarm_list(self.my_logic_controller.get_alarm_list())

    def check_time(self, alarm):
        if alarm['minutes'] == self.clock.get_minutes() and alarm['hours'] == self.clock.get_horurs():
            return True
        return False

    def check_day(self, alarm):
        day = self.clock.get_week_day()
        if day == 0 and alarm['monday']:
            return True
        if day == 1 and alarm['tuesday']:
            return True
        if day == 2 and alarm['wednesday']:
            return True
        if day == 3 and alarm['thursday']:
            return True
        if day == 4 and alarm['friday']:
            return True
        if day == 5 and alarm['saturday']:
            return True
        if day == 6 and alarm['sunday']:
            return True
        return False

    def check_alarms(self):
        self.alarm_actives = 0
        for alarm_name in self.alarm_list:
            alarm = self.my_logic_controller.get_alarm_parameters(alarm_name)
            if alarm['active']:
                self.alarm_actives += 1
                if alarm['days']:
                    if self.check_time(alarm):
                        # sonar alarma
                        print("sonando alarma")
                else:
                    if self.check_day(alarm):
                        if self.check_time(alarm):
                            # sonar alarma
                            print("sonando alarma")

    def set_alarm_list(self, list):
        self.alarm_list = list
        self.check_alarms()
        self.alarm_info()

    def reload_alarm_items(self, event):
        self.set_alarm_list(event.data)

    def resend_info_message(self):
        self.message = ""
        self.alarm_info()

    def alarm_info(self):
        self.message_new = "Alarmas activas: {0}".format(self.alarm_actives)
        if self.message_new != self.message:
            self.event_dispatcher.dispatch_event(
                EventDispatcher.EventDispatcher.MyInfoEvent(
                    EventDispatcher.EventDispatcher.MyInfoEvent.DELETE_MESSAGE,
                    [self.message]
                )
            )
            self.event_dispatcher.dispatch_event(
                EventDispatcher.EventDispatcher.MyInfoEvent(
                    EventDispatcher.EventDispatcher.MyInfoEvent.SET_NEW_MESSAGE,
                    [self.message_new, True]
                )
            )
            self.message = self.message_new

