# -*- coding: utf-8 -*-
import gi
import random
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GdkPixbuf, GObject
from datetime import datetime
from PresentationLayer.ConsoleInfo import ConsoleInfo
import EventDispatcher.EventDispatcher


class AlarmManager(Gtk.Window):
    def __init__(self, my_alarm_screen_controller=None):
        if my_alarm_screen_controller:
            self.my_alarm_screen_controller = my_alarm_screen_controller
        else:
            raise NameError("AlarmManager needs alarm_screen_controller instance")
        self.window = Gtk.Window.__init__(self, title="Menu de alarmas")

        table = Gtk.Table(6, 4, True)
        self.add(table)
        self.set_border_width(20)
        self.lst_alarms = Gtk.ComboBoxText()
        self.alarm_button_list = []

        self.btn_add_alarm = Gtk.Button.new_with_label("Agregar nueva alarma")
        self.btn_add_alarm.connect("clicked", self.on_click_btn_add_alarm)
        self.btn_modify = Gtk.Button.new_with_label("Modificar")
        self.btn_modify.connect("clicked", self.on_click_modificar)
        self.btn_rm_alarm = Gtk.Button.new_with_label("Eliminar")
        self.btn_rm_alarm.connect("clicked", self.on_click_btn_rm_alarm)

        self.lbl_fast_alarm = Gtk.Label(label="Alarma rapida")
        self.lbl_library = Gtk.Label(label="Biblioteca")
        self.btn_add_quick_allarm15 = Gtk.Button.new_with_label("15 Min")
        self.btn_add_quick_allarm15.connect("clicked", self.on_click_btn_add_quick_allarm15)
        self.btn_add_quick_allarm30 = Gtk.Button.new_with_label("30 Min")
        self.btn_add_quick_allarm30.connect("clicked", self.on_click_btn_add_quick_allarm30)
        self.btn_add_quick_allarm45 = Gtk.Button.new_with_label("45 Min")
        self.btn_add_quick_allarm45.connect("clicked", self.on_click_btn_add_quick_allarm45)
        self.btn_add_quick_allarm1 = Gtk.Button.new_with_label("1 Hour")
        self.btn_add_quick_allarm1.connect("clicked", self.on_click_btn_add_quick_allarm1)

        self.lst_library = Gtk.ComboBoxText()

        table.attach(self.btn_add_alarm, 2, 5, 1, 2)
        table.attach(self.lst_alarms, 2,5, 3,4)
        table.attach(self.btn_modify, 6, 7, 3, 4)
        table.attach(self.btn_rm_alarm,0,1, 3,4)
        table.attach(self.lbl_fast_alarm, 0, 4, 6, 7)
        table.attach(self.lbl_library, 5, 7, 6, 7)
        table.attach(self.btn_add_quick_allarm15,0,1, 7,8)
        table.attach(self.btn_add_quick_allarm30,1,2, 7,8)
        table.attach(self.btn_add_quick_allarm45,2,3, 7,8)
        table.attach(self.btn_add_quick_allarm1,3,4, 7,8)
        table.attach(self.lst_library, 4, 7, 7, 8)

    def on_click_btn_add_quick_allarm15(self, widget):
        self.my_alarm_screen_controller.quick_alarm(self.lst_library.get_active_text(), 15)

    def on_click_btn_add_quick_allarm30(self, widget):
        self.my_alarm_screen_controller.quick_alarm(self.lst_library.get_active_text(), 30)

    def on_click_btn_add_quick_allarm45(self, widget):
        self.my_alarm_screen_controller.quick_alarm(self.lst_library.get_active_text(), 45)

    def on_click_btn_add_quick_allarm1(self, widget):
        self.my_alarm_screen_controller.quick_alarm(self.lst_library.get_active_text(), 60)

    def reset_alarm_items(self):
        self.lst_alarms.remove_all()

    def reset_library_items(self):
        self.lst_library.remove_all()

    def add_alarm_item(self, item):
        self.lst_alarms.append_text(item)

    def add_library_item(self, item):
        self.lst_library.append_text(item)

    def on_click_modificar(self, widget):
        self.my_alarm_screen_controller.modify_alarm_config(self.lst_alarms.get_active_text())

    def on_click_btn_add_alarm(self, widget):
        self.my_alarm_screen_controller.open_alarm_config()

    def reload_alarm_items(self, items):
        self.reset_alarm_items()
        for i in sorted(items):
            self.add_alarm_item(i)
        self.lst_alarms.set_active(0)

    def reload_library_items(self, items):
        self.reset_library_items()
        for i in sorted(items):
            self.add_library_item(i)
        self.lst_library.set_active(0)
        print(items)

    def on_click_btn_rm_alarm(self, widget):
        self.my_alarm_screen_controller.delete_alarm(self.lst_alarms.get_active_text())


class AlarmConfig(Gtk.Window):
    def __init__(self, my_alarm_screen_controller=None):
        if my_alarm_screen_controller:
            self.my_alarm_screen_controller = my_alarm_screen_controller
        else:
            raise NameError("AlarmManager needs alarm_screen_controller instance")

        self.alarm = {'name': '', 'active': False, 'days': False, 'monday': False, 'tuesday': False,
                      'wednesday': False, 'thursday': False, 'friday': False, 'saturday': False, 'sunday': False,
                      'hours': 0, 'minutes': 0, 'library': "", 'snooze': False, 'min_snooze': 5}

        self.window = Gtk.Window.__init__(self)
        self.connect('delete-event', self.delete_event)
        table = Gtk.Table(11, 7, True)
        self.alarm_name = self.my_alarm_screen_controller.get_next_alarm_name()
        self.set_title(self.alarm_name)
        self.set_border_width(20)
        self.add(table)

        lbl_name = Gtk.Label("Nombre")
        self.ent_name = Gtk.Entry()
        self.ent_name.set_text(self.alarm_name)

        lbl_active = Gtk.Label("Activa")
        self.sw_active = Gtk.Switch()
        self.sw_active.connect("notify::active", self.on_sw_active_activated)

        self.lbl_days = Gtk.Label("Todos los dias")
        self.sw_days = Gtk.Switch()
        self.sw_days.connect("notify::active", self.on_sw_days_activated)

        self.chk_monday = Gtk.CheckButton().new_with_label("Lunes")
        self.chk_tuesday = Gtk.CheckButton().new_with_label("Martes")
        self.chk_wednesday = Gtk.CheckButton().new_with_label("Miercoles")
        self.chk_thursday = Gtk.CheckButton().new_with_label("Jueves")
        self.chk_friday = Gtk.CheckButton().new_with_label("Viernes")
        self.chk_saturday = Gtk.CheckButton().new_with_label("Sabado")
        self.chk_sunday = Gtk.CheckButton().new_with_label("Domingo")

        self.lbl_hours = Gtk.Label("Horas")
        adj_hours = Gtk.Adjustment(0, 0, 23, 1, 0, 0)
        self.spb_hours = Gtk.SpinButton()
        self.spb_hours.set_adjustment(adj_hours)

        self.lbl_minutes = Gtk.Label("Minutos")
        adj_minutes = Gtk.Adjustment(0, 0, 59, 1, 0, 0)
        self.spb_minutes = Gtk.SpinButton()
        self.spb_minutes.set_adjustment(adj_minutes)

        self.btn_save = Gtk.Button.new_with_label("Guardar")
        self.btn_save.connect("clicked", self.on_click_save)
        self.btn_cancel = Gtk.Button.new_with_label("Cancelar")
        self.btn_cancel.connect("clicked", self.on_click_cancel)

        self.lbl_snooze = Gtk.Label("Dormitar")
        self.sw_snooze = Gtk.Switch()
        self.sw_snooze.connect("notify::active", self.on_sw_snooze_activated)
        self.spb_snooze = Gtk.SpinButton()
        adj_snooze = Gtk.Adjustment(10, 1, 30, 1, 0, 0)
        self.spb_snooze.set_adjustment(adj_snooze)

        self.lst_library = Gtk.ComboBoxText()

        self.update_sensitives()

        table.attach(lbl_name, 0, 2, 0, 1)
        table.attach(self.ent_name, 3, 5, 0, 1)
        table.attach(lbl_active, 0, 2, 1, 2)
        table.attach(self.sw_active, 3, 4, 1, 2)
        table.attach(self.lbl_snooze, 0, 2, 2, 3)
        table.attach(self.sw_snooze, 3, 4, 2, 3)
        table.attach(self.spb_snooze, 5, 6, 2, 3)
        table.attach(self.lbl_days, 0, 2, 4, 5)
        table.attach(self.sw_days, 3, 4, 4, 5)
        table.attach(self.chk_monday, 0, 1, 5, 6)
        table.attach(self.chk_tuesday, 1, 2, 5, 6)
        table.attach(self.chk_wednesday, 2, 3, 5, 6)
        table.attach(self.chk_thursday, 3, 4, 5, 6)
        table.attach(self.chk_friday, 4, 5, 5, 6)
        table.attach(self.chk_saturday, 5, 6, 5, 6)
        table.attach(self.chk_sunday, 6, 7, 5, 6)
        table.attach(self.lbl_hours, 2, 3, 6, 7)
        table.attach(self.spb_hours, 2, 3, 7, 8)
        table.attach(self.lbl_minutes, 3, 4,  6,7)
        table.attach(self.spb_minutes, 3, 4, 7, 8)
        table.attach(self.lst_library, 2, 5, 8, 9)
        table.attach(self.btn_save, 1, 3, 10, 11)
        table.attach(self.btn_cancel, 4, 6, 10, 11)
        self.show_all()

    def update_sensitives(self):
        # Comprobamos el status de la alarm
        sw_active = self.sw_active.get_active()
        self.lbl_days.set_sensitive(sw_active)
        self.sw_days.set_sensitive(sw_active)
        self.lbl_hours.set_sensitive(sw_active)
        self.spb_hours.set_sensitive(sw_active)
        self.lbl_minutes.set_sensitive(sw_active)
        self.spb_minutes.set_sensitive(sw_active)
        self.sw_snooze.set_sensitive(sw_active)

        sw_days = self.sw_days.get_active()
        self.chk_monday.set_sensitive(sw_days and sw_active)
        self.chk_tuesday.set_sensitive(sw_days and sw_active)
        self.chk_wednesday.set_sensitive(sw_days and sw_active)
        self.chk_thursday.set_sensitive(sw_days and sw_active)
        self.chk_friday.set_sensitive(sw_days and sw_active)
        self.chk_saturday.set_sensitive(sw_days and sw_active)
        self.chk_sunday.set_sensitive(sw_days and sw_active)

        sw_snooze = self.sw_snooze.get_active()
        self.spb_snooze.set_sensitive(sw_snooze)



    def on_sw_days_activated(self, switch, gparam):
        self.update_sensitives()

    def on_sw_active_activated(self, switch, gparam):
        self.update_sensitives()

    def on_sw_snooze_activated(self, switch, gparam):
        self.update_sensitives()

    def load_params(self, alarm_dict):
        self.alarm = alarm_dict
        self.ent_name.set_text(self.alarm['name'])
        self.sw_active.set_active(self.alarm['active'])
        self.sw_days.set_active(self.alarm['days'])
        self.chk_monday.set_active(self.alarm['monday'])
        self.chk_tuesday.set_active(self.alarm['tuesday'])
        self.chk_wednesday.set_active(self.alarm['wednesday'])
        self.chk_thursday.set_active(self.alarm['thursday'])
        self.chk_friday.set_active(self.alarm['friday'])
        self.chk_saturday.set_active(self.alarm['saturday'])
        self.chk_sunday.set_active(self.alarm['sunday'])
        self.spb_hours.set_value(self.alarm['hours'])
        self.spb_minutes.set_value(self.alarm['minutes'])

        # This block put the correct active text on comboBox
        num_items = len(self.lst_library.get_model())
        for i in range(num_items):
            self.lst_library.set_active(i)
            if self.lst_library.get_active_text() == self.alarm['library']:
                break

        self.sw_snooze.set_active(self.alarm['snooze'])
        self.spb_snooze.set_value(self.alarm['min_snooze'])

    def reload_library_items(self, items):
        self.reset_library_items()
        for i in sorted(items):
            self.add_library_item(i)
        self.lst_library.set_active(0)

    def add_library_item(self, item):
        self.lst_library.append_text(item)

    def reset_library_items(self):
        self.lst_library.remove_all()

    def on_click_save(self, button):
        self.alarm['name'] = self.ent_name.get_text()
        self.alarm['active'] = self.sw_active.get_active()
        self.alarm['days'] = self.sw_days.get_active()
        self.alarm['monday'] = self.chk_monday.get_active()
        self.alarm['tuesday'] = self.chk_tuesday.get_active()
        self.alarm['wednesday'] = self.chk_wednesday.get_active()
        self.alarm['thursday'] = self.chk_thursday.get_active()
        self.alarm['friday'] = self.chk_friday.get_active()
        self.alarm['saturday'] = self.chk_saturday.get_active()
        self.alarm['sunday'] = self.chk_sunday.get_active()
        self.alarm['hours'] = self.spb_hours.get_value_as_int()
        self.alarm['minutes'] = self.spb_minutes.get_value_as_int()
        self.alarm['library'] = str(self.lst_library.get_active_text())
        self.alarm['snooze'] = self.sw_snooze.get_active()
        self.alarm['min_snooze'] = self.spb_snooze.get_value_as_int()
        print (self.alarm)
        self.my_alarm_screen_controller.save_alarm(self.alarm)


    def delete_event(self, widget, event=None):
        a = 1

    def on_click_cancel(self, button):
        self.close()


class SoundAlarm(Gtk.Window):
    def __init__(self, my_alarm_screen_controller, alarm, event_dispatcher):
        self.window = Gtk.Window.__init__(self)
        self.connect('delete-event', self.delete_event)
        self.set_modal(True)
        self.set_decorated(False)
        self.set_position(Gtk.WindowPosition.CENTER)
        self.set_border_width(20)
        self.my_alarm_screen_controller = my_alarm_screen_controller
        self.event_dispatcher = event_dispatcher
        self.notebook = Gtk.Notebook()
        self.notebook.set_scrollable(True)
        self.add(self.notebook)
        self.alarm_list = []
        self.alarm_pages = []
        self.alarm_ringing_list = []
        self.create_alarm_page(alarm)

        #self.update_id = GObject.timeout_add(1000, self.update_hora_timeout, None)
        self.fullscreen()

        self.show_all()

    def create_alarm_page(self, alarm):
        my_page = AlarmPage(self, alarm, self.event_dispatcher)
        self.alarm_list.append(alarm)
        self.alarm_pages.append(my_page)
        self.notebook.append_page(my_page.get_table(), Gtk.Label(alarm['name']))
        self.notebook.show_all()


    def add_new_alarm(self, alarm):
        self.create_alarm_page(alarm)

    def delete_alarm_page(self, my_page):
        if my_page in self.alarm_pages:
            self.notebook.remove_page(self.alarm_pages.index(my_page))
            self.alarm_pages.remove(my_page)
            self.notebook.show_all()
            self.my_alarm_screen_controller.deactivate_alarm(my_page.get_alarm_name())
            print("deactivated: " + my_page.get_alarm_name())
            self.alarm_list.remove(my_page.get_alarm())
        if not (len(self.alarm_pages)):
            self.delete_event()

    def snooze_alarm(self, alarm_name):
        self.my_alarm_screen_controller.snooze_alarm(alarm_name)

    def delete_event(self, widget=None, other=None):
        for alarm in self.alarm_list:
            print("deactivated: " + alarm['name'])
            self.my_alarm_screen_controller.deactivate_alarm(alarm['name'])
        if not len(self.alarm_pages):
            self.my_alarm_screen_controller.delete_my_sound_alarm()
            self.destroy()
        # Eliminamos el gobject
        # Paramos el reproductor
        # Recargamos bibliotecas
        # Eliminamos nuestra ventana


class AlarmPage(ConsoleInfo):
    def __init__(self, parent_window, alarm, event_dispatcher):
        ConsoleInfo.__init__(self)
        self.lblhour = Gtk.Label(label="")
        self.lbldate = Gtk.Label(label="")
        self.table = Gtk.Table(11, 7, True)
        self.table.set_border_width(20)
        code1 = []
        code2 = code1
        self.my_parent_window = parent_window
        self.my_alarm = alarm
        self.event_dispatcher = event_dispatcher
        self.event_dispatcher.add_event_listener(
            EventDispatcher.EventDispatcher.MyDateEvent.MAIN_WINDOW_SET_HOUR, self.set_hour)
        self.event_dispatcher.add_event_listener(
            EventDispatcher.EventDispatcher.MyDateEvent.MAIN_WINDOW_SET_DATE, self.set_date)
        self.event_dispatcher.add_event_listener(
                EventDispatcher.EventDispatcher.MyAlarmEvent.SET_CRONOMETER, self.set_snooze_crono)
        self.font_color = "black"
        if self.my_alarm['snooze']:
            self.btn_snooze = Gtk.Button()
            self.lbl_btn_snooze = "Snooze {} Min".format(self.my_alarm['min_snooze'])
            self.btn_snooze.set_label(self.lbl_btn_snooze)
            self.btn_snooze.connect("clicked", self.on_btn_snooze_clicked)
            self.table.attach(self.btn_snooze, 0, 3, 5, 6)
        self.lst_sw_deactivate = []
        self.lst_lbl_deactivate = []
        self.code1 = []
        self.code2 = []
        for i in range(8):
            self.lst_sw_deactivate.append(Gtk.Switch())
            self.lst_lbl_deactivate.append(Gtk.Label(label=i))
            self.lst_sw_deactivate[i].connect("notify::active", self.on_sw_deact_activated)
            if (i < 4):
                self.table.attach(self.lst_sw_deactivate[i], i, i + 1, 7, 8)
            else:
                self.table.attach(self.lst_sw_deactivate[i], i - 4, i - 3, 9, 10)
        self.lbl_combination1 = Gtk.Label()
        self.lbl_combination2 = Gtk.Label()
        self.txt_combination1 = ""
        self.txt_combination2 = self.txt_combination1
        self.new_combination()
        self.add_msg("Alarma {}".format(self.my_alarm['name']))

        #self.info_max_leng = 34
        #self.txt_info.set_max_length(self.info_max_leng)

        self.table.attach(self.txt_info, 1, 6, 1, 2)
        self.table.attach(self.lbldate, 0, 5, 2, 3)
        self.table.attach(self.lblhour, 0, 5, 3, 5)

        self.table.attach(self.lbl_combination1, 1, 4, 10, 11)
        self.table.attach(self.lbl_combination2, 1, 4, 11, 12)

    def get_table(self):
        return self.table

    def get_library(self):
        return self.my_alarm['library']

    def get_alarm_name(self):
        return self.my_alarm['name']

    def get_alarm(self):
        return self.my_alarm

    def on_sw_deact_activated(self, switch, widget=None):
        if switch.get_active():
            self.code2[int(self.get_switch_number_from_label(switch))] = 1
        else:
            self.code2[int(self.get_switch_number_from_label(switch))] = 0
        self.txt_combination2 = "Combinacion introducida: {0}".format(self.code2)
        self.lbl_combination2.set_text(self.txt_combination2)
        print(self.code1)
        print(self.code2)
        if self.code1 == self.code2:
            self.delete_event()

    def get_switch_number_from_label(self, switch):
        position = self.get_switch_position_from_list(switch)
        return self.lst_lbl_deactivate[position].get_text()

    def get_switch_position_from_list(self, switch):
        for i in range(8):
            if self.lst_sw_deactivate[i] == switch:
                return i

    def new_combination(self):
        random.shuffle(self.lst_lbl_deactivate)
        for i in range(8):
            self.code2.append(0)
            if (i < 4):
                self.table.attach(self.lst_lbl_deactivate[i], i, i+1, 6, 7)
            else:
                self.table.attach(self.lst_lbl_deactivate[i], i-4, i-3, 8, 9)
        for i in range(random.randint(4, 5)):
            self.code1.append(1)
        for i in range(8-len(self.code1)):
            self.code1.append(0)
        random.shuffle(self.code1)
        self.txt_combination1 = "Combinacion de desbloqueo: "+str(self.code1)
        self.lbl_combination1.set_text(self.txt_combination1)

    def delete_event(self):
        self.event_dispatcher.remove_event_listener(
                EventDispatcher.EventDispatcher.MyDateEvent.MAIN_WINDOW_SET_HOUR, self.set_hour)
        self.event_dispatcher.remove_event_listener(
                EventDispatcher.EventDispatcher.MyDateEvent.MAIN_WINDOW_SET_DATE, self.set_date)
        self.my_parent_window.delete_alarm_page(self)

    def set_hour(self, event):
        self.lblhour.set_markup(str("<span font='50' foreground='"+self.font_color+"'>Hora Actual: "+event.data)+"</span>")

    def set_date(self, event):
        self.lbldate.set_markup(str("<span variant='smallcaps'>" + event.data) + "</span>")

    def set_snooze_crono(self, event):
        if event.data[0] == self.my_alarm['name']:
            result = event.data[1]
            if result:
                self.btn_snooze.set_label(self.lbl_btn_snooze + "\n Próxima activación en: " + str(event.data[1])[:-7])
            else:
                self.btn_snooze.set_label(self.lbl_btn_snooze + "\n")

    def on_btn_snooze_clicked(self, widget=None):
        self.my_parent_window.snooze_alarm(self.my_alarm['name'])



