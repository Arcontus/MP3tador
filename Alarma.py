import os
from gi.repository import Gtk, Gio, GObject, GdkPixbuf
import Biblioteca
from Reloj import *
from Reproductor import *
import random
from random import randint
from datetime import datetime, timedelta

lista_alarmas = []

def add_alarma(alarma_id):
    lista_alarmas.append(alarma_id)

def rm_alarma(alarma_id):
    alarm_dir = "./alarmas/"
    if os.path.exists (alarm_dir+alarma_id.get_nombre()+".alarm"):
        os.remove(alarm_dir+alarma_id.get_nombre()+".alarm")
    lista_alarmas.remove(alarma_id)

def load_alarmas():
    alarm_dir = "./alarmas/"
    if not os.path.exists(alarm_dir):
            os.makedirs(alarm_dir)
    ficheros = os.listdir(alarm_dir)
    for i in sorted(ficheros):
        mi_alarma = Alarma()
        mi_alarma.cargar(str(i[:-6]))
        lista_alarmas.append( mi_alarma)

def get_alarma_por_nombre(nombre):
    for i in lista_alarmas:
        if (i.get_nombre() == nombre):
            return i
    return False

def rm_alarma_por_nombre(nombre):
    for i in lista_alarmas:
        if (i.get_nombre() == nombre):
            rm_alarma(i)

def get_alarma_biblioteca_uso(nombre):
    a = 0
    for i in lista_alarmas:
        if (i.get_biblioteca() == nombre):
            a = a +1
    return a


class Menu_alarma(Gtk.Window):
    def __init__(self):
        self.window = Gtk.Window.__init__(self, title="Menu de alarmas")
        self.lib_dir = "./bibliotecas/"
        table = Gtk.Table(6, 4, True)
        self.add(table)
        self.set_border_width(20)
        self.lst_alarmas = Gtk.ComboBoxText()
        self.lista_botones_alarma = []
        for i in lista_alarmas:
            self.add_item(i.get_nombre())
        self.lst_alarmas.set_active(0)
        self.btn_add_alarm = Gtk.Button.new_with_label("Agregar nueva alarma")
        self.btn_add_alarm.connect("clicked", self.on_click_btn_add_alarm)
        self.btn_modificar = Gtk.Button.new_with_label("Modificar")
        self.btn_modificar.connect("clicked", self.on_click_modificar)
        self.btn_rm_alarm = Gtk.Button.new_with_label("Eliminar")
        self.btn_rm_alarm.connect("clicked", self.on_click_btn_rm_alarm)

        self.lbl_alarma_rapida = Gtk.Label(label="Alarma rapida")
        self.lbl_biblioteca = Gtk.Label(label="Biblioteca")
        self.btn_add_quick_allarm15 = Gtk.Button.new_with_label("15 Min")
        self.btn_add_quick_allarm15.connect("clicked", self.on_click_btn_add_quick_allarm15)
        self.btn_add_quick_allarm30 = Gtk.Button.new_with_label("30 Min")
        self.btn_add_quick_allarm30.connect("clicked", self.on_click_btn_add_quick_allarm30)
        self.btn_add_quick_allarm45 = Gtk.Button.new_with_label("45 Min")
        self.btn_add_quick_allarm45.connect("clicked", self.on_click_btn_add_quick_allarm45)
        self.btn_add_quick_allarm1 = Gtk.Button.new_with_label("1 Hora")
        self.btn_add_quick_allarm1.connect("clicked", self.on_click_btn_add_quick_allarm1)

        self.lst_bibliotecas = Gtk.ComboBoxText()
        if not os.path.exists(self.lib_dir):
            os.makedirs(self.lib_dir)
        ficheros = os.listdir(self.lib_dir)
        for i in sorted(ficheros):
            self.lst_bibliotecas.append_text(i[:-4])
        self.lst_bibliotecas.set_active(0)

        table.attach(self.btn_add_alarm, 2, 5, 1, 2)
        table.attach(self.lst_alarmas, 2,5, 3,4)
        table.attach(self.btn_modificar, 6,7, 3,4)
        table.attach(self.btn_rm_alarm,0,1, 3,4)
        table.attach(self.lbl_alarma_rapida,0,4, 6,7)
        table.attach(self.lbl_biblioteca,5,7, 6,7)
        table.attach(self.btn_add_quick_allarm15,0,1, 7,8)
        table.attach(self.btn_add_quick_allarm30,1,2, 7,8)
        table.attach(self.btn_add_quick_allarm45,2,3, 7,8)
        table.attach(self.btn_add_quick_allarm1,3,4, 7,8)
        table.attach(self.lst_bibliotecas,4,7, 7,8)

    def on_click_btn_add_quick_allarm15(self, widget):
        alarma = SuenaAlarmaRapida(self.lst_bibliotecas.get_active_text())
        alarma.retardar(1)

    def on_click_btn_add_quick_allarm30(self, widget):
        alarma = SuenaAlarmaRapida(self.lst_bibliotecas.get_active_text())
        alarma.retardar(30)

    def on_click_btn_add_quick_allarm45(self, widget):
        alarma = SuenaAlarmaRapida(self.lst_bibliotecas.get_active_text())
        alarma.retardar(45)

    def on_click_btn_add_quick_allarm1(self, widget):
        alarma = SuenaAlarmaRapida(self.lst_bibliotecas.get_active_text())
        alarma.retardar(60)

    def reset_items(self):
        self.lst_alarmas.remove_all()

    def add_item(self, item):
        self.lst_alarmas.append_text(item)

    def on_click_modificar(self, widget):
        alarma = VentanaAlarma(self, self.lst_alarmas.get_active_text())

    def on_click_btn_add_alarm(self, widget):
        alarma = VentanaAlarma(self, "Alarma " + str(int(len(self.lst_alarmas.get_model())) + 1))
        alarma.connect("delete-event", self.reload_items)

    def reload_items(self, widget, widget2):
        self.reset_items()
        for i in sorted(lista_alarmas):
            self.add_item(i.get_nombre())
        self.lst_alarmas.set_active(0)


    def on_click_btn_rm_alarm(self, widget):
        alarma = self.lst_alarmas.get_active_text()
        rm_alarma_por_nombre(alarma)
        self.reload_items(self, self)

class Alarma():
    def __init__(self):
        self.nombre = ""
        self.lib_dir =  "./bibliotecas/"
        self.alarm_dir =  "./alarmas/"
        self.myfile = ""
        self.activa = False
        self.dias = False
        self.lunes = False
        self.martes = False
        self.miercoles = False
        self.jueves = False
        self.viernes = False
        self.sabado = False
        self.domingo = False
        self.horas = 0
        self.minutos = 0
        self.biblioteca = ""
        self.snooze = False
        self.min_snooze = 5

    def set_nombre(self, nombre):
        self.nombre = nombre

    def set_mifichero(self):
        if not os.path.exists(self.alarm_dir):
            os.makedirs(self.alarm_dir)
        self.myfile = self.alarm_dir+str(self.nombre) + ".alarm"

    def cargar(self, nombre):
        self.set_nombre(nombre)
        self.set_mifichero()
        self.load_params()

    def load_params(self):
        if os.path.isfile(self.myfile):
            fichero = open(self.myfile, "r")
            for line in fichero:
                if (line.split(":")[0] == 'activa'):
                    if ((line.split(":")[1]) == "True\n"):
                        self.activa = True
                    else:
                        self.activa = False

                elif (line.split(":")[0] == "dias"):
                    if ((line.split(":")[1]) == "True\n"):
                        self.dias = True
                    else:
                        self.dias = False

                elif (line.split(":")[0] == "lunes"):
                    if ((line.split(":")[1]) == "True\n"):
                        self.lunes = True
                    else:
                        self.lunes = False

                elif (line.split(":")[0] == "martes"):
                    if ((line.split(":")[1]) == "True\n"):
                        self.martes = True
                    else:
                        self.martes = False

                elif (line.split(":")[0] == "miercoles"):
                    if ((line.split(":")[1]) == "True\n"):
                        self.miercoles = True
                    else:
                        self.miercoles = False

                elif (line.split(":")[0] == "jueves"):
                    if ((line.split(":")[1]) == "True\n"):
                        self.jueves = True
                    else:
                        self.jueves = False

                elif (line.split(":")[0] == "viernes"):
                    if ((line.split(":")[1]) == "True\n"):
                        self.viernes = True
                    else:
                        self.viernes = False

                elif (line.split(":")[0] == "sabado"):
                    if ((line.split(":")[1]) == "True\n"):
                        self.sabado = True
                    else:
                        self.sabado = False

                elif (line.split(":")[0] == "domingo"):
                    if ((line.split(":")[1]) == "True\n"):
                        self.domingo = True
                    else:
                        self.domingo = False

                elif (line.split(":")[0] == "hora"):
                    self.horas= int(line.split(":")[1])

                elif (line.split(":")[0] == "minutos"):
                    self.minutos = int(line.split(":")[1])

                elif (line.split(":")[0] == "biblioteca"):
                    self.biblioteca = str(line.split(":")[1])[:-1]

                elif (line.split(":")[0] == "snooze"):
                    if ((line.split(":")[1]) == "True\n"):
                        self.snooze = True
                    else:
                        self.snooze = False

                elif (line.split(":")[0] == "min_snooze"):
                    self.min_snooze = int(line.split(":")[1])

        fichero.close()

    def save_params(self):
        fichero = open(self.alarm_dir + self.nombre + ".alarm", "w")
        fichero.write("activa:"+str(self.activa)+"\n")
        fichero.write("dias:"+str(self.dias)+"\n")
        fichero.write("lunes:"+str(self.lunes)+"\n")
        fichero.write("martes:"+str(self.martes)+"\n")
        fichero.write("miercoles:"+str(self.miercoles)+"\n")
        fichero.write("jueves:"+str(self.jueves)+"\n")
        fichero.write("viernes:"+str(self.viernes)+"\n")
        fichero.write("sabado:"+str(self.sabado)+"\n")
        fichero.write("domingo:"+str(self.domingo)+"\n")
        fichero.write("hora:"+self.horas+"\n")
        fichero.write("minutos:"+self.minutos+"\n")
        fichero.write("biblioteca:"+self.biblioteca+"\n")
        fichero.write("snooze:"+str(self.snooze)+"\n")
        fichero.write("min_snooze:"+str(self.min_snooze)+"\n")
        fichero.close()

    def get_nombre(self):
        return self.nombre
    def set_nombre(self, nombre):
        self.nombre = nombre

    def get_myfile(self):
        return self.myfile
    def set_myfile(self, file):
        self.myfile = file

    def get_activa(self):
        return self.activa

    def set_activa(self, activa):
        self.activa = activa

    def get_dias(self):
        return self.dias
    def set_dias(self,dias):
        self.dias= dias

    def get_lunes(self):
        return self.lunes
    def set_lunes(self,lunes):
        self.lunes = lunes

    def get_martes(self):
        return self.martes
    def set_martes(self, martes):
        self.martes = martes

    def get_miercoles(self):
        return self.miercoles
    def set_miercoles(self, miercoles):
        self.miercoles =miercoles

    def get_jueves(self):
        return self.jueves
    def set_jueves(self,jueves):
        self.jueves = jueves

    def get_viernes(self):
        return self.viernes
    def set_viernes(self, viernes):
        self.viernes = viernes

    def get_sabado(self):
        return self.sabado
    def set_sabado(self, sabado):
        self.sabado = sabado

    def get_domingo(self):
        return self.domingo
    def set_domingo(self, domingo):
        self.domingo = domingo

    def get_horas(self):
        return self.horas
    def set_horas(self, horas):
        self.horas = horas

    def get_minutos(self):
        return self.minutos
    def set_minutos(self, minutos):
        self.minutos = minutos

    def get_biblioteca(self):
        return self.biblioteca
    def set_biblioteca(self, biblioteca):
        self.biblioteca = biblioteca

    def get_snooze(self):
        return self.snooze
    def set_snooze(self, snooze):
        self.snooze = snooze

    def get_min_snooze(self):
        return self.min_snooze
    def set_min_snooze(self, minutos):
        self.min_snooze = minutos

class SuenaAlarmaRapida(Gtk.Window):
    def __init__(self, biblioteca):
        self.window = Gtk.Window.__init__(self)
        self.set_name('Alarma')
        self.set_modal(True)
        self.set_decorated(False)
        self.set_position(Gtk.WindowPosition.CENTER)
        self.set_border_width(20)
        self.table = Gtk.Table(5, 5, True)
        self.add(self.table)
        self.connect('delete-event', self.mi_delete_event)

        self.cronometro = cronometro()


        self.codigo1 = []
        self.codigo2 = []
        self.lbl_nombre = Gtk.Label(label="Alarma rapida")
        self.lbl_tiempo = Gtk.Label(label="00:00")
        self.lbl_reproductor_info = Gtk.Label()
        self.reproductor = Reproductor(self.lbl_reproductor_info)
        self.reproductor.load_biblioteca(biblioteca+".lib")

        self.tiempo_cero = self.cronometro.get_time_now() - self.cronometro.get_time_now()

        self.btn_next = Gtk.Button()
        self.btn_next.connect("clicked", self.on_btn_next_clicked)
        pb_next = GdkPixbuf.Pixbuf.new_from_file("./Icons/Next2.png")
        img_next = Gtk.Image()
        img_next.set_from_pixbuf(pb_next)
        self.btn_next.set_image(img_next)
        self.btn_next.set_always_show_image (True)

        self.snooze = True

        self.btn_snooze = Gtk.Button()
        self.btn_snooze.connect("clicked", self.on_btn_snooze_clicked)
        self.lbl_btn_snooze = "Snooze "+str(10)+" Min\n"
        self.btn_snooze.set_label(self.lbl_btn_snooze)
        self.table.attach(self.btn_snooze, 0,2, 4,6)

        self.lst_sw_desact = []
        self.lst_lbl_desact = []
        for i in range(8):
            self.lst_sw_desact.append(Gtk.Switch())
            self.lst_lbl_desact.append(Gtk.Label(label=i))
            self.lst_sw_desact[i].connect("notify::active", self.on_sw_desact_activated)
            if (i < 4):
                self.table.attach(self.lst_sw_desact[i], i,i+1, 7,8)
            else:
                self.table.attach(self.lst_sw_desact[i], i-4,i-3, 9,10)

        self.lbl_combinacion1 = Gtk.Label()
        self.lbl_combinacion2 = Gtk.Label()

        self.nueva_combinacion()

        self.table.attach(self.lbl_nombre, 0,2, 0,1)
        self.table.attach(self.lbl_tiempo, 2,5, 0,1)
        self.table.attach(self.lbl_reproductor_info, 0,5, 2,4)

        self.table.attach(self.btn_next, 3,5, 4,6)
        self.table.attach(self.lbl_combinacion1, 1,4, 10,11)
        self.table.attach(self.lbl_combinacion2, 1,4, 11,12)

        self.update_id = GObject.timeout_add(1000, self.update_hora_timeout, None)

        self.show_all()


    def on_btn_snooze_clicked(self, widget):
        self.snooze = True
        self.cronometro_snooze = cronometro()
        minuto = timedelta(minutes=1)
        self.desactivar = self.cronometro_snooze.get_time_now()+(minuto * 10)
        self.cronometro_snooze._set_time((self.cronometro_snooze.get_time_now()+(minuto * 10)) - self.cronometro_snooze.get_time_now())
        self.reproductor.stop()

    def retardar(self, minutos):
        self.snooze = True
        self.cronometro_snooze = cronometro()
        minuto = timedelta(minutes=1)
        self.desactivar = self.cronometro_snooze.get_time_now()+(minuto * minutos)
        self.cronometro_snooze._set_time((self.cronometro_snooze.get_time_now()+(minuto * minutos)) - self.cronometro_snooze.get_time_now())
        self.reproductor.stop()

    def update_hora_timeout(self, kaka):
        self.cronometro.update()
        self.lbl_tiempo.set_text(str("Tiempo desde inicio Alarma: "+str(self.cronometro._get_time_formated()))[:-7])
        if (self.snooze == True):
            self.cronometro_snooze.update()
            tiempo = self.desactivar - self.cronometro_snooze.get_time_now()
            if (tiempo > self.tiempo_cero):
                self.btn_snooze.set_label(self.lbl_btn_snooze + str(tiempo)[:-7])

            else:
                self.reproductor.next_song()
                self.snooze = False
                self.btn_snooze.set_label(self.lbl_btn_snooze)

        return True

    def on_sw_desact_activated(self, switch, gparam):
        if (switch.get_active() == True):
            self.codigo2[int(self.get_switch_number_from_label(switch))] = 1
        else:
            self.codigo2[int(self.get_switch_number_from_label(switch))] = 0
        self.txt_combinacion2 = "Combinacion introducida: "+str(self.codigo2)
        self.lbl_combinacion2.set_text(self.txt_combinacion2)
        print self.codigo1
        print self.codigo2
        if (self.codigo1 == self.codigo2):
            self.on_btn_stop_clicked(self)


    def get_switch_number_from_label(self, switch):
        posicion = self.get_switch_position_from_list(switch)
        return self.lst_lbl_desact[posicion].get_text()

    def get_switch_position_from_list(self, switch):
        for i in range(8):
            if (self.lst_sw_desact[i] == switch):
                return i

    def reset_combinacion(self):
        for i in range(8):
            self.table.remove(self.lst_lbl_desact[i])

    def nueva_combinacion(self):
        random.shuffle(self.lst_lbl_desact)
        for i in range(8):
            self.codigo2.append(0)
            if (i < 4):
                self.table.attach(self.lst_lbl_desact[i], i,i+1, 6,7)
            else:
                self.table.attach(self.lst_lbl_desact[i], i-4,i-3, 8,9)
        for i in range(randint(4,5)):
            self.codigo1.append(1)
        for i in range(8-len(self.codigo1)):
            self.codigo1.append(0)
        random.shuffle(self.codigo1)
        self.txt_combinacion1 = "Combinacion de desbloqueo: "+str(self.codigo1)
        self.lbl_combinacion1.set_text(self.txt_combinacion1)

    def on_btn_stop_clicked(self, widget):
        self.mi_delete_event(self, None)

    def on_btn_next_clicked(self, widget):
        self.reproductor.next_song()

    def mi_delete_event(self, widget, event=None):
        GObject.source_remove(self.update_id)
        self.reproductor.stop()
        self.destroy()

class SuenaAlarma(Gtk.Window):
    def __init__(self, alarma, obj_principal):
        self.window = Gtk.Window.__init__(self)
        self.set_name('Alarma')
        self.set_modal(True)
        self.set_decorated(False)
        self.set_position(Gtk.WindowPosition.CENTER)
        self.set_border_width(20)
        self.table = Gtk.Table(5, 5, True)
        self.add(self.table)
        self.connect('delete-event', self.mi_delete_event)
        self.obj_principal = obj_principal
        self.cronometro = cronometro()

        self.alarma = alarma
        self.codigo1 = []
        self.codigo2 = []
        self.lbl_nombre = Gtk.Label(label=alarma.get_nombre())
        self.lbl_tiempo = Gtk.Label(label="00:00")
        self.lbl_reproductor_info = Gtk.Label()
        self.reproductor = Reproductor(self.lbl_reproductor_info)
        self.reproductor.load_biblioteca(self.alarma.get_biblioteca()+".lib")
        self.reproductor.play()
        self.tiempo_cero = self.cronometro.get_time_now() - self.cronometro.get_time_now()

        self.btn_next = Gtk.Button()
        self.btn_next.connect("clicked", self.on_btn_next_clicked)
        pb_next = GdkPixbuf.Pixbuf.new_from_file("./Icons/Next2.png")
        img_next = Gtk.Image()
        img_next.set_from_pixbuf(pb_next)
        self.btn_next.set_image(img_next)
        self.btn_next.set_always_show_image (True)

        self.snooze = False
        if (self.alarma.get_snooze() == True):
            self.btn_snooze = Gtk.Button()
            self.btn_snooze.connect("clicked", self.on_btn_snooze_clicked)
            self.lbl_btn_snooze = "Snooze "+str(self.alarma.get_min_snooze())+" Min\n"
            self.btn_snooze.set_label(self.lbl_btn_snooze)
            self.table.attach(self.btn_snooze, 0,2, 4,6)

        self.lst_sw_desact = []
        self.lst_lbl_desact = []
        for i in range(8):
            self.lst_sw_desact.append(Gtk.Switch())
            self.lst_lbl_desact.append(Gtk.Label(label=i))
            self.lst_sw_desact[i].connect("notify::active", self.on_sw_desact_activated)
            if (i < 4):
                self.table.attach(self.lst_sw_desact[i], i,i+1, 7,8)
            else:
                self.table.attach(self.lst_sw_desact[i], i-4,i-3, 9,10)

        self.lbl_combinacion1 = Gtk.Label()
        self.lbl_combinacion2 = Gtk.Label()

        self.nueva_combinacion()

        self.table.attach(self.lbl_nombre, 0,2, 0,1)
        self.table.attach(self.lbl_tiempo, 2,5, 0,1)
        self.table.attach(self.lbl_reproductor_info, 0,5, 2,4)

        self.table.attach(self.btn_next, 3,5, 4,6)
        self.table.attach(self.lbl_combinacion1, 1,4, 10,11)
        self.table.attach(self.lbl_combinacion2, 1,4, 11,12)

        self.update_id = GObject.timeout_add(1000, self.update_hora_timeout, None)

        self.show_all()


    def on_btn_snooze_clicked(self, widget):
        self.snooze = True
        self.cronometro_snooze = cronometro()
        minuto = timedelta(minutes=1)
        self.desactivar = self.cronometro_snooze.get_time_now()+(minuto * self.alarma.get_min_snooze())
        self.cronometro_snooze._set_time((self.cronometro_snooze.get_time_now()+(minuto * self.alarma.get_min_snooze())) - self.cronometro_snooze.get_time_now())
        self.reproductor.stop()

    def update_hora_timeout(self, kaka):
        self.cronometro.update()
        self.lbl_tiempo.set_text(str("Tiempo desde primera Alarma: "+str(self.cronometro._get_time_formated()))[:-7])
        if (self.snooze == True):
            self.cronometro_snooze.update()
            tiempo = self.desactivar - self.cronometro_snooze.get_time_now()
            if (tiempo > self.tiempo_cero):
                self.btn_snooze.set_label(self.lbl_btn_snooze + str(tiempo)[:-7])

            else:
                self.reproductor.next_song()
                self.snooze = False
                self.btn_snooze.set_label(self.lbl_btn_snooze)

        return True

    def on_sw_desact_activated(self, switch, gparam):
        if (switch.get_active() == True):
            self.codigo2[int(self.get_switch_number_from_label(switch))] = 1
        else:
            self.codigo2[int(self.get_switch_number_from_label(switch))] = 0
        self.txt_combinacion2 = "Combinacion introducida: "+str(self.codigo2)
        self.lbl_combinacion2.set_text(self.txt_combinacion2)
        print self.codigo1
        print self.codigo2
        if (self.codigo1 == self.codigo2):
            self.on_btn_stop_clicked(self)


    def get_switch_number_from_label(self, switch):
        posicion = self.get_switch_position_from_list(switch)
        return self.lst_lbl_desact[posicion].get_text()

    def get_switch_position_from_list(self, switch):
        for i in range(8):
            if (self.lst_sw_desact[i] == switch):
                return i

    def reset_combinacion(self):
        for i in range(8):
            self.table.remove(self.lst_lbl_desact[i])

    def nueva_combinacion(self):
        random.shuffle(self.lst_lbl_desact)
        for i in range(8):
            self.codigo2.append(0)
            if (i < 4):
                self.table.attach(self.lst_lbl_desact[i], i,i+1, 6,7)
            else:
                self.table.attach(self.lst_lbl_desact[i], i-4,i-3, 8,9)
        for i in range(randint(4,5)):
            self.codigo1.append(1)
        for i in range(8-len(self.codigo1)):
            self.codigo1.append(0)
        random.shuffle(self.codigo1)
        self.txt_combinacion1 = "Combinacion de desbloqueo: "+str(self.codigo1)
        self.lbl_combinacion1.set_text(self.txt_combinacion1)

    def on_btn_stop_clicked(self, widget):
        self.mi_delete_event(self, None)

    def on_btn_next_clicked(self, widget):
        self.reproductor.next_song()

    def mi_delete_event(self, widget, event=None):
        GObject.source_remove(self.update_id)
        self.reproductor.stop()
        self.obj_principal.reload_biblioteca(None)
        self.destroy()

class VentanaAlarma(Gtk.Window):
    def __init__(self, parent, nombre):
        self.window = Gtk.Window.__init__(self, title=str(nombre))
        self.connect('delete-event', self.delete_event)
        table = Gtk.Table(11, 7, True)
        self.miLstBiblioteca = Biblioteca.ObjLstBiblioteca()
        self.lst_biblioteca = self.miLstBiblioteca.get_lst_biblioteca()
        self.set_border_width(20)
        self.add(table)
        self.nombre = nombre
        self.lib_dir = "./bibliotecas/"
        self.temporalidad = 0 #Indica si existe un fichero de alarma asociado o bien es una alarma virtual.

        lbl_nombre = Gtk.Label("Nombre")
        self.ent_nombre = Gtk.Entry()
        self.ent_nombre.set_text(str(nombre))

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
        table.attach(self.lst_biblioteca,2,5, 8,9)
        table.attach(self.btn_guardar,1,3,10,11)
        table.attach(self.btn_cancelar,4,6,10,11)
        self.show_all()

    def on_click_cancelar(self, button):
        self.close()

    def update_sensitives(self):
        # Comprobamos el status de la alarma
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
        self.miAlarma = get_alarma_por_nombre(self.nombre)
        if (self.miAlarma == False):
            self.temporalidad = 1
            self.miAlarma = Alarma()
            self.miAlarma.set_nombre(self.nombre)
            add_alarma(self.miAlarma)

        self.sw_activa.set_active(self.miAlarma.get_activa())
        self.sw_dias.set_active(self.miAlarma.get_dias())
        self.chk_lunes.set_active(self.miAlarma.get_lunes())
        self.chk_martes.set_active(self.miAlarma.get_martes())
        self.chk_miercoles.set_active(self.miAlarma.get_miercoles())
        self.chk_jueves.set_active(self.miAlarma.get_jueves())
        self.chk_viernes.set_active(self.miAlarma.get_viernes())
        self.chk_sabado.set_active(self.miAlarma.get_sabado())
        self.chk_domingo.set_active(self.miAlarma.get_domingo())
        self.spb_horas.set_value(int(self.miAlarma.get_horas()))
        self.spb_minutos.set_value(int(self.miAlarma.get_minutos()))
        self.lst_biblioteca.set_active(Biblioteca.get_id_from_text(self.lst_biblioteca, self.miAlarma.get_biblioteca()))
        self.spb_snooze.set_value(int(self.miAlarma.get_min_snooze()))
        self.sw_snooze.set_active(self.miAlarma.get_snooze())

    def on_click_guardar(self, button):
        self.miAlarma = get_alarma_por_nombre(self.nombre)
        if (self.miAlarma == False):
            print "Creamos uno nuevo"
            self.miAlarma = Alarma()
            self.miAlarma.set_nombre(self.nombre)
            add_alarma(self.miAlarma)
        self.miAlarma.set_nombre(self.ent_nombre.get_text())
        self.miAlarma.set_activa(self.sw_activa.get_active())
        self.miAlarma.set_dias(self.sw_dias.get_active())
        self.miAlarma.set_lunes(self.chk_lunes.get_active())
        self.miAlarma.set_martes(self.chk_martes.get_active())
        self.miAlarma.set_miercoles(self.chk_miercoles.get_active())
        self.miAlarma.set_jueves(self.chk_jueves.get_active())
        self.miAlarma.set_viernes(self.chk_viernes.get_active())
        self.miAlarma.set_sabado(self.chk_sabado.get_active())
        self.miAlarma.set_domingo(self.chk_domingo.get_active())
        self.miAlarma.set_horas(str(self.spb_horas.get_value_as_int()))
        self.miAlarma.set_minutos(str(self.spb_minutos.get_value_as_int()))
        self.miAlarma.set_biblioteca(str(self.lst_biblioteca.get_active_text()))
        self.miAlarma.set_snooze(self.sw_snooze.get_active())
        self.miAlarma.set_min_snooze(self.spb_snooze.get_value_as_int())
        self.miAlarma.save_params()
        self.close()
        self.temporalidad = 0

    def delete_event(self, widget, event=None):
        Biblioteca.rm_bibliotecas(self.lst_biblioteca)
        if (self.temporalidad == 1):
            rm_alarma(self.miAlarma)
