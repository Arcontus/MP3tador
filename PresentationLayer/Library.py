# -*- coding: utf-8 -*-
import gi
import os
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GdkPixbuf

class LibraryManagerWindow(Gtk.Window):
    def __init__(self, my_library_screen_controller=None):
        if my_library_screen_controller:
            self.my_library_screen_controller = my_library_screen_controller
        else:
            raise NameError("LibraryManager needs library_screen_controller instance")
        self.window = Gtk.Window.__init__(self, title="Menu de bibliotecas")
        Gtk.Window.__init__(self, title="Biblioteca")
        window = Gtk.Table(1, 1, True)
        self.set_border_width(20)
        self.add(window)
        self.connect('delete-event', self.delete_event)
        self.lst_library = Gtk.ComboBoxText()

        self.btn_add_library = Gtk.Button(label="Nueva biblioteca")
        self.btn_add_library.connect("clicked", self.on_btn_add_library_clicked)

        self.btn_rm_library = Gtk.Button(label="Eliminar")
        self.btn_rm_library.connect("clicked", self.on_btn_rm_library_clicked)

        self.btn_mdf_library = Gtk.Button(label="Modificar")
        self.btn_mdf_library.connect("clicked", self.on_btn_mdf_library_clicked)

        window.attach(self.btn_add_library, 2,5,0,1)
        window.attach(self.lst_library, 2, 5, 2, 3)
        window.attach(self.btn_rm_library, 0,1,2,3)
        window.attach(self.btn_mdf_library, 6,7 ,2,3)

    def reload_library_items(self, items):
        self.reset_library_items()
        for i in sorted(items):
            self.add_library_item(i)
        self.lst_library.set_active(0)

    def add_library_item(self, item):
        self.lst_library.append_text(item)

    def reset_library_items(self):
        self.lst_library.remove_all()

    def on_btn_add_library_clicked(self, widget):
        self.my_library_screen_controller.open_new_library_window()

    def get_library(self):
        a =1

    def on_btn_rm_library_clicked(self, widget):
        a =1

    def on_btn_mdf_library_clicked(self, widget):
        a =1

    def error_rm_params(self, num):
        a =1

    def delete_event(self, widget, event=None):
        a =1


class AddNewLibrary(Gtk.Window):
    def __init__(self, my_library_screen_controller=None):
        if my_library_screen_controller:
            self.my_library_screen_controller = my_library_screen_controller
        else:
            raise NameError("AlarmManager needs alarm_screen_controller instance")
        Gtk.Window.__init__(self, title="Agregar Biblioteca")
        self.window = Gtk.Table(6, 5, True)
        self.set_border_width(20)
        self.add(self.window)
        self.library_dic = {'name': '', 'items': 0,
                            'songs': []}
        self.name = Gtk.Entry()
        self.library = []

        self.name.set_text("Nombre de la biblioteca")
        self.window.attach(self.name, 1, 3, 0, 1)

        btn_library = Gtk.Button(label="Añadir ruta")
        btn_library.connect("clicked", self.on_btn_add_library_clicked)
        self.window.attach(btn_library, 3,4,0,1)

        self.num_items=0
        self.lbl_num_items = Gtk.Label("Canciones en la biblioteca: " + str(self.num_items))
        self.window.attach(self.lbl_num_items, 1,3 ,1,2)

        btn_accept = Gtk.Button(label="Aceptar")
        btn_accept.connect("clicked", self.on_btn_accept_clicked)
        self.window.attach(btn_accept, 1,2 ,4,5)

        btn_cancel = Gtk.Button(label="Cancelar")
        btn_cancel.connect("clicked", self.on_btn_cancel_clicked)
        self.window.attach(btn_cancel, 3,4 ,4,5)
        self.show_all()

    def on_btn_accept_clicked(self, widget):
        self.library_dic = {'name': self.name.get_text(), 'items': len(self.library),
                            'songs': self.library}


    def error_params(self, widget):
        a = 1

    def on_btn_cancel_clicked(self, widget):
        self.close()

    def on_btn_add_library_clicked(self, widget):
        library = FileChooserWindow()
        library_aux = self.library+library.select_folder()

        # It Check if the same songs exists on library, if not add it.
        for i in library_aux:
            if i not in self.library:
                self.library.append(i)
        self.num_items = len(self.library)

        self.lbl_num_items.set_text("Canciones en la biblioteca: " + str(self.num_items))


class FileChooserWindow(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self, title="Seleccion libreria")
        self.library = []

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

    @staticmethod
    def add_filters(dialog):
        filter_any = Gtk.FileFilter()
        filter_any.set_name("Any files")
        filter_any.add_pattern("*")
        dialog.add_filter(filter_any)

    def select_folder(self):
        self.on_folder_clicked(None)
        return self.library

    def on_folder_clicked(self, widget):
        dialog = Gtk.FileChooserDialog("Selecciona una carpeta", self,
            Gtk.FileChooserAction.SELECT_FOLDER,
            (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
             "Seleccionar", Gtk.ResponseType.OK))
        dialog.set_default_size(800, 400)

        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            print("Folder selected: " + dialog.get_filename())
            self.directory = dialog.get_filename()
            music = self.get_music_from_dir(dialog.get_filename())

        elif response == Gtk.ResponseType.CANCEL:
            print("Cancel clicked")

        dialog.destroy()

    def get_directory(self):
        return self.directory

    def get_music_from_dir(self, directory):
        for root, dirs, files in os.walk(directory):
            for file in files:
                if file.endswith(".mp3"):
                    #print(os.path.join(root, file))
                    self.library.append(str(os.path.join(root, file)))
        return self.library