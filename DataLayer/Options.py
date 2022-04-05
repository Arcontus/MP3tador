import os

option_dir = "./options/"
option_file = option_dir + "options.opt"
options = {
    "GPIO": 12,
    "is_enable_GPIO": False,
    "is_enable_auto_stop": True,
    "auto_stop_after_minutes": 45
}

def get_options():
    load_options()
    return options

def load_options():
    if not os.path.exists(option_dir):
        os.makedirs(option_dir)

    if os.path.exists(option_file):
        opt = Options()
        opt.load()
    else:
        opt = Options()
        opt.save_params()
        opt.load()


def save_options():
    if not os.path.exists(option_dir):
        os.makedirs(option_dir)
    opt = Options()
    opt.save_params()


class Options:
    def load(self):
        self.load_params()

    def load_params(self):
        if os.path.isfile(option_file):
            file = open(option_file, "r")
            for line in file:
                if line.split(":")[0] == 'is_enable_GPIO':
                    if (line.split(":")[1]) == "True\n":
                        options["is_enable_GPIO"] = True
                    else:
                        options["is_enable_GPIO"] = False

                elif line.split(":")[0] == "GPIO":
                    options["GPIO"] = int(line.split(":")[1])
                elif line.split(":")[0] == "is_enable_auto_stop":
                    if (line.split(":")[1]) == "True\n":
                        options["is_enable_auto_stop"] = True
                    else:
                        options["is_enable_auto_stop"] = False
                elif line.split(":")[0] == "auto_stop_after_minutes":
                    options["GPIO"] = int(line.split(":")[1])
            file.close()
        else:
            self.save_params()

    def save_params(self):
        if not os.path.exists(option_dir):
            os.makedirs(option_dir)

        file = open(option_file, "w")
        file.write("is_enable_GPIO:" + str(options["is_enable_GPIO"]) + "\n")
        file.write("GPIO:" + str(options["GPIO"]) + "\n")
        file.write("is_enable_auto_stop:" + str(options["is_enable_auto_stop"]) + "\n")
        file.write("auto_stop_after_minutes:" + str(options["auto_stop_after_minutes"]) + "\n")
        file.close()

    def get_is_enable_GPIO(self):
        return options["is_enable_GPIO"]

    def set_is_enable_GPIO(self, value):
        options["is_enable_GPIO"] = value

    def get_GPIO(self):
        return options["GPIO"]

    def set_GPIO(self, value):
        options["GPIO"] = value

    def get_is_enable_auto_stop(self):
        return options["is_enable_auto_stop"]

    def set_is_enable_auto_stop(self, value):
        options["is_enable_auto_stop"] = value

    def get_auto_stop_after_minutes(self):
        return options["auto_stop_after_minutes"]

    def set_auto_stop_after_minutes(self, value):
        options["auto_stop_after_minutes"] = value
