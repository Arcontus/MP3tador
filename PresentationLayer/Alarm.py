# -*- coding: utf-8 -*-
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GdkPixbuf


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
        a = 1

    def on_click_btn_add_quick_allarm30(self, widget):
        a = 1

    def on_click_btn_add_quick_allarm45(self, widget):
        a = 1

    def on_click_btn_add_quick_allarm1(self, widget):
        a = 1

    def reset_alarm_items(self):
        self.lst_alarms.remove_all()

    def reset_library_items(self):
        self.lst_library.remove_all()

    def add_alarm_item(self, item):
         self.lst_alarms.append_text(item)

    def add_library_item(self, item):
         self.lst_library.append_text(item)

    def on_click_modificar(self, widget):
        a = 1

    def on_click_btn_add_alarm(self, widget):
        self.my_alarm_screen_controller.open_alarm_window()

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
        a = 1


class AlarmWindow(Gtk.Window):
    def __init__(self, my_alarm_screen_controller=None):
        if my_alarm_screen_controller:
            self.my_alarm_screen_controller = my_alarm_screen_controller
        else:
            raise NameError("AlarmManager needs alarm_screen_controller instance")
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

        self.load_params()
        self.update_sensitives()

        table.attach(lbl_name, 0,2, 0,1)
        table.attach(self.ent_name, 3, 5, 0, 1)
        table.attach(lbl_active, 0,2, 1,2)
        table.attach(self.sw_active, 3,4, 1,2)
        table.attach(self.lbl_snooze,0,2, 2,3)
        table.attach(self.sw_snooze,3,4, 2,3 )
        table.attach(self.spb_snooze, 5,6, 2,3 )
        table.attach(self.lbl_days, 0,2, 4,5)
        table.attach(self.sw_days, 3,4, 4,5)
        table.attach(self.chk_monday,0,1 ,5,6)
        table.attach(self.chk_tuesday,1,2 ,5,6)
        table.attach(self.chk_wednesday,2,3 ,5,6)
        table.attach(self.chk_thursday,3,4 ,5,6)
        table.attach(self.chk_friday,4,5 ,5,6)
        table.attach(self.chk_saturday,5,6 ,5,6)
        table.attach(self.chk_sunday,6,7 ,5,6)
        table.attach(self.lbl_hours,2,3,6,7)
        table.attach(self.spb_hours,2,3,7,8)
        table.attach(self.lbl_minutes,3,4,6,7)
        table.attach(self.spb_minutes,3,4,7,8)
        table.attach(self.btn_save,1,3,10,11)
        table.attach(self.btn_cancel,4,6,10,11)
        self.show_all()

    def on_click_cancel(self, button):
        a = 1

    def update_sensitives(self):
        # Comprobamos el status de la alarm
        if self.sw_active.get_active() is True:
            self.lbl_days.set_sensitive(True)
            self.sw_days.set_sensitive(True)
            self.lbl_hours.set_sensitive(True)
            self.spb_hours.set_sensitive(True)
            self.lbl_minutes.set_sensitive(True)
            self.spb_minutes.set_sensitive(True)
            self.sw_snooze.set_sensitive(True)
            if self.sw_days.get_active() is True:
                self.chk_monday.set_sensitive(False)
                self.chk_tuesday.set_sensitive(False)
                self.chk_wednesday.set_sensitive(False)
                self.chk_thursday.set_sensitive(False)
                self.chk_friday.set_sensitive(False)
                self.chk_saturday.set_sensitive(False)
                self.chk_sunday.set_sensitive(False)
            else:
                self.chk_monday.set_sensitive(True)
                self.chk_tuesday.set_sensitive(True)
                self.chk_wednesday.set_sensitive(True)
                self.chk_thursday.set_sensitive(True)
                self.chk_friday.set_sensitive(True)
                self.chk_saturday.set_sensitive(True)
                self.chk_sunday.set_sensitive(True)
            if self.sw_snooze.get_active is True :
                self.spb_snooze.set_sensitive(True)
            else:
                self.spb_snooze.set_sensitive(False)
        else:
            self.spb_snooze.set_sensitive(False)
            self.lbl_days.set_sensitive(False)
            self.sw_days.set_sensitive(False)
            self.chk_monday.set_sensitive(False)
            self.chk_tuesday.set_sensitive(False)
            self.chk_wednesday.set_sensitive(False)
            self.chk_thursday.set_sensitive(False)
            self.chk_friday.set_sensitive(False)
            self.chk_saturday.set_sensitive(False)
            self.chk_sunday.set_sensitive(False)
            self.lbl_hours.set_sensitive(False)
            self.spb_hours.set_sensitive(False)
            self.lbl_minutes.set_sensitive(False)
            self.spb_minutes.set_sensitive(False)
            self.sw_snooze.set_sensitive(False)
            self.spb_snooze.set_sensitive(False)

    def on_sw_days_activated(self, switch, gparam):
        self.update_sensitives()

    def on_sw_active_activated(self, switch, gparam):
        self.update_sensitives()

    def on_sw_snooze_activated(self, switch, gparam):
        self.update_sensitives()

    def load_params(self):
        a = 1

    def on_click_save(self, button):
        a = 1

    def delete_event(self, widget, event=None):
        a = 1
