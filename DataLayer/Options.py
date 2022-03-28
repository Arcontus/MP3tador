import os

option_dir = "./opciones/"
option_file = option_dir + "options.opt"
options = None


def load_options():
    if not os.path.exists(option_dir):
        os.makedirs(option_dir)

    if os.path.exists(option_file):
        global options
        options = Options()
        options.load()
    else:
        options = Options()
        options.save_params()


def save_options():
    if not os.path.exists(option_dir):
        os.makedirs(option_dir)
    global options
    options = Options()
    options.save_params()


class Options:
    def __init__(self):
        self.is_enable_GPIO = False
        self.GPIO = 0

    def load(self):
        self.load_params()

    def load_params(self):
        if os.path.isfile(option_file):
            file = open(option_file, "r")
            for line in file:
                if line.split(":")[0] == 'run_GPIO':
                    if (line.split(":")[1]) == "True\n":
                        self.is_enable_GPIO = True
                    else:
                        self.is_enable_GPIO = False

                elif line.split(":")[0] == "GPIO":
                    self.GPIO= int(line.split(":")[1])
            file.close()

    def save_params(self):
        file = open(option_file)
        file.write("active:" + str(self.is_enable_GPIO) + "\n")
        file.write("hours:" + str(self.GPIO) + "\n")
        file.close()

    def get_is_enable_GPIO(self):
        return self.is_enable_GPIO

    def set_is_enable_GPIO(self, value):
        self.is_enable_GPIO = value

    def get_GPIO(self):
        return self.GPIO

    def set_GPIO(self, value):
        self.GPIO = value
