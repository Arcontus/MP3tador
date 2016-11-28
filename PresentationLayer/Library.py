# -*- coding: utf-8 -*-
import gi
import os
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk


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
        self.my_library_screen_controller.open_library_config()

    def get_library(self):
        a =1

    def on_btn_rm_library_clicked(self, widget):
        self.my_library_screen_controller.delete_library(self.lst_library.get_active_text())

    def on_btn_mdf_library_clicked(self, widget):
        self.my_library_screen_controller.open_library_config(self.lst_library.get_active_text())

    def delete_event(self, widget, event=None):
        a =1


class LibraryConfigWindow(Gtk.Window):
    def __init__(self, title, my_library_screen_controller=None):
        if my_library_screen_controller:
            self.my_library_screen_controller = my_library_screen_controller
        else:
            raise NameError("AlarmManager needs alarm_screen_controller instance")
        Gtk.Window.__init__(self, title=title)
        self.connect('delete-event', self.delete_event)
        self.set_border_width(20)
        self.grid = Gtk.Grid()
        self.grid.set_column_homogeneous(True)
        self.grid.set_row_homogeneous(True)
        self.grid.set_row_spacing(20)
        self.grid.set_column_spacing(10)
        self.add(self.grid)

        self.library_dic = {'name': '', 'items': 0,
                            'songs': []}

        self.library = []

        self.gtk_song_list = Gtk.ListStore(str)
        self.fill_song_list()

        self.treeview = Gtk.TreeView(model=self.gtk_song_list)
        renderer = Gtk.CellRendererText()
        column = Gtk.TreeViewColumn("Cancion", renderer, text=0)
        column.set_sort_column_id(0)
        self.treeview.append_column(column)

        self.buttons = list()
        for prog_language in ["Reproducir", "Detener", "Eliminar"]:
            button = Gtk.Button(prog_language)
            self.buttons.append(button)
            button.connect("clicked", self.on_selection_button_clicked)

        self.scrollable_treelist = Gtk.ScrolledWindow()
        self.scrollable_treelist.set_vexpand(True)
        self.lbl_name = Gtk.Label("Nombre de la biblioteca")
        self.name = Gtk.Entry()
        self.name.set_text(title)
        self.grid.attach(self.lbl_name, 0, 0, 2, 1)
        self.grid.attach_next_to(self.name, self.lbl_name, Gtk.PositionType.BOTTOM, 2, 1)
        btn_library = Gtk.Button(label="Añadir ruta")
        btn_library.connect("clicked", self.on_btn_add_library_clicked)
        self.grid.attach_next_to(btn_library, self.lbl_name, Gtk.PositionType.RIGHT, 2, 1)
        self.num_items = 0
        self.lbl_num_items = Gtk.Label("Canciones en la biblioteca: " + str(self.num_items))
        self.grid.attach_next_to(self.lbl_num_items, self.name, Gtk.PositionType.RIGHT, 2, 1)

        self.grid.attach_next_to(self.scrollable_treelist, self.name, Gtk.PositionType.BOTTOM, 5, 7)
        self.grid.attach_next_to(self.buttons[0], self.scrollable_treelist, Gtk.PositionType.BOTTOM, 1, 1)
        for i, button in enumerate(self.buttons[1:]):
            self.grid.attach_next_to(button, self.buttons[i], Gtk.PositionType.RIGHT, 1, 1)

        self.scrollable_treelist.add(self.treeview)

        btn_accept = Gtk.Button(label="Aceptar")
        btn_accept.connect("clicked", self.on_btn_accept_clicked)
        self.grid.attach_next_to(btn_accept, self.buttons[0], Gtk.PositionType.BOTTOM, 1, 1)

        btn_cancel = Gtk.Button(label="Cancelar")
        btn_cancel.connect("clicked", self.on_btn_cancel_clicked)
        self.grid.attach_next_to(btn_cancel, btn_accept, Gtk.PositionType.RIGHT,1,1)
        self.show_all()

    def fill_song_list(self):
        for song in sorted(self.library):
            self.gtk_song_list.append([song])

    def set_library(self, library):
        self.library = library
        self.recalculate()

    def set_library_name(self, name):
        self.name.set_text(name)
        self.name.set_sensitive(False)

    def on_btn_accept_clicked(self, widget):
        self.library_dic = {'name': self.name.get_text(), 'items': len(self.library),
                            'songs': self.library}
        self.my_library_screen_controller.save_library(self.library_dic)

    def on_btn_cancel_clicked(self, widget):
        self.close()

    def delete_event(self, widget, event=None):
        self.my_library_screen_controller.reload_libraries()

    def on_selection_button_clicked(self, widget):
        button_label = widget.get_label()
        if button_label == "Eliminar":
            selection = self.treeview.get_selection()
            model, rows = selection.get_selected_rows()
            if len(rows) > 0:
                for row in rows:
                    self.library.remove(model[row][0])
                    iter = model.get_iter(row)
                    model.remove(iter)

        if button_label == "Reproducir":
            selection = self.treeview.get_selection()
            model, rows = selection.get_selected_rows()
            if len(rows) > 0:
                for row in rows:
                    self.my_library_screen_controller.play_this_song(model[row][0])

        if button_label == "Detener":
            self.my_library_screen_controller.stop_song()

    def on_btn_add_library_clicked(self, widget):
        library = FileChooserWindow()
        library_aux = self.library+library.select_folder()

        # It Check if the same songs exists on library, if not add it.
        for i in library_aux:
            if i not in self.library:
                self.library.append(i)
        self.recalculate()

    def recalculate(self):
        self.num_items = len(self.library)
        self.lbl_num_items.set_text("Canciones en la biblioteca: " + str(self.num_items))
        self.fill_song_list()


class FileChooserWindow(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self, title="Seleccion biblioteca")
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