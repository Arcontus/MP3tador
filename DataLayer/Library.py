import os

library_list = []   ## List of all library objects

def add_library(library):
    library_list.append(library)

def rm_library(library):
    library_list.remove(library)

def load_library_list():
    library_list = []
    lib_dir = "./bibliotecas/"
    if not os.path.exists(lib_dir):
            os.makedirs(lib_dir)
    files = os.listdir(lib_dir)
    for i in sorted(files):
        add_library(Library(i))

def get_id_from_text(comboboxText, text):
    model = comboboxText.get_model()
    position = 0
    for i in model:
        var = str(i[:])
        var = var.split(",")[0]
        var = var[2:-1]
        if (var == text): return position
        else: position = position +1
    return -1

def get_library_item_number():
    return len(library_list)

def get_library_list():
    return library_list

class Library():
    def __init__(self, myfile=None ):
        self.file_name = myfile
        self.lib_dir = "./bibliotecas/"
        self.num_items = 0
        self.songs = []
        self.load_params()
        print (self.file_name)
        print(self.songs)

    def __str__(self):
        return self.file_name

    def __repr__(self):
        return self.file_name

    def load_params(self):
        if os.path.isfile(self.lib_dir+self.file_name):
            my_file = open(self.lib_dir+self.file_name, "r")
            for line in my_file:
                if (line.split(":")[0] == 'items'):
                    self.num_items = int(line.split(":")[1])
                elif (line.split(":")[0] == "cancion"):
                    self.songs.append(line.split(":")[1])

    def save_params(self):
        if not os.path.exists(self.lib_dir):
            os.makedirs(self.lib_dir)
        if (self.num_items > 0):
            file = open(self.lib_dir+self.file_name, "w")
            file.write("nombre:"+str(self.file_name)[:-4]+"\n")
            file.write("items:"+str(self.num_items)+"\n")
            for i in self.songs:
                file.write("cancion:"+i+"\n")
            file.close()
            self.close()
        else:
            a = 1
            ## ERROR

    def get_name(self):
        return self.file_name[:-4]

    def get_file_name(self):
        return self.file_name

    def remove_all_songs(self):
        self.songs = []

    def add_song(self, song):
        if song not in self.songs:
            self.songs.append(song)

    def add_song_list(self, list):
        for i in list:
            if i not in self.songs:
                self.songs.append(i)

    def del_song(self, song):
        self.songs.remove(song)

