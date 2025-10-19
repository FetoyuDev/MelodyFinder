# Migrated to PyQt6 scaffold for MelodyFinder UI
import os
import sys
import time
import json
import threading
import shutil
import subprocess
import requests

# PyQt6 imports
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QLabel, QPushButton, QProgressBar,
    QVBoxLayout, QHBoxLayout, QGridLayout, QFileDialog, QMessageBox, QLineEdit,
    QFrame
)
from PyQt6.QtGui import QPixmap, QDesktopServices
from PyQt6.QtCore import Qt, QTimer, QUrl

# Optional: placeholders for future integrations
try:
    # discord rich presence placeholder (do not initialize yet)
    pass
except Exception:
    pass

class MelodyFinderWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("MelodyFinder - PyQt6 Refactor Prep")
        self.base_dir = os.path.dirname(os.path.abspath(__file__))

        # Load config (keep key from original structure when possible)
        self.config = self._load_config()

        # State
        self.is_playing = False
        self.is_paused = False
        self.song_length = 0.0
        self.current_pos = 0.0
        self.current_song_path = None

        # Root central widget
        central = QWidget(self)
        self.setCentralWidget(central)

        # Layouts
        root = QVBoxLayout(central)

        # Dynamic labels area
        self.label_title = QLabel("Título: —")
        self.label_artist = QLabel("Artista: —")
        self.label_album = QLabel("Álbum: —")
        self.label_time = QLabel("00:00 / 00:00")
        self.label_remaining = QLabel("Restante: 00:00")

        labels_box = QVBoxLayout()
        labels_box.addWidget(self.label_title)
        labels_box.addWidget(self.label_artist)
        labels_box.addWidget(self.label_album)
        labels_box.addWidget(self.label_time)
        labels_box.addWidget(self.label_remaining)

        # Thumbnail area
        thumb_row = QHBoxLayout()
        self.thumb_label = QLabel()
        self.thumb_label.setFixedSize(160, 160)
        self.thumb_label.setFrameShape(QFrame.Shape.StyledPanel)
        self.thumb_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.thumb_label.setText("Sem capa")

        thumb_controls = QVBoxLayout()
        self.thumb_path_edit = QLineEdit()
        self.thumb_path_edit.setPlaceholderText("Caminho da capa (jpg/png)")
        btn_pick_thumb = QPushButton("Escolher capa…")
        btn_pick_thumb.clicked.connect(self.pick_thumb)

        thumb_controls.addWidget(self.thumb_path_edit)
        thumb_controls.addWidget(btn_pick_thumb)

        thumb_row.addWidget(self.thumb_label)
        thumb_row.addLayout(thumb_controls)

        # Progress bar
        self.progress = QProgressBar()
        self.progress.setRange(0, 1000)  # we will map position proportionally
        self.progress.setValue(0)

        # Link buttons row (placeholders)
        links_row = QHBoxLayout()
        btn_github = QPushButton("GitHub")
        btn_github.clicked.connect(lambda: self.open_link("https://github.com/FetoyuDev/MelodyFinder"))
        btn_discord = QPushButton("Discord")
        btn_discord.clicked.connect(lambda: self.open_link("https://discord.com"))
        btn_docs = QPushButton("Docs")
        btn_docs.clicked.connect(lambda: self.open_link("https://example.com/docs"))
        links_row.addWidget(btn_github)
        links_row.addWidget(btn_discord)
        links_row.addWidget(btn_docs)
        links_row.addStretch()

        # Control buttons (basic placeholders)
        controls = QHBoxLayout()
        btn_open = QPushButton("Abrir arquivo…")
        btn_open.clicked.connect(self.open_file)
        btn_play = QPushButton("Play")
        btn_play.clicked.connect(self.play)
        btn_pause = QPushButton("Pausar")
        btn_pause.clicked.connect(self.pause)
        btn_stop = QPushButton("Parar")
        btn_stop.clicked.connect(self.stop)
        controls.addWidget(btn_open)
        controls.addWidget(btn_play)
        controls.addWidget(btn_pause)
        controls.addWidget(btn_stop)
        controls.addStretch()

        # Assemble root layout
        root.addLayout(thumb_row)
        root.addLayout(labels_box)
        root.addWidget(self.progress)
        root.addLayout(controls)
        root.addLayout(links_row)

        # Timer to simulate UI updates (replace later with real player callbacks)
        self.timer = QTimer(self)
        self.timer.timeout.connect(self._update_ui)
        self.timer.start(500)

        self.resize(640, 420)

    # ===== Basic behaviors for new UI =====
    def open_link(self, url: str):
        QDesktopServices.openUrl(QUrl(url))

    def pick_thumb(self):
        path, _ = QFileDialog.getOpenFileName(self, "Escolher capa", self.base_dir, "Imagens (*.png *.jpg *.jpeg)")
        if path:
            self.thumb_path_edit.setText(path)
            self._set_thumb(path)

    def _set_thumb(self, path: str):
        try:
            pix = QPixmap(path)
            if not pix.isNull():
                self.thumb_label.setPixmap(pix.scaled(self.thumb_label.size(), Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation))
                self.thumb_label.setText("")
            else:
                self.thumb_label.setText("Capa inválida")
        except Exception:
            self.thumb_label.setText("Erro ao carregar capa")

    def open_file(self):
        path, _ = QFileDialog.getOpenFileName(self, "Abrir música", self.base_dir, "Áudio (*.mp3 *.wav *.flac)")
        if path:
            self.current_song_path = path
            # placeholders to set labels dynamically
            self.label_title.setText(f"Título: {os.path.basename(path)}")
            self.label_artist.setText("Artista: —")
            self.label_album.setText("Álbum: —")
            self.song_length = 180.0  # placeholder 3min
            self.current_pos = 0.0
            self.is_playing = False
            self.is_paused = False
            self.progress.setValue(0)

    def play(self):
        if self.current_song_path:
            self.is_playing = True
            self.is_paused = False

    def pause(self):
        if self.is_playing:
            self.is_paused = not self.is_paused

    def stop(self):
        self.is_playing = False
        self.is_paused = False
        self.current_pos = 0.0
        self._reflect_progress()

    def _reflect_progress(self):
        # Map current_pos -> progress bar range
        if self.song_length > 0:
            frac = max(0.0, min(1.0, self.current_pos / self.song_length))
            self.progress.setValue(int(frac * 1000))
            self.label_time.setText(f"{self._fmt(self.current_pos)} / {self._fmt(self.song_length)}")
            remaining = max(0, int(self.song_length - self.current_pos))
            self.label_remaining.setText(f"Restante: {self._fmt(remaining)}")
        else:
            self.progress.setValue(0)
            self.label_time.setText("00:00 / 00:00")
            self.label_remaining.setText("Restante: 00:00")

    def _update_ui(self):
        # Simulate playback advance for preview
        if self.is_playing and not self.is_paused and self.song_length > 0:
            self.current_pos += 0.5
            if self.current_pos >= self.song_length:
                self.current_pos = self.song_length
                self.is_playing = False
        self._reflect_progress()

    def _fmt(self, v):
        v = int(v)
        m, s = divmod(v, 60)
        return f"{m:02d}:{s:02d}"

    def _load_config(self):
        cfg_path = os.path.join(self.base_dir, "config.json")
        if os.path.exists(cfg_path):
            try:
                with open(cfg_path, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception:
                return {}
        return {}

# Entry point for PyQt6 app
def main():
    app = QApplication(sys.argv)
    win = MelodyFinderWindow()
    win.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
