# -*- coding: utf-8 -*-
import os

library_list = []   ## List of all library objects
library_dir = "./bibliotecas/"

def add_library(library):
    library_list.append(library)


def rm_library(library):
    if os.path.exists(library_dir+library.get_name()+".lib"):
        os.remove(library_dir+library.get_name()+".lib")
    library_list.remove(library)


def load_library_list():
    if not os.path.exists(library_dir):
        os.makedirs(library_dir)
    files = os.listdir(library_dir)
    for i in sorted(files):
        add_library(Library(i))


def get_library_by_name(name):
    for i in library_list:
        if i.get_name() == name:
            return i
    return False


def rm_library_by_name(name):
    my_library = False
    my_library = get_library_by_name(name)
    if my_library:
        rm_library(my_library)
        return True
    return False


def get_library_item_number():
    return len(library_list)


def get_library_list():
    return library_list


class Library:
    def __init__(self, myfile=None ):
        self.file_name = myfile

        self.num_items = 0
        self.songs = []
        if self.file_name:
            self.load_params()

    def __str__(self):
        return self.file_name

    def __repr__(self):
        return self.file_name

    def load_params(self):
        if os.path.isfile(library_dir+self.file_name):
            my_file = open(library_dir + self.file_name, "r")
            for line in my_file:
                if line.split(":")[0] == "cancion":
                    self.songs.append(line.split(":")[1].rstrip())
            self.num_items = len(self.songs)

    def save_params(self):
        if not os.path.exists(library_dir):
            os.makedirs(library_dir)

        self.num_items = len(self.songs)
        if self.num_items > 0:
            my_file = open(library_dir + self.file_name, "w")
            my_file.write("nombre:"+str(self.file_name)[:-4]+"\n")
            my_file.write("items:"+str(self.num_items)+"\n")
            for i in self.songs:
                my_file.write("cancion:"+i+"\n")
            my_file.close()
            print("file saved")
        else:
            a = 1
            ## ERROR

    def get_name(self):
        return self.file_name[:-4]

    def set_name(self, name):
        self.file_name = "{0}.lib".format(name)


    def get_num_items(self):
        return len(self.songs)

    def get_file_name(self):
        return self.file_name

    def remove_all_songs(self):
        self.songs = []
        self.num_items = len(self.songs)

    def add_song(self, song):
        if song not in self.songs:
            self.songs.append(song)
        self.num_items = len(self.songs)

    def add_song_list(self, list):
        for i in list:
            if i not in self.songs:
                self.songs.append(i)
        self.num_items = len(self.songs)

    def is_song(self, name):
        if name in self.songs:
            return True
        return False

    def del_song(self, name):
        if self.is_song(name):
            self.songs.remove(name)
            self.num_items = len(self.songs)
            return True
        return False

    def get_songs(self):
        return self.songs
