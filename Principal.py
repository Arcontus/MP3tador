###############################################################################
########### MAIN FILE #########################################################
###############################################################################

import os.path
import os
import pygame
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gio, GObject, GdkPixbuf
import Biblioteca
from Alarma import *
from Reproductor import *
from Reloj import *
from Opciones import *


###############################################################################

class Principal(Gtk.Window):
    def __init__(self):
        self.lib_dir = "./bibliotecas/"
        mylst = Biblioteca.ObjLstBiblioteca()
        load_alarmas()
        cargar_parametros()
        self.ultimo_minuto_calculado = -1;
        self.lst_biblioteca = mylst.get_lst_biblioteca()

        self.lbl_reproductor_info = Gtk.Label("")
        self.reproductor = Reproductor(self.lbl_reproductor_info)
        self.window = Gtk.Window.__init__(self, title="MP3tador,  v0.3")

        self.set_border_width(20)

        self.color_fuente = "black"
        self.reloj = Reloj()
        self.lblhora = Gtk.Label(label= "")
        self.lbldata = Gtk.Label(label= "")
        self.tabla()
        self._update_id = GObject.timeout_add(1000, self.update_hora_timeout, None)
        #SuenaAlarma(lista_alarmas[0], self)

    def update_hora_timeout(self, kaka):
        self.update_hora()
        if (self.ultimo_minuto_calculado != self.reloj.get_minutos()):
            self.ultimo_minuto_calculado = self.reloj.get_minutos()
            for i in lista_alarmas:
                if (i.get_activa() == True):
                    if (i.get_dias() == True):
                        if ((int(i.get_minutos()) == int(self.reloj.get_minutos())) and (int(i.get_horas()) == int(self.reloj.get_horas()))):
                            SuenaAlarma(i, self)
                    else:
                        if ((self.reloj.get_dia_semana() == 0) and (i.get_lunes() == True)):
                            if ((int(i.get_minutos()) == int(self.reloj.get_minutos())) and (int(i.get_horas()) == int(self.reloj.get_horas()))):
                                SuenaAlarma(i, self)

                        if ((self.reloj.get_dia_semana() == 1) and (i.get_martes() == True)):
                            if ((int(i.get_minutos()) == int(self.reloj.get_minutos())) and (int(i.get_horas()) == int(self.reloj.get_horas()))):
                                SuenaAlarma(i, self)

                        if ((self.reloj.get_dia_semana() == 2) and (i.get_miercoles() == True)):
                            if ((int(i.get_minutos()) == int(self.reloj.get_minutos())) and (int(i.get_horas()) == int(self.reloj.get_horas()))):
                                SuenaAlarma(i, self)

                        if ((self.reloj.get_dia_semana() == 3) and (i.get_jueves() == True)):
                            if ((int(i.get_minutos()) == int(self.reloj.get_minutos())) and (int(i.get_horas()) == int(self.reloj.get_horas()))):
                                SuenaAlarma(i, self)

                        if ((self.reloj.get_dia_semana() == 4) and (i.get_viernes() == True)):
                            if ((int(i.get_minutos()) == int(self.reloj.get_minutos())) and (int(i.get_horas()) == int(self.reloj.get_horas()))):
                                SuenaAlarma(i, self)

                        if ((self.reloj.get_dia_semana() == 5) and (i.get_sabado() == True)):
                            if ((int(i.get_minutos()) == int(self.reloj.get_minutos())) and (int(i.get_horas()) == int(self.reloj.get_horas()))):
                                SuenaAlarma(i, self)

                        if ((self.reloj.get_dia_semana() == 6) and (i.get_domingo() == True)):
                            if ((int(i.get_minutos()) == int(self.reloj.get_minutos())) and (int(i.get_horas()) == int(self.reloj.get_horas()))):
                                SuenaAlarma(i, self)



                        #Dias de la semana
        return True

    def update_hora(self):
        self.lblhora.set_markup(str("<span font='50' foreground='"+self.color_fuente+"'>"+self.reloj._get_time_formated())+"</span>")
        self.lbldata.set_markup(str("<span variant='smallcaps'>" +self.reloj._get_date_formated())+"</span>")


    def tabla(self):
        table = Gtk.Table(8, 5, True)
        self.add(table)
        btn_alarmas = Gtk.Button(label="Alarmas")
        btn_alarmas.connect("clicked", self.on_btn_alarmas_clicked)

        btn_opciones = Gtk.Button(label="Opciones")
        btn_opciones.connect("clicked", self.on_btn_opciones_clicked)

        btn_play = Gtk.Button()
        btn_play.connect("clicked", self.on_btn_play_clicked)
        pb_play = GdkPixbuf.Pixbuf.new_from_file("./Icons/play2.png")
        img_play = Gtk.Image()
        img_play.set_from_pixbuf(pb_play)
        btn_play.set_image(img_play)
        btn_play.set_always_show_image (True)

        btn_stop = Gtk.Button()
        btn_stop.connect("clicked", self.on_btn_stop_clicked)
        pb_stop = GdkPixbuf.Pixbuf.new_from_file("./Icons/stop2.png")
        img_stop = Gtk.Image()
        img_stop.set_from_pixbuf(pb_stop)
        btn_stop.set_image(img_stop)
        btn_stop.set_always_show_image (True)

        btn_pause = Gtk.Button()
        btn_pause.connect("clicked", self.on_btn_pause_clicked)
        pb_pause = GdkPixbuf.Pixbuf.new_from_file("./Icons/pause2.png")
        img_pause = Gtk.Image()
        img_pause.set_from_pixbuf(pb_pause)
        btn_pause.set_image(img_pause)
        btn_pause.set_always_show_image (True)

        btn_next = Gtk.Button()
        btn_next.connect("clicked", self.on_btn_next_clicked)
        pb_next = GdkPixbuf.Pixbuf.new_from_file("./Icons/Next2.png")
        img_next = Gtk.Image()
        img_next.set_from_pixbuf(pb_next)
        btn_next.set_image(img_next)
        btn_next.set_always_show_image (True)

        btn_biblioteca = Gtk.Button(label="Biblioteca")
        btn_biblioteca.connect("clicked", self.on_btn_biblioteca_clicked)


        self.lst_biblioteca.set_active(0)
        self.lst_biblioteca.connect("changed", self.on_lst_biblioteca_changed)
        self.on_lst_biblioteca_changed(self.lst_biblioteca)

        self.update_hora()
        table.attach(self.lbldata, 0, 8, 0, 1)
        table.attach(self.lblhora, 0, 8 ,1, 5)
        table.attach(btn_alarmas, 10, 15, 2, 3)
        table.attach(btn_biblioteca, 10, 15, 4, 5)
        table.attach(btn_opciones, 10, 15, 6, 7)
        table.attach(self.lst_biblioteca, 0,8, 5,6)
        table.attach(btn_play, 0, 2, 6, 9)
        table.attach(btn_pause, 2, 4, 6, 9)
        table.attach(btn_next, 4, 6, 6, 9)
        table.attach(btn_stop, 6, 8, 6, 9)
        table.attach(self.lbl_reproductor_info, 0, 15, 10, 12)

        return self.lblhora

    def on_btn_biblioteca_clicked(self, widget):

        self.biblioteca = Biblioteca.Biblioteca(self)
        self.biblioteca.show_all()
        # self.reproductor.set_biblioteca(self.musica)

    def on_btn_opciones_clicked(self, widget):
        self.menu_opciones = MenuOpciones()

    def on_lst_biblioteca_changed(self, widget):
        lib_file = str(self.lst_biblioteca.get_active_text()) + ".lib"
        if (lib_file != "None.lib"):
            self.reproductor.stop()
            self.reproductor.load_biblioteca(lib_file)

    def reload_biblioteca(self, widget, event=None):
        self.on_lst_biblioteca_changed(self)

    def on_btn_play_clicked(self, widget):
        self.reproductor.play()

    def on_btn_stop_clicked(self, widget):
        self.reproductor.stop()

    def on_btn_pause_clicked(self, widget):
        self.reproductor.pause()

    def on_btn_next_clicked(self, widget):
        self.reproductor.next_song()

    def on_btn_alarmas_clicked(self, widget):
        alarmas = Menu_alarma()
        alarmas.show_all()




###########################################################################
win = Principal()
win.connect("delete-event", Gtk.main_quit)
win.show_all()
Gtk.main()
