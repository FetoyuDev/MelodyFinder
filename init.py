# MelodyFinder - Desktop (PyQt6) with Discord integration, dynamic actions, modular core
# Portable core to be reused by mobile (Kivy) build

import os
import sys
import json
import time
import threading
from dataclasses import dataclass, asdict
from typing import Optional, Dict, Any

# Networking
import requests

# Discord Rich Presence (pypresence) is optional
try:
    from pypresence import Presence  # type: ignore
except Exception:
    Presence = None  # gracefully degrade if unavailable

# PyQt6 UI
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QLabel, QPushButton, QProgressBar,
    QVBoxLayout, QHBoxLayout, QFileDialog, QMessageBox, QLineEdit, QFrame
)
from PyQt6.QtGui import QPixmap, QDesktopServices
from PyQt6.QtCore import Qt, QTimer, QUrl


# ===== Portable Core (reused by desktop and mobile) =====
@dataclass
class TrackMeta:
    title: str = "—"
    artist: str = "—"
    album: str = "—"
    duration: float = 0.0  # seconds
    cover_path: Optional[str] = None


class MelodyCore:
    def __init__(self):
        self.meta = TrackMeta()
        self.position = 0.0
        self.is_playing = False
        self.is_paused = False

    def load_file(self, path: str):
        # Placeholder metadata extraction
        self.meta = TrackMeta(
            title=os.path.basename(path),
            artist="—",
            album="—",
            duration=180.0,
            cover_path=None,
        )
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

    def tick(self, dt: float):
        if self.is_playing and not self.is_paused and self.meta.duration > 0:
            self.position = min(self.meta.duration, self.position + dt)
            if self.position >= self.meta.duration:
                self.is_playing = False


# ===== Discord Helpers =====
class DiscordRPC:
    def __init__(self, client_id: Optional[str]):
        self.client_id = client_id
        self.rpc = None
        self.connected = False

    def connect(self):
        if not self.client_id or not Presence:
            return
        try:
            self.rpc = Presence(self.client_id)
            self.rpc.connect()
            self.connected = True
        except Exception:
            self.rpc = None
            self.connected = False

    def update(self, details: str, state: str, large_image: str = "melodyfinder", small_image: Optional[str] = None):
        if not self.connected or not self.rpc:
            return
        payload = {
            "details": details,
            "state": state,
            "large_image": large_image,
        }
        if small_image:
            payload["small_image"] = small_image
        try:
            self.rpc.update(**payload)
        except Exception:
            pass

    def clear(self):
        if self.connected and self.rpc:
            try:
                self.rpc.clear()
            except Exception:
                pass

    def close(self):
        if self.connected and self.rpc:
            try:
                self.rpc.close()
            except Exception:
                pass
            self.connected = False


# ===== Desktop UI (PyQt6) =====
class MelodyFinderWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("MelodyFinder")
        self.base_dir = os.path.dirname(os.path.abspath(__file__))

        # Config
        self.config = self._load_config()
        discord_id = self.config.get("discord_client_id")

        # Core and Discord RPC
        self.core = MelodyCore()
        self.rpc = DiscordRPC(discord_id)
        self.rpc.connect()

        # UI widgets
        central = QWidget(self)
        self.setCentralWidget(central)
        root = QVBoxLayout(central)

        # Top actions row: dynamic buttons (Ouvir Agora, Download MelodyFinder)
        actions_row = QHBoxLayout()
        self.btn_listen_now = QPushButton("Ouvir Agora")
        self.btn_listen_now.clicked.connect(self._action_listen_now)
        self.btn_download = QPushButton("Download MelodyFinder")
        self.btn_download.clicked.connect(lambda: self.open_link(self.config.get("download_url", "https://github.com/FetoyuDev/MelodyFinder/releases")))
        actions_row.addWidget(self.btn_listen_now)
        actions_row.addWidget(self.btn_download)
        actions_row.addStretch()

        # Login via Discord section (simple button -> open OAuth URL)
        login_row = QHBoxLayout()
        self.btn_login_discord = QPushButton("Login com Discord")
        self.btn_login_discord.clicked.connect(self._login_discord)
        self.discord_status = QLabel("Não autenticado")
        login_row.addWidget(self.btn_login_discord)
        login_row.addWidget(self.discord_status)
        login_row.addStretch()

        # Labels
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

        # Thumbnail
        thumb_row = QHBoxLayout()
        self.thumb_label = QLabel("Sem capa")
        self.thumb_label.setFixedSize(160, 160)
        self.thumb_label.setFrameShape(QFrame.Shape.StyledPanel)
        self.thumb_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
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
        self.progress.setRange(0, 1000)
        self.progress.setValue(0)

        # Controls
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

        # Links row
        links_row = QHBoxLayout()
        btn_github = QPushButton("GitHub")
        btn_github.clicked.connect(lambda: self.open_link("https://github.com/FetoyuDev/MelodyFinder"))
        btn_discord = QPushButton("Discord")
        btn_discord.clicked.connect(lambda: self.open_link("https://discord.com"))
        links_row.addWidget(btn_github)
        links_row.addWidget(btn_discord)
        links_row.addStretch()

        # Assemble
        root.addLayout(actions_row)
        root.addLayout(login_row)
        root.addLayout(thumb_row)
        root.addLayout(labels_box)
        root.addWidget(self.progress)
        root.addLayout(controls)
        root.addLayout(links_row)

        # Timer to update UI/progress
        self.timer = QTimer(self)
        self.timer.timeout.connect(self._update_ui)
        self.timer.start(500)

        self.resize(720, 480)

    # ===== Actions =====
    def open_link(self, url: str):
        QDesktopServices.openUrl(QUrl(url))

    def _action_listen_now(self):
        # Dynamic: open a listening page/playlist if configured
        url = self.config.get("listen_url") or "https://open.spotify.com"
        self.open_link(url)

    # Thumbnail helpers
    def pick_thumb(self):
        path, _ = QFileDialog.getOpenFileName(self, "Escolher capa", self.base_dir, "Imagens (*.png *.jpg *.jpeg)")
        if path:
            self.thumb_path_edit.setText(path)
            self.core.meta.cover_path = path
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

    # File/Open
    def open_file(self):
        path, _ = QFileDialog.getOpenFileName(self, "Abrir música", self.base_dir, "Áudio (*.mp3 *.wav *.flac)")
        if path:
            self.core.load_file(path)
            self._update_labels()
            self._reflect_progress()
            # Update Discord Rich Presence
            self._update_rpc_now()

    # Playback
    def play(self):
        self.core.play()
        self._update_rpc_now()

    def pause(self):
        self.core.toggle_pause()
        self._update_rpc_now()

    def stop(self):
        self.core.stop()
        self._reflect_progress()
        self._update_rpc_now()

    # UI updates
    def _reflect_progress(self):
        dur = self.core.meta.duration
        pos = self.core.position
        if dur > 0:
            frac = max(0.0, min(1.0, pos / dur))
            self.progress.setValue(int(frac * 1000))
            self.label_time.setText(f"{self._fmt(pos)} / {self._fmt(dur)}")
            remaining = max(0, int(dur - pos))
            self.label_remaining.setText(f"Restante: {self._fmt(remaining)}")
        else:
            self.progress.setValue(0)
            self.label_time.setText("00:00 / 00:00")
            self.label_remaining.setText("Restante: 00:00")

    def _update_labels(self):
        m = self.core.meta
        self.label_title.setText(f"Título: {m.title}")
        self.label_artist.setText(f"Artista: {m.artist}")
        self.label_album.setText(f"Álbum: {m.album}")
        if m.cover_path:
            self._set_thumb(m.cover_path)
        else:
            self.thumb_label.setText("Sem capa")

    def _update_ui(self):
        self.core.tick(0.5)
        self._reflect_progress()

    def _fmt(self, v: float):
        v = int(v)
        m, s = divmod(v, 60)
        return f"{m:02d}:{s:02d}"

    # Discord Login and Mobile bot data sender
    def _login_discord(self):
        # Open OAuth2 URL if provided; otherwise open Discord
        oauth = self.config.get("discord_oauth_url")
        if oauth:
            self.open_link(oauth)
            self.discord_status.setText("Aguardando autenticação…")
        else:
            self.open_link("https://discord.com/login")
            self.discord_status.setText("Abra o Discord para autenticar")

    def send_mobile_data(self, payload: Dict[str, Any]):
        # Send data to bot/mobile endpoint if configured
        url = self.config.get("mobile_bot_url")
        if not url:
            return False
        try:
            r = requests.post(url, json=payload, timeout=8)
            return r.ok
        except Exception:
            return False

    def _update_rpc_now(self):
        title = self.core.meta.title or "—"
        if self.core.is_playing and not self.core.is_paused:
            state = "Reproduzindo"
        elif self.core.is_paused:
            state = "Pausado"
        else:
            state = "Parado"
        self.rpc.update(details=title, state=state)

    # Config
    def _load_config(self):
        cfg_path = os.path.join(self.base_dir, "config.json")
        if os.path.exists(cfg_path):
            try:
                with open(cfg_path, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception:
                return {}
        return {}


# Entry point
def main():
    app = QApplication(sys.argv)
    win = MelodyFinderWindow()
    win.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
