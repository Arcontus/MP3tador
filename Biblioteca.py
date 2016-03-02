# -​*- coding: utf-8 -*​-

import os

from gi.repository import Gtk, Gio, GObject, GdkPixbuf
from datetime import datetime
import random
import Alarma
from Reproductor import Reproductor

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

class MenuModify(Gtk.Window):
    def __init__(self, nombre_biblioteca):
        Gtk.Window.__init__(self, title="Modificar biblioteca "+nombre_biblioteca)
        self.nombre_biblioteca = nombre_biblioteca
        self.musica = []
        self.lbl_reproductor_info = Gtk.Label()
        self.mi_reproductor = Reproductor(self.lbl_reproductor_info)
        self.load_biblioteca()
        self.set_border_width(20)
        self.grid = Gtk.Grid()
        self.grid.set_column_homogeneous(True)
        self.grid.set_row_homogeneous(True)
        self.add(self.grid)

        self.canciones_lista = Gtk.ListStore(str)
        self.rellenar_listado()

        self.treeview = Gtk.TreeView(model=self.canciones_lista)
        renderer = Gtk.CellRendererText()
        column = Gtk.TreeViewColumn("Cancion", renderer, text=0)
        column.set_sort_column_id(0)
        self.treeview.append_column(column)

        self.buttons = list()
        for prog_language in ["Reproducir", "Detener", "Eliminar", "Agregar", "Guardar", "Cancelar"]:
            button = Gtk.Button(prog_language)
            self.buttons.append(button)
            button.connect("clicked", self.on_selection_button_clicked)

        self.scrollable_treelist = Gtk.ScrolledWindow()
        self.scrollable_treelist.set_vexpand(True)
        self.grid.attach(self.scrollable_treelist, 0, 0, 6, 8)
        self.grid.attach_next_to(self.buttons[0], self.scrollable_treelist, Gtk.PositionType.BOTTOM, 1, 1)
        for i, button in enumerate(self.buttons[1:]):
            self.grid.attach_next_to(button, self.buttons[i], Gtk.PositionType.RIGHT, 1, 1)

        self.scrollable_treelist.add(self.treeview)
        self.show_all()

    def rellenar_listado(self):
        for cancion in sorted(self.musica):
            self.canciones_lista.append([cancion])

    def on_selection_button_clicked(self, widget):
        self.mi_biblioteca = []
        self.mi_reproductor.stop()
        self.tipo_boton = widget.get_label()
        if (self.tipo_boton == "Reproducir"):
            model, rows = self.treeview.get_selection().get_selected()
            if (rows != None):   ## Prevent a empty treelist
                self.mi_biblioteca.append(model[rows][0])
                self.mi_reproductor.set_biblioteca(self.mi_biblioteca)
                self.mi_reproductor.manager_biblioteca()
                self.mi_reproductor.play()
        if (self.tipo_boton == "Detener"):
            self.mi_reproductor.stop()

        if (self.tipo_boton == "Eliminar"):
            self.mi_reproductor.stop()
            selection = self.treeview.get_selection()
            model, rows = selection.get_selected_rows()
            if (len(rows) > 0): ## Prevent a empty treelist
                for row in rows:
                   iter = model.get_iter(row)
                   # Remove the ListStore row referenced by iter
                print(model[row][0])
                self.musica.remove(model[row][0])
                model.remove(iter)

        if (self.tipo_boton == "Agregar"):
            biblioteca= FileChooserWindow()
            biblioteca_aux = self.musica+biblioteca.seleccionar_carpeta()
            for i in biblioteca_aux:
                if i not in sorted(self.musica):
                    self.musica.append(i)
                    self.canciones_lista.append([i])

        if (self.tipo_boton == "Guardar"):
            lib_directory = "./bibliotecas/"
            if not os.path.exists(lib_directory):
                os.makedirs(lib_directory)
            if (len(self.musica) > 0):
                if os.path.exists(lib_directory+self.nombre_biblioteca+".lib"):
                    os.remove(lib_directory+self.nombre_biblioteca+".lib")
                fichero = open(lib_directory+self.nombre_biblioteca+".lib", "w")
                fichero.write("nombre:"+self.nombre_biblioteca+"\n")
                fichero.write("items:"+str(len(self.musica))+"\n")
                for i in self.musica:
                    fichero.write("cancion:"+i+"\n")
                fichero.close()
                self.close()
            else:
                self.error_params(self)
        if (self.tipo_boton == "Cancelar"):
            self.close()

    def error_params(self, widget):
        dialog = Gtk.MessageDialog(self, 0, Gtk.MessageType.INFO,
            Gtk.ButtonsType.OK, "Error en la modificacion de la biblioteca")
        dialog.format_secondary_text(
            "Asegurate de que la biblioteca tenga al menos un fichero de audio")
        dialog.run()
        print("Aceptar")
        dialog.destroy()


    def language_filter_func(self, model, iter, data):
        return True

    def load_biblioteca(self):
        numero = 1
        lib_directory = "./bibliotecas/"
        fichero = open(lib_directory+self.nombre_biblioteca+".lib")
        for line in fichero:
            if (line.split(":")[0] == 'nombre'):
                self.nombre = (line.split(":")[1])

            elif (line.split(":")[0] == "items"):
                items =(line.split(":")[1])

            elif (line.split(":")[0] == 'cancion'):
                self.musica.append (line.split(":")[1][:-1])
                numero = numero +1



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
    def __init__(self, obj_principal):
        Gtk.Window.__init__(self, title="Biblioteca")
        self.obj_principal = obj_principal
        window = Gtk.Table(1, 1, True)
        self.set_border_width(20)
        self.add(window)
        self.lib_dir = "./bibliotecas/"
        self.connect('delete-event', self.delete_event)
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

    def on_btn_mdf_bilbioteca_clicked(self, widget):
        MenuModify(str(self.lst_bibliotecas.get_active_text()))

    def error_rm_params(self, num):
        dialog = Gtk.MessageDialog(self, 0, Gtk.MessageType.INFO,
            Gtk.ButtonsType.OK, "Error en la eliminacion de la biblioteca")
        dialog.format_secondary_text("Error al eliminar la biblioteca.\nLa biblioteca esta siendo usada por " + str(num) + " alarma(s)")
        dialog.run()
        print("Aceptar")
        dialog.destroy()

    def delete_event(self, widget, event=None):
        self.obj_principal.reload_biblioteca(self)

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
        if not os.path.exists(self.lib_dir):
            os.makedirs(self.lib_dir)

        ficheros = os.listdir(self.lib_dir)
        for i in sorted(ficheros):
            self.add_item(i[:-4])

        self.lst_biblioteca.set_active(0)
        add_bibliotecas(self.lst_biblioteca)

    def get_lst_biblioteca(self):
        return self.lst_biblioteca

    def add_item(self, item):
        self.lst_biblioteca.append_text(item)




