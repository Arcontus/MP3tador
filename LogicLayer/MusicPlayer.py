# -*- coding: utf-8 -*-
# coding=utf-8

import pygame
import eyeD3
import random
from gi.repository import GObject
import EventDispatcher.EventDispatcher


class MusicPlayer:
    def __init__(self, logic_controller, event_dispatcher):
        self.event_dispatcher = event_dispatcher
        pygame.mixer.init()
        pygame.init()

        self.library_dic = {'name': "", 'items': 0,
                           'songs': []}
        self.current_song_dic = {'artist': "", 'name': "", 'year': 0, 'album': ""}
        self.info_string_current_song = ["", True]
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
        if self.is_playing:
            self.stop()
        self.unload_info()
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
        if len(self.library_dic['songs']) > 0:
            self.next_song = random.choice(self.library_dic['songs'])
            self.current_song = self.next_song

        if len(self.library_dic['songs']) > 1:
            while self.next_song == self.current_song:
                self.next_song = random.choice(self.library_dic['songs'])

        pygame.mixer.music.set_endevent(self.finish_song)
        pygame.mixer.music.load(self.current_song)

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
                    self.set_info()

    def play_this_song(self, filename):
        self.stop()
        pygame.mixer.music.load(filename)
        pygame.mixer.music.play()
        self.is_playing = False
        self.set_info()

    def pause(self):
        if self.is_pause is False:
            pygame.mixer.music.pause()
            self.is_pause = True
            self.event_dispatcher.dispatch_event(
                EventDispatcher.EventDispatcher.MyInfoEvent(
                    EventDispatcher.EventDispatcher.MyInfoEvent.SET_NEW_MESSAGE,
                    ["PAUSE  ", False]
                    )
                )
        else:
            pygame.mixer.music.unpause()
            self.is_pause = False

    def stop(self):
        pygame.mixer.music.stop()
        self.is_playing = False
        self.is_pause = False
        #Opciones.apagar_altavoces()
        self.event_dispatcher.dispatch_event(
                EventDispatcher.EventDispatcher.MyInfoEvent(
                    EventDispatcher.EventDispatcher.MyInfoEvent.SET_NEW_MESSAGE,
                    ["STOP   ", False]
                )
        )
        self.event_dispatcher.dispatch_event(
                EventDispatcher.EventDispatcher.MyInfoEvent(
                    EventDispatcher.EventDispatcher.MyInfoEvent.DELETE_MESSAGE,
                    self.info_string_current_song
                )
        )

    def unload_info(self):
        self.event_dispatcher.dispatch_event(
                EventDispatcher.EventDispatcher.MyInfoEvent(
                    EventDispatcher.EventDispatcher.MyInfoEvent.DELETE_MESSAGE,
                    self.info_string_current_song
                )
        )

    def set_info(self):
        self.unload_info()
        tag = eyeD3.Tag()
        tag.link(self.current_song)
        self.current_song_dic['artist'] = tag.getArtist().encode("utf-8")
        self.current_song_dic['name'] = tag.getTitle().encode("utf-8")
        if tag.getYear():
            self.current_song_dic['year'] = tag.getYear().encode("utf-8")
        else:
            self.current_song_dic['year'] = "Year?"

        if tag.getAlbum():
            self.current_song_dic['album'] = tag.getAlbum().encode("utf-8")
        else:
            self.current_song_dic['album'] = "Album?"

        self.info_string_current_song = ["Canción: {1}, Artista: {0}, Año: {2}, Album: {3}".format(self.current_song_dic['artist'],
                                                                                                   self.current_song_dic['name'],
                                                                                                   self.current_song_dic['year'],
                                                                                                   self.current_song_dic['album']),
                                         True]
        tag.link(self.next_song)

        self.event_dispatcher.dispatch_event(
                EventDispatcher.EventDispatcher.MyInfoEvent(
                    EventDispatcher.EventDispatcher.MyInfoEvent.SET_NEW_MESSAGE,
                    self.info_string_current_song
                )
        )


