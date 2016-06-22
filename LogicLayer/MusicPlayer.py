import pygame
import eyeD3
from gi.repository import GObject
import random


class MusicPlayer:
    def __init__(self):
        pygame.mixer.init()
        pygame.init()

        self.is_pause = False
        self.is_playing = False
        self.music = []
        self.current_song = None
        self.next_song = None
        self.finish_song = pygame.constants.USEREVENT + 1
        GObject.timeout_add(1000, self.check_status_play)

    def load_library(self, name_file):
        self.music = []
        self.is_pause = False
        self.is_playing = False
        lib_directory = "./bibliotecas/"
        my_file = open(lib_directory + name_file +".lib")
        for line in my_file:
            if line.split(":")[0] == 'nombre':
                self.name = (line.split(":")[1])

            elif line.split(":")[0] == "items":
                items = (line.split(":")[1])

            elif line.split(":")[0] == 'cancion':
                self.music.append (line.split(":")[1][:-1])

        self.manager_library()

    def check_status_play(self):
        if self.is_playing is True:
            for event in pygame.event.get():
                if event.type == self.finish_song:
                    self.play_next_song()
        return True # keep running this event

    def set_library(self, music):
        self.music = music
        for i, val in enumerate(music):
            if i is not 0:
                if i is 1:
                    pygame.mixer.music.load(val)
                else:
                    pygame.mixer.music.queue(val)

    def manager_library(self):
        self.next_song = random.choice(self.music)
        self.current_song = self.next_song
        if len(self.music) > 1:
            while self.next_song == self.current_song:
                self.next_song = random.choice(self.music)
        pygame.mixer.music.set_endevent(self.finish_song)
        pygame.mixer.music.load(self.current_song)
        self.set_info()

    def play_next_song(self):
        self.manager_library()
        self.is_playing = False
        self.is_pause = False
        self.play()

    def play(self):
        if self.is_playing is True:
            self.pause()
        else:
            if self.is_pause is False:
                pygame.mixer.music.play()
                #Opciones.encender_altavoces()
                self.is_playing = True

    def pause(self):
        if self.is_pause is False:
            pygame.mixer.music.pause()
            self.is_pause = True
        else:
            pygame.mixer.music.unpause()
            self.is_pause = False

    def stop(self):
        pygame.mixer.music.stop()
        self.is_playing = False
        self.is_pause = False
        #Opciones.apagar_altavoces()

    def set_info(self):
        tag = eyeD3.Tag()
        tag.link(self.current_song)
        if ((tag.getTitle() is not None) and (tag.getArtist() is not None) and
                (tag.getAlbum() is not None) and (tag.getYear() is not None)):
            a = 1
            #self.lbl_info.set_text(
            #                        "Cancion: " + tag.getTitle() +
            #                        "                    Artista: " + tag.getArtist() +
            #                        "\nAlbum: " + tag.getAlbum() +
            #                        "                    Ano: " + tag.getYear())
        else:
            a =2
           # self.lbl_info.set_text("")
