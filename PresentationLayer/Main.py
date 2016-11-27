# -*- coding: utf-8 -*-
# coding: utf-8
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GdkPixbuf, Gdk, GObject


class MainWindow(Gtk.Window):
    def __init__(self, presentation_controller=None):
        if presentation_controller is not None:
            self.myMainScreenController = presentation_controller
        self.window = Gtk.Window.__init__(self, title="MP3tador,  v0.3") ## TODO: Implement a variable or function to do this"
        self.set_border_width(20)
        self.font_color = "black"
        self.lblhour = Gtk.Label(label="")
        self.lbldate = Gtk.Label(label="")

        self.txt_info = Gtk.Entry()
        self.txt_info.set_text("")
        self.txt_info.set_sensitive(False)
        self.info_max_leng = 34
        #self.txt_info.set_max_length(self.info_max_leng)

        self.style_provider = Gtk.CssProvider()

        css = """
        GtkEntry{
            color: darkgrey;
            background-color: yellow;
            }

        .colorize {
           background: rgba(0,0,0,1);
           color: green;
           font-size: xx-large;
           padding-left: 25px;
           font-family: monospace;
        }
        """
        self.style_provider.load_from_data(css)
        Gtk.StyleContext.add_provider_for_screen(
            Gdk.Screen.get_default(), self.style_provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)
        self.txt_info.get_style_context().add_class("colorize")

        table = Gtk.Table(8, 5, True)
        self.add(table)
        btn_alarm = Gtk.Button(label="Alarmas")     ## TODO: Implement a variable or function to do this"
        btn_alarm.connect("clicked", self.on_btn_alarm_clicked)

        btn_option = Gtk.Button(label="Opciones")
        btn_option.connect("clicked", self.on_btn_option_clicked)

        self.lst_library = Gtk.ComboBoxText()
        self.lst_library.connect("changed", self.on_lst_library_changed)

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

        btn_library = Gtk.Button(label="Biblioteca")
        btn_library.connect("clicked", self.on_btn_biblioteca_clicked)

        table.attach(self.lbldate, 0, 8, 0, 1)
        table.attach(self.lblhour, 0, 8, 1, 5)
        table.attach(btn_alarm, 10, 15, 2, 3)
        table.attach(btn_library, 10, 15, 4, 5)
        table.attach(btn_option, 10, 15, 6, 7)

        table.attach(self.lst_library, 0, 8, 5, 6)
        table.attach(btn_play, 0, 2, 6, 9)
        table.attach(btn_pause, 2, 4, 6, 9)
        table.attach(btn_next, 4, 6, 6, 9)
        table.attach(btn_stop, 6, 8, 6, 9)
        table.attach(self.txt_info, 0, 15, 10, 11)

    def get_info_max_leng(self):
        return self.info_max_leng

    def set_info_text(self, text):
        self.txt_info.set_text(text)

    def reset_library_items(self):
        self.lst_library.remove_all()

    def reload_library_items(self, items):
        self.reset_library_items()
        for i in sorted(items):
            self.add_library_item(i)
        self.lst_library.set_active(0)
        print(items)

    def add_library_item(self, item):
         self.lst_library.append_text(item)

    def on_btn_biblioteca_clicked(self, widget):
        self.myMainScreenController.open_library_manager()

    def on_btn_option_clicked(self, widget):
        self.myMainScreenController.open_option_manager()

    def on_lst_library_changed(self, widget):
        self.myMainScreenController.set_library_player(self.lst_library.get_active_text())

    def on_btn_play_clicked(self, widget):
        self.myMainScreenController.play_song()

    def on_btn_stop_clicked(self, widget):
        self.myMainScreenController.stop_song()

    def on_btn_pause_clicked(self, widget):
        self.myMainScreenController.pause_song()

    def on_btn_next_clicked(self, widget):
        self.myMainScreenController.next_song()

    def on_btn_alarm_clicked(self, widget):
        self.myMainScreenController.open_alarm_manager()

    def set_hour(self, event):
        self.lblhour.set_markup(str("<span font='50' foreground='"+self.font_color+"'>"+event.data)+"</span>")

    def set_date(self, event):
        self.lbldate.set_markup(str("<span variant='smallcaps'>" + event.data) + "</span>")


class console_info():
    def __init__(self, window, presentation_controller):
        self.my_window = window
        self.my_presentation_controller = presentation_controller
        self.msg_list = []
        self.iterator = 0
        self._update_id = GObject.timeout_add(80, self.update_msg, None)
        self.txt_completed = 0
        self.wait_msg = 15

    def update_msg(self, extra):
        if len(self.msg_list):
            if self.txt_completed < len(self.msg_list[self.iterator]['message']):
                self.txt_completed += 1

                if self.txt_completed > self.my_window.get_info_max_leng():
                    my_str = str(self.msg_list[self.iterator]['message'][self.txt_completed - self.my_window.get_info_max_leng():self.txt_completed])
                    self.my_utf8 = my_str.decode("utf-8", errors='ignore')
                else:
                    my_str = self.msg_list[self.iterator]['message'][:self.txt_completed]
                    self.my_utf8 =my_str.decode("utf-8", errors='ignore')
                self.my_window.set_info_text(self.my_utf8)

            else:
                if self.wait_msg == 0:
                    if not self.msg_list[self.iterator]['always']:
                        self.msg_list.remove(self.msg_list[self.iterator])
                        if self.iterator > 0:
                            self.iterator -= 1
                    if self.iterator +1 < len(self.msg_list):
                        self.iterator += 1
                    else:
                        self.iterator = 0
                    self.wait_msg = 20
                    self.txt_completed = 0
                else:
                    self.wait_msg -= 1
        else:
            self.my_window.set_info_text("")
        return True

    def add_msg(self, message, always=True):
        msg_dict = {'message':  message, 'always': always}
        if always:
            self.msg_list.append(msg_dict)
        else:
            self.msg_list.insert(self.iterator +1, msg_dict)
            self.txt_completed = len(self.msg_list[self.iterator]['message'])
            self.wait_msg = 0

    def delete_message(self, message):
        if len(self.msg_list):
            for i in range(len(self.msg_list)):
                if self.msg_list[i]['message'] == message:
                    self.wait_msg = 0
                    self.txt_completed = 0
                    self.msg_list.remove(self.msg_list[i])
                    return True
        return False



