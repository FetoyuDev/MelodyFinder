# MelodyFinder Mobile (Kivy) - reusing MelodyCore
# Requires: kivy, requests

import os
from typing import Dict, Any

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.progressbar import ProgressBar
from kivy.clock import Clock

# Import portable core from desktop module path
from importlib import import_module

try:
    desktop = import_module('init')  # MelodyCore and TrackMeta live here
    MelodyCore = desktop.MelodyCore
except Exception:
    # Fallback minimal core if import fails on Android packaging context
    class MelodyCore:
        def __init__(self):
            self.meta = type('M', (), dict(title='—', artist='—', album='—', duration=0.0, cover_path=None))()
            self.position = 0.0
            self.is_playing = False
            self.is_paused = False
        def load_file(self, path):
            self.meta.title = os.path.basename(path)
            self.meta.duration = 180.0
            self.position = 0.0
            self.is_playing = False
            self.is_paused = False
        def play(self):
            if self.meta.duration > 0:
                self.is_playing = True
                self.is_paused = False
        def toggle_pause(self):
            if self.is_playing:
                self.is_paused = not self.is_paused
        def stop(self):
            self.is_playing = False
            self.is_paused = False
            self.position = 0.0
        def tick(self, dt):
            if self.is_playing and not self.is_paused and self.meta.duration > 0:
                self.position = min(self.meta.duration, self.position + dt)
                if self.position >= self.meta.duration:
                    self.is_playing = False

class MelodyMobile(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(orientation='vertical', **kwargs)
        self.core = MelodyCore()
        self.title_lbl = Label(text='Título: —')
        self.artist_lbl = Label(text='Artista: —')
        self.album_lbl = Label(text='Álbum: —')
        self.time_lbl = Label(text='00:00 / 00:00')
        self.remaining_lbl = Label(text='Restante: 00:00')
        self.cover = Image(size_hint=(1, 0.5), allow_stretch=True, keep_ratio=True)
        self.progress = ProgressBar(max=1000, value=0)
        ctr = BoxLayout(size_hint=(1, None), height=50)
        ctr.add_widget(Button(text='Play', on_release=lambda *_: self.play()))
        ctr.add_widget(Button(text='Pausar', on_release=lambda *_: self.pause()))
        ctr.add_widget(Button(text='Parar', on_release=lambda *_: self.stop()))
        self.add_widget(self.cover)
        self.add_widget(self.title_lbl)
        self.add_widget(self.artist_lbl)
        self.add_widget(self.album_lbl)
        self.add_widget(self.time_lbl)
        self.add_widget(self.remaining_lbl)
        self.add_widget(self.progress)
        self.add_widget(ctr)
        Clock.schedule_interval(self._tick, 0.5)

    def play(self):
        self.core.play()

    def pause(self):
        self.core.toggle_pause()

    def stop(self):
        self.core.stop()
        self._reflect()

    def _tick(self, dt):
        self.core.tick(0.5)
        self._reflect()

    def _reflect(self):
        dur = self.core.meta.duration
        pos = self.core.position
        if dur > 0:
            frac = max(0.0, min(1.0, pos / dur))
            self.progress.value = int(frac * 1000)
            self.time_lbl.text = f"{self._fmt(pos)} / {self._fmt(dur)}"
            rem = max(0, int(dur - pos))
            self.remaining_lbl.text = f"Restante: {self._fmt(rem)}"
        else:
            self.progress.value = 0
            self.time_lbl.text = "00:00 / 00:00"
            self.remaining_lbl.text = "Restante: 00:00"
        self.title_lbl.text = f"Título: {getattr(self.core.meta, 'title', '—')}"

    def _fmt(self, v):
        v = int(v)
        m, s = divmod(v, 60)
        return f"{m:02d}:{s:02d}"

class MelodyFinderApp(App):
    def build(self):
        return MelodyMobile()

if __name__ == '__main__':
    MelodyFinderApp().run()
