# -​*- coding: utf-8 -*​-

import os

from gi.repository import Gtk, Gio, GObject, GdkPixbuf
from datetime import datetime
import random
import Alarma

lista_bibliotecas = []


def add_bibliotecas(biblioteca_id):
    lista_bibliotecas.append(biblioteca_id)

def rm_bibliotecas(biblioteca_id):
    lista_bibliotecas.remove(biblioteca_id)

def add_item_biblioteca(item):
    for indice in lista_bibliotecas:
        indice.append(str(item), str(item))

def get_id_from_text(comboboxText, text):
    modelo = comboboxText.get_model()
    posicion = 0
    for i in modelo:

        var = str(i[:])
        var = var.split(",")[0]
        var = var[2:-1]
        if (var == text): return posicion
        else: posicion = posicion +1
    return 0

class MenuAdd(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self, title="Biblioteca")
        self.window = Gtk.Table(6, 5, True)
        self.set_border_width(20)
        self.add(self.window)
        self.nombre = Gtk.Entry()
        self.biblioteca = []

        self.nombre.set_text("Nombre de la biblioteca")
        self.window.attach(self.nombre, 1,3 ,0,1)

        btn_biblioteca = Gtk.Button(label="Añadir ruta")
        btn_biblioteca.connect("clicked", self.on_btn_add_biblioteca_clicked)
        self.window.attach(btn_biblioteca, 3,4,0,1)

        self.num_items=0
        self.lbl_num_items = Gtk.Label("Canciones en la biblioteca: " + str(self.num_items))
        self.window.attach(self.lbl_num_items, 1,3 ,1,2)

        btn_aceptar = Gtk.Button(label="Aceptar")
        btn_aceptar.connect("clicked", self.on_btn_aceptar_clicked)
        self.window.attach(btn_aceptar, 1,2 ,4,5)

        btn_cancelar = Gtk.Button(label="Cancelar")
        btn_cancelar.connect("clicked", self.on_btn_cancelar_clicked)
        self.window.attach(btn_cancelar, 3,4 ,4,5)

    def on_btn_aceptar_clicked(self, widget):
        lib_directory = "./bibliotecas/"
        if not os.path.exists(lib_directory):
            os.makedirs(lib_directory)
        if ((self.num_items > 0) and (len(self.nombre.get_text()) > 0 )):
            fichero = open(lib_directory+self.nombre.get_text()+".lib", "w")
            fichero.write("nombre:"+self.nombre.get_text()+"\n")
            fichero.write("items:"+str(self.num_items)+"\n")
            for i in self.biblioteca:
                fichero.write("cancion:"+i+"\n")
            fichero.close()
            add_item_biblioteca(self.nombre.get_text())
            self.close()
        else:
            self.error_params(self)

    def error_params(self, widget):
        dialog = Gtk.MessageDialog(self, 0, Gtk.MessageType.INFO,
            Gtk.ButtonsType.OK, "Error en la creacion de la biblioteca")
        dialog.format_secondary_text(
            "Asegurate de que la biblioteca tenga nombre y de haber seleccionado al menos un fichero de audio")
        dialog.run()
        print("Aceptar")
        dialog.destroy()

    def on_btn_cancelar_clicked(self, widget):
        self.close()

    def on_btn_add_biblioteca_clicked(self, widget):
        biblioteca= FileChooserWindow()
        biblioteca_aux = self.biblioteca+biblioteca.seleccionar_carpeta()
        for i in biblioteca_aux:
            if i not in self.biblioteca:
                self.biblioteca.append(i)
        self.num_items = len(self.biblioteca)

        self.lbl_num_items.set_text("Canciones en la biblioteca: " + str(self.num_items))


class Biblioteca(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self, title="Biblioteca")
        window = Gtk.Table(1, 1, True)
        self.set_border_width(20)
        self.add(window)
        self.lib_dir = "./bibliotecas/"
        self.lst_bibliotecas = Gtk.ComboBoxText()
        self.reload_list()

        self.btn_add_biblioteca = Gtk.Button(label="Nueva biblioteca")
        self.btn_add_biblioteca.connect("clicked", self.on_btn_add_biblioteca_clicked)

        self.btn_rm_bilbioteca = Gtk.Button(label="Eliminar")
        self.btn_rm_bilbioteca.connect("clicked", self.on_btn_rm_biblioteca_clicked)

        self.btn_mdf_bilbioteca = Gtk.Button(label="Modificar")
        self.btn_mdf_bilbioteca.connect("clicked", self.on_btn_mdf_bilbioteca_clicked)

        window.attach(self.btn_add_biblioteca, 2,5,0,1)
        window.attach(self.lst_bibliotecas, 2,5, 2,3)
        window.attach(self.btn_rm_bilbioteca, 0,1,2,3)
        window.attach(self.btn_mdf_bilbioteca, 6,7 ,2,3)

    def reload_items(self, widget1, widget2):
        self.lst_bibliotecas.remove_all()
        if not os.path.exists(self.lib_dir):
            os.makedirs(self.lib_dir)
        ficheros = os.listdir(self.lib_dir)
        for i in sorted(ficheros):
            self.add_item(i[:-4])
        self.lst_bibliotecas.set_active(0)


    def reload_list(self):
        self.lst_bibliotecas.remove_all()
        if not os.path.exists(self.lib_dir):
            os.makedirs(self.lib_dir)
        ficheros = os.listdir(self.lib_dir)
        for i in sorted(ficheros):
            self.add_item(i[:-4])
        self.lst_bibliotecas.set_active(0)

    def add_item(self, item):
        self.lst_bibliotecas.append_text(item)

    def on_btn_add_biblioteca_clicked(self, widget):
        mymenu = MenuAdd()
        mymenu.show_all()
        mymenu.connect("delete-event", self.reload_items)

    def get_biblioteca(self):
        return self.biblioteca

    def on_btn_rm_biblioteca_clicked(self, widget):
        nombre=str(self.lst_bibliotecas.get_active_text())
        usos= Alarma.get_alarma_biblioteca_uso(nombre)
        if(usos > 0):
            self.error_rm_params(usos)
        else:
            os.remove(self.lib_dir+nombre+".lib")
            self.reload_list()


    def on_btn_mdf_bilbioteca_clicked(self):
        a = 0

    def error_rm_params(self, num):
        dialog = Gtk.MessageDialog(self, 0, Gtk.MessageType.INFO,
            Gtk.ButtonsType.OK, "Error en la eliminacion de la biblioteca")
        dialog.format_secondary_text("Error al eliminar la biblioteca.\nLa biblioteca esta siendo usada por " + str(num) + " alarma(s)")
        dialog.run()
        print("Aceptar")
        dialog.destroy()

class FileChooserWindow(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self, title="Seleccion libreria")
        self.biblioteca = []

    def on_file_clicked(self, widget):
        dialog = Gtk.FileChooserDialog("Selecciona un fichero", self,
            Gtk.FileChooserAction.OPEN,
            (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
             Gtk.STOCK_OPEN, Gtk.ResponseType.OK))

        self.add_filters(dialog)

        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            print("Open clicked")
            print("File selected: " + dialog.get_filename())
        elif response == Gtk.ResponseType.CANCEL:
            print("Cancel clicked")

        dialog.destroy()

    def add_filters(self, dialog):
        filter_text = Gtk.FileFilter()
        filter_text.set_name("Text files")
        filter_text.add_mime_type("text/plain")
        dialog.add_filter(filter_text)

        filter_py = Gtk.FileFilter()
        filter_py.set_name("Python files")
        filter_py.add_mime_type("text/x-python")
        dialog.add_filter(filter_py)

        filter_any = Gtk.FileFilter()
        filter_any.set_name("Any files")
        filter_any.add_pattern("*")
        dialog.add_filter(filter_any)

    def seleccionar_carpeta(self):
        self.on_folder_clicked(None)
        return self.biblioteca

    def on_folder_clicked(self, widget):
        dialog = Gtk.FileChooserDialog("Selecciona una carpeta", self,
            Gtk.FileChooserAction.SELECT_FOLDER,
            (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
             "Seleccionar", Gtk.ResponseType.OK))
        dialog.set_default_size(800, 400)

        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            print("Folder selected: " + dialog.get_filename())
            self.directorio = dialog.get_filename()
            musica = self.get_musica_from_dir(dialog.get_filename())


        elif response == Gtk.ResponseType.CANCEL:
            print("Cancel clicked")

        dialog.destroy()

    def get_directorio(self):
        return self.directorio

    def get_musica_from_dir(self, directorio):
        for root, dirs, files in os.walk(directorio):
            for file in files:
                if file.endswith(".mp3"):
                    #print(os.path.join(root, file))
                    self.biblioteca.append( str(os.path.join(root, file)))
        return self.biblioteca

class ObjLstBiblioteca():
    def __init__(self):
        self.lst_biblioteca = Gtk.ComboBoxText()
        self.lib_dir = "./bibliotecas/"
        ficheros = os.listdir(self.lib_dir)
        for i in sorted(ficheros):
            self.add_item(i[:-4])

        self.lst_biblioteca.set_active(0)
        add_bibliotecas(self.lst_biblioteca)

    def get_lst_biblioteca(self):
        return self.lst_biblioteca

    def add_item(self, item):
        self.lst_biblioteca.append_text(item)




