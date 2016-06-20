# -*- coding: utf-8 -*-
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GdkPixbuf
import PresentationLayer.PresentationController
import EventDispatcher.EventDispatcher

class AlarmManager(Gtk.Window):
    def __init__(self, my_alarm_screen_controller = None):
        if (my_alarm_screen_controller != None):
            self.my_alarm_screen_controller = my_alarm_screen_controller
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
        self.btn_add_quick_allarm1 = Gtk.Button.new_with_label("1 Hora")
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
        self.myAlarmScreenController.openAlarmWindow()

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
    def __init__(self):
        self.window = Gtk.Window.__init__(self, title=str("nombre"))
        self.connect('delete-event', self.delete_event)
        table = Gtk.Table(11, 7, True)

        self.set_border_width(20)
        self.add(table)

        lbl_nombre = Gtk.Label("Nombre")
        self.ent_nombre = Gtk.Entry()
        self.ent_nombre.set_text(str("nombre"))

        lbl_activa = Gtk.Label("Activa")
        self.sw_activa = Gtk.Switch()
        self.sw_activa.connect("notify::active", self.on_sw_activa_activated)

        self.lbl_dias = Gtk.Label("Todos los dias")
        self.sw_dias = Gtk.Switch()
        self.sw_dias.connect("notify::active", self.on_sw_dias_activated)

        self.chk_lunes = Gtk.CheckButton().new_with_label("Lunes")
        self.chk_martes = Gtk.CheckButton().new_with_label("Martes")
        self.chk_miercoles = Gtk.CheckButton().new_with_label("Miercoles")
        self.chk_jueves = Gtk.CheckButton().new_with_label("Jueves")
        self.chk_viernes = Gtk.CheckButton().new_with_label("Viernes")
        self.chk_sabado = Gtk.CheckButton().new_with_label("Sabado")
        self.chk_domingo = Gtk.CheckButton().new_with_label("Domingo")

        self.lbl_horas = Gtk.Label("Horas")
        adj_horas = Gtk.Adjustment(0, 0, 23, 1, 0, 0)
        self.spb_horas = Gtk.SpinButton()
        self.spb_horas.set_adjustment(adj_horas)

        self.lbl_minutos = Gtk.Label("Minutos")
        adj_minutos = Gtk.Adjustment(0, 0, 59, 1, 0, 0)
        self.spb_minutos = Gtk.SpinButton()
        self.spb_minutos.set_adjustment(adj_minutos)

        self.btn_guardar = Gtk.Button.new_with_label("Guardar")
        self.btn_guardar.connect("clicked", self.on_click_guardar)
        self.btn_cancelar = Gtk.Button.new_with_label("Cancelar")
        self.btn_cancelar.connect("clicked", self.on_click_cancelar)

        self.lbl_snooze = Gtk.Label("Dormitar")
        self.sw_snooze = Gtk.Switch()
        self.sw_snooze.connect("notify::active", self.on_sw_snooze_activated)
        self.spb_snooze = Gtk.SpinButton()
        adj_snooze = Gtk.Adjustment(10, 1, 30, 1, 0, 0)
        self.spb_snooze.set_adjustment(adj_snooze)

        self.load_params()
        self.update_sensitives()

        table.attach(lbl_nombre, 0,2, 0,1)
        table.attach(self.ent_nombre, 3, 5, 0, 1)
        table.attach(lbl_activa, 0,2, 1,2)
        table.attach(self.sw_activa, 3,4, 1,2)
        table.attach(self.lbl_snooze,0,2, 2,3)
        table.attach(self.sw_snooze,3,4, 2,3 )
        table.attach(self.spb_snooze, 5,6, 2,3 )
        table.attach(self.lbl_dias, 0,2, 4,5)
        table.attach(self.sw_dias, 3,4, 4,5)
        table.attach(self.chk_lunes,0,1 ,5,6)
        table.attach(self.chk_martes,1,2 ,5,6)
        table.attach(self.chk_miercoles,2,3 ,5,6)
        table.attach(self.chk_jueves,3,4 ,5,6)
        table.attach(self.chk_viernes,4,5 ,5,6)
        table.attach(self.chk_sabado,5,6 ,5,6)
        table.attach(self.chk_domingo,6,7 ,5,6)
        table.attach(self.lbl_horas,2,3,6,7)
        table.attach(self.spb_horas,2,3,7,8)
        table.attach(self.lbl_minutos,3,4,6,7)
        table.attach(self.spb_minutos,3,4,7,8)
        table.attach(self.btn_guardar,1,3,10,11)
        table.attach(self.btn_cancelar,4,6,10,11)
        self.show_all()

    def on_click_cancelar(self, button):
        a = 1

    def update_sensitives(self):
        # Comprobamos el status de la alarm
        if (self.sw_activa.get_active() == True ):
            self.lbl_dias.set_sensitive(True)
            self.sw_dias.set_sensitive(True)
            self.lbl_horas.set_sensitive(True)
            self.spb_horas.set_sensitive(True)
            self.lbl_minutos.set_sensitive(True)
            self.spb_minutos.set_sensitive(True)
            self.sw_snooze.set_sensitive(True)
            if (self.sw_dias.get_active() == True ):
                self.chk_lunes.set_sensitive(False)
                self.chk_martes.set_sensitive(False)
                self.chk_miercoles.set_sensitive(False)
                self.chk_jueves.set_sensitive(False)
                self.chk_viernes.set_sensitive(False)
                self.chk_sabado.set_sensitive(False)
                self.chk_domingo.set_sensitive(False)
            else:
                self.chk_lunes.set_sensitive(True)
                self.chk_martes.set_sensitive(True)
                self.chk_miercoles.set_sensitive(True)
                self.chk_jueves.set_sensitive(True)
                self.chk_viernes.set_sensitive(True)
                self.chk_sabado.set_sensitive(True)
                self.chk_domingo.set_sensitive(True)
            if (self.sw_snooze.get_active() == True ):
                self.spb_snooze.set_sensitive(True)
            else:
                self.spb_snooze.set_sensitive(False)
        else:
            self.spb_snooze.set_sensitive(False)
            self.lbl_dias.set_sensitive(False)
            self.sw_dias.set_sensitive(False)
            self.chk_lunes.set_sensitive(False)
            self.chk_martes.set_sensitive(False)
            self.chk_miercoles.set_sensitive(False)
            self.chk_jueves.set_sensitive(False)
            self.chk_viernes.set_sensitive(False)
            self.chk_sabado.set_sensitive(False)
            self.chk_domingo.set_sensitive(False)
            self.lbl_horas.set_sensitive(False)
            self.spb_horas.set_sensitive(False)
            self.lbl_minutos.set_sensitive(False)
            self.spb_minutos.set_sensitive(False)
            self.sw_snooze.set_sensitive(False)
            self.spb_snooze.set_sensitive(False)

    def on_sw_dias_activated(self, switch, gparam):
        self.update_sensitives()

    def on_sw_activa_activated(self, switch, gparam):
        self.update_sensitives()

    def on_sw_snooze_activated(self, switch, gparam):
        self.update_sensitives()


    def load_params(self):
        a = 1

    def on_click_guardar(self, button):
        a = 1

    def delete_event(self, widget, event=None):
        a = 1
