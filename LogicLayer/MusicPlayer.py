import pygame
import eyeD3
from gi.repository import GObject
import random


class MusicPlayer:
    def __init__(self, logic_controller):
        pygame.mixer.init()
        pygame.init()

        self.library_dic = {'name': "", 'items': 0,
                           'songs': []}
        self.my_logic_controller = logic_controller
        self.is_pause = False
        self.is_playing = False
        self.current_song = None
        self.next_song = None
        self.finish_song = pygame.constants.USEREVENT + 1
        GObject.timeout_add(1000, self.check_status_play)

    def load_library(self, name):
        if name is not None:
            self.library_dic['songs'] = []
            self.is_pause = False
            self.is_playing = False
            self.library_dic['name'] = name
            self.library_dic = self.my_logic_controller.get_library_parameters(self.library_dic['name'])
            self.manager_library()
        else:
            self.unload_library()

    def unload_library(self):
        self.stop()
        self.library_dic['songs'] = []
        self.library_dic['name'] = ""

    def check_status_play(self):
        if self.is_playing is True:
            for event in pygame.event.get():
                if event.type == self.finish_song:
                    self.play_next_song()
        return True # keep running this event

    def set_library(self, music):
        self.library_dic['songs'] = music
        for i, val in enumerate(music):
            if i is not 0:
                if i is 1:
                    pygame.mixer.music.load(val)
                else:
                    pygame.mixer.music.queue(val)

    def manager_library(self):
        self.next_song = random.choice(self.library_dic['songs'])
        self.current_song = self.next_song
        if len(self.library_dic['songs']) > 1:
            while self.next_song == self.current_song:
                self.next_song = random.choice(self.library_dic['songs'])
        pygame.mixer.music.set_endevent(self.finish_song)
        pygame.mixer.music.load(self.current_song)
        self.set_info()

    def play_next_song(self):
        self.manager_library()
        self.is_playing = False
        self.is_pause = False
        self.play()

    def play(self):
        if len(self.library_dic['songs']) > 0:
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
