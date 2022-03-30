import EventDispatcher.EventDispatcher
from LogicLayer.Clock import Cronometer


class Alarm:
    def __init__(self, logic_controller, clock, event_dispatcher):
        self.event_dispatcher = event_dispatcher
        self.my_logic_controller = logic_controller
        self.clock = clock
        self.event_dispatcher.add_event_listener(
                EventDispatcher.EventDispatcher.MyAlarmEvent.SET_ALARM_LIST, self.reload_alarm_items)
        self.alarm_actives = 0
        self.crono_list = []
        self.message = ""
        self.message_new = self.message
        self.sound_alarms = []
        self.sound_alarms_message_new = []
        self.sound_alarms_message = self.sound_alarms_message_new
        self.set_alarm_list(self.my_logic_controller.get_alarm_list())
        self.my_quick_alarm = {'name': "", 'active': True, 'days': False,
                     'monday': True, 'tuesday': True,
                     'wednesday': True, 'thursday': True,
                     'friday': True, 'saturday': True,
                     'sunday': True, 'hours': "00", 'minutes': "00",
                     'library': "", 'snooze': True,
                     'min_snooze': 10}


    def check_time(self, alarm):
        if alarm['minutes'] == self.clock.get_minutes() and alarm['hours'] == self.clock.get_hours():
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
                        self.event_dispatcher.dispatch_event(
                            EventDispatcher.EventDispatcher.MyAlarmEvent(
                                EventDispatcher.EventDispatcher.MyAlarmEvent.SOUND_ALARM,
                                alarm
                            )
                        )
                        self.my_logic_controller.set_player_library_by_name(alarm['library'])
                        self.my_logic_controller.play_song()
                        self.sound_alarms.append(alarm)
        # Check the cronometers
        self.alarm_info()

    def check_cronometers(self):
        if len(self.crono_list) > 0:
            for crono in self.crono_list:
                crono['cronometer_snooze'].update()
                if crono['cronometer_snooze'].get_delta_time() is not None:
                    self.event_dispatcher.dispatch_event(EventDispatcher.EventDispatcher.MyInfoEvent(
                            EventDispatcher.EventDispatcher.MyAlarmEvent.SET_CRONOMETER,
                            [crono['name'],
                             crono['cronometer_snooze'].get_delta_time()])
                    )
                else:
                    self.event_dispatcher.dispatch_event(EventDispatcher.EventDispatcher.MyInfoEvent(
                            EventDispatcher.EventDispatcher.MyAlarmEvent.SET_CRONOMETER,
                            [crono['name'],
                             None])
                    )
                    self.my_logic_controller.set_player_library_by_name(crono['alarm']['library'])
                    self.my_logic_controller.play_song()
                    self.crono_list.remove(crono)

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
        for iterator in self.sound_alarms:
            if name == iterator['name']:
                if self.my_logic_controller.get_alarm_parameters(name):
                    self.sound_alarms.remove(self.my_logic_controller.get_alarm_parameters(name))
                else:
                    self.sound_alarms.remove(self.my_quick_alarm)

                for item in self.crono_list:
                    if item['name'] == name:
                        self.crono_list.remove(item)
                self.my_logic_controller.stop_song(None)
                self.alarm_info()

    def find_crono_list(self, name):
        return [element for element in self.crono_list if element['name'] == name]

    def snooze_alarm(self, name):
        crono_alarm = {'name':"", 'alarm':None, 'cronometer_snooze':None}
        for iterator in self.sound_alarms:
            if name == iterator['name']:
                crono_alarm['name'] = name
                crono_alarm['alarm'] = iterator
                crono_alarm['cronometer_snooze'] = Cronometer()
                crono_alarm['cronometer_snooze'].set_delta_time(iterator['min_snooze'])
                crono_search = self.find_crono_list(name)
                if crono_search:
                    crono_search[0]['cronometer_snooze'].set_delta_time(iterator['min_snooze'])
                else:
                    self.crono_list.append(crono_alarm)
                self.my_logic_controller.stop_song(None)
                print(len(self.crono_list))

    def quick_alarm(self, library, time):
        name = "Alarma rapida"
        self.my_quick_alarm['name'] = name
        self.my_quick_alarm['library'] = library
        self.my_quick_alarm['min_snooze'] = 10

        self.event_dispatcher.dispatch_event(
                EventDispatcher.EventDispatcher.MyAlarmEvent(
                        EventDispatcher.EventDispatcher.MyAlarmEvent.SOUND_ALARM,
                        self.my_quick_alarm)
        )
        self.sound_alarms.append(self.my_quick_alarm)
        self.my_quick_alarm['min_snooze'] = time
        self.snooze_alarm(name)
        self.my_quick_alarm['min_snooze'] = 10



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

