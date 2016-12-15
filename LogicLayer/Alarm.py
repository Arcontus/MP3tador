import EventDispatcher.EventDispatcher


class Alarm:
    def __init__(self, logic_controller, clock, event_dispatcher):
        self.event_dispatcher = event_dispatcher
        self.my_logic_controller = logic_controller
        self.clock = clock
        self.event_dispatcher.add_event_listener(
                EventDispatcher.EventDispatcher.MyAlarmEvent.SET_ALARM_LIST, self.reload_alarm_items)
        self.alarm_actives = 0
        self.message = ""
        self.message_new = self.message
        self.sound_alarms = []
        self.sound_alarms_message_new = []
        self.sound_alarms_message = self.sound_alarms_message_new
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
                if alarm['days'] or self.check_day(alarm):
                    if self.check_time(alarm):
                        # sonar alarma
                        self.event_dispatcher.dispatch_event(
                            EventDispatcher.EventDispatcher.MyAlarmEvent(
                                EventDispatcher.EventDispatcher.MyAlarmEvent.SOUND_ALARM,
                                alarm
                            )
                        )
                        self.my_logic_controller.set_player_library_by_name(alarm['library'])
                        self.my_logic_controller.play_song()
                        self.sound_alarms.append(alarm)
        self.alarm_info()

    def set_alarm_list(self, list):
        self.alarm_list = list
        self.check_alarms()
        self.alarm_info()

    def reload_alarm_items(self, event):
        self.set_alarm_list(event.data)

    def resend_info_message(self):
        self.message = ""
        self.alarm_info()

    def deactivate_alarm(self, name):
        if name in self.sound_alarms:
            self.sound_alarms.remove(self.my_logic_controller.get_alarm_parameters(name))
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
        if len(self.sound_alarms) > 0:
            for alarm in self.sound_alarms:
                self.sound_alarms_message_new.append("Sonando alarma: {0}".format(alarm['name']))

        if self.sound_alarms_message != self.sound_alarms_message_new:
            for message in self.sound_alarms_message:
                self.event_dispatcher.dispatch_event(
                    EventDispatcher.EventDispatcher.MyInfoEvent(
                        EventDispatcher.EventDispatcher.MyInfoEvent.DELETE_MESSAGE,
                        [message]
                    )
                )
            for message in self.sound_alarms_message_new:
                self.event_dispatcher.dispatch_event(
                    EventDispatcher.EventDispatcher.MyInfoEvent(
                        EventDispatcher.EventDispatcher.MyInfoEvent.SET_NEW_MESSAGE,
                        [message, True]
                    )
                )
        self.sound_alarms_message = self.sound_alarms_message_new

