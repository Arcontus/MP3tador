import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GdkPixbuf


class Main(Gtk.Window):
    def __init__(self):
        self.lbl_player_info = Gtk.Label("")
        self.window = Gtk.Window.__init__(self, title="MP3tador,  v0.3") ## TODO: Implement a variable or function to do this"
        self.set_border_width(20)
        self.font_color = "black"
        self.lblhour = Gtk.Label(label="")
        self.lbldata = Gtk.Label(label= "")

        table = Gtk.Table(8, 5, True)
        self.add(table)
        btn_alarm = Gtk.Button(label="Alarmas")     ## TODO: Implement a variable or function to do this"
        btn_alarm.connect("clicked", self.on_btn_alarmas_clicked)

        btn_options = Gtk.Button(label="Opciones")
        btn_options.connect("clicked", self.on_btn_opciones_clicked)

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

        table.attach(self.lbldata, 0, 8, 0, 1)
        table.attach(self.lblhour, 0, 8, 1, 5)
        table.attach(btn_alarm, 10, 15, 2, 3)
        table.attach(btn_library, 10, 15, 4, 5)
        table.attach(btn_options, 10, 15, 6, 7)

        table.attach(btn_play, 0, 2, 6, 9)
        table.attach(btn_pause, 2, 4, 6, 9)
        table.attach(btn_next, 4, 6, 6, 9)
        table.attach(btn_stop, 6, 8, 6, 9)
        table.attach(self.lbl_player_info, 0, 15, 10, 12)

    def on_btn_biblioteca_clicked(self, widget):
        a = 1

    def on_btn_opciones_clicked(self, widget):
        a = 1

    def on_lst_biblioteca_changed(self, widget):
        a = 1

    def reload_biblioteca(self, widget, event=None):
        self.on_lst_biblioteca_changed(self)

    def on_btn_play_clicked(self, widget):
        a = 1

    def on_btn_stop_clicked(self, widget):
        a = 1

    def on_btn_pause_clicked(self, widget):
        a = 1

    def on_btn_next_clicked(self, widget):
        a = 1

    def on_btn_alarmas_clicked(self, widget):
        a = 1

