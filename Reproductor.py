import os
import pygame
from gi.repository import Gtk, Gio, GObject, GdkPixbuf
import random
from Biblioteca import *
import Opciones
import eyeD3

class Reproductor(Gtk.Window):
    def __init__(self, lbl_info):
        pygame.mixer.init()
        pygame.init()

        self.lbl_info = lbl_info

        self.pausa = False
        self.reproduciendo = False
        self.musica = []
        self.cancion_actual = None
        self.siguiente_cancion = None
        self.fin_cancion = pygame.constants.USEREVENT +1
        GObject.timeout_add(1000, self.check_status_play)


    def load_biblioteca(self, archivo):
        self.musica = []
        lib_directory = "./bibliotecas/"
        fichero = open(lib_directory+archivo)
        for line in fichero:
            if (line.split(":")[0] == 'nombre'):
                self.nombre = (line.split(":")[1])

            elif (line.split(":")[0] == "items"):
                items =(line.split(":")[1])

            elif (line.split(":")[0] == 'cancion'):
                self.musica.append (line.split(":")[1][:-1])

        self.manager_biblioteca()

    def check_status_play(self):
        if self.reproduciendo == True:
            for event in pygame.event.get():
                if event.type == self.fin_cancion:
                    self.next_song()
        return True # keep running this event


    def set_biblioteca(self, musica):
        self.musica = musica
        for i, val in enumerate(musica):
            if (i != 0):
                if (i == 1):
                    pygame.mixer.music.load(val)
                else:
                    pygame.mixer.music.queue(val)

    def manager_biblioteca(self):
        self.siguiente_cancion = random.choice(self.musica)
        self.cancion_actual = self.siguiente_cancion
        if (len(self.musica ) > 1):
            while self.siguiente_cancion == self.cancion_actual:
                self.siguiente_cancion = random.choice(self.musica)
        pygame.mixer.music.set_endevent(self.fin_cancion)
        pygame.mixer.music.load(self.cancion_actual)
        self.set_info()

    def next_song(self):
        self.manager_biblioteca()
        self.reproduciendo = False
        self.pausa = False
        self.play()

    def play(self):
        if (self.reproduciendo == True):
            self.pause()
        else:
            if (self.pausa == False):
                pygame.mixer.music.play()
                Opciones.encender_altavoces()
                self.reproduciendo = True

    def pause(self):
        if (self.pausa == False):
            pygame.mixer.music.pause()
            self.pausa = True
        else:
            pygame.mixer.music.unpause()
            self.pausa = False

    def stop(self):
        pygame.mixer.music.stop()
        self.reproduciendo = False
        self.pausa = False
        Opciones.apagar_altavoces()

    def set_info(self):
        tag = eyeD3.Tag()
        tag.link(self.cancion_actual)
        if ((tag.getTitle() != None) and (tag.getArtist() != None) and (tag.getAlbum() != None) and (tag.getYear() != None)):
            self.lbl_info.set_text("Cancion: "+tag.getTitle()+"                    Artista: "+tag.getArtist()+"\nAlbum: "+tag.getAlbum()+"                    Ano: "+tag.getYear())
        else:
            self.lbl_info.set_text("")

