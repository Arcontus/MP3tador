from gi.repository import Gtk, GObject, Gdk


class ConsoleInfo(object):
    def __init__(self):
        self.msg_list = []
        self.iterator = 0
        self._update_id = GObject.timeout_add(80, self.update_msg, None)
        self.txt_completed = 0
        self.wait_msg = 20

        self.style_provider = Gtk.CssProvider()

        self.txt_info = Gtk.Entry()
        self.txt_info.set_text("")
        self.txt_info.set_sensitive(False)

        css = """
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

        self.info_max_leng = 34
        #self.txt_info.set_max_length(self.info_max_leng)

    def get_info_max_leng(self):
        return self.info_max_leng

    def update_msg(self, extra):
        if len(self.msg_list):
            if self.txt_completed < len(self.msg_list[self.iterator]['message']):
                self.txt_completed += 1

                if self.txt_completed > self.get_info_max_leng():
                    my_str = str(self.msg_list[self.iterator]['message'][self.txt_completed - self.get_info_max_leng():self.txt_completed])
                    self.my_utf8 = my_str.decode("utf-8", errors='ignore')
                else:
                    my_str = self.msg_list[self.iterator]['message'][:self.txt_completed]
                    self.my_utf8 =my_str.decode("utf-8", errors='ignore')
                self.set_info_text(self.my_utf8)

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
            self.set_info_text("")
        return True

    def add_msg(self, message, always=True):
        msg_dict = {'message':  message, 'always': always}
        if always:
            self.msg_list.append(msg_dict)
        else:
            self.msg_list.insert(self.iterator +1, msg_dict)
            if len(self.msg_list) == 0:
                self.txt_completed = len(self.msg_list[self.iterator]['message'])

    def delete_message(self, message):
        if len(self.msg_list):
            for i in range(len(self.msg_list)):
                if self.msg_list[i]['message'] == message:
                    self.wait_msg = 0
                    self.txt_completed = 0
                    self.msg_list.remove(self.msg_list[i])
                    return True
        return False

    def set_info_text(self, text):
        self.txt_info.set_text(text)

